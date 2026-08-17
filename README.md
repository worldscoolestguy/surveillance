# Front Yard Surveillance System

Multi-node edge surveillance pipeline using Raspberry Pi 4, Raspberry Pi 5, and NVIDIA Jetson Orin Nano.

## Overview

- **Pi 4 + Camera Module 3** continuously records the front yard in 5-minute clips and uploads them to the Pi 5.
- **Pi 5** acts as the central hub. It receives the full videos and forwards them to the Jetson Orin Nano.
- **Jetson Orin Nano** runs YOLOv8 to detect person / dog / car (while ignoring parked cars), cuts short event clips, sends only the short clips back to the Pi 5, and deletes the original long videos.

## Hardware

| Node          | Device                          | Role                              | IP          |
|---------------|---------------------------------|-----------------------------------|-------------|
| camera1       | Raspberry Pi 4 (8GB) + Cam 3    | Continuous recording              | 10.0.0.31   |
| raspberrypi   | Raspberry Pi 5                  | Central storage & hub             | 10.0.0.23   |
| Jetson        | NVIDIA Jetson Orin Nano         | AI event detection & clipping     | 10.0.1.69   |

## Current Architecture
```
Pi 4 (Camera Module 3)
        │
        ▼  MediaMTX (rpiCamera) → 5-minute H.264 MP4
        │
        ▼  SCP
Pi 5 ──► /home/matt/surveillance_drops/
        │
        ▼  rsync (monitor_surveillance.sh)
Jetson Orin Nano ──► /home/matt/videotransfer/
        │
        ▼  YOLOv8 (clip_all_events.py)
        │   - Detect person / dog / car
        │   - Ignore parked cars
        │   - Cut short event clips (max ~22s)
        │
        ▼  SCP short clips
Pi 5 ──► /home/matt/surveillance_drops/events/
```


## Status (2026-08-17)

- [x] Pi 4 continuous recording + 5-min segmentation
- [x] Automatic upload Pi 4 → Pi 5
- [x] Automatic forward Pi 5 → Nano
- [x] YOLO event detection + short clip generation on Nano
- [x] Short clips returned to Pi 5
- [x] Original long videos deleted on Nano
- [ ] Further clip quality tuning
- [ ] Full GitHub documentation of all configs

## Key Files

### Pi 4 (camera1)
- `~/mediamtx.yml` – MediaMTX configuration
- `~/upload_to_pi5.sh` – upload + delete script
- `~/diag.sh` – diagnostic script

### Pi 5
- `~/monitor_surveillance.sh` – watches for new full videos and forwards them to the Nano

### Jetson Orin Nano
- `/home/matt/video/watcher.sh` – watches `/home/matt/videotransfer/`
- `/home/matt/video/clip_all_events.py` – YOLO detection + clipping + send back
- `~/yolo-env/` – virtual environment with Ultralytics YOLO

## Diagnostic

Each node has (or should have) a `diag.sh` script. Run it at the start of troubleshooting sessions.

