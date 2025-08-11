#!/bin/bash

# Check if persistent storage is available and set up logging accordingly
if [ -d "/data" ]; then
    mkdir -p /data/logs
    LOG_FILE="/data/logs/radextract-$(date +%Y-%m-%d).log"
    exec gunicorn \
        --workers 6 \
        --worker-class sync \
        --timeout 60 \
        --keep-alive 5 \
        --error-logfile - \
        --log-level warning \
        -b 0.0.0.0:7870 \
        app:app 2>&1 | tee -a "$LOG_FILE"
else
    # No persistent storage, just run normally
    exec gunicorn \
        --workers 6 \
        --worker-class sync \
        --timeout 60 \
        --keep-alive 5 \
        --error-logfile - \
        --log-level warning \
        -b 0.0.0.0:7870 \
        app:app
fi 