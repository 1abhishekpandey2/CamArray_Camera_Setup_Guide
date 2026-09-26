"""Minimal camera-only validation for the synchronized CamArray stream.

No YOLO, no stereo matching, no dataset logic. The goal is to prove that
libcamera -> GStreamer -> OpenCV works and that the combined frame layout is
1280x400 split into two 640x400 images.
"""

import cv2

PIPELINE = (
    "libcamerasrc ! "
    "video/x-raw, width=1280, height=400, framerate=15/1 ! "
    "videoconvert ! video/x-raw, format=BGR ! "
    "appsink drop=true max-buffers=1 sync=false"
)


def main():
    cap = cv2.VideoCapture(PIPELINE, cv2.CAP_GSTREAMER)
    print("opened:", cap.isOpened())
    if not cap.isOpened():
        raise SystemExit("Failed to open GStreamer/libcamera pipeline")

    ret, frame = cap.read()
    cap.release()

    if not ret or frame is None:
        raise SystemExit("Camera opened but no frame was received")

    print("frame shape:", frame.shape)
    height, width = frame.shape[:2]
    half = width // 2
    left = frame[:, :half]
    right = frame[:, half:]
    print("left shape: ", left.shape)
    print("right shape:", right.shape)

    if (width, height) != (1280, 400):
        print("WARNING: expected a 1280x400 combined frame")


if __name__ == "__main__":
    main()
