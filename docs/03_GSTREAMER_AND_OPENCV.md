# 3. GStreamer and OpenCV Setup

## Why GStreamer is required

The project does not open a generic `/dev/video0` device. It uses a `libcamerasrc` GStreamer pipeline so libcamera can configure the Arducam camera and deliver the synchronized combined frame to OpenCV.

## Install GStreamer runtime packages

```bash
sudo apt update
sudo apt install -y \
  gstreamer1.0-tools \
  gstreamer1.0-plugins-base \
  gstreamer1.0-plugins-good \
  gstreamer1.0-plugins-bad \
  gstreamer1.0-libav
```

## Confirm the libcamera GStreamer element

```bash
gst-inspect-1.0 libcamerasrc
```

If this command cannot find `libcamerasrc`, first repair/reinstall the matching Arducam/libcamera stack. Avoid mixing an arbitrary current upstream libcamera build with an older vendor Pivariety driver unless you intentionally validate that combination.

## Live GStreamer smoke test

```bash
gst-launch-1.0 -v \
  libcamerasrc ! \
  video/x-raw,width=1280,height=400,framerate=15/1 ! \
  videoconvert ! autovideosink
```

The target is one combined synchronized frame of `1280 x 400` at `15 FPS`.

## Production OpenCV pipeline

```text
libcamerasrc ! video/x-raw, width=1280, height=400, framerate=15/1 ! videoconvert ! video/x-raw, format=BGR ! appsink drop=true max-buffers=1 sync=false
```

### Why the appsink options matter

`drop=true`
: Allows old frames to be discarded if downstream processing is slower than capture. For a live robotics pipeline, the newest frame is normally more useful than a backlog.

`max-buffers=1`
: Restricts the appsink queue to one buffer, preventing latency and memory growth.

`sync=false`
: Disables sink-side clock synchronization so the application can consume frames as soon as they are available.

## OpenCV package choice

Preferred first attempt on Raspberry Pi OS:

```bash
sudo apt install -y python3-opencv
```

Verify GStreamer support:

```bash
python3 - <<'PY'
import cv2
print('OpenCV version:', cv2.__version__)
for line in cv2.getBuildInformation().splitlines():
    if 'GStreamer' in line:
        print(line)
PY
```

Expected:

```text
GStreamer: YES
```

A generic PyPI `opencv-python` wheel may not contain the GStreamer support required by this project. Do not replace a working distro OpenCV without verifying the build information afterwards.

## Optional: build OpenCV with GStreamer support

Only use this section if the system package reports `GStreamer: NO` and you deliberately want a custom OpenCV build.

```bash
sudo apt install -y \
  build-essential cmake pkg-config \
  libgtk-3-dev \
  libavcodec-dev libavformat-dev libswscale-dev \
  libv4l-dev \
  libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev \
  python3-dev python3-numpy

git clone --depth 1 https://github.com/opencv/opencv.git
git clone --depth 1 https://github.com/opencv/opencv_contrib.git

cd opencv
mkdir -p build && cd build
cmake \
  -D CMAKE_BUILD_TYPE=Release \
  -D CMAKE_INSTALL_PREFIX=/usr/local \
  -D WITH_GSTREAMER=ON \
  -D WITH_V4L=ON \
  -D BUILD_opencv_python3=ON \
  -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \
  ..

make -j2
sudo make install
sudo ldconfig
```

Then repeat the `cv2.getBuildInformation()` check.
