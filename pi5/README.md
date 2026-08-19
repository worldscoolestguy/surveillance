# pi5 – Raspberry Pi 5 (Central Hub)

Receives full 5-minute videos from the Pi 4 and forwards them to the Jetson Orin Nano.

## Key Files

* `monitor_surveillance.sh` – Uses inotifywait to watch `/home/YOUR_USERNAME/surveillance_drops/`.
  When a new non-event .mp4 appears, it rsyncs it to the Nano (`YOUR_USERNAME@YOUR_JETSON_IP:/home/YOUR_USERNAME/videotransfer/`).
