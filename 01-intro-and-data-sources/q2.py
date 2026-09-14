"""
Question 2: Macro Indexes YTD (as of August 21, 2026)

Main Task: How many indexes (out of 10) have better YTD returns than the US
(S&P 500) as of August 21, 2026?
Additional Task: Compare 3, 5, and 10-year performance trends.
"""
import yfinance as yf
import pandas as pd

TICKERS = {
    "S&P 500 (US)": "^GSPC",
    "Shanghai Composite (China)": "000001.SS",
    "Hang Seng (Hong Kong)": "^HSI",
    "S&P/ASX 200 (Australia)": "^AXJO",
    "Nifty 50 (India)": "^NSEI",
    "S&P/TSX Composite (Canada)": "^GSPTSE",
    "DAX (Germany)": "^GDAXI",
    "FTSE 100 (UK)": "^FTSE",
    "Nikkei 225 (Japan)": "^N225",
    "IPC Mexico": "^MXX",
    "Ibovespa (Brazil)": "^BVSP",
}

START_DATE = "2026-01-01"
END_DATE = "2026-08-21"


def ytd_return(ticker, start_date=START_DATE, end_date=END_DATE):
    # yfinance end_date is exclusive, so add a day to include Aug 21 close.
    end_inclusive = (pd.Timestamp(end_date) + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
    df = yf.download(ticker, start=start_date, end=end_inclusive, progress=False, auto_adjust=False)
    if df.empty:
        return None
    close = df["Close"].dropna()
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
    first_close = close.iloc[0]
    last_close = close.iloc[-1]
    ret = (last_close / first_close - 1) * 100
    return float(ret), close.index[0], close.index[-1]


def multi_year_return(ticker, years, end_date=END_DATE):
    end_ts = pd.Timestamp(end_date)
    start_ts = end_ts - pd.DateOffset(years=years)
    end_inclusive = (end_ts + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
    df = yf.download(ticker, start=start_ts.strftime("%Y-%m-%d"), end=end_inclusive, progress=False, auto_adjust=False)
    if df.empty:
        return None
    close = df["Close"].dropna()
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
    return float((close.iloc[-1] / close.iloc[0] - 1) * 100)


def main():
    print(f"YTD ({START_DATE} to {END_DATE}) returns:\n")
    results = {}
    for name, ticker in TICKERS.items():
        r = ytd_return(ticker)
        if r is None:
            print(f"{name:35s} ({ticker:10s}): NO DATA")
            continue
        ret, first_dt, last_dt = r
        results[name] = ret
        print(f"{name:35s} ({ticker:10s}): {ret:7.2f}%   [{first_dt.date()} -> {last_dt.date()}]")

    us_ret = results["S&P 500 (US)"]
    others = {k: v for k, v in results.items() if k != "S&P 500 (US)"}
    better = {k: v for k, v in others.items() if v > us_ret}

    print(f"\nS&P 500 YTD return: {us_ret:.2f}%")
    print(f"Indexes beating the S&P 500 (out of {len(others)}): {len(better)}")
    for k, v in sorted(better.items(), key=lambda kv: -kv[1]):
        print(f"  {k}: {v:.2f}%")

    print(f"\nANSWER Q2 (main): {len(better)} indexes out of {len(others)} beat the S&P 500 YTD.")

    # --- Additional task: 3, 5, 10-year trends ---
    print("\n--- Multi-year performance trends ---")
    for years in (3, 5, 10):
        print(f"\n{years}-year returns (through {END_DATE}):")
        multi = {}
        for name, ticker in TICKERS.items():
            r = multi_year_return(ticker, years)
            multi[name] = r
            if r is not None:
                print(f"  {name:35s}: {r:8.2f}%")
            else:
                print(f"  {name:35s}: NO DATA")
        us_multi = multi.get("S&P 500 (US)")
        if us_multi is not None:
            beat = [k for k, v in multi.items() if v is not None and k != "S&P 500 (US)" and v > us_multi]
            print(f"  -> Indexes beating S&P 500 over {years}y: {len(beat)} ({', '.join(beat) if beat else 'none'})")


if __name__ == "__main__":
    main()
