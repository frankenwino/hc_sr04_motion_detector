# Implementation Tasks — HC-SR04 Motion Detector Modernization

## Task Group 1: Project Scaffolding

**Dependency:** None
**Estimate:** 1 hour

### Task 1.1: Create `pyproject.toml`

- Metadata, Python ≥3.11, deps (gpiozero), optional deps (pygame), dev deps (pytest stack)
- Entry point: `hc-sr04-detector = "hc_sr04_motion_detector.__main__:main"`
- Hatchling build backend

### Task 1.2: Create module skeleton

- `hc_sr04_motion_detector/{__init__, __main__, config, sensor, detector, actions}.py`

### Task 1.3: Remove legacy files

- Delete `docs/`, `AUTHORS.rst`, `CONTRIBUTING.rst`, old tests, old `__init__.py`

**Completion criteria:** `pip install -e ".[dev]"` succeeds; entry point runs.

---

## Task Group 2: Configuration

**Dependency:** Task Group 1
**Estimate:** 1 hour

### Task 2.1: Implement Config dataclass + TOML loading

- All fields with defaults per design.md
- CLI `--config` flag
- Validate: pins 0–27, threshold > 0, cooldown ≥ 0, interval > 0

**Completion criteria:** Unit tests pass.

---

## Task Group 3: Sensor

**Dependency:** Task Group 2
**Estimate:** 1 hour

### Task 3.1: Implement UltrasonicSensor

- Wrap `gpiozero.DistanceSensor(trigger=pin, echo=pin)`
- `measure()`: return `sensor.distance * 100` (meters → cm)
- `close()`: `sensor.close()`
- Handle init failure gracefully

**Completion criteria:** Unit tests pass with mocked gpiozero.

---

## Task Group 4: Actions

**Dependency:** Task Group 2
**Estimate:** 30 minutes

### Task 4.1: Implement action functions

- `log_action(distance)`: log INFO message
- `command_action(command, distance)`: `subprocess.run(command, shell=True)`
- `sound_action(sound_path, distance)`: pygame.mixer playback
- `get_action(config)`: factory returning the appropriate callable

**Completion criteria:** Unit tests pass with mocked subprocess/pygame.

---

## Task Group 5: Detector Loop

**Dependency:** Task Groups 3 and 4
**Estimate:** 1 hour

### Task 5.1: Implement Detector

- `run()`: measure → compare → act/sleep → repeat
- `shutdown()`: close sensor
- KeyboardInterrupt handling

**Completion criteria:** Integration tests pass with mocked sensor.

---

## Task Group 6: Entry Point & Logging

**Dependency:** Task Group 5
**Estimate:** 30 minutes

### Task 6.1: Wire up `__main__.py`

- Parse args → config → logging → sensor → action → detector → run

**Completion criteria:** Full startup works (mocked in tests).

---

## Task Group 7: Tests

**Dependency:** Task Groups 1–6
**Estimate:** 2 hours

### Task 7.1: Unit + integration tests

- test_config.py, test_sensor.py, test_actions.py, test_detector.py, test_integration.py
- conftest.py with shared fixtures

**Completion criteria:** `pytest --cov --cov-fail-under=80` passes.

---

## Task Group 8: Documentation

**Dependency:** Task Group 7
**Estimate:** 30 minutes

### Task 8.1: Write README.md

- Wiring reference, installation, configuration, usage, tests, troubleshooting

**Completion criteria:** README complete, old docs removed.

---

## Summary

| Group | Description | Estimate | Depends On |
|-------|-------------|----------|------------|
| 1 | Scaffolding | 1h | — |
| 2 | Configuration | 1h | 1 |
| 3 | Sensor | 1h | 2 |
| 4 | Actions | 30m | 2 |
| 5 | Detector loop | 1h | 3, 4 |
| 6 | Entry point | 30m | 5 |
| 7 | Tests | 2h | 1–6 |
| 8 | Documentation | 30m | 7 |

**Total estimate:** 7–9 hours
