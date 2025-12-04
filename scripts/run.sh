#!/bin/bash

echo "Activating virtual environment..."
source ../venv/bin/activate

echo "Changing directory to project root..."
cd ..

echo "Starting FastAPI server..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
