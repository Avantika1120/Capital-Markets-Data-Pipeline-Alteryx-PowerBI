from pathlib import Path
import pandas as pd
import yfinance as yf

TICKERS = ["AAPL", "MSFT", "JPM", "XOM", "JNJ", "AMZN"]
BENCHMARK = "SPY"
START = "2023-01-01"
END = None
RAW = Path("data/raw")
RAW.mkdir(parents=True, exist_ok=True)


def download_one(ticker: str) -> pd.DataFrame:
    df = yf.download(ticker, start=START, end=END, auto_adjust=False, progress=False)
    if df.empty:
        raise RuntimeError(f"No data returned for {ticker}")
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df.reset_index()
    df.columns = [str(c).lower().replace(" ", "_") for c in df.columns]
    df["ticker"] = ticker
    keep = ["date", "ticker", "open", "high", "low", "close", "adj_close", "volume"]
    return df[keep]


def main() -> None:
    prices = pd.concat([download_one(t) for t in TICKERS], ignore_index=True)
    benchmark = download_one(BENCHMARK)
    prices.to_csv(RAW / "security_prices.csv", index=False)
    benchmark.to_csv(RAW / "benchmark_prices.csv", index=False)
    print(f"security rows: {len(prices):,}")
    print(f"benchmark rows: {len(benchmark):,}")


if __name__ == "__main__":
    main()
