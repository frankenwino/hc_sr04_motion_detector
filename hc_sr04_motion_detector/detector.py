"""Detection loop."""

import logging
import time
from collections.abc import Callable

from .config import Config
from .sensor import UltrasonicSensor

logger = logging.getLogger(__name__)


class Detector:
    """Polls sensor and triggers action when object is within threshold."""

    def __init__(self, config: Config, sensor: UltrasonicSensor, action: Callable[[float], None]) -> None:
        self._config = config
        self._sensor = sensor
        self._action = action

    def run(self) -> None:
        """Run detection loop until KeyboardInterrupt."""
        logger.info(
            "Detector ready. Threshold: %.1f cm, cooldown: %.1fs",
            self._config.distance_threshold_cm,
            self._config.cooldown_seconds,
        )
        try:
            while True:
                distance = self._sensor.measure()

                if distance < self._config.distance_threshold_cm:
                    self._action(distance)
                    time.sleep(self._config.cooldown_seconds)
                else:
                    time.sleep(self._config.measurement_interval)
        except KeyboardInterrupt:
            logger.info("Interrupted. Shutting down...")
            self.shutdown()

    def shutdown(self) -> None:
        """Release resources."""
        self._sensor.close()
        logger.info("Shutdown complete.")
