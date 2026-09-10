# Power BI Build Guide

## Load these tables

- `output/security_daily.csv`
- `output/security_summary.csv`
- `output/sector_summary.csv`
- `data/company_metadata.csv`

## Recommended model

Create a Date table and relate:

- `Date[Date]` 1:* `security_daily[date]`
- `company_metadata[ticker]` 1:* `security_daily[ticker]`
- `company_metadata[ticker]` 1:1 `security_summary[ticker]`

Use `security_daily` for time-series visuals and `security_summary` / `sector_summary` for current snapshot cards and rankings.

## Core DAX measures

```DAX
Latest Price =
VAR LatestDate = MAX(security_daily[date])
RETURN CALCULATE(MAX(security_daily[adj_close]), security_daily[date] = LatestDate)
```

```DAX
Cumulative Return % =
MAX(security_daily[cumulative_return])
```

```DAX
Benchmark Return % =
MAX(security_daily[benchmark_cumulative_return])
```

```DAX
Excess Return % =
[Cumulative Return %] - [Benchmark Return %]
```

```DAX
Annualized 20D Volatility % =
MAX(security_daily[volatility_20_ann])
```

```DAX
Max Drawdown % =
MIN(security_daily[drawdown])
```

```DAX
Average Daily Return % =
AVERAGE(security_daily[daily_return])
```

```DAX
Positive Trading Days % =
DIVIDE(
    CALCULATE(COUNTROWS(security_daily), security_daily[daily_return] > 0),
    CALCULATE(COUNTROWS(security_daily), NOT ISBLANK(security_daily[daily_return]))
)
```

## Report page 1 — Executive Market Overview

Top KPI cards:
- Latest selected-security price
- Cumulative return %
- Benchmark return %
- Excess return %
- Annualized 20D volatility %
- Max drawdown %

Visuals:
1. **Line chart** — Date vs cumulative return, legend ticker, with benchmark comparison.
2. **Scatter plot** — x = annualized volatility, y = cumulative return, size = latest price, legend = sector.
3. **Bar chart** — sector average cumulative return.
4. **Bar chart** — max drawdown by ticker.
5. **Table** — ticker, company, sector, latest price, cumulative return, volatility, max drawdown, excess return.

Slicers:
- Date
- Sector
- Ticker

## Report page 2 — Security Detail

- Adjusted-close price line with 20-day moving average.
- Daily return column chart.
- Drawdown area chart.
- Cumulative security return vs benchmark line chart.
- Cards for latest price, volatility, max drawdown, excess return.

## Report page 3 — Sector & Risk View

- Sector return bar chart.
- Sector volatility bar chart.
- Risk-return scatter.
- Matrix: Sector → Ticker with cumulative return, volatility, drawdown.

## Formatting

Use percentage formatting for all return/volatility/drawdown fields. Keep the visual style restrained and finance-oriented: strong hierarchy, limited decorative elements, clear green/red conditional formatting only where it conveys performance direction.

## Screenshot checklist

After building and refreshing the real report in Power BI Desktop, save screenshots as:

- `docs/screenshots/powerbi_executive.png`
- `docs/screenshots/powerbi_security_detail.png`
- `docs/screenshots/powerbi_sector_risk.png`

Only then add the actual `.pbix` file if file size permits and describe the dashboard as executed in Power BI.
