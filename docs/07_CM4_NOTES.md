# 7. Compute Module 4 Notes

## What changes on CM4

The camera software stack can remain the same, but the physical CSI connector and carrier-board routing differ from a Raspberry Pi 4.

The project CM4 hardware was identified as:

```text
Raspberry Pi Compute Module 4 Rev 1.0
```

The carrier exposes a Raspberry Pi-compatible GPIO header, so the 2x3 CamArray header still maps to physical pins 1 through 6 as documented in the wiring guide.

## CSI connector

Compute Module carrier boards commonly expose a 22-pin camera connector. Use the appropriate CSI ribbon for the carrier and HAT.

Do not assume a Pi 4 15-pin cable can be inserted directly into a CM4 carrier's 22-pin connector.

## OS note

The known-good project camera stack is Bullseye/libcamera/Pivariety. An earlier 32-bit Buster CM4 image did not contain the required working libcamera/Pivariety environment and is not the documented target for this guide.

## Camera overlay

The verified Pi 4 configuration used:

```ini
dtoverlay=arducam-pivariety
```

On a CM4 carrier with multiple camera interfaces, the exact overlay parameters can depend on which CSI port is wired by the carrier. If the default overlay does not bind, check the installed Arducam overlay documentation for the correct `cam0`/camera-port parameter rather than guessing.
