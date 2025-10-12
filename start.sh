#!/bin/bash

# Start script for Render.com deployment
# This script uses gunicorn with optimized production settings

# Set Flask environment to production
export FLASK_ENV=production

# Start gunicorn with:
# - 4 workers (adjust based on your dyno size)
# - worker-tmp-dir in /dev/shm for better performance
# - Access logs enabled
# - Bind to 0.0.0.0:$PORT (Render provides PORT env variable)
# - Timeout of 120 seconds for long-running requests

gunicorn \
    --workers=4 \
    --worker-class=sync \
    --worker-tmp-dir=/dev/shm \
    --bind=0.0.0.0:${PORT:-5001} \
    --timeout=120 \
    --access-logfile=- \
    --error-logfile=- \
    --log-level=info \
    app:app
