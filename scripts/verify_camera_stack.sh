#!/usr/bin/env bash
set -u

echo '=== OS ==='
cat /etc/os-release 2>/dev/null | grep -E 'PRETTY_NAME|VERSION_CODENAME' || true
uname -m

echo
echo '=== I2C ==='
ls -l /dev/i2c* 2>/dev/null || true
i2cdetect -l 2>/dev/null || true

echo
echo '=== CAMERA MODULES ==='
lsmod | grep -Ei 'arducam|unicam|v4l2' || true

echo
echo '=== ARDUCAM DMESG ==='
dmesg 2>/dev/null | grep -i arducam | tail -n 30 || true

echo
echo '=== VIDEO NODES ==='
ls -l /dev/video* 2>/dev/null || true

echo
echo '=== LIBCAMERA CAMERAS ==='
if command -v libcamera-hello >/dev/null 2>&1; then
  libcamera-hello --list-cameras || true
elif command -v rpicam-hello >/dev/null 2>&1; then
  rpicam-hello --list-cameras || true
else
  echo 'No libcamera-hello/rpicam-hello command found.'
fi

echo
echo '=== GSTREAMER ==='
gst-launch-1.0 --version 2>/dev/null || echo 'gst-launch-1.0 not found'
gst-inspect-1.0 libcamerasrc >/dev/null 2>&1 && echo 'libcamerasrc: FOUND' || echo 'libcamerasrc: NOT FOUND'

echo
echo '=== OPENCV ==='
python3 - <<'PY' 2>/dev/null || true
try:
    import cv2
    print('OpenCV:', cv2.__version__)
    gs = [line.strip() for line in cv2.getBuildInformation().splitlines() if 'GStreamer' in line]
    print('\n'.join(gs) if gs else 'GStreamer build line not found')
except Exception as exc:
    print('OpenCV import failed:', exc)
PY
