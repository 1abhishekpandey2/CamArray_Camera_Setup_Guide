# Production Application Placeholder

This camera-setup repository intentionally stops after a verified synchronized stereo stream.

The downstream production application can be added here later after the camera stack is reproduced successfully.

Recommended integration contract:

```text
Input frame: 1280 x 400 BGR
Left view:   frame[:, 0:640]
Right view:  frame[:, 640:1280]
Capture FPS: 15
Transport:   OpenCV + GStreamer libcamerasrc
```

The earlier dataset-collector application has deliberately been excluded from this repository version.
