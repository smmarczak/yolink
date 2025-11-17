# YoLink Custom Integration for Home Assistant

This is a custom version of the YoLink integration with additional device support.

## Features

This custom integration extends the official YoLink integration with enhanced support for:

### YS5008-UC Water Meter
- **Real-time water running detection** - Binary sensor using `recentUsage` field
- **Flow rate sensor** - Gallons per minute (GPM) for instant flow monitoring
- **Recent usage sensor** - Water used in most recent period
- **Daily usage sensor** - Total daily water consumption
- All sensors update in real-time via MQTT

### Additional Resources
- **[Sensors Guide](SENSORS_GUIDE.md)** - Complete documentation of all sensors and automation examples
- **[Template Sensors](template_sensors.yaml)** - Optional calculated sensors (dew point, heat index, comfort indicators)

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
