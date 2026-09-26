# Camera Setup Checklist

- [ ] Raspberry Pi powered off before wiring
- [ ] CamArray 2x3 header connected to physical pins 1-6 with correct orientation
- [ ] CSI ribbon connected and latched
- [ ] 64-bit Bullseye known-good image or intentionally validated replacement OS
- [ ] `dtparam=i2c_arm=on`
- [ ] `camera_auto_detect=0`
- [ ] `dtoverlay=arducam-pivariety`
- [ ] Arducam `libcamera_dev` installed
- [ ] Arducam `libcamera_apps` installed
- [ ] `libcamera-v4l2` installed
- [ ] `arducam_pivariety` kernel module loaded
- [ ] `libcamera-hello --list-cameras` sees the camera
- [ ] `libcamera-hello -t 0 --camera 0` previews successfully
- [ ] `gst-inspect-1.0 libcamerasrc` succeeds
- [ ] GStreamer live pipeline displays `1280x400 @ 15 FPS`
- [ ] OpenCV reports `GStreamer: YES`
- [ ] `stereo_capture_smoke_test.py` returns `(400, 1280, 3)`
- [ ] Left and right splits are each `(400, 640, 3)`
