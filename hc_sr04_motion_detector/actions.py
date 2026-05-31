"""Pluggable detection actions."""

import logging
import subprocess
from collections.abc import Callable
from pathlib import Path

from .config import Config

logger = logging.getLogger(__name__)


def get_action(config: Config) -> Callable[[float], None]:
    """Return the appropriate action function based on config."""
    if config.action == "command" and config.action_command:
        cmd = config.action_command
        return lambda distance: _command_action(cmd, distance)
    elif config.action == "sound" and config.action_sound:
        path = config.action_sound
        return lambda distance: _sound_action(path, distance)
    return _log_action


def _log_action(distance: float) -> None:
    """Default action: log the detection."""
    logger.info("DETECTED: object at %.1f cm", distance)


def _command_action(command: str, distance: float) -> None:
    """Run a shell command on detection."""
    logger.info("DETECTED at %.1f cm — running: %s", distance, command)
    try:
        subprocess.run(command, shell=True, check=False, timeout=10)
    except Exception as e:
        logger.warning("Command failed: %s", e)


def _sound_action(sound_path: Path, distance: float) -> None:
    """Play a sound file on detection."""
    logger.info("DETECTED at %.1f cm — playing: %s", distance, sound_path.name)
    try:
        from pygame import mixer

        if not mixer.get_init():
            mixer.init()
        mixer.music.load(str(sound_path))
        mixer.music.play()
    except Exception as e:
        logger.warning("Sound playback failed: %s", e)
