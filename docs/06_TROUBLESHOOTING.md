# 6. Troubleshooting

## Camera is not listed

Run:

```bash
lsmod | grep -Ei 'arducam|unicam'
dmesg | grep -i arducam
libcamera-hello --list-cameras
```

Check:

- `camera_auto_detect=0`
- `dtoverlay=arducam-pivariety`
- CSI ribbon orientation and full insertion
- 2x3 header orientation
- camera/HAT connected before power-up

## `gst-inspect-1.0 libcamerasrc` fails

This means the libcamera GStreamer source element is unavailable to GStreamer.

First re-check the Arducam/libcamera installation. Do not attempt to solve this by installing `opencv-python` because `libcamerasrc` is a GStreamer/libcamera component, not an OpenCV component.

Useful checks:

```bash
gst-inspect-1.0 --version
gst-inspect-1.0 libcamerasrc
libcamera-hello --list-cameras
```

## OpenCV says `opened: False`

Verify both components independently:

```bash
gst-launch-1.0 -v libcamerasrc ! video/x-raw,width=1280,height=400,framerate=15/1 ! videoconvert ! autovideosink
```

and:

```bash
python3 - <<'PY'
import cv2
print(cv2.__version__)
print([x for x in cv2.getBuildInformation().splitlines() if 'GStreamer' in x])
PY
```

If OpenCV reports `GStreamer: NO`, use a GStreamer-enabled OpenCV build.

## Stream opens but latency keeps increasing

Use the project appsink options:

```text
appsink drop=true max-buffers=1 sync=false
```

These prevent a large stale-frame queue from building up.

## Wrong frame dimensions

The project expects:

```text
combined = 1280 x 400
left     =  640 x 400
right    =  640 x 400
```

If the camera returns another layout, do not blindly split the frame in half and assume the calibration remains valid. Confirm the HAT mode and camera stream configuration first.

## `numpy.core.multiarray failed to import` / `_ARRAY_API not found`

This project previously encountered a NumPy 2.x / system OpenCV ABI mismatch. If you are using an older Raspberry Pi OS OpenCV compiled against NumPy 1.x, avoid installing an incompatible NumPy 2.x into the same Python environment.

## Native `Segmentation fault` involving `GstLibcameraSrcState`

The project observed native crashes when heavy inference libraries were initialized after the libcamera/GStreamer stream was already running. For camera-only validation, remove AI/ONNX from the test path and confirm the camera/GStreamer stack is stable first.

## Thermal throttling

On Raspberry Pi 4/5:

```bash
vcgencmd measure_temp
vcgencmd get_throttled
```

A healthy non-throttled result is typically:

```text
throttled=0x0
```
