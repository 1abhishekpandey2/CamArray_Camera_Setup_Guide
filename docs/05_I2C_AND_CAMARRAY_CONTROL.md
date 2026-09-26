# 5. I2C and CamArray Control

## Physical control header

The CamArray / synchronized stereo HAT 2x3 header maps one-to-one to Raspberry Pi physical pins 1 through 6. See [Hardware Wiring](01_HARDWARE_WIRING.md).

## HAT I2C address

The Arducam synchronized stereo HAT datasheet documents a default 7-bit HAT slave address of:

```text
0x24
```

## Discover the Linux I2C buses first

```bash
i2cdetect -l
```

The correct bus number depends on the board and the camera stack. Current Arducam documentation uses different examples for Pi 4 and Pi 5, so do not hard-code a bus number without checking the system.

For example, current Arducam CamArray documentation shows Pi 4 composition switching using an `i2c-10` camera-control bus in some libcamera configurations.

## Example channel/composition commands

Only run these after identifying the correct camera-control I2C bus for your installation.

Using bus `10` as an **example**:

```bash
# Single channel 0
i2cset -y 10 0x24 0x24 0x02

# Single channel 1
i2cset -y 10 0x24 0x24 0x12

# Dual channel 0 + 1
i2cset -y 10 0x24 0x24 0x01

# Four-in-one/default composition on supported kits
i2cset -y 10 0x24 0x24 0x00
```

These values are vendor examples for CamArray composition switching. The exact supported modes depend on the HAT/firmware revision. Always check the specific Arducam product documentation before changing modes.

## Why the project normally leaves composition alone

The main project assumes the HAT already produces the synchronized combined stereo frame expected by the software. Once the stream is confirmed as `1280 x 400`, no channel-switch command is required during normal capture.
