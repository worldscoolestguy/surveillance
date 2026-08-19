# camera1 – Raspberry Pi 4 + Camera Module 3

This node continuously records the front yard and uploads 5-minute clips to the Pi 5.

## Key Files

- `mediamtx.yml` – MediaMTX configuration (rpiCamera source, 5-minute segments)
- `upload_to_pi5.sh` – Called by MediaMTX when a segment finishes. Uploads the clip via SCP and deletes the local file.
- `diag.sh` – Full diagnostic script for this node.

## Important Settings (mediamtx.yml)

- Resolution / FPS / Bitrate controlled by MediaMTX rpiCamera options
- `recordSegmentDuration: 5m`
- `runOnRecordSegmentComplete: /home/YOUR_USERNAME/upload_to_pi5.sh`
