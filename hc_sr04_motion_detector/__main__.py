"""Entry point for hc-sr04-detector."""

import argparse
import logging
from pathlib import Path

from .actions import get_action
from .config import load_config
from .detector import Detector
from .sensor import UltrasonicSensor


def main() -> None:
    args = _parse_args()
    config = load_config(args.config)
    _setup_logging(config.log_level)

    sensor = UltrasonicSensor(config.trigger_pin, config.echo_pin)
    action = get_action(config)
    detector = Detector(config, sensor, action)
    detector.run()


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="hc-sr04-detector",
        description="HC-SR04 ultrasonic motion detector",
    )
    parser.add_argument("--config", type=Path, default=None, help="Path to config.toml")
    return parser.parse_args()


def _setup_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


if __name__ == "__main__":
    main()
