"""
Question 4: Earnings Surprise Analysis for Amazon (AMZN)

Main Task: Calculate the median 2-day percentage change in stock prices
following positive earnings surprise days.
Additional Task: Examine correlation between surprise magnitude and price
reaction; assess bull vs bear market differences.

Methodology (per the homework spec): for each sequence of 3 consecutive
trading days (Day 1, Day 2, Day 3) where Day 2 is the earnings-announcement
day, the "2-day return" is Close_Day3 / Close_Day1 - 1.

`ticker_obj.get_earnings_dates()` (no `limit`) returns 25 entries starting
from 2020-10-29; the most recent one is a future date with no Reported EPS /
Surprise(%) yet, so it drops out once we filter to rows with surprise data.
"""
import pandas as pd
import yfinance as yf

TICKER = "AMZN"


def get_earnings_surprises(ticker=TICKER):
    tk = yf.Ticker(ticker)
    df = tk.get_earnings_dates()
    df = df.dropna(subset=["Surprise(%)"]).sort_index()
    return df


def get_price_history(ticker=TICKER, start="2020-01-01"):
    df = yf.download(ticker, start=start, progress=False, auto_adjust=False)
    close = df["Close"].dropna()
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
    return close


def two_day_return_around(close: pd.Series, earnings_ts: pd.Timestamp):
    """Day 1 / Day 2 / Day 3 sequence, Day 2 = the earnings announcement.
    2-day return = Close_Day3 / Close_Day1 - 1.
    """
    earnings_date = pd.Timestamp(earnings_ts).tz_localize(None).normalize()
    idx = close.index
    day2_pos = idx.searchsorted(earnings_date)  # Day 2 (or next trading day)
    if day2_pos - 1 < 0 or day2_pos + 1 >= len(idx):
        return None
    day1, day2, day3 = idx[day2_pos - 1], idx[day2_pos], idx[day2_pos + 1]
    ret_pct = (close.iloc[day2_pos + 1] / close.iloc[day2_pos - 1] - 1) * 100
    return ret_pct, day1, day2, day3


def main():
    earnings = get_earnings_surprises()
    print(f"Earnings entries with surprise data: {len(earnings)}")
    print(earnings[["Reported EPS", "EPS Estimate", "Surprise(%)"]].to_string())

    close = get_price_history(start="2020-01-01")
    print(f"\nPrice history: {close.index[0].date()} -> {close.index[-1].date()} ({len(close)} rows)")

    records = []
    for ts, row in earnings.iterrows():
        result = two_day_return_around(close, ts)
        if result is None:
            continue
        ret_pct, d_before, d_announce, d_after = result
        records.append(
            {
                "earnings_date": pd.Timestamp(ts).tz_localize(None),
                "surprise_pct": row["Surprise(%)"],
                "day_before": d_before,
                "announce_day": d_announce,
                "day_after": d_after,
                "two_day_return_pct": ret_pct,
            }
        )

    res = pd.DataFrame(records).sort_values("earnings_date")
    print("\nPer-earnings 2-day returns (day-before -> day-after close):")
    print(res.to_string(index=False))

    positive = res[res["surprise_pct"] > 0]
    print(f"\nPositive-surprise earnings events: {len(positive)} / {len(res)}")

    median_2day = positive["two_day_return_pct"].median()
    print(f"\nANSWER Q4 (main): Median 2-day % change after positive surprises = {median_2day:.2f}%")

    # --- Additional task: correlation between surprise magnitude and reaction ---
    corr_all = res["surprise_pct"].corr(res["two_day_return_pct"])
    corr_pos = positive["surprise_pct"].corr(positive["two_day_return_pct"])
    print(f"\nCorrelation (surprise % vs 2-day return), all events: {corr_all:.3f}")
    print(f"Correlation (surprise % vs 2-day return), positive-surprise events only: {corr_pos:.3f}")

    # crude bull/bear split: 2022 was a broad bear market for growth/tech names
    bear_mask = (res["earnings_date"] >= "2022-01-01") & (res["earnings_date"] <= "2022-12-31")
    bear = res[bear_mask]
    bull = res[~bear_mask]
    print(f"\n'Bear market' (2022) events: {len(bear)}, median 2-day return = {bear['two_day_return_pct'].median():.2f}%")
    print(f"'Bull/other' events: {len(bull)}, median 2-day return = {bull['two_day_return_pct'].median():.2f}%")


if __name__ == "__main__":
    main()
