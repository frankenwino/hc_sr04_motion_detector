# Interfaces

## CLI

```
hc-sr04-detector [--config PATH]
```

## Configuration (TOML)

```toml
[sensor]
trigger_pin = 23        # BCM 0-27
echo_pin = 24           # BCM 0-27

[detection]
distance_threshold_cm = 30.0
cooldown_seconds = 2.0
measurement_interval = 0.5

[action]
type = "log"            # "log", "command", "sound"
command = "..."         # For type="command"
sound = "/path/to.mp3" # For type="sound"

[app]
log_level = "INFO"
```

## Python APIs

```python
# Config
load_config(config_path: Path | None) -> Config

# Sensor
UltrasonicSensor(trigger_pin: int, echo_pin: int)
UltrasonicSensor.measure() -> float  # cm, or inf on error
UltrasonicSensor.close() -> None

# Actions
get_action(config: Config) -> Callable[[float], None]

# Detector
Detector(config: Config, sensor: UltrasonicSensor, action: Callable)
Detector.run() -> None      # Blocks until KeyboardInterrupt
Detector.shutdown() -> None
```

## Hardware Interface

| HC-SR04 Pin | RPi Connection |
|-------------|---------------|
| VCC | 5V (Pin 2) |
| GND | GND (Pin 6) |
| TRIG | BCM 23 (configurable) |
| ECHO | BCM 24 via voltage divider (configurable) |
