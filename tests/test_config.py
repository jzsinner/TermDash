"""Tests for TermDash configuration loading."""

from __future__ import annotations

import json

import pytest

from termdash.config import TermDashConfig, load_config


def test_load_config_returns_defaults_when_file_missing(tmp_path) -> None:
    missing_config_path = tmp_path / "missing.json"

    config = load_config(missing_config_path)

    assert config == TermDashConfig()


def test_load_config_reads_valid_file(tmp_path) -> None:
    config_path = tmp_path / "termdash.json"
    config_path.write_text(
        json.dumps(
            {
                "location": "New York",
                "stock_symbols": ["NVDA", "AMD"],
                "crypto_ids": ["bitcoin"],
                "refresh_seconds": 60,
            }
        ),
        encoding="utf-8",
    )

    config = load_config(config_path)

    assert config.location == "New York"
    assert config.stock_symbols == ["NVDA", "AMD"]
    assert config.crypto_ids == ["bitcoin"]
    assert config.refresh_seconds == 60


def test_load_config_rejects_non_object_json(tmp_path) -> None:
    config_path = tmp_path / "termdash.json"
    config_path.write_text(json.dumps(["not", "an", "object"]), encoding="utf-8")

    with pytest.raises(ValueError, match="JSON object"):
        load_config(config_path)


def test_load_config_rejects_invalid_location(tmp_path) -> None:
    config_path = tmp_path / "termdash.json"
    config_path.write_text(json.dumps({"location": ""}), encoding="utf-8")

    with pytest.raises(ValueError, match="location"):
        load_config(config_path)


def test_load_config_rejects_invalid_stock_symbols(tmp_path) -> None:
    config_path = tmp_path / "termdash.json"
    config_path.write_text(
        json.dumps({"stock_symbols": "AAPL"}),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="stock_symbols"):
        load_config(config_path)


def test_load_config_rejects_invalid_refresh_seconds(tmp_path) -> None:
    config_path = tmp_path / "termdash.json"
    config_path.write_text(
        json.dumps({"refresh_seconds": 0}),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="refresh_seconds"):
        load_config(config_path)