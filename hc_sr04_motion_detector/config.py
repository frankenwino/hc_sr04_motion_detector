"""Configuration loading and validation."""

import logging
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class Config:
    """Application configuration with sensible defaults."""

    trigger_pin: int = 23
    echo_pin: int = 24
    distance_threshold_cm: float = 30.0
    cooldown_seconds: float = 2.0
    measurement_interval: float = 0.5
    action: str = "log"
    action_command: str | None = None
    action_sound: Path | None = None
    log_level: str = "INFO"


def load_config(config_path: Path | None = None) -> Config:
    """Load config from TOML file. Returns defaults if file is missing."""
    if config_path is None or not config_path.exists():
        return Config()

    try:
        with open(config_path, "rb") as f:
            data = tomllib.load(f)
    except tomllib.TOMLDecodeError as e:
        logger.error("Invalid config file %s: %s", config_path, e)
        sys.exit(1)

    sensor = data.get("sensor", {})
    detection = data.get("detection", {})
    action = data.get("action", {})
    app = data.get("app", {})

    config = Config(
        trigger_pin=sensor.get("trigger_pin", Config.trigger_pin),
        echo_pin=sensor.get("echo_pin", Config.echo_pin),
        distance_threshold_cm=detection.get("distance_threshold_cm", Config.distance_threshold_cm),
        cooldown_seconds=detection.get("cooldown_seconds", Config.cooldown_seconds),
        measurement_interval=detection.get("measurement_interval", Config.measurement_interval),
        action=action.get("type", Config.action),
        action_command=action.get("command"),
        action_sound=Path(action["sound"]) if "sound" in action else None,
        log_level=app.get("log_level", Config.log_level),
    )

    _validate(config)
    return config


def _validate(config: Config) -> None:
    """Validate config values, exit on failure."""
    if not 0 <= config.trigger_pin <= 27:
        logger.error("Trigger pin must be 0–27, got %s", config.trigger_pin)
        sys.exit(1)
    if not 0 <= config.echo_pin <= 27:
        logger.error("Echo pin must be 0–27, got %s", config.echo_pin)
        sys.exit(1)
    if config.distance_threshold_cm <= 0:
        logger.error("Distance threshold must be > 0, got %s", config.distance_threshold_cm)
        sys.exit(1)
    if config.cooldown_seconds < 0:
        logger.error("Cooldown must be >= 0, got %s", config.cooldown_seconds)
        sys.exit(1)
    if config.measurement_interval <= 0:
        logger.error("Measurement interval must be > 0, got %s", config.measurement_interval)
        sys.exit(1)
    if config.action not in ("log", "command", "sound"):
        logger.error("Action must be 'log', 'command', or 'sound', got '%s'", config.action)
        sys.exit(1)
