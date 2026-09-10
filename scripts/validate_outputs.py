from pathlib import Path
import pandas as pd

OUT = Path("output")

def require_columns(df, cols, name):
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise AssertionError(f"{name} missing columns: {missing}")


def main():
    daily = pd.read_csv(OUT / "security_daily.csv")
    summary = pd.read_csv(OUT / "security_summary.csv")
    sector = pd.read_csv(OUT / "sector_summary.csv")

    require_columns(daily, ["date","ticker","adj_close","daily_return","volatility_20_ann","drawdown","benchmark_daily_return","excess_daily_return"], "daily")
    require_columns(summary, ["ticker","company","sector","cumulative_return","max_drawdown"], "summary")
    require_columns(sector, ["sector","avg_cumulative_return","avg_volatility_20_ann"], "sector")

    assert not daily.duplicated(["date","ticker"]).any(), "duplicate ticker/date rows found"
    assert daily["ticker"].nunique() == 6, "expected six securities"
    assert (daily["adj_close"] > 0).all(), "non-positive adjusted close found"
    assert summary["ticker"].is_unique, "summary should have one row per ticker"
    assert sector["sector"].notna().all(), "missing sector values"
    print("Validation passed")

if __name__ == "__main__":
    main()
