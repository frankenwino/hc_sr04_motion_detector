# Data Models

## Config Dataclass

```python
@dataclass
class Config:
    trigger_pin: int = 23
    echo_pin: int = 24
    distance_threshold_cm: float = 30.0
    cooldown_seconds: float = 2.0
    measurement_interval: float = 0.5
    action: str = "log"
    action_command: str | None = None
    action_sound: Path | None = None
    log_level: str = "INFO"
```

## Runtime State

| Component | State | Description |
|-----------|-------|-------------|
| UltrasonicSensor | `_sensor` | gpiozero.DistanceSensor instance |
| Detector | `_config`, `_sensor`, `_action` | Injected dependencies |

No persistent state. No file outputs. No database.
