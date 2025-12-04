#!/bin/bash

# Go to project root (relative to scripts folder)
cd "$(dirname "$0")/.."

echo "Enter commit message:"
read commit_message

echo "Enter branch name:"
read branch_name

echo "Adding changes..."
git add .

echo "Committing..."
git commit -m "$commit_message"

echo "Pushing to branch '$branch_name'..."
git push origin "$branch_name"

echo "Done!"
