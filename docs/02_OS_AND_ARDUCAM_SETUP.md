# 2. Raspberry Pi OS and Arducam Setup

## Known-good operating system

The known-good development system used **Debian / Raspberry Pi OS Bullseye on AArch64 (64-bit)**.

This guide records that environment because it is the one that was verified with the project hardware. Newer Raspberry Pi OS releases may use different camera commands (`rpicam-*` rather than `libcamera-*`) and different boot file locations.

## Step 1: install prerequisite packages

```bash
sudo apt update
sudo apt install -y \
  wget git i2c-tools v4l-utils \
  python3 python3-pip python3-venv python3-opencv \
  gstreamer1.0-tools \
  gstreamer1.0-plugins-base \
  gstreamer1.0-plugins-good \
  gstreamer1.0-plugins-bad \
  gstreamer1.0-libav
```

Useful diagnostic tools installed here:

- `i2cdetect`, `i2cset` from `i2c-tools`
- `v4l2-ctl` from `v4l-utils`
- `gst-launch-1.0`, `gst-inspect-1.0` from GStreamer tools
- system `cv2` from `python3-opencv`

## Step 2: install Arducam Pivariety packages

The commands below were recovered from the shell history of the working project machine:

```bash
cd ~
wget -O install_pivariety_pkgs.sh \
  https://github.com/ArduCAM/Arducam-Pivariety-V4L2-Driver/releases/download/install_script/install_pivariety_pkgs.sh
chmod +x install_pivariety_pkgs.sh

./install_pivariety_pkgs.sh -p libcamera_dev
./install_pivariety_pkgs.sh -p libcamera_apps
sudo apt install -y libcamera-v4l2
```

Do not substitute the legacy `MIPI_Camera` SDK for this project unless intentionally reproducing an older Arducam stack. The verified project system uses the **Pivariety V4L2 kernel module plus libcamera**.

## Step 3: edit `/boot/config.txt`

On Bullseye:

```bash
sudo nano /boot/config.txt
```

Ensure the following lines exist in the appropriate section:

```ini
dtparam=i2c_arm=on
camera_auto_detect=0
dtoverlay=vc4-kms-v3d
dtoverlay=arducam-pivariety
```

Save and reboot:

```bash
sudo reboot
```

## Step 4: confirm kernel modules

```bash
lsmod | grep -Ei 'arducam|unicam|v4l2'
```

The working system included modules such as:

```text
arducam_pivariety
bcm2835_unicam
bcm2835_isp
bcm2835_v4l2
```

## Step 5: inspect camera devices

```bash
ls -l /dev/video* 2>/dev/null
ls -l /dev/i2c* 2>/dev/null
i2cdetect -l
```

Multiple `/dev/video*` entries are normal because the Raspberry Pi camera/ISP stack exposes several video nodes.

## Step 6: verify with libcamera

```bash
libcamera-hello --list-cameras
libcamera-hello -t 0 --camera 0
```

If `libcamera-hello` is unavailable on a newer OS, the equivalent application may be named `rpicam-hello`.
