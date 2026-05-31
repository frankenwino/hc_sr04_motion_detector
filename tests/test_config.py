"""Tests for configuration."""

import pytest
from pathlib import Path
from hc_sr04_motion_detector.config import Config, load_config


class TestConfigDefaults:
    def test_default_values(self):
        c = Config()
        assert c.trigger_pin == 23
        assert c.echo_pin == 24
        assert c.distance_threshold_cm == 30.0
        assert c.cooldown_seconds == 2.0
        assert c.measurement_interval == 0.5
        assert c.action == "log"
        assert c.log_level == "INFO"


class TestLoadConfig:
    def test_missing_file_returns_defaults(self):
        assert load_config(Path("/nonexistent")) == Config()

    def test_none_returns_defaults(self):
        assert load_config(None) == Config()

    def test_valid_toml(self, tmp_path):
        f = tmp_path / "c.toml"
        f.write_text('[sensor]\ntrigger_pin = 17\necho_pin = 27\n[detection]\ndistance_threshold_cm = 50.0\n')
        c = load_config(f)
        assert c.trigger_pin == 17
        assert c.echo_pin == 27
        assert c.distance_threshold_cm == 50.0

    def test_invalid_toml_exits(self, tmp_path):
        f = tmp_path / "bad.toml"
        f.write_text("invalid[[[")
        with pytest.raises(SystemExit):
            load_config(f)

    def test_invalid_pin_exits(self, tmp_path):
        f = tmp_path / "c.toml"
        f.write_text('[sensor]\ntrigger_pin = 99\n')
        with pytest.raises(SystemExit):
            load_config(f)

    def test_invalid_threshold_exits(self, tmp_path):
        f = tmp_path / "c.toml"
        f.write_text('[detection]\ndistance_threshold_cm = -5\n')
        with pytest.raises(SystemExit):
            load_config(f)

    def test_invalid_action_exits(self, tmp_path):
        f = tmp_path / "c.toml"
        f.write_text('[action]\ntype = "invalid"\n')
        with pytest.raises(SystemExit):
            load_config(f)
