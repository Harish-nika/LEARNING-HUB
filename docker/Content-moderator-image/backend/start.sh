#!/bin/bash

echo "🚀 Starting FastAPI Backend..."
cd /app/backend  # Ensure correct directory

# Ensure correct module path
uvicorn backend:app --host 0.0.0.0 --port 8000 --reload
