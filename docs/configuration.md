# TermDash Configuration

TermDash supports an optional local JSON configuration file.

By default, TermDash looks for this file at:

```text
~/.termdash.json
```

If the file does not exist, TermDash uses built-in defaults.

## Example configuration

```json
{
  "location": "San Francisco",
  "stock_symbols": ["AAPL", "GOOGL", "MSFT", "TSLA"],
  "crypto_ids": ["bitcoin", "ethereum"],
  "refresh_seconds": 30
}
```

## Supported fields

| Field | Type | Default | Description |
|---|---|---|---|
| `location` | string | `"San Francisco"` | Location used for weather data |
| `stock_symbols` | array of strings | `["AAPL", "GOOGL", "MSFT", "TSLA"]` | Stock symbols shown in the dashboard |
| `crypto_ids` | array of strings | `["bitcoin", "ethereum"]` | Cryptocurrency IDs shown in the dashboard |
| `refresh_seconds` | integer | `30` | Number of seconds between dashboard refreshes |

## Field details

### `location`

The `location` field controls the location used for weather data.

Example:

```json
{
  "location": "New York"
}
```

The value must be a non-empty string.

### `stock_symbols`

The `stock_symbols` field controls which stock symbols appear in the dashboard.

Example:

```json
{
  "stock_symbols": ["NVDA", "AMD", "AAPL"]
}
```

The value must be a non-empty array of non-empty strings.

### `crypto_ids`

The `crypto_ids` field controls which cryptocurrency IDs appear in the dashboard.

Example:

```json
{
  "crypto_ids": ["bitcoin", "ethereum"]
}
```

The value must be a non-empty array of non-empty strings.

### `refresh_seconds`

The `refresh_seconds` field controls how often TermDash refreshes the dashboard.

Example:

```json
{
  "refresh_seconds": 60
}
```

The value must be an integer greater than zero.

## Minimal configuration

You do not need to specify every field. Missing fields use default values.

Example:

```json
{
  "location": "Seattle"
}
```

## Invalid configuration

TermDash validates configuration when the app starts.

Invalid configuration should produce a clear error and exit instead of showing a Python traceback.

Examples of invalid configuration:

```json
{
  "location": ""
}
```

```json
{
  "stock_symbols": "AAPL"
}
```

```json
{
  "refresh_seconds": 0
}
```

## Creating a local config file

Create a config file with:

```bash
cat > ~/.termdash.json <<'CONFIG'
{
  "location": "San Francisco",
  "stock_symbols": ["AAPL", "GOOGL", "MSFT", "TSLA"],
  "crypto_ids": ["bitcoin", "ethereum"],
  "refresh_seconds": 30
}
CONFIG
```

Then run:

```bash
termdash
```

## Removing local configuration

To return to defaults, delete the config file:

```bash
rm -f ~/.termdash.json
```

Then run:

```bash
termdash
```
