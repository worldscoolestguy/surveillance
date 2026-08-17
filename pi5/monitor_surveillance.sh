#!/bin/bash
inotifywait -m /home/matt/surveillance_drops -e close_write |
    while read path action file; do
        if [[ "$file" == *.mp4 && "$file" != event_* ]]; then
            echo "=== $(date) - Forwarding $file to Nano ==="
            rsync -avz /home/matt/surveillance_drops/"$file" matt@10.0.1.69:/home/matt/videotransfer/
        else
            echo "=== $(date) - Skipped event clip: $file ==="
        fi
    done
