# GitHub Synchronization for Kairo

This document explains the GitHub synchronization capabilities of Kairo and how to use them.

## Overview

Kairo has built-in capabilities to synchronize its codebase with a GitHub repository, enabling:

1. Preservation of improvements across Replit sessions
2. Backup of your code and memory to a safe external repository 
3. Versioning of code changes with timestamps
4. Collaboration with multiple developers

## Telegram Commands

Use the following commands in the Telegram bot to interact with GitHub synchronization:

- `/sync` or `/github` or `/push` - Synchronize code to GitHub

## How Synchronization Works

When you trigger a sync, Kairo:

1. Detects if there's a configured GitHub repository
2. Adds all current changes to Git staging
3. Creates a commit with a timestamp
4. Intelligently pushes to GitHub based on remote repository state:
   - For new branches: Sets up the upstream branch
   - For diverged branches: Safely merges or rebases changes
   - For simple pushes: Performs a standard push

## Advanced Synchronization Tools

Kairo includes specialized tools for GitHub synchronization:

### github_sync.py

This script provides robust synchronization capabilities with smart handling of complex Git scenarios:

```bash
# Basic sync
python github_sync.py

# Force sync when needed (uses --force-with-lease)
python github_sync.py --force

# Custom commit message
python github_sync.py --message "Your commit message"

# Verbose logging
python github_sync.py --verbose
```

### fix_github_sync.py

A specialized tool for resolving difficult synchronization issues:

```bash
# Fix sync issues
python fix_github_sync.py

# With verbose logging
python fix_github_sync.py --verbose
```

This tool creates a backup branch before attempting fixes, handles tricky merge conflicts, and safely reapplies your changes when local and remote histories have diverged significantly.

## Troubleshooting

If you encounter GitHub sync issues:

1. **"Failed to push changes to GitHub"** - This generally indicates a diverged history. Run the fix tool:
   ```bash
   python fix_github_sync.py
   ```

2. **"Failed to set upstream branch"** - The local and remote repositories have diverged significantly. Try:
   ```bash
   python github_sync.py --force
   ```

3. **"GitHub token not configured"** - Ensure you've set the `GITHUB_TOKEN` environment variable with a valid GitHub personal access token.

4. **Merge Conflicts** - When local and remote have conflicting changes, use:
   ```bash
   python fix_github_sync.py
   ```
   This will attempt to preserve your changes while resolving conflicts with the remote repository.

## Best Practices

1. Sync regularly to avoid large divergence between local and remote code
2. Use descriptive commit messages when possible
3. Check the GitHub repository web interface to verify syncs
4. Use the `/sync` command before making major changes to ensure you're starting from a clean state

## GitHub Token

For synchronization to work, you need to set up a GitHub Personal Access Token:

1. Generate a token on GitHub with the `repo` scope
2. Set it as the `GITHUB_TOKEN` environment variable in your Replit environment
3. Protect your token and never share it publicly