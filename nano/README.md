# nano – Jetson Orin Nano (AI Processing)

Watches for new full videos, runs YOLOv8 detection, cuts short event clips, and sends them back to the Pi 5.

## Key Files

- `watcher.sh` – inotifywait watcher on `/home/matt/videotransfer/`. Calls `clip_all_events.py` when a new `.mp4` arrives.
- `clip_all_events.py` – Main processing script:
  - Learns parked cars
  - Detects person / dog / car
  - Creates short clips (max ~22 seconds)
  - Sends clips to `matt@10.0.0.23:/home/matt/surveillance_drops/events/`
  - Deletes the original long video

## Environment

Runs inside the `yolo-env` virtual environment with Ultralytics YOLO.
