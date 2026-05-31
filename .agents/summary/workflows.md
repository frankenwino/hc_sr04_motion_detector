# Workflows

## Startup

```mermaid
sequenceDiagram
    participant CLI as __main__
    participant CFG as Config
    participant S as Sensor
    participant A as Actions
    participant D as Detector

    CLI->>CFG: load_config(args.config)
    CLI->>CLI: _setup_logging()
    CLI->>S: UltrasonicSensor(trigger, echo)
    CLI->>A: get_action(config)
    CLI->>D: Detector(config, sensor, action)
    CLI->>D: run()
```

## Detection Cycle

1. `sensor.measure()` → distance in cm
2. If distance < threshold → call `action(distance)` → sleep(cooldown)
3. If distance ≥ threshold → sleep(interval)
4. Repeat

## Shutdown

`KeyboardInterrupt` → `detector.shutdown()` → `sensor.close()`
