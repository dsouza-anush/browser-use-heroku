#!/bin/bash
set -e

echo "Syncing with upstream repository..."

# Get current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Fetch updates from upstream
git fetch upstream

# Create a temp branch to merge the updates
git checkout -b temp_update_branch

# Merge upstream changes
git merge upstream/main -m "Merge updates from upstream repository"

# Save Heroku-specific files
echo "Preserving Heroku-specific files..."
git checkout $CURRENT_BRANCH -- Procfile Aptfile app.json runtime.txt bin/post_compile requirements.txt

# Commit any conflicts or changes to Heroku files
if git diff --staged --quiet; then
  echo "No changes to Heroku-specific files detected."
else
  git commit -m "Preserve Heroku-specific configurations"
fi

# Switch back to the original branch
git checkout $CURRENT_BRANCH

# Merge the temp branch with our updates
git merge temp_update_branch -m "Sync with upstream and preserve Heroku configurations"

# Delete the temporary branch
git branch -D temp_update_branch

echo "Sync completed! Your Heroku deployment is now updated with the latest changes from upstream."