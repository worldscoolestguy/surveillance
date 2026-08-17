#!/bin/bash
inotifywait -m /home/matt/videotransfer/ -e close_write -e moved_to -e create |
    while read path action file; do
        if [[ "$file" == *.mp4 ]]; then
            echo "$(date) - Detected $file ($action)" >> /home/matt/video/watcher.log
            python3 /home/matt/video/clip_all_events.py
        fi
    done
