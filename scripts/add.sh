#!/bin/bash

# FAST installer script
# Usage: ./add <package_name> [<package_name2> ...]

if [ $# -eq 0 ]; then
    echo "❌ Error: No package provided."
    echo "Usage: ./add <package-name> [<package-name2> ...]"
    exit 1
fi

PROJECT_ROOT="$(dirname "$0")/.."
VENV="$PROJECT_ROOT/venv"

# Activate virtual environment
if [ ! -f "$VENV/bin/activate" ]; then
    echo "❌ Virtual environment not found at: $VENV"
    exit 1
fi

source "$VENV/bin/activate"

# Install packages with timeout + retries
for PKG in "$@"; do
    echo "🚀 Installing '$PKG' with timeout and retries..."
    pip install --default-timeout=200 --retries=10 "$PKG"
    if [ $? -ne 0 ]; then
        echo "❌ Installation of '$PKG' failed."
    else
        echo "📦 '$PKG' installed successfully."
    fi
done

# Update minimal requirements using pipreqs
TMP_REQ="$PROJECT_ROOT/requirements_tmp.txt"
REQ_FILE="$PROJECT_ROOT/requirements.txt"

echo "📝 Updating minimal requirements.txt..."
pipreqs "$PROJECT_ROOT" --force --savepath "$TMP_REQ" >/dev/null 2>&1
if [ ! -f "$TMP_REQ" ]; then
    echo "⚠️ pipreqs failed, falling back to pip freeze..."
    pip freeze > "$REQ_FILE"
else
    mv "$TMP_REQ" "$REQ_FILE"
fi

echo "✅ Done!"
