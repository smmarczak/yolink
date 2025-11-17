# YoLink Custom Integration for Home Assistant

This is a custom version of the YoLink integration with additional device support.

## Features

This custom integration extends the official YoLink integration with support for:

- **YS5008-UC Water Meter**: Added real-time water running detection via binary sensor

## Installation via HACS

### Prerequisites

1. [HACS](https://hacs.xyz/) must be installed in your Home Assistant instance
2. Remove the core YoLink integration if installed

### Installation Steps

1. **Add Custom Repository**:
   - Open HACS in Home Assistant
   - Click the three dots menu (⋮) in the top right
   - Select "Custom repositories"
   - Add this repository URL: `https://github.com/smmarczak/yolink`
   - Select category: "Integration"
   - Click "Add"

2. **Install the Integration**:
   - Search for "YoLink" in HACS
   - Click "Download"
   - Restart Home Assistant

3. **Configure**:
   - Go to Settings → Devices & Services
   - Click "+ Add Integration"
   - Search for "YoLink"
   - Follow the configuration steps

## Supported Devices

This integration includes all devices from the official YoLink integration, plus:

### Water Meters with Water Running Detection
- YS5008-UC - Water Meter Controller
- YS5018-UC - Water Meter (US version)
- YS5018-EC - Water Meter (European version)

The water running binary sensor provides real-time detection when water is flowing, enabling immediate alerts for:
- Running faucets/fixtures
- Potential leaks
- Water usage monitoring

## Differences from Core Integration

- **YS5008-UC Support**: The core integration doesn't include the YS5008-UC model in the water running sensor
- **Real-time Flow Detection**: Binary sensor for immediate water flow detection (vs. cumulative meter reading only)

## Issues

If you encounter any issues with this custom integration, please [open an issue](https://github.com/smmarczak/yolink/issues) on GitHub.

## Credits

Based on the official Home Assistant YoLink integration by [@matrixd2](https://github.com/matrixd2).
