# Sources and Project Evidence

This guide combines the project's known-good machine configuration with official vendor references.

## Project-observed configuration

Recovered from the working Bullseye Raspberry Pi:

- `/boot/config.txt` included `dtparam=i2c_arm=on`, `camera_auto_detect=0`, `dtoverlay=vc4-kms-v3d`, and `dtoverlay=arducam-pivariety`.
- loaded kernel modules included `arducam_pivariety` and `bcm2835_unicam`.
- shell history showed the Arducam Pivariety installer commands used in this guide.
- the application successfully used `libcamerasrc` with a `1280 x 400 @ 15 FPS` combined stream.

## Official references

### Arducam CamArray quick start

https://docs.arducam.com/Raspberry-Pi-Camera/Multi-Camera-CamArray/quick-start/

Includes hardware connection guidance, CamArray composition switching examples, and camera/I2C bus notes.

### Arducam Synchronized Stereo Camera HAT datasheet

https://arducam.com/downloads/modules/RaspberryPi_camera/Synchronized_Stereo_Camera_HAT_DS.pdf

Table 3 documents the 2x3 header mapping:

1. 3V3
2. 5V
3. SDA
4. 5V
5. SCL
6. GND

The same datasheet documents HAT control registers and I2C address information.

### Arducam Pivariety V4L2 driver installer

https://github.com/ArduCAM/Arducam-Pivariety-V4L2-Driver

### Raspberry Pi camera / libcamera documentation

https://www.raspberrypi.com/documentation/computers/camera_software.html

### Raspberry Pi libcamera source/package notes

https://github.com/RPi-Distro/libcamera
