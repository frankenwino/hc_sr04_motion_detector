"""Tests for detector loop."""

from unittest.mock import MagicMock, patch
import pytest

from hc_sr04_motion_detector.config import Config
from hc_sr04_motion_detector.detector import Detector


class TestDetector:
    @pytest.fixture
    def config(self):
        return Config(cooldown_seconds=0, measurement_interval=0)

    @pytest.fixture
    def mock_sensor(self):
        return MagicMock()

    @pytest.fixture
    def mock_action(self):
        return MagicMock()

    @patch("hc_sr04_motion_detector.detector.time.sleep")
    def test_triggers_action_when_below_threshold(self, mock_sleep, config, mock_sensor, mock_action):
        # First measure: 20cm (below 30cm threshold), then KeyboardInterrupt
        mock_sensor.measure.side_effect = [20.0, KeyboardInterrupt]

        detector = Detector(config, mock_sensor, mock_action)
        detector.run()

        mock_action.assert_called_once_with(20.0)

    @patch("hc_sr04_motion_detector.detector.time.sleep")
    def test_no_action_when_above_threshold(self, mock_sleep, config, mock_sensor, mock_action):
        mock_sensor.measure.side_effect = [50.0, KeyboardInterrupt]

        detector = Detector(config, mock_sensor, mock_action)
        detector.run()

        mock_action.assert_not_called()

    @patch("hc_sr04_motion_detector.detector.time.sleep")
    def test_shutdown_closes_sensor(self, mock_sleep, config, mock_sensor, mock_action):
        detector = Detector(config, mock_sensor, mock_action)
        detector.shutdown()
        mock_sensor.close.assert_called_once()

    @patch("hc_sr04_motion_detector.detector.time.sleep")
    def test_keyboard_interrupt_triggers_shutdown(self, mock_sleep, config, mock_sensor, mock_action):
        mock_sensor.measure.side_effect = KeyboardInterrupt

        detector = Detector(config, mock_sensor, mock_action)
        detector.run()

        mock_sensor.close.assert_called_once()
