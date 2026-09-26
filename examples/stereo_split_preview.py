"""Visual preview of the synchronized 1280x400 combined stereo stream."""

import cv2
import numpy as np

PIPELINE = (
    "libcamerasrc ! "
    "video/x-raw, width=1280, height=400, framerate=15/1 ! "
    "videoconvert ! video/x-raw, format=BGR ! "
    "appsink drop=true max-buffers=1 sync=false"
)


def main():
    cap = cv2.VideoCapture(PIPELINE, cv2.CAP_GSTREAMER)
    if not cap.isOpened():
        raise SystemExit("Could not open libcamerasrc pipeline")

    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            continue

        h, w = frame.shape[:2]
        half = w // 2
        left = frame[:, :half]
        right = frame[:, half:]

        cv2.putText(left, "LEFT", (12, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(right, "RIGHT", (12, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        preview = np.hstack((left, right))
        cv2.imshow("CamArray Stereo Split - press q to quit", preview)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
