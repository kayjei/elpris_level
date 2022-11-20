# Integration 
Home assistant integration to calculate price level for energy per hour with purpose to minimize energy cost. 

## Prerequisites
This integration is using the nordpool custom component for hourly rates.
Nordpool custom component is found at https://github.com/custom-components/nordpool

1. Download the folder elpris_level into $CONFIG/custom_components/
2. Add configuration to your ```sensors.yaml```

```
  - platform: elpris_level
    entity_id: <nordpool entity id>
```

Or add it as a custom repo from HACS

Sensor will be available as sensor.elpris_level
