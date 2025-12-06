#!/bin/bash

# Move to project root
cd "$(dirname "$0")/.."

VENV="$PWD/venv"

# Activate virtual environment
if [ -f "$VENV/bin/activate" ]; then
    echo "Activating virtual environment..."
    source "$VENV/bin/activate"
else
    echo "❌ Virtual environment not found! Make sure venv exists in the project root."
    exit 1
fi

# -------------------------
# Generate minimal requirements
# -------------------------
TMP_REQ="$PWD/requirements_tmp.txt"
REQ_FILE="$PWD/requirements.txt"

echo "📝 Generating minimal requirements.txt..."
pipreqs . --force --savepath "$TMP_REQ" >/dev/null 2>&1

# fallback if pipreqs fails for any reason
if [ ! -f "$TMP_REQ" ]; then
    echo "⚠️ pipreqs failed, falling back to full venv freeze..."
    pip freeze > "$REQ_FILE"
else
    mv "$TMP_REQ" "$REQ_FILE"
fi

echo "requirements.txt updated!"

# -------------------------
# Git commit and push
# -------------------------
echo "Enter commit message:"
read commit_message

echo "Enter branch name:"
read branch_name

git add .
git commit -m "$commit_message"
git push origin "$branch_name"

echo "✅ Done!"
