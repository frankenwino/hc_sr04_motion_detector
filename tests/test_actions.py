"""Tests for actions module."""

from unittest.mock import patch, MagicMock
from pathlib import Path

from hc_sr04_motion_detector.config import Config
from hc_sr04_motion_detector.actions import get_action, _log_action, _command_action


class TestGetAction:
    def test_default_returns_log_action(self):
        config = Config()
        action = get_action(config)
        assert action is _log_action

    def test_command_action(self):
        config = Config(action="command", action_command="echo hi")
        action = get_action(config)
        assert action is not _log_action

    def test_sound_action(self):
        config = Config(action="sound", action_sound=Path("/fake/sound.mp3"))
        action = get_action(config)
        assert action is not _log_action


class TestLogAction:
    def test_does_not_raise(self):
        _log_action(25.5)  # Should just log


class TestCommandAction:
    @patch("hc_sr04_motion_detector.actions.subprocess.run")
    def test_runs_command(self, mock_run):
        _command_action("echo detected", 15.0)
        mock_run.assert_called_once_with("echo detected", shell=True, check=False, timeout=10)

    @patch("hc_sr04_motion_detector.actions.subprocess.run", side_effect=OSError("fail"))
    def test_handles_failure(self, mock_run):
        _command_action("bad_cmd", 10.0)  # Should not raise
