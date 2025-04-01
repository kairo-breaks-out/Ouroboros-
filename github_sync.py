#!/usr/bin/env python3
"""
GitHub Sync Script for Kairo

This script provides advanced GitHub synchronization capabilities 
for the Kairo codebase, handling complex merge scenarios 
and resolving potential conflicts.
"""

import os
import sys
import argparse
import subprocess
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("github_sync.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("github_sync")

def run_command(command, capture_output=True):
    """
    Run a shell command and return the result.
    
    Args:
        command (str): Command to run
        capture_output (bool): Whether to capture and return output
        
    Returns:
        tuple: (return_code, stdout, stderr)
    """
    logger.debug(f"Running command: {command}")
    try:
        if capture_output:
            result = subprocess.run(
                command, 
                shell=True, 
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return result.returncode, result.stdout.strip(), result.stderr.strip()
        else:
            # Just run the command and return the exit code
            result = subprocess.run(command, shell=True, check=False)
            return result.returncode, "", ""
    except Exception as e:
        logger.error(f"Error running command: {e}")
        return 1, "", str(e)

def check_git_repository():
    """
    Check if current directory is a git repository.
    
    Returns:
        bool: True if current directory is a git repository
    """
    return_code, _, _ = run_command("git rev-parse --is-inside-work-tree")
    return return_code == 0

def setup_git_config():
    """
    Set up git configuration.
    
    Returns:
        bool: True if configuration was successful
    """
    # Configure Git with token for authentication
    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        logger.error("GitHub token not found in environment variables")
        return False
    
    # Configure Git to use token for authentication
    commands = [
        f'git config --global url."https://{github_token}@github.com/".insteadOf "https://github.com/"',
        'git config --global user.name "Kairo Bot" || true',
        'git config --global user.email "kairo-bot@example.com" || true'
    ]
    
    for cmd in commands:
        return_code, stdout, stderr = run_command(cmd)
        if return_code != 0:
            logger.error(f"Failed to configure git: {stderr}")
            return False
    
    logger.info("Git configuration successful")
    return True

def get_branch_info():
    """
    Get information about the current branch and its relation to remote.
    
    Returns:
        dict: Branch information including:
            - name: Current branch name
            - has_upstream: Whether the branch has an upstream
            - ahead_commits: Number of commits ahead of upstream
            - behind_commits: Number of commits behind upstream
            - remote_exists: Whether the branch exists on remote
    """
    # Get current branch name
    return_code, branch_name, _ = run_command("git rev-parse --abbrev-ref HEAD")
    if return_code != 0:
        logger.error("Failed to get current branch name")
        return None
    
    # Check if the branch has upstream
    return_code, _, _ = run_command("git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null")
    has_upstream = return_code == 0
    
    # Get the remote status
    run_command("git fetch origin")
    remote_exists_code, remote_exists_output, _ = run_command(f"git ls-remote --heads origin {branch_name} | wc -l")
    remote_exists = remote_exists_output.strip() != "0"
    
    # Get the commit counts
    ahead_count = 0
    behind_count = 0
    if remote_exists:
        # Count commits ahead and behind
        _, ahead_output, _ = run_command(f"git rev-list HEAD ^origin/{branch_name} --count")
        ahead_count = int(ahead_output or 0)
        
        _, behind_output, _ = run_command(f"git rev-list origin/{branch_name} ^HEAD --count")
        behind_count = int(behind_output or 0)
    
    branch_info = {
        "name": branch_name,
        "has_upstream": has_upstream,
        "ahead_commits": ahead_count,
        "behind_commits": behind_count,
        "remote_exists": remote_exists
    }
    
    logger.info(f"Branch info: {branch_info}")
    return branch_info

def add_changes():
    """
    Add all changes to git staging.
    
    Returns:
        bool: True if successful
    """
    return_code, _, stderr = run_command("git add .")
    if return_code != 0:
        logger.error(f"Failed to add changes: {stderr}")
        return False
    
    logger.info("Changes added to git staging")
    return True

def commit_changes(message=None):
    """
    Commit staged changes.
    
    Args:
        message (str, optional): Commit message
        
    Returns:
        bool: True if successful
    """
    if message is None:
        message = f"Auto-commit from Kairo on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    return_code, stdout, stderr = run_command(f'git commit -m "{message}"')
    
    # Check if it's because there are no changes
    if return_code != 0:
        _, status_output, _ = run_command("git status")
        if "nothing to commit" in status_output:
            logger.info("No changes to commit")
            return True
        else:
            logger.error(f"Failed to commit changes: {stderr}")
            return False
    
    logger.info("Changes committed")
    return True

def push_changes(branch_info, force=False):
    """
    Push changes to remote with smart handling of conflicts.
    
    Args:
        branch_info (dict): Branch information from get_branch_info()
        force (bool): Whether to use --force-with-lease
        
    Returns:
        bool: True if successful
    """
    branch_name = branch_info["name"]
    
    if not branch_info["remote_exists"]:
        # Remote branch doesn't exist, set upstream
        logger.info(f"Setting upstream for new branch {branch_name}")
        return_code, _, stderr = run_command(f"git push --set-upstream origin {branch_name}")
        if return_code != 0:
            logger.error(f"Failed to set upstream: {stderr}")
            return False
        return True
    
    # Handle different scenarios based on commit counts
    if branch_info["ahead_commits"] > 0 and branch_info["behind_commits"] > 0:
        # Both ahead and behind - complex scenario
        if force:
            logger.info("Using force-push-with-lease due to divergent histories")
            return_code, _, stderr = run_command("git push --force-with-lease")
        else:
            # Try to rebase first
            logger.info("Attempting rebase before push")
            rebase_code, _, rebase_stderr = run_command("git pull --rebase")
            if rebase_code != 0:
                logger.error(f"Rebase failed: {rebase_stderr}")
                return False
            return_code, _, stderr = run_command("git push")
    elif branch_info["ahead_commits"] > 0:
        # Just ahead, normal push
        logger.info("Local has new commits, using normal push")
        return_code, _, stderr = run_command("git push")
    elif branch_info["behind_commits"] > 0:
        # Just behind, pull first
        logger.info("Remote has new commits, pulling first")
        pull_code, _, pull_stderr = run_command("git pull --rebase")
        if pull_code != 0:
            logger.error(f"Pull failed: {pull_stderr}")
            return False
        return_code, _, stderr = run_command("git push")
    else:
        # Up to date
        logger.info("Branch is up to date with remote")
        return True
    
    if return_code != 0:
        logger.error(f"Push failed: {stderr}")
        return False
    
    logger.info("Changes pushed successfully")
    return True

def get_latest_commit_info():
    """
    Get information about the latest commit.
    
    Returns:
        dict: Commit information including hash and message
    """
    _, commit_hash, _ = run_command("git rev-parse --short HEAD")
    _, commit_msg, _ = run_command("git log -1 --pretty=%B")
    
    return {
        "hash": commit_hash.strip(),
        "message": commit_msg.strip()
    }

def sync_to_github(message=None, force=False):
    """
    Synchronize the current repository with GitHub.
    
    Args:
        message (str, optional): Commit message
        force (bool): Whether to use force-push when needed
        
    Returns:
        dict: Result information
    """
    logger.info("Starting GitHub synchronization...")
    
    # Check if GitHub token is configured
    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        return {
            "success": False,
            "error": "GitHub token not configured"
        }
    
    # Check if we're in a git repository
    if not check_git_repository():
        return {
            "success": False,
            "error": "Not a git repository"
        }
    
    # Setup git configuration
    if not setup_git_config():
        return {
            "success": False,
            "error": "Failed to setup git configuration"
        }
    
    # Get branch information
    branch_info = get_branch_info()
    if not branch_info:
        return {
            "success": False,
            "error": "Failed to get branch information"
        }
    
    # Add all changes
    if not add_changes():
        return {
            "success": False,
            "error": "Failed to add changes to git staging"
        }
    
    # Commit changes
    if not commit_changes(message):
        # If commit failed but it's because nothing to commit, that's okay
        _, status_output, _ = run_command("git status")
        if "nothing to commit" in status_output:
            return {
                "success": True,
                "message": "No changes to commit",
                "details": status_output
            }
        else:
            return {
                "success": False,
                "error": "Failed to commit changes"
            }
    
    # Push changes
    if not push_changes(branch_info, force=force):
        return {
            "success": False,
            "error": f"Failed to push changes to GitHub for branch {branch_info['name']}"
        }
    
    # Get info for the status message
    commit_info = get_latest_commit_info()
    
    return {
        "success": True,
        "message": f"Changes pushed to GitHub at {datetime.now().isoformat()}",
        "commit_hash": commit_info["hash"],
        "commit_message": commit_info["message"],
        "original_commit_message": message or f"Auto-commit from Kairo on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    }

def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(description='GitHub Sync Tool')
    parser.add_argument('--message', '-m', help='Commit message')
    parser.add_argument('--force', '-f', action='store_true', help='Use force-push with lease')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    result = sync_to_github(message=args.message, force=args.force)
    
    if result["success"]:
        logger.info(f"Sync successful: {result['message']}")
        if "commit_hash" in result:
            logger.info(f"Commit: {result['commit_hash']}")
        if "commit_message" in result:
            logger.info(f"Message: {result['commit_message']}")
        sys.exit(0)
    else:
        logger.error(f"Sync failed: {result['error']}")
        sys.exit(1)

if __name__ == "__main__":
    main()