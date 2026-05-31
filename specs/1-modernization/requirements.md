# Requirements — HC-SR04 Motion Detector Modernization

## Goal

Modernize the hc_sr04_motion_detector codebase: replace raw RPi.GPIO with gpiozero, fix all bugs, adopt Python 3.11+ idioms, add configurable actions on detection, and produce a maintainable, testable application.

## Target Users

- Raspberry Pi hobbyists running Raspberry Pi OS (Bookworm or later)
- The original author maintaining the project

## Functional Requirements

### FR-1: Distance Measurement Loop

The application must continuously measure distance using an HC-SR04 ultrasonic sensor and trigger an action when an object is within a configurable threshold.

**Acceptance Criteria:**
- Measures distance at configurable intervals (default: 0.5s)
- Triggers when measured distance < threshold (default: 30cm)
- Configurable cooldown after detection (default: 2s)
- Loop runs indefinitely until Ctrl+C

### FR-2: Detection Action

The application must execute a configurable action when an object is detected.

**Acceptance Criteria:**
- Default action: log the detection event
- Optional action: run a shell command (configurable via TOML)
- Optional action: play a sound file (via pygame.mixer, reusing pattern from halloween-motion-detector)
- Actions are pluggable — easy to add new ones

### FR-3: Configuration

The application must support external configuration.

**Acceptance Criteria:**
- Configuration loaded from a TOML file (with sensible defaults if absent)
- Configurable values: trigger pin, echo pin, distance threshold, cooldown, measurement interval, action, log level
- CLI argument to specify config file path

### FR-4: Graceful Shutdown

The application must clean up GPIO resources on exit.

**Acceptance Criteria:**
- GPIO cleaned up on Ctrl+C
- No orphaned processes or pin states

## Non-Functional Requirements

### NFR-1: Python 3.11+ Only

- Drop Python 2.x support
- Use type hints, `pathlib`, f-strings, `tomllib`, dataclasses

### NFR-2: Use gpiozero

- Replace raw `RPi.GPIO` with `gpiozero.DistanceSensor`
- Simpler API, better error messages, mock-friendly for testing

### NFR-3: Correct Dependencies

- All runtime dependencies declared in `pyproject.toml`
- Use `pyproject.toml` with hatchling build backend

### NFR-4: Error Handling

- Sensor initialization failure: clear error message and exit
- Invalid distance readings: log warning, skip iteration
- Missing config file: use defaults (no error)
- Invalid TOML: clear error and exit

### NFR-5: Logging

- Use Python `logging` module instead of `print()`
- Configurable log level (default: INFO)

### NFR-6: Testability

- Sensor abstracted for mocking
- Unit tests with pytest
- Minimum 80% coverage on non-hardware code

#### Unit Tests

- Config loading (valid, missing, invalid TOML, validation)
- Distance measurement logic (mocked sensor)
- Detection trigger logic (threshold comparison)
- Action execution (mocked)

#### Integration Tests

- Full detection cycle (mock sensor returns < threshold → action triggered)
- Graceful shutdown (KeyboardInterrupt → cleanup)
- Config override via CLI

### NFR-7: Documentation (README)

- Clear README.md with wiring diagram reference, installation, configuration, usage, testing, troubleshooting

### NFR-8: Modern Packaging

- `pyproject.toml` as single source of metadata
- Remove all legacy files
- Entry point: `hc-sr04-detector` CLI command

## Constraints

- Must run on Raspberry Pi (ARM)
- `gpiozero` cannot be fully tested off-device (mock `DistanceSensor`)
- HC-SR04 requires voltage divider on echo pin (3.3V logic)

## Out of Scope

- Web dashboard
- Multiple sensor support
- Recording/camera integration (use halloween-motion-detector for that)
- Stepper motor control (was in a related repo)
