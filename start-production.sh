#!/bin/bash

echo "Starting Event Scoring System in Production Mode..."

# Install dependencies if needed
pip install -r requirements.txt

# Start with Gunicorn
exec gunicorn --config gunicorn.conf.py app:app