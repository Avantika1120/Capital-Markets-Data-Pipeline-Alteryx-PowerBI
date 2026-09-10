# Architecture

```text
Yahoo Finance                                 Company Reference
(security prices)                             (metadata CSV)
      |                                              |
      v                                              v
security_prices.csv                           company_metadata.csv
      |                                              |
      +-------------------+--------------------------+
                          |
                          v
                    Alteryx Designer
        Input → Clean → Select → Sort → Join
                          |
              Multi-row / Formula logic
                          |
        returns • MA20 • volatility • drawdown
                          |
                          +----------------------+
                          |                      |
                          v                      v
                security_daily.csv        security_summary.csv
                          |                      |
                          +----------+-----------+
                                     |
                                     v
                              sector_summary.csv
                                     |
                                     v
                                  Power BI
                                     |
            Executive overview • security detail • risk/sector view
```

## Design decisions

**Why multiple sources?** Capital-markets reporting rarely comes from one table. Prices, benchmark series, and instrument reference data have different grains and must be standardized before analysis.

**Why adjusted close?** Return calculations use adjusted close so corporate-action adjustments are reflected in the historical series available from the data provider.

**Why Alteryx?** The workflow is deliberately visual and auditable. Each stage—typing, cleansing, joining, row-aware calculations, summarization, output—can be inspected by an analyst without reading application code.

**Why a separate summary layer?** Power BI time-series visuals need daily grain, while ranking cards and sector comparisons are easier and faster against current-state summary tables.

**Why Python is present?** Python makes the market-data pull reproducible and provides an independent validation/reference implementation. It does not replace the intended Alteryx transformation artifact.

## Grain

- `security_daily.csv`: one row per ticker per trading date.
- `security_summary.csv`: one row per ticker for the latest available trading date plus historical max drawdown.
- `sector_summary.csv`: one row per sector.

## Controls

The validation layer checks required columns, ticker/date uniqueness, positive adjusted-close values, expected security count, unique security summaries, and non-null sector assignments.
