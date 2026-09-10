# Project Case Study — Capital Markets Data Pipeline

## Problem

Capital-markets reporting often requires analysts to combine market-price history, benchmark data, and instrument reference data before any useful performance or risk analysis can happen. The goal of this project is to design a repeatable Alteryx-to-Power-BI workflow that turns those separate inputs into a clean analytical layer.

## Data

The reproducible data pull covers six large-cap U.S. equities across multiple sectors plus SPY as the benchmark. Company metadata is maintained separately so price data can be enriched with company, sector, and industry attributes.

## Transformation design

The workflow standardizes field types, removes invalid records, trims identifiers, sorts each security chronologically, and joins security prices to reference data and the benchmark series. Row-aware calculations derive daily return, 20-day moving average, annualized 20-day volatility, cumulative return, running peak, drawdown, and benchmark-relative return.

A second branch summarizes the daily table to current security and sector snapshots for efficient dashboard use.

## Why these metrics

- **Daily return** measures short-term price change.
- **Moving average** gives a simple trend reference.
- **Rolling volatility** provides a recent risk proxy.
- **Cumulative return** measures performance over the selected history.
- **Drawdown** captures downside from prior peaks.
- **Excess return** puts security performance in benchmark context.

## Power BI reporting layer

The report design contains three pages:

1. **Executive Market Overview** — performance, benchmark comparison, risk-return scatter, sector return, drawdown ranking.
2. **Security Detail** — price and moving-average trend, daily returns, drawdown, cumulative security vs benchmark performance.
3. **Sector & Risk View** — sector-level return/volatility and constituent comparison.

## Data quality

A separate Python validator checks uniqueness at ticker/date grain, required columns, positive adjusted prices, complete sector mappings, and one-row-per-security summary output. This provides an independent QA layer alongside Alteryx workflow inspection.

## What is complete in GitHub

- reproducible real-market data acquisition
- reference metadata
- transformation reference implementation
- output QA checks
- exact Alteryx build specification
- Power BI model and DAX specification
- browser-based real-output dashboard
- architecture and data dictionary

## What still requires desktop execution

The repository intentionally does not include a fabricated `.yxmd` or `.pbix`. Those should be added only after the workflow is opened, configured, and run in Alteryx Designer and the report is built/refreshed in Power BI Desktop. Screenshots should likewise come from real desktop execution.

## Interview explanation

A concise explanation is:

> I wanted to demonstrate the full reporting path rather than only build another dashboard. I separated source acquisition, transformation, validation, and reporting. The Alteryx workflow integrates security prices, benchmark prices, and reference data, then creates performance and risk measures before publishing a Power BI-ready layer. I also built an independent Python validation path so I could confirm grain, joins, and metric logic instead of treating the visual workflow as a black box.
