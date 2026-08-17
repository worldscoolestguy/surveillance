#!/bin/bash
VIDEO_FILE="$MTX_SEGMENT_PATH"
scp -o StrictHostKeyChecking=no "$VIDEO_FILE" matt@10.0.0.23:/var/www/html/videos/
if [ $? -eq 0 ]; then
    rm "$VIDEO_FILE"
fi
