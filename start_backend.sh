#!/bin/bash
cd "$(dirname "$0")/backend"

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
pip install -q -r requirements.txt

# Run the application
python -m app.main
