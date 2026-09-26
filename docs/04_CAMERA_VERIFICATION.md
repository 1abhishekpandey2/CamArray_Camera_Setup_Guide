# 4. Camera Verification Procedure

Perform these checks in order. Do not start higher-level application debugging until the previous level passes.

## Level 1: hardware and I2C

```bash
ls /dev/i2c* 2>/dev/null
i2cdetect -l
```

The exact Linux I2C bus number used by the camera/HAT control path may vary by Raspberry Pi generation, kernel, and camera stack. Do not assume that the physical GPIO SDA/SCL pins always appear as the same bus number in every driver configuration.

## Level 2: Arducam kernel driver

```bash
lsmod | grep -Ei 'arducam|unicam'
dmesg | grep -i arducam
```

Expected project module:

```text
arducam_pivariety
```

## Level 3: libcamera discovery

```bash
libcamera-hello --list-cameras
```

Then preview camera 0:

```bash
libcamera-hello -t 0 --camera 0
```

## Level 4: GStreamer discovery

```bash
gst-inspect-1.0 libcamerasrc
```

## Level 5: GStreamer live stream

```bash
gst-launch-1.0 -v \
  libcamerasrc ! \
  video/x-raw,width=1280,height=400,framerate=15/1 ! \
  videoconvert ! autovideosink
```

## Level 6: OpenCV capture

```bash
python3 examples/stereo_capture_smoke_test.py
```

Success means:

```text
opened: True
frame shape: (400, 1280, 3)
left shape:  (400, 640, 3)
right shape: (400, 640, 3)
```

## Level 7: visual stereo split

```bash
python3 examples/stereo_split_preview.py
```

The window should show two separate `640 x 400` views produced from the one `1280 x 400` combined frame.
