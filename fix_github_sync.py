#!/usr/bin/env python3
"""
Fix GitHub Sync Script for Kairo

This script fixes GitHub synchronization issues by performing a force push with lease
after cleaning the local Git state. It's useful for resolving the "rejected non-fast-forward"
error that can occur when local and remote histories have diverged.
"""

import os
import sys
import argparse
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("github_sync_fix.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("github_sync_fix")

def run_command(command):
    """Run a shell command and log the result."""
    logger.info(f"Running: {command}")
    result = os.system(command)
    if result != 0:
        logger.error(f"Command failed with code {result}: {command}")
    return result

def fix_github_sync():
    """Fix GitHub sync by resetting and force pushing."""
    # Check if GITHUB_TOKEN is set
    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        logger.error("GITHUB_TOKEN environment variable is not set")
        return False
    
    # Configure Git to use token for authentication
    run_command(f'git config --global url."https://{github_token}@github.com/".insteadOf "https://github.com/"')
    run_command('git config --global user.name "Kairo Bot" || true')
    run_command('git config --global user.email "kairo-bot@example.com" || true')
    
    # Get current branch name
    current_branch = os.popen("git rev-parse --abbrev-ref HEAD").read().strip()
    logger.info(f"Current branch: {current_branch}")
    
    # First try a simple force push with lease (safer than force push)
    logger.info("Attempting force push with lease")
    force_push_result = run_command("git push --force-with-lease")
    
    if force_push_result == 0:
        logger.info("Force push with lease successful")
        return True
    
    # If that failed, try more aggressive approach
    logger.info("Force push with lease failed, trying more aggressive approach")
    
    # Fetch the latest from origin
    run_command("git fetch origin")
    
    # Check if the remote branch exists
    remote_exists = os.popen(f"git ls-remote --heads origin {current_branch} | wc -l").read().strip()
    
    if remote_exists == "0":
        # If remote branch doesn't exist, just push
        logger.info(f"Remote branch {current_branch} does not exist, pushing normally")
        return run_command(f"git push -u origin {current_branch}") == 0
    
    # Create a backup branch of our current state
    backup_branch = f"backup-{current_branch}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    run_command(f"git branch {backup_branch}")
    logger.info(f"Created backup branch: {backup_branch}")
    
    # Try to reset to remote state and apply our changes on top
    logger.info(f"Resetting to origin/{current_branch} and reapplying changes")
    
    # First create a patch of our changes compared to origin
    patch_file = f"/tmp/kairo-sync-patch-{datetime.now().strftime('%Y%m%d%H%M%S')}.patch"
    run_command(f"git diff origin/{current_branch} > {patch_file}")
    
    # Reset to match origin
    run_command(f"git reset --hard origin/{current_branch}")
    
    # Apply our changes as a single commit
    run_command(f"git apply {patch_file}")
    run_command("git add .")
    run_command(f'git commit -m "Sync fix: reapplied changes after reset to origin/{current_branch}"')
    
    # Push our changes
    push_result = run_command(f"git push origin {current_branch}")
    
    if push_result == 0:
        logger.info("Sync fix successful")
        # Clean up the patch file
        run_command(f"rm {patch_file}")
        return True
    
    # If all else failed, we can try force push as a last resort
    logger.warning("All previous approaches failed, trying force push as last resort")
    
    # Force push should only be used as a last resort with clear understanding
    # that this will override remote history
    force_result = run_command(f"git push -f origin {current_branch}")
    
    if force_result == 0:
        logger.info("Force push successful")
        return True
    
    # If we got here, nothing worked
    logger.error("All sync fix attempts failed")
    
    # Restore from backup branch
    logger.info(f"Restoring from backup branch {backup_branch}")
    run_command(f"git checkout {backup_branch}")
    run_command(f"git branch -D {current_branch}")
    run_command(f"git checkout -b {current_branch}")
    
    return False

def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(description='Fix GitHub Sync Issues')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    print("Kairo GitHub Sync Fix Tool")
    print("=========================")
    print("This tool will attempt to fix GitHub synchronization issues")
    print("by resetting the local repository to match the remote and then")
    print("reapplying your changes.")
    print()
    print("WARNING: This is a potentially destructive operation.")
    print("A backup branch will be created, but proceed with caution.")
    print()
    
    result = fix_github_sync()
    
    if result:
        print("\nSync fix completed successfully!")
        sys.exit(0)
    else:
        print("\nSync fix failed. Check the logs for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()