# Capital Markets Data Pipeline — Alteryx → Power BI

**Alteryx Designer · Power BI · SQL-style transformations · Python validation · Yahoo Finance market data**

A portfolio project that models a realistic capital-markets analytics workflow: ingest multiple market-data sources, standardize and join them in Alteryx, calculate return/risk features, publish a Power BI-ready analytical dataset, and visualize security- and sector-level performance.

> **Integrity note:** The repository contains the complete workflow design, reproducible real-data acquisition, validation code, Power BI model/DAX specification, and a browser dashboard that reads the generated output. The Alteryx `.yxmd` and Power BI `.pbix` should only be added after the workflow/report are opened and saved in the actual desktop tools. I do not claim an Alteryx or Power BI runtime execution that has not been performed.

## Business question

A capital-markets analyst needs a repeatable process to combine security prices, benchmark prices, and company metadata into one reporting layer that answers:

- How are individual securities performing versus the market benchmark?
- Which sectors are generating the strongest cumulative returns?
- Which securities carry the highest rolling volatility?
- Where are drawdowns most severe?
- Which names offer the strongest risk-adjusted recent performance?

## Real data sources

The project uses real historical market data pulled reproducibly from Yahoo Finance through `yfinance`:

1. **Security price history** — AAPL, MSFT, JPM, XOM, JNJ, AMZN
2. **Benchmark price history** — SPY as the S&P 500 ETF benchmark
3. **Company metadata** — ticker, company, sector, industry, benchmark mapping

The ticker basket intentionally spans multiple sectors so the dashboard supports both security-level and sector-level analysis.

## End-to-end flow

```text
Yahoo Finance prices      Company metadata CSV      SPY benchmark prices
        |                         |                         |
        +-------------+-----------+-------------------------+
                      |
              Alteryx Input Data
                      |
          Select / Data Cleansing
                      |
             Join on ticker/date
                      |
        Sort + Multi-Row Formula
                      |
    Returns / MA / volatility / drawdown
                      |
            Summarize by sector
                      |
              Output Data CSVs
                      |
                 Power BI
                      |
      Executive capital-markets dashboard
```

## What the workflow calculates

At the daily security level:

- Daily return %
- 20-day moving average
- 20-day annualized rolling volatility
- Cumulative return
- Running peak
- Drawdown %
- Benchmark daily return
- Benchmark cumulative return
- Excess return vs benchmark

At the summary layer:

- Security latest price and cumulative return
- Security 20-day volatility and max drawdown
- Sector average return and volatility
- Best/worst security by cumulative return
- Risk-return ranking inputs

## Repository structure

```text
scripts/
  download_market_data.py
  build_analytics_output.py
  validate_outputs.py

data/
  company_metadata.csv
  README.md

output/
  README.md

alteryx/
  WORKFLOW_BUILD_SPEC.md

docs/
  ARCHITECTURE.md
  DATA_DICTIONARY.md
  POWER_BI_BUILD.md
  PROJECT_CASE_STUDY.md

dashboard/
  index.html

requirements.txt
.gitignore
LICENSE
README.md
```

## Run the reproducible data layer

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/download_market_data.py
python scripts/build_analytics_output.py
python scripts/validate_outputs.py
```

This creates the raw price files plus Power BI-ready analytical outputs under `output/`.

## Build it in Alteryx Designer

Follow [`alteryx/WORKFLOW_BUILD_SPEC.md`](alteryx/WORKFLOW_BUILD_SPEC.md). It gives the exact tools, join keys, data types, formulas, sort order, and output names needed to reproduce the transformation pipeline visually.

Recommended canvas sequence:

```text
Input Data × 3
 → Select
 → Data Cleansing
 → Join
 → Sort
 → Multi-Row Formula
 → Formula
 → Summarize
 → Output Data
```

Once you build it in Designer, add:

- `alteryx/capital_markets_pipeline.yxmd`
- `docs/screenshots/alteryx_workflow.png`

## Build the Power BI report

Follow [`docs/POWER_BI_BUILD.md`](docs/POWER_BI_BUILD.md). It includes:

- model relationships
- measures/DAX
- recommended visuals
- filters/slicers
- dashboard layout
- recruiter demo flow

Once opened and saved in Power BI Desktop, add the real `.pbix` and screenshots.

## Browser dashboard

[`dashboard/index.html`](dashboard/index.html) is a lightweight showcase that does **not** hard-code market results. It lets you load the generated `output/security_daily.csv` and computes the displayed KPIs/charts from that file in the browser.

## Skills demonstrated

| Skill | Evidence |
|---|---|
| Alteryx | Exact multi-input workflow design using Input, Select, Data Cleansing, Join, Sort, Multi-Row Formula, Formula, Summarize, Output |
| Power BI | Star-style reporting model, DAX measures, executive dashboard specification |
| Capital markets | Security prices, benchmark-relative returns, volatility, drawdown, sector analysis |
| Data integration | Multiple sources joined by ticker/date and metadata keys |
| Transformation logic | Returns, moving averages, volatility, cumulative performance, drawdown |
| Data quality | Null handling, type validation, uniqueness checks, required-field validation |
| Python | Reproducible data acquisition and independent output validation |
