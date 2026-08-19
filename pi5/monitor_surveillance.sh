#!/bin/bash
inotifywait -m /home/YOUR_USERNAME/surveillance_drops -e close_write |
    while read path action file; do
        if [[ "$file" == *.mp4 && "$file" != event_* ]]; then
            echo "=== $(date) - Forwarding $file to Nano ==="
            rsync -avz /home/YOUR_USERNAME/surveillance_drops/"$file" YOUR_USERNAME@YOUR_JETSON_IP:/home/YOUR_USERNAME/videotransfer/
        else
            echo "=== $(date) - Skipped event clip: $file ==="
        fi
    done
