"""Tests for sensor wrapper."""

import sys
from unittest.mock import MagicMock
from hc_sr04_motion_detector.sensor import UltrasonicSensor


class TestUltrasonicSensor:
    def test_measure_returns_cm(self):
        mock_gpiozero = sys.modules["gpiozero"]
        mock_sensor = mock_gpiozero.DistanceSensor.return_value
        mock_sensor.distance = 0.30  # 30cm in meters

        sensor = UltrasonicSensor(23, 24)
        assert sensor.measure() == 30.0

    def test_measure_error_returns_inf(self):
        mock_gpiozero = sys.modules["gpiozero"]
        mock_sensor = mock_gpiozero.DistanceSensor.return_value
        mock_sensor.distance = property(lambda self: (_ for _ in ()).throw(RuntimeError("fail")))
        # Simpler: make .distance raise
        type(mock_sensor).distance = property(lambda self: (_ for _ in ()).throw(RuntimeError()))

        sensor = UltrasonicSensor(23, 24)
        result = sensor.measure()
        assert result == float("inf")

        # Reset
        type(mock_sensor).distance = MagicMock(return_value=0.5)

    def test_close(self):
        mock_gpiozero = sys.modules["gpiozero"]
        mock_sensor = mock_gpiozero.DistanceSensor.return_value

        sensor = UltrasonicSensor(23, 24)
        sensor.close()
        mock_sensor.close.assert_called()
