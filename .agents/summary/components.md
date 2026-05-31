# Components

## Config (`config.py`)

- `Config` dataclass: pins, threshold, cooldown, interval, action type/params, log level
- `load_config(path)`: TOML parsing with defaults
- `_validate()`: pin range, threshold > 0, cooldown ≥ 0, interval > 0, action type valid

## UltrasonicSensor (`sensor.py`)

- Wraps `gpiozero.DistanceSensor`
- `measure()`: returns distance in cm (`sensor.distance * 100`)
- `close()`: releases GPIO resources
- Returns `inf` on measurement error

## Actions (`actions.py`)

- `get_action(config)`: factory returning appropriate callable
- `_log_action(distance)`: logs detection at INFO level
- `_command_action(command, distance)`: runs shell command via subprocess
- `_sound_action(sound_path, distance)`: plays MP3 via pygame.mixer

## Detector (`detector.py`)

- `run()`: polling loop — measure → compare → act or sleep
- `shutdown()`: closes sensor
- Catches `KeyboardInterrupt` for clean exit

## Entry Point (`__main__.py`)

- Parse `--config` → load config → setup logging → create sensor → get action → run detector
