# YoLink Custom Integration - Sensors Guide

## New Water Meter Sensors (YS5008-UC)

This custom integration adds the following sensors for your YS5008-UC water meters that aren't in the core integration:

### Real-Time Sensors

1. **Water Running** (`binary_sensor.main_water_meter_water_running`)
   - **Type**: Binary Sensor
   - **Purpose**: Instant detection when water is flowing
   - **Use Cases**:
     - Leak detection alerts
     - "Water left running" notifications
     - Usage pattern tracking
   - **Updates**: Real-time via MQTT

2. **Flow Rate** (`sensor.main_water_meter_flow_rate`)
   - **Type**: Sensor
   - **Unit**: Gallons per minute (GPM)
   - **Purpose**: Current water flow rate
   - **Use Cases**:
     - Detect slow leaks (constant low flow)
     - Monitor high-flow fixtures
     - Track instantaneous usage

3. **Recent Usage** (`sensor.main_water_meter_recent_usage`)
   - **Type**: Sensor
   - **Unit**: Gallons
   - **Purpose**: Water used in the most recent measurement period
   - **Use Cases**:
     - Track individual fixture usage
     - Detect usage patterns
     - Quick usage snapshots

4. **Daily Usage** (`sensor.main_water_meter_daily_usage`)
   - **Type**: Sensor
   - **Unit**: Gallons
   - **Purpose**: Total water used today
   - **State Class**: Total Increasing
   - **Use Cases**:
     - Daily consumption tracking
     - Cost calculations
     - Conservation monitoring
     - Energy dashboard integration

## Automation Ideas

### Leak Detection
```yaml
automation:
  - alias: "Water Leak Alert"
    trigger:
      - platform: state
        entity_id: binary_sensor.main_water_meter_water_running
        to: "on"
        for:
          minutes: 30
    condition:
      - condition: time
        after: "22:00:00"
        before: "06:00:00"
    action:
      - service: notify.mobile_app
        data:
          message: "Water has been running for 30 minutes at night!"
          title: "Possible Water Leak"
```

### High Usage Alert
```yaml
automation:
  - alias: "High Water Usage Alert"
    trigger:
      - platform: numeric_state
        entity_id: sensor.main_water_meter_daily_usage
        above: 200  # gallons
    action:
      - service: notify.mobile_app
        data:
          message: "Daily water usage exceeded 200 gallons"
```

### Flow Rate Monitoring
```yaml
automation:
  - alias: "High Flow Rate Alert"
    trigger:
      - platform: numeric_state
        entity_id: sensor.main_water_meter_flow_rate
        above: 10  # GPM
    action:
      - service: notify.mobile_app
        data:
          message: "High water flow detected: {{ states('sensor.main_water_meter_flow_rate') }} GPM"
```

## Template Sensors (Optional)

See `template_sensors.yaml` for additional calculated sensors you can add:

### Dew Point Sensors
- **Purpose**: Identify condensation risk, mold prevention
- **Locations**: All temp/humidity sensors (Garage, Living Room, Master Bedroom, Outside, Sauna, Stan4 Room)
- **Formula**: Temperature - ((100 - Humidity) / 5)

### Heat Index (Sauna)
- **Purpose**: "Feels like" temperature
- **When**: Temperature > 27°C (80°F)
- **Use Case**: Sauna safety monitoring

### Absolute Humidity
- **Purpose**: Actual moisture content (g/m³)
- **Use Case**: Compare moisture levels across rooms regardless of temperature

### Binary Sensors
- **Sauna Ready**: Alerts when sauna reaches target temperature (> 60°C)
- **Condensation Risk**: Warns when dew point is within 3°C of temperature
- **Comfort Level**: Indicates if room is in comfort zone (18-24°C, 30-60% RH)

## Installation

### Via HACS
1. Add repository: `https://github.com/smmarczak/yolink`
2. Install "YoLink (Custom)"
3. Restart Home Assistant
4. Configure integration

### Template Sensors (Optional)
1. Copy contents of `template_sensors.yaml`
2. Add to your `configuration.yaml` under the `template:` section
3. Restart Home Assistant or reload template entities

## Energy Dashboard Integration

Add water meter sensors to your Energy Dashboard:

1. **Settings → Dashboards → Energy**
2. **Water → Add Water Source**
3. Select: `sensor.main_water_meter_daily_usage` or `sensor.main_water_meter_water_meter_reading`
4. Set unit cost if desired

## Device-Specific Features

### Temperature/Humidity Sensors
- **Available Sensors**: Temperature, Humidity, Battery, Signal Strength
- **Template Options**: Dew Point, Heat Index, Absolute Humidity, Comfort Indicators

### Door Sensors
- **Available Sensors**: Door State, Battery
- **Automation Ideas**:
  - Duration open tracking
  - Night-time open alerts
  - Security monitoring

### Water Meters (YS5008-UC)
- **Available Sensors**:
  - Water meter reading (total)
  - Flow rate (GPM)
  - Recent usage
  - Daily usage
  - Water running status
  - Battery
  - Signal strength
  - Temperature
  - Moisture (leak detection)
- **Valve Control**: Open/close water valve

## Troubleshooting

### Water Running Sensor Always Shows "Off"
1. Verify you have a YS5008-UC model (not YS5007)
2. Check if `recentUsage` is updating in device attributes
3. Turn on water and wait ~10-30 seconds for MQTT update

### Sensors Not Appearing
1. Reload the integration (Settings → Devices & Services → YoLink (Custom) → Reload)
2. Check device model matches supported models
3. Restart Home Assistant

### Template Sensors Show "Unavailable"
1. Verify entity IDs match your actual sensor names
2. Check that base sensors have valid values
3. Look for errors in Settings → System → Logs

## Credits

Based on the official Home Assistant YoLink integration.

Custom enhancements:
- YS5008-UC water running detection using `recentUsage` field
- Additional water meter sensors (flow rate, recent usage, daily usage)
- Template sensor examples for calculated values
