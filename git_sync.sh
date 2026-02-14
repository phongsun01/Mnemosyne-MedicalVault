#!/bin/bash

# MedicalVault Git Sync Tool for Mac

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Error: Not a git repository. Run 'git init' first."
    exit 1
fi

# Get commit message
COMMIT_MSG=$1
if [ -z "$COMMIT_MSG" ]; then
    read -p "Enter commit message: " COMMIT_MSG
fi

if [ -z "$COMMIT_MSG" ]; then
    COMMIT_MSG="Update MedicalVault: $(date '+%Y-%m-%d %H:%M:%S')"
fi

echo "🚀 Staging changes..."
git add .

echo "📦 Committing..."
git commit -m "$COMMIT_MSG"

echo "☁️ Pushing to GitHub..."
git push

echo "✅ Done!"
