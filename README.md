# HC-SR04 Motion Detector

Detects nearby objects using an HC-SR04 ultrasonic distance sensor on a Raspberry Pi. When something is within a configurable distance threshold, triggers a configurable action (log, run a command, or play a sound).

## Hardware Requirements

- Raspberry Pi (any model)
- HC-SR04 ultrasonic distance sensor
- 1kΩ and 2kΩ resistors (voltage divider for echo pin)
- Breadboard and jumper wires

## Wiring

| HC-SR04 Pin | Connection |
|-------------|-----------|
| VCC | 5V (Pin 2) |
| GND | GND (Pin 6) |
| TRIG | BCM 23 (Pin 16) — configurable |
| ECHO | BCM 24 (Pin 18) via voltage divider — configurable |

**Important**: The echo pin requires a voltage divider (1kΩ + 2kΩ) to step down from 5V to 3.3V for the Pi's GPIO.

## Installation

```bash
git clone https://github.com/frankenwino/hc_sr04_motion_detector.git
cd hc_sr04_motion_detector

python3 -m venv .venv
source .venv/bin/activate
pip install -e .

# For sound action support
pip install -e ".[sound]"

# For development
pip install -e ".[dev]"
```

## Configuration

Create a `config.toml` (all values optional — defaults shown):

```toml
[sensor]
trigger_pin = 23
echo_pin = 24

[detection]
distance_threshold_cm = 30.0
cooldown_seconds = 2.0
measurement_interval = 0.5

[action]
type = "log"                          # "log", "command", or "sound"
# command = "echo 'Something detected!'"
# sound = "/path/to/alert.mp3"

[app]
log_level = "INFO"
```

## Usage

```bash
# Run with defaults (log action, 30cm threshold)
hc-sr04-detector

# Run with custom config
hc-sr04-detector --config /path/to/config.toml

# Stop with Ctrl+C
```

## Running Tests

```bash
pytest
pytest -v
pytest --cov --cov-report=term-missing
```

## Troubleshooting

### Sensor not responding

- Check wiring (VCC, GND, TRIG, ECHO)
- Verify voltage divider on echo pin
- Ensure user is in `gpio` group: `sudo usermod -aG gpio $USER`

### Readings always max distance

- Check the sensor is not obstructed
- Verify TRIG and ECHO pins match config
- Try a shorter threshold to confirm sensor works

### Permission denied

```bash
sudo usermod -aG gpio $USER
# Log out and back in
```

## License

MIT — see [LICENSE](LICENSE) for details.
