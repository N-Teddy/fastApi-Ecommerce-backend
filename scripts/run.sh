#!/bin/bash

echo "Activating virtual environment..."

# Go to project root (parent of scripts folder)
cd "$(dirname "$0")/.." || exit

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found! Create it with:"
    echo "python3 -m venv venv"
    exit 1
fi

# Activate venv
source venv/bin/activate

echo "Starting FastAPI app..."
uvicorn main:app --reload
