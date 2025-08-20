#!/bin/bash

LOG_FILE="htop_log.txt"
INTERVAL_SECONDS=60 # Log every 5 seconds

while true; do
    echo "--- $(date) ---" >> "$LOG_FILE"
    #htop -b -d 10 | head -n 15 >> "$LOG_FILE"  # -d 10 sets delay to 1 second (10 tenths of a second)
    #htop -n 1 | grep "Mem" >> "$LOG_FILE"
    top -b -n 1 | grep "Mem" >> "$LOG_FILE"
    echo "" >> "$LOG_FILE" # Add an empty line for readability
    sleep "$INTERVAL_SECONDS"
done
