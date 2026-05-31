# Codebase Information

## Project Identity

- **Name**: hc-sr04-detector
- **Version**: 0.2.0
- **License**: MIT
- **Python**: ≥3.11
- **Author**: Andy Browne

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.11+ |
| Distance sensor | gpiozero (DistanceSensor) |
| Sound (optional) | pygame (mixer) |
| Configuration | tomllib (stdlib) |
| CLI | argparse (stdlib) |
| Logging | logging (stdlib) |
| Build | hatchling |
| Testing | pytest, pytest-cov, pytest-mock |

## Directory Structure

```
hc_sr04_motion_detector/
├── hc_sr04_motion_detector/    # Application package
│   ├── __init__.py             # Version metadata
│   ├── __main__.py             # CLI entry point
│   ├── config.py               # Config dataclass + TOML loading
│   ├── sensor.py               # UltrasonicSensor (gpiozero wrapper)
│   ├── actions.py              # Pluggable detection actions
│   └── detector.py             # Detection loop
├── tests/                      # pytest suite
│   ├── conftest.py             # Shared fixtures + hardware mocks
│   ├── test_config.py
│   ├── test_sensor.py
│   ├── test_actions.py
│   └── test_detector.py
├── pyproject.toml              # Project metadata + build config
├── config.example.toml         # Example configuration
├── README.md                   # User documentation
└── LICENSE                     # MIT
```

## Entry Points

| Entry Point | Location |
|-------------|----------|
| CLI command | `hc-sr04-detector` |
| Function | `hc_sr04_motion_detector.__main__:main` |

## Target Platform

- Raspberry Pi (any model)
- HC-SR04 ultrasonic sensor with voltage divider
- Raspberry Pi OS (any version with gpiozero)
