# Arducam CamArray Stereo Camera Setup on Raspberry Pi

This repository documents the **camera hardware, Arducam driver, libcamera, I2C, GStreamer, and OpenCV setup** used for the synchronized stereo camera system in this project.

It intentionally **does not include the dataset-collector application**. The goal is to let another engineer reproduce the camera stack first, verify the synchronized `1280 x 400` stream, and only then integrate stereo-depth or AI code.

## Known-good project configuration

| Item | Project configuration |
|---|---|
| SBC | Raspberry Pi 4; Compute Module 4 is also used in the project |
| OS | Raspberry Pi OS / Debian Bullseye, 64-bit (`AArch64`) for the known-good system |
| Camera | Arducam synchronized stereo / CamArray HAT with two monochrome cameras |
| Camera driver | Arducam Pivariety V4L2 driver |
| Camera API | `libcamera` |
| Image transport | GStreamer `libcamerasrc` |
| Combined frame | `1280 x 400` |
| Left frame | `640 x 400` |
| Right frame | `640 x 400` |
| Frame rate used by the project | `15 FPS` |
| Control header | Raspberry Pi physical GPIO pins `1` through `6` connected one-to-one to the HAT 2x3 header |

## Hardware connection

![CamArray I2C/power header connection](assets/camarray_i2c_connection.png)

The 2x3 header mapping is documented by Arducam as:

| Raspberry Pi physical pin | Raspberry Pi signal | CamArray HAT pin | HAT signal |
|---:|---|---:|---|
| 1 | 3.3 V | 1 | 3V3 |
| 2 | 5 V | 2 | 5V |
| 3 | GPIO2 / SDA1 | 3 | SDA |
| 4 | 5 V | 4 | 5V |
| 5 | GPIO3 / SCL1 | 5 | SCL |
| 6 | GND | 6 | GND |

> **Power the Raspberry Pi off before connecting or disconnecting the 2x3 header or the CSI ribbon.**

The MIPI CSI ribbon carries the image stream. The 2x3 header provides power and the SDA/SCL control lines used by the HAT.

## Quick installation path

### 1. Install base tools and GStreamer

```bash
sudo apt update
sudo apt install -y \
  wget git i2c-tools v4l-utils \
  python3 python3-pip python3-venv python3-opencv \
  gstreamer1.0-tools \
  gstreamer1.0-plugins-base \
  gstreamer1.0-plugins-good \
  gstreamer1.0-plugins-bad \
  gstreamer1.0-libav
```

### 2. Install the Arducam Pivariety/libcamera packages

These are the exact commands recovered from the known-good project machine:

```bash
wget -O install_pivariety_pkgs.sh \
  https://github.com/ArduCAM/Arducam-Pivariety-V4L2-Driver/releases/download/install_script/install_pivariety_pkgs.sh

chmod +x install_pivariety_pkgs.sh
./install_pivariety_pkgs.sh -p libcamera_dev
./install_pivariety_pkgs.sh -p libcamera_apps
sudo apt install -y libcamera-v4l2
```

### 3. Configure `/boot/config.txt`

The known-good Bullseye system contains:

```ini
dtparam=i2c_arm=on
camera_auto_detect=0
dtoverlay=vc4-kms-v3d
dtoverlay=arducam-pivariety
```

Then reboot:

```bash
sudo reboot
```

### 4. Verify the camera driver

```bash
lsmod | grep -Ei 'arducam|unicam'
dmesg | grep -i arducam
libcamera-hello --list-cameras
libcamera-hello -t 0 --camera 0
```

The known-good system loads modules including `arducam_pivariety` and `bcm2835_unicam`.

### 5. Verify GStreamer `libcamerasrc`

```bash
gst-inspect-1.0 libcamerasrc
```

Then test a live display:

```bash
gst-launch-1.0 -v \
  libcamerasrc ! \
  video/x-raw,width=1280,height=400,framerate=15/1 ! \
  videoconvert ! autovideosink
```

### 6. Verify OpenCV was built with GStreamer support

```bash
python3 - <<'PY'
import cv2
print('OpenCV:', cv2.__version__)
for line in cv2.getBuildInformation().splitlines():
    if 'GStreamer' in line:
        print(line)
PY
```

The expected build information should report:

```text
GStreamer: YES
```

> Avoid replacing the working Raspberry Pi OS OpenCV with a generic `pip install opencv-python` wheel unless you have verified that wheel was built with GStreamer. The project relies on `cv2.CAP_GSTREAMER`.

## Project GStreamer pipeline

```text
libcamerasrc !
video/x-raw, width=1280, height=400, framerate=15/1 !
videoconvert !
video/x-raw, format=BGR !
appsink drop=true max-buffers=1 sync=false
```

The final three `appsink` options are important for real-time operation:

- `drop=true` — stale frames may be discarded when software cannot keep up.
- `max-buffers=1` — prevents a large backlog of queued frames.
- `sync=false` — avoids waiting on the GStreamer clock at the sink.

## Minimal OpenCV test

Run:

```bash
python3 examples/stereo_capture_smoke_test.py
```

Expected output includes:

```text
opened: True
frame shape: (400, 1280, 3)
left shape:  (400, 640, 3)
right shape: (400, 640, 3)
```

For a visual split preview:

```bash
python3 examples/stereo_split_preview.py
```

## Documentation

- [Hardware wiring](docs/01_HARDWARE_WIRING.md)
- [Bullseye and Arducam installation](docs/02_OS_AND_ARDUCAM_SETUP.md)
- [GStreamer and OpenCV](docs/03_GSTREAMER_AND_OPENCV.md)
- [Camera verification procedure](docs/04_CAMERA_VERIFICATION.md)
- [Advanced I2C / CamArray controls](docs/05_I2C_AND_CAMARRAY_CONTROL.md)
- [Troubleshooting](docs/06_TROUBLESHOOTING.md)
- [CM4 hardware notes](docs/07_CM4_NOTES.md)
- [Sources and references](SOURCES.md)

## Scope boundary

This repository stops at a verified synchronized stereo stream. Detection, stereo-depth mathematics, dataset collection, touchscreen UI, and application packaging are deliberately outside this version of the guide.
