# AGENTS.md

<!-- tags: navigation, architecture, conventions -->

## Project Overview

Raspberry Pi HC-SR04 ultrasonic distance detector. Polls sensor, triggers configurable action when object is within threshold. Python 3.11+, gpiozero, TOML config.

**Entry point**: `hc_sr04_motion_detector/__main__.py` → `main()`
**CLI**: `hc-sr04-detector [--config PATH]`

## Directory Map

```
hc_sr04_motion_detector/        # Application package
├── __main__.py                 # Entry: args → config → sensor → action → detector
├── config.py                   # Config dataclass + TOML loading + validation
├── sensor.py                   # UltrasonicSensor (gpiozero.DistanceSensor wrapper)
├── actions.py                  # Pluggable actions: log, command, sound
└── detector.py                 # Polling detection loop
tests/                          # pytest suite (21 tests, 86% coverage)
```

## Architecture

Polling loop: `measure()` → compare threshold → trigger action or sleep → repeat.

- **gpiozero.DistanceSensor** handles ultrasonic timing (returns meters, converted to cm)
- **Actions are callables** returned by `get_action(config)` factory
- **Lazy pygame import** — only if action="sound"
- **`float('inf')` on error** — measurement failures don't trigger false positives

## Patterns That Deviate from Defaults

- **Pluggable action system** — factory returns callable based on config `action.type`
- **Optional pygame dependency** — declared in `[project.optional-dependencies.sound]`
- **Sensor returns inf on error** — not 0 or None, prevents false triggers

## Error Handling

| Scenario | Result |
|----------|--------|
| Sensor init failure | CRITICAL, exit |
| Invalid reading | WARNING, returns inf (skips) |
| Invalid config | ERROR, exit |
| Command action fails | WARNING, continues |
| Sound file missing | WARNING, continues |

## Detailed Documentation

See `.agents/summary/index.md` for full documentation.

## Custom Instructions
<!-- This section is for human and agent-maintained operational knowledge.
     Add repo-specific conventions, gotchas, and workflow rules here.
     This section is preserved exactly as-is when re-running codebase-summary. -->
