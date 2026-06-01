# TermDash Architecture

TermDash is an early-stage terminal dashboard for developers and power users. The project is intentionally small, local-first, and structured to keep terminal rendering, configuration, and data retrieval easy to understand.

## Current package layout

```text
termdash/
  __init__.py
  cli.py
  config.py
tests/
  test_config.py
  test_package.py
```

## CLI entry point

The `termdash` command is defined in `pyproject.toml` and points to:

```text
termdash.cli:main
```

The CLI module is currently responsible for starting the dashboard, rendering the terminal UI, refreshing data, and handling shutdown behavior.

## Configuration loading

Configuration is handled by `termdash/config.py`.

TermDash looks for an optional local configuration file at:

```text
~/.termdash.json
```

If no config file is present, TermDash uses built-in defaults.

Supported configuration fields currently include:

```json
{
  "location": "San Francisco",
  "stock_symbols": ["AAPL", "GOOGL", "MSFT", "TSLA"],
  "crypto_ids": ["bitcoin", "ethereum"],
  "refresh_seconds": 30
}
```

Configuration validation happens when the app starts. Invalid configuration should produce a clear error instead of a traceback.

## Dashboard rendering loop

The dashboard runs as a live terminal interface. It periodically refreshes the displayed data using the configured refresh interval.

Current rendering responsibilities are concentrated in `termdash/cli.py`. This is acceptable for the current alpha release, but the long-term direction is to split data retrieval and rendering into smaller modules.

## External data integrations

TermDash currently uses external APIs for some dashboard data. These integrations should remain optional and resilient.

Design goals for integrations:

- Use explicit request timeouts
- Avoid crashing when a provider fails
- Return fallback values when practical
- Avoid real network calls in automated tests
- Keep provider logic separate from terminal rendering

## Planned provider structure

A future refactor should move external data retrieval into provider modules:

```text
termdash/
  providers/
    weather.py
    stocks.py
    crypto.py
    quotes.py
    system.py
```

This will make the project easier to test and extend.

## Testing strategy

The current test suite validates package imports and configuration loading.

Near-term testing goals:

- Add unit tests for provider modules
- Mock external HTTP calls
- Add tests for API failure behavior
- Add tests for CLI argument parsing once CLI options are introduced

## Release process

TermDash uses semantic versioning.

The initial release is:

```text
v0.1.0
```

Future releases should include:

- Updated changelog
- Passing CI
- Version alignment between `pyproject.toml` and `termdash/__init__.py`
- Git tag
- GitHub release notes
