#!/usr/bin/env python3
"""
Main entry point for the Event Scoring System
Compatible with various deployment platforms
"""

from app import app

# For servers that expect 'application' variable
application = app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)