"""
Question 2: [IPO] Median Sharpe Ratio for 2025 IPOs (First 8 Months)

What is the median Sharpe ratio (as of 11 September 2026) for companies that
went public before 1 September 2025?

The downloaded OHLCV data is cached to data/stocks_df.csv so Q3 can reuse the
same stocks_df without hitting yfinance again. Delete the file to re-download.
"""
import io
from pathlib import Path

import numpy as np
import pandas as pd
import requests
import yfinance as yf

URL = "https://www.iposcoop.com/2025-pricings/"
OFFER_CUTOFF = pd.Timestamp("2025-09-01")
END_DATE = "2026-09-12"  # yfinance end is exclusive -> includes 2026-09-11
EVAL_DATE = "2026-09-11"
RISK_FREE = 0.05

CACHE = Path(__file__).parent / "data" / "stocks_df.csv"


def load_ipos_2025():
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(URL, headers=headers, timeout=30)
    resp.raise_for_status()
    return pd.read_html(io.StringIO(resp.text))[0]


def filter_ipos(ipos):
    ipos = ipos.copy()
    ipos["Offer Date"] = pd.to_datetime(ipos["Offer Date"], format="%m/%d/%Y")
    ipos["Return"] = pd.to_numeric(ipos["Return"].str.replace("%", "", regex=False), errors="coerce")
    return ipos[(ipos["Offer Date"] < OFFER_CUTOFF) & (ipos["Return"] != 0)]


def download_stocks(tickers):
    frames = []
    missing = []
    for ticker in tickers:
        try:
            df = yf.download(ticker, start="2025-01-01", end=END_DATE, progress=False, auto_adjust=False)
        except Exception:
            df = pd.DataFrame()
        if df.empty:
            missing.append(ticker)  # probably delisted / not on Yahoo
            continue
        df.columns = df.columns.get_level_values(0)
        df["Ticker"] = ticker
        frames.append(df)
    print(f"Downloaded {len(frames)} tickers, missing {len(missing)}: {missing}")
    return pd.concat(frames)


def add_features(stocks_df):
    stocks_df = stocks_df.sort_values(["Ticker", "Date"]).copy()
    close = stocks_df.groupby("Ticker")["Close"]
    stocks_df["growth_252d"] = stocks_df["Close"] / close.shift(252)
    stocks_df["volatility"] = close.transform(lambda s: s.rolling(30).std()) * np.sqrt(252)
    stocks_df["Sharpe"] = (stocks_df["growth_252d"] - RISK_FREE) / stocks_df["volatility"]
    return stocks_df


def load_stocks_df():
    """Filtered 2025 IPO tickers' daily OHLCV + features (shared with Q3)."""
    if CACHE.exists():
        stocks_df = pd.read_csv(CACHE, parse_dates=["Date"])
    else:
        ipos = filter_ipos(load_ipos_2025())
        print(f"IPOs before {OFFER_CUTOFF.date()} with non-zero return: {len(ipos)} (spec expects 148)")
        stocks_df = download_stocks(ipos["Symbol"].tolist()).reset_index()
        CACHE.parent.mkdir(exist_ok=True)
        stocks_df.to_csv(CACHE, index=False)
    return add_features(stocks_df)


def main():
    stocks_df = load_stocks_df()
    print(f"Tickers in stocks_df: {stocks_df['Ticker'].nunique()} (spec expects ~134)")

    on_date = stocks_df[stocks_df["Date"] == EVAL_DATE]
    stats = on_date[["growth_252d", "volatility", "Sharpe"]].describe()
    print(f"\nDescriptive stats on {EVAL_DATE}:")
    print(stats)

    print("\nTop 10 by Sharpe vs. their growth rank:")
    ranked = on_date.dropna(subset=["Sharpe"]).copy()
    ranked["growth_rank"] = ranked["growth_252d"].rank(ascending=False).astype(int)
    print(
        ranked.sort_values("Sharpe", ascending=False)
        .head(10)[["Ticker", "growth_252d", "volatility", "Sharpe", "growth_rank"]]
        .to_string(index=False)
    )

    print(f"\nANSWER Q2: median Sharpe on {EVAL_DATE} = {stats.loc['50%', 'Sharpe']:.4f}")


if __name__ == "__main__":
    main()
