"""Shared test fixtures."""

import sys
from unittest.mock import MagicMock

import pytest

# Mock hardware dependencies
sys.modules.setdefault("gpiozero", MagicMock())
sys.modules.setdefault("pygame", MagicMock())
sys.modules.setdefault("pygame.mixer", MagicMock())
