"""Tests for TermDash command-line arguments."""

from __future__ import annotations

from pathlib import Path

import pytest

from termdash.cli import apply_cli_overrides, parse_args
from termdash.config import TermDashConfig


def test_parse_args_defaults() -> None:
    args = parse_args([])

    assert args.config is None
    assert args.refresh_seconds is None


def test_parse_args_accepts_config_path() -> None:
    args = parse_args(["--config", "custom-config.json"])

    assert args.config == Path("custom-config.json")


def test_parse_args_accepts_refresh_seconds() -> None:
    args = parse_args(["--refresh-seconds", "15"])

    assert args.refresh_seconds == 15


def test_apply_cli_overrides_updates_refresh_seconds() -> None:
    config = TermDashConfig(refresh_seconds=30)
    args = parse_args(["--refresh-seconds", "15"])

    updated_config = apply_cli_overrides(config, args)

    assert updated_config.refresh_seconds == 15


def test_apply_cli_overrides_rejects_invalid_refresh_seconds() -> None:
    config = TermDashConfig(refresh_seconds=30)
    args = parse_args(["--refresh-seconds", "0"])

    with pytest.raises(ValueError, match="refresh-seconds"):
        apply_cli_overrides(config, args)
