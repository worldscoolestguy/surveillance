#!/usr/bin/env python3
import cv2
import subprocess
import os
from pathlib import Path
from datetime import datetime
from ultralytics import YOLO
import numpy as np

print("=== FIXED VERSION (no duplicates + safer ffmpeg) ===")
print("Script started at", datetime.now())

WATCH_DIR = Path("/home/matt/videotransfer")
files = sorted([f for f in WATCH_DIR.glob("*.mp4")], key=os.path.getctime)

if not files:
    print("No files found. Exiting.")
    exit(0)

TARGET_FILE = files[0]
print(f"Processing: {TARGET_FILE.name}")

TEMP_DIR = Path("/tmp/yolo_clips")
TEMP_DIR.mkdir(parents=True, exist_ok=True)

REMOTE_DEST = "matt@10.0.0.23:/home/matt/surveillance_drops/events/"

MODEL = "/home/matt/yolov8n.pt"
CONF_BG = 0.45
CONF_MAIN = 0.60
SAMPLE = 8
PRE = 5
POST = 6
MAX_CLIP = 22
SILENCE = 9

model = YOLO(MODEL)

print("Learning parked cars...")
background = []
for i, r in enumerate(model.predict(source=str(TARGET_FILE), stream=True, conf=CONF_BG, classes=[2], verbose=False)):
    if i >= 50:
        break
    if r.boxes is not None:
        background.extend(r.boxes.xyxy.cpu().numpy())

def is_parked(box):
    cx = (box[0] + box[2]) / 2
    cy = (box[1] + box[3]) / 2
    for bg in background:
        dist = np.hypot(cx - (bg[0]+bg[2])/2, cy - (bg[1]+bg[3])/2)
        if dist < 65:
            return True
    return False

print("Detecting events...")
cap = cv2.VideoCapture(str(TARGET_FILE))
fps = cap.get(cv2.CAP_PROP_FPS) or 15
duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps

raw_events = []
current_start = None
last_seen = -100
frame_idx = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if frame_idx % SAMPLE == 0:
        results = model.predict(frame, classes=[0, 16, 2], conf=CONF_MAIN, verbose=False)
        has_new = False
        if results[0].boxes is not None:
            for box in results[0].boxes.xyxy.cpu().numpy():
                if not is_parked(box):
                    has_new = True
                    break

        t = frame_idx / fps

        if has_new:
            if current_start is None:
                current_start = max(0, t - PRE)
            last_seen = t
        elif current_start is not None and (t - last_seen) > SILENCE:
            end = min(duration, last_seen + POST)
            if end - current_start > MAX_CLIP:
                end = current_start + MAX_CLIP
            raw_events.append((current_start, end))
            current_start = None

    frame_idx += 1

if current_start is not None:
    end = min(duration, last_seen + POST)
    if end - current_start > MAX_CLIP:
        end = current_start + MAX_CLIP
    raw_events.append((current_start, end))

cap.release()

# Merge overlapping events
events = []
for start, end in sorted(raw_events):
    if not events:
        events.append([start, end])
    else:
        last_start, last_end = events[-1]
        if start <= last_end + 3:
            events[-1][1] = max(last_end, end)
        else:
            events.append([start, end])

print(f"Found {len(events)} event(s)")

ts = datetime.now().strftime("%Y%m%d_%H%M%S")

for i, (start, end) in enumerate(events, 1):
    clip = TEMP_DIR / f"event_{ts}_{i:02d}.mp4"

    cmd = [
        "/usr/bin/ffmpeg", "-y",
        "-ss", f"{start:.2f}",
        "-i", str(TARGET_FILE),
        "-t", f"{end - start:.2f}",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
        "-c:a", "aac",
        str(clip)
    ]

    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        print(f"ffmpeg failed for event {i}, skipping")
        continue

    print(f"Sending {clip.name} → {REMOTE_DEST}")
    scp_result = subprocess.run(["scp", "-q", str(clip), REMOTE_DEST], capture_output=True, text=True)

    if scp_result.returncode == 0:
        print("✅ Sent")
    else:
        print("❌ SCP failed:", scp_result.stderr)

    if clip.exists():
        clip.unlink()

if TARGET_FILE.exists():
    TARGET_FILE.unlink()
    print(f"Deleted original: {TARGET_FILE.name}")

print("=== DONE ===")
