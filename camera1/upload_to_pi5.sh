#!/bin/bash
VIDEO_FILE="$MTX_SEGMENT_PATH"
scp -o StrictHostKeyChecking=no "$VIDEO_FILE" YOUR_USERNAME@YOUR_PI5_IP:/var/www/html/videos/
if [ $? -eq 0 ]; then
    rm "$VIDEO_FILE"
fi
