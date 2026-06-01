"""Configuration loading for TermDash."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


DEFAULT_CONFIG_PATH = Path.home() / ".termdash.json"


@dataclass(frozen=True)
class TermDashConfig:
    """Runtime configuration for TermDash."""

    location: str = "San Francisco"
    stock_symbols: list[str] = field(default_factory=lambda: ["AAPL", "GOOGL", "MSFT", "TSLA"])
    crypto_ids: list[str] = field(default_factory=lambda: ["bitcoin", "ethereum"])
    refresh_seconds: int = 30


def load_config(config_path: Path | None = None) -> TermDashConfig:
    """Load configuration from disk, falling back to defaults when absent."""
    path = config_path or DEFAULT_CONFIG_PATH

    if not path.exists():
        return TermDashConfig()

    with path.open("r", encoding="utf-8") as config_file:
        raw_config = json.load(config_file)

    if not isinstance(raw_config, dict):
        raise ValueError(f"Config file must contain a JSON object: {path}")

    return _parse_config(raw_config)


def _parse_config(raw_config: dict[str, Any]) -> TermDashConfig:
    """Parse raw JSON config values into a typed config object."""
    default_config = TermDashConfig()

    location = _get_string(raw_config, "location", default_config.location)
    stock_symbols = _get_string_list(
        raw_config,
        "stock_symbols",
        default_config.stock_symbols,
    )
    crypto_ids = _get_string_list(
        raw_config,
        "crypto_ids",
        default_config.crypto_ids,
    )
    refresh_seconds = _get_positive_int(
        raw_config,
        "refresh_seconds",
        default_config.refresh_seconds,
    )

    return TermDashConfig(
        location=location,
        stock_symbols=stock_symbols,
        crypto_ids=crypto_ids,
        refresh_seconds=refresh_seconds,
    )


def _get_string(raw_config: dict[str, Any], key: str, default: str) -> str:
    value = raw_config.get(key, default)

    if not isinstance(value, str):
        raise ValueError(f"Config value '{key}' must be a string")

    value = value.strip()
    if not value:
        raise ValueError(f"Config value '{key}' cannot be empty")

    return value


def _get_string_list(raw_config: dict[str, Any], key: str, default: list[str]) -> list[str]:
    value = raw_config.get(key, default)

    if not isinstance(value, list):
        raise ValueError(f"Config value '{key}' must be a list of strings")

    cleaned_values = []
    for item in value:
        if not isinstance(item, str):
            raise ValueError(f"Config value '{key}' must be a list of strings")

        cleaned_item = item.strip()
        if not cleaned_item:
            raise ValueError(f"Config value '{key}' cannot contain empty strings")

        cleaned_values.append(cleaned_item)

    if not cleaned_values:
        raise ValueError(f"Config value '{key}' cannot be empty")

    return cleaned_values


def _get_positive_int(raw_config: dict[str, Any], key: str, default: int) -> int:
    value = raw_config.get(key, default)

    if not isinstance(value, int):
        raise ValueError(f"Config value '{key}' must be an integer")

    if value <= 0:
        raise ValueError(f"Config value '{key}' must be greater than zero")

    return value