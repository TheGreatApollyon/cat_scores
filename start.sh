#!/bin/bash

echo "=========================================="
echo "Event Scoring System - Quick Start"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
echo "Checking dependencies..."
pip install -q -r requirements.txt

echo ""
echo "=========================================="
echo "Starting Event Scoring System..."
echo "=========================================="
echo ""
echo "🌐 PUBLIC ACCESS (No login required):"
echo "  http://127.0.0.1:5000/"
echo "  http://127.0.0.1:5000/overview"
echo ""
echo "🔐 MANAGEMENT ACCESS (Login required):"
echo "  http://127.0.0.1:5000/login"
echo "  http://127.0.0.1:5000/manage"
echo ""
echo "👤 Default admin credentials:"
echo "  Username: admin"
echo "  Password: admin123"
echo ""
echo "⚠️  IMPORTANT: Change admin password after first login!"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=========================================="
echo ""

# Run the application
python app.py
