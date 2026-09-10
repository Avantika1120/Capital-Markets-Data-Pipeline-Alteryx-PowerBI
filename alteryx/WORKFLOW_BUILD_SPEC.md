# Alteryx Workflow Build Specification

This file is the exact desktop build plan for `capital_markets_pipeline.yxmd`.

## Inputs

Use three **Input Data** tools:

1. `data/raw/security_prices.csv`
2. `data/raw/benchmark_prices.csv`
3. `data/company_metadata.csv`

## Branch A — security prices

**Select**
- `date` → Date
- `ticker` → V_String(10)
- `open/high/low/close/adj_close` → Double
- `volume` → Int64

**Data Cleansing**
- Remove rows where `date`, `ticker`, or `adj_close` is null.
- Trim whitespace in `ticker`.

**Sort**
- ticker ascending
- date ascending

**Multi-Row Formula — Previous Adjusted Close**
Create `prev_adj_close` (Double):

```text
IF [Row-1:ticker] = [ticker] THEN [Row-1:adj_close] ELSE NULL() ENDIF
```

**Formula — Daily Return**

```text
IF IsNull([prev_adj_close]) OR [prev_adj_close] = 0 THEN NULL()
ELSE ([adj_close] / [prev_adj_close]) - 1
ENDIF
```

Name: `daily_return`

**Multi-Row Formula / Moving tools**
Use a 20-row window within ticker for:
- `ma_20` = average adjusted close
- `volatility_20_ann` = standard deviation of daily return × SQRT(252)

If using **Multi-Row Formula**, group by ticker and construct the 20-row window. If your Designer version includes moving-window tools, use the equivalent moving average and moving standard deviation configuration.

**Running Total / Multi-Row Formula**
Create a running peak within ticker and then:

```text
[drawdown] = ([adj_close] / [running_peak]) - 1
```

For cumulative return, retain each ticker's first adjusted close and calculate:

```text
([adj_close] / [first_adj_close]) - 1
```

## Branch B — company metadata

**Select**
- ticker → V_String(10)
- company → V_WString(100)
- sector → V_WString(100)
- industry → V_WString(100)
- benchmark → V_String(10)

**Data Cleansing**
Trim all string columns.

## Join 1 — prices + metadata

Use **Join** tool:
- Left: cleaned security-price branch
- Right: company metadata
- Key: `ticker = ticker`
- Keep only the Joined output for the main analytical table.
- Review Left-Unjoined output during QA; it should be empty for the six configured securities.

## Branch C — benchmark prices

Use **Select → Data Cleansing → Sort → Multi-Row Formula** exactly as the security-price branch, but calculate:
- `benchmark_daily_return`
- `benchmark_cumulative_return`

Rename adjusted-close fields as needed to avoid collisions.

## Join 2 — securities + benchmark

Use **Join** tool:
- Left: price + metadata stream
- Right: benchmark stream
- Key: `date = date`

Then **Formula**:

```text
[excess_daily_return] = [daily_return] - [benchmark_daily_return]
[excess_cumulative_return] = [cumulative_return] - [benchmark_cumulative_return]
```

## Output 1 — daily analytical table

**Output Data** → `output/security_daily.csv`

Required fields:
- date
- ticker
- company
- sector
- industry
- adj_close
- volume
- daily_return
- ma_20
- volatility_20_ann
- cumulative_return
- running_peak
- drawdown
- benchmark_daily_return
- benchmark_cumulative_return
- excess_daily_return
- excess_cumulative_return

## Summary stream

From the joined daily stream, use **Summarize** grouped by ticker/company/sector/industry to support:
- latest available date / latest price
- minimum drawdown as max drawdown
- latest cumulative return
- latest 20-day volatility
- latest benchmark cumulative return
- latest excess cumulative return

Output → `output/security_summary.csv`

Then use another **Summarize** grouped by sector:
- Count distinct ticker
- Average cumulative return
- Average annualized 20-day volatility
- Average excess cumulative return
- Minimum max drawdown

Output → `output/sector_summary.csv`

## QA checklist before saving the `.yxmd`

- Six distinct securities in security output.
- No duplicate ticker/date rows.
- No null ticker/sector after metadata join.
- Adjusted close always > 0.
- Daily return only null on first observation or missing-history boundaries.
- 20-day measures remain null until enough observations exist.
- Benchmark join does not unexpectedly drop trading dates.
- Left-unjoined metadata stream is empty.

## Screenshot to capture

Once the workflow executes successfully in Alteryx Designer, capture one screenshot showing the complete canvas from the three Input Data tools through both joins, transformation tools, summaries, and outputs. Save as:

`docs/screenshots/alteryx_workflow.png`

Only after executing successfully should you describe the workflow as **built and executed in Alteryx**.
