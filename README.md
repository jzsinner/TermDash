# TermDash

A local-first terminal dashboard for developers and power users.

TermDash displays useful daily context in a live-updating terminal interface, including system stats, weather, market data, crypto prices, top processes, and daily motivation.

> Status: early alpha. APIs, integrations, configuration, packaging, and tests are still being hardened.

## Features

| Feature | Status | Notes |
|---|---:|---|
| System stats | Implemented | CPU, memory, and disk usage |
| Top processes | Implemented | Shows high-CPU local processes |
| Weather | Implemented | Uses a public weather endpoint |
| Stocks | Implemented | Basic market data support |
| Crypto | Implemented | Basic crypto price support |
| Motivation quote | Implemented | Remote quote API with fallback |
| Auto-refresh | Implemented | Live terminal updates |
| Configuration | Planned | User-editable config file |
| GitHub activity | Planned | Future GitHub API integration |
| Calendar / schedule | Planned | Future calendar integration |
| Plugin architecture | Planned | Future extension model |

## Demo

![TermDash terminal demo](https://raw.githubusercontent.com/owner/termdash/main/docs/demo.gif)

## Requirements

- Python 3.10 or newer
- macOS, Linux, or WSL
- Terminal with Unicode support

## Installation

### Install from source

Clone the repository:

```bash
git clone https://github.com/jzsinner/TermDash.git
cd TermDash
```

Install in editable mode:

```bash
python3 -m pip install -e .
```

Run TermDash:

```bash
termdash
```

Stop the dashboard with:

```text
Ctrl+C
```

## Configuration

TermDash looks for an optional local configuration file at:

```text
~/.termdash.json
```

Example:

```json
{
  "location": "San Francisco",
  "stock_symbols": ["AAPL", "GOOGL", "MSFT", "TSLA"],
  "crypto_ids": ["bitcoin", "ethereum"],
  "refresh_seconds": 30
}
```

If no config file exists, TermDash uses built-in defaults.

## Development setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the project:

```bash
python3 -m pip install -e .
```

Run the app:

```bash
termdash
```

## Documentation

- [Architecture](docs/architecture.md)
- [Configuration](docs/configuration.md)
- [Release process](docs/release.md)
- [Contributing](CONTRIBUTING.md)
- [Security policy](SECURITY.md)

## Project goals

TermDash is intended to become a lightweight, local-first terminal dashboard that can be customized for different developer workflows.

The project priorities are:

- Keep setup simple
- Avoid unnecessary dependencies
- Prefer local-first behavior
- Make API integrations optional
- Handle network failures cleanly
- Support configuration without requiring code changes
- Build toward a plugin-friendly architecture

## Roadmap

Near-term work:

- Expand configuration options and validation
- Add tests for core data providers
- Improve API error handling
- Add GitHub Actions CI
- Add a screenshot or terminal demo GIF
- Publish a `v0.1.0` GitHub release

Later work:

- GitHub activity integration
- Calendar integration
- Theme support
- Plugin architecture
- PyPI publishing

## Contributing

Contributions are welcome, especially around tests, configuration, documentation, terminal UI improvements, and API integration cleanup.

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Security

Do not commit API keys, credentials, tokens, or private configuration files.

See [SECURITY.md](SECURITY.md) for vulnerability reporting guidance.

## License

MIT. See [LICENSE](LICENSE).