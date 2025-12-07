# /scripts/add.sh
#!/bin/bash

# =========================================
# FAST Installer Script (Clean & Fixed)
# Usage: ./add <package> [<package2> ...]
# =========================================

# Resolve project root (always correct, even if run from anywhere)
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENV="$PROJECT_ROOT/venv"
REQ_FILE="$PROJECT_ROOT/requirements.txt"

echo "🏠 Project root: $PROJECT_ROOT"

# --- Check arguments ---
if [ $# -eq 0 ]; then
    echo "❌ Error: No package provided."
    echo "Usage: ./add <package-name> [<package-name2> ...]"
    exit 1
fi

# --- Check venv ---
if [ ! -f "$VENV/bin/activate" ]; then
    echo "❌ Virtual environment not found at: $VENV"
    echo "💡 Run: python3 -m venv venv"
    exit 1
fi

# Activate venv
source "$VENV/bin/activate"

echo ""
echo "========================================="
echo "📦 Installing Packages:"
for PKG in "$@"; do echo "  → $PKG"; done
echo "========================================="

# --- Install packages ---
for PKG in "$@"; do
    echo ""
    echo "🚀 Installing '$PKG'..."
    pip install --default-timeout=200 --retries=10 "$PKG"

    if [ $? -ne 0 ]; then
        echo "❌ Installation of '$PKG' failed!"
    else
        echo "✅ '$PKG' installed."
    fi
done

# --- Update requirements.txt using pipreqs ---
echo ""
echo "📝 Updating minimal requirements.txt..."

# Use a temporary file to avoid overwriting incomplete output
TMP_REQ="$PROJECT_ROOT/.requirements_tmp"

pipreqs "$PROJECT_ROOT" --force --encoding=utf-8 --ignore "venv" --savepath "$TMP_REQ" >/dev/null 2>&1

if [ ! -f "$TMP_REQ" ] || [ ! -s "$TMP_REQ" ]; then
    echo "⚠️ pipreqs failed. Falling back to pip freeze..."
    pip freeze > "$REQ_FILE"
else
    mv "$TMP_REQ" "$REQ_FILE"
fi

echo ""
echo "✅ Done!"
echo "📄 requirements.txt updated at: $REQ_FILE"
