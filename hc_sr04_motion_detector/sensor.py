"""Ultrasonic distance sensor wrapper."""

import logging
import sys

from gpiozero import DistanceSensor

logger = logging.getLogger(__name__)


class UltrasonicSensor:
    """Wraps gpiozero.DistanceSensor for HC-SR04."""

    def __init__(self, trigger_pin: int, echo_pin: int) -> None:
        try:
            self._sensor = DistanceSensor(trigger=trigger_pin, echo=echo_pin)
            logger.info("Sensor initialized (trigger=%d, echo=%d)", trigger_pin, echo_pin)
        except Exception as e:
            logger.critical("Failed to initialize sensor: %s", e)
            sys.exit(1)

    def measure(self) -> float:
        """Return distance in centimeters. Returns inf on error."""
        try:
            return self._sensor.distance * 100
        except Exception as e:
            logger.warning("Measurement error: %s", e)
            return float("inf")

    def close(self) -> None:
        """Release sensor resources."""
        self._sensor.close()
        logger.info("Sensor closed.")
