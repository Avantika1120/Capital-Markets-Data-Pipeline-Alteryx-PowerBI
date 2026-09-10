# Data Dictionary

## `security_daily.csv`

| Field | Meaning |
|---|---|
| `date` | Trading date |
| `ticker` | Security symbol |
| `company` | Company name from reference data |
| `sector` | GICS-style sector label used for portfolio grouping |
| `industry` | Industry label |
| `adj_close` | Adjusted closing price |
| `volume` | Reported daily trading volume |
| `daily_return` | One-day percentage return as decimal |
| `ma_20` | 20-trading-day moving average of adjusted close |
| `volatility_20_ann` | 20-day standard deviation of daily returns annualized with sqrt(252) |
| `cumulative_return` | Return from first observation in the dataset to current date |
| `running_peak` | Highest adjusted close observed to date for the ticker |
| `drawdown` | Percentage decline from running peak |
| `benchmark_daily_return` | SPY daily return |
| `benchmark_cumulative_return` | SPY cumulative return from first benchmark observation |
| `excess_daily_return` | Security daily return minus benchmark daily return |
| `excess_cumulative_return` | Security cumulative return minus benchmark cumulative return |

## `security_summary.csv`

One row per ticker containing the latest available market snapshot plus historical max drawdown.

## `sector_summary.csv`

One row per sector with security count, average cumulative return, average 20-day annualized volatility, average benchmark-relative cumulative return, and worst constituent drawdown.

## Data-quality expectations

- `(ticker, date)` must be unique in the daily table.
- `adj_close` must be positive.
- All configured tickers must match company metadata.
- Sector should never be null after the metadata join.
- Rolling metrics are expected to be null before enough observations exist.
