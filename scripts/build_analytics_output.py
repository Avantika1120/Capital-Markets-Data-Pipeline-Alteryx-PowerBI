from pathlib import Path
import numpy as np
import pandas as pd

RAW = Path("data/raw")
OUT = Path("output")
OUT.mkdir(exist_ok=True)


def main() -> None:
    px = pd.read_csv(RAW / "security_prices.csv", parse_dates=["date"])
    bm = pd.read_csv(RAW / "benchmark_prices.csv", parse_dates=["date"])
    meta = pd.read_csv("data/company_metadata.csv")

    px = px.dropna(subset=["date", "ticker", "adj_close"]).sort_values(["ticker", "date"]).copy()
    bm = bm.dropna(subset=["date", "adj_close"]).sort_values("date").copy()

    px["daily_return"] = px.groupby("ticker")["adj_close"].pct_change()
    px["ma_20"] = px.groupby("ticker")["adj_close"].transform(lambda s: s.rolling(20).mean())
    px["volatility_20_ann"] = px.groupby("ticker")["daily_return"].transform(lambda s: s.rolling(20).std() * np.sqrt(252))
    px["cumulative_return"] = px.groupby("ticker")["adj_close"].transform(lambda s: s / s.iloc[0] - 1)
    px["running_peak"] = px.groupby("ticker")["adj_close"].cummax()
    px["drawdown"] = px["adj_close"] / px["running_peak"] - 1

    bm["benchmark_daily_return"] = bm["adj_close"].pct_change()
    bm["benchmark_cumulative_return"] = bm["adj_close"] / bm["adj_close"].iloc[0] - 1
    bm_small = bm[["date", "benchmark_daily_return", "benchmark_cumulative_return"]]

    daily = px.merge(meta, on="ticker", how="left").merge(bm_small, on="date", how="left")
    daily["excess_daily_return"] = daily["daily_return"] - daily["benchmark_daily_return"]
    daily["excess_cumulative_return"] = daily["cumulative_return"] - daily["benchmark_cumulative_return"]

    latest = daily.sort_values("date").groupby("ticker", as_index=False).tail(1)
    max_dd = daily.groupby("ticker", as_index=False)["drawdown"].min().rename(columns={"drawdown":"max_drawdown"})
    summary = latest[["ticker","company","sector","industry","date","adj_close","cumulative_return","volatility_20_ann","benchmark_cumulative_return","excess_cumulative_return"]].merge(max_dd, on="ticker")

    sector = summary.groupby("sector", as_index=False).agg(
        securities=("ticker", "count"),
        avg_cumulative_return=("cumulative_return", "mean"),
        avg_volatility_20_ann=("volatility_20_ann", "mean"),
        avg_excess_cumulative_return=("excess_cumulative_return", "mean"),
        worst_drawdown=("max_drawdown", "min"),
    )

    daily.to_csv(OUT / "security_daily.csv", index=False)
    summary.to_csv(OUT / "security_summary.csv", index=False)
    sector.to_csv(OUT / "sector_summary.csv", index=False)
    print(f"Wrote {len(daily):,} daily rows, {len(summary)} security rows, {len(sector)} sector rows")


if __name__ == "__main__":
    main()
