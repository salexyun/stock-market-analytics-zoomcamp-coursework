"""
Question 3: S&P 500 Market Corrections Analysis

Main Task: Calculate the median drawdown (in %) of significant market
corrections in the S&P 500 index.

Definition: a correction = a decline of at least 5% from a running
all-time high (peak) to the subsequent trough before a new all-time high
is made.
"""
import numpy as np
import pandas as pd
import yfinance as yf

TICKER = "^GSPC"
START_DATE = "1950-01-01"
MIN_DRAWDOWN_PCT = 5.0  # correction threshold


def get_sp500_history(start=START_DATE):
    df = yf.download(TICKER, start=start, progress=False, auto_adjust=False)
    close = df["Close"].dropna()
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
    return close


def find_drawdown_episodes(close: pd.Series):
    """Identify peak-to-trough episodes relative to the running all-time high.

    A new episode starts every time the series makes a new all-time high and
    then declines; it ends when a new all-time high is reached (or at the
    end of the series, for an ongoing/unresolved drawdown).
    """
    episodes = []

    running_peak = close.iloc[0]
    episode_peak = close.iloc[0]
    episode_peak_date = close.index[0]
    episode_trough = close.iloc[0]
    episode_trough_date = close.index[0]
    in_episode = False

    for date, price in close.items():
        if price >= running_peak:
            if in_episode:
                dd_pct = (episode_trough / episode_peak - 1) * 100
                duration_days = (episode_trough_date - episode_peak_date).days
                episodes.append(
                    {
                        "peak_date": episode_peak_date,
                        "peak_price": episode_peak,
                        "trough_date": episode_trough_date,
                        "trough_price": episode_trough,
                        "drawdown_pct": dd_pct,
                        "duration_days": duration_days,
                        "resolved": True,
                    }
                )
                in_episode = False
            running_peak = price
            episode_peak = price
            episode_peak_date = date
            episode_trough = price
            episode_trough_date = date
        else:
            in_episode = True
            if price < episode_trough:
                episode_trough = price
                episode_trough_date = date

    if in_episode:
        dd_pct = (episode_trough / episode_peak - 1) * 100
        duration_days = (episode_trough_date - episode_peak_date).days
        episodes.append(
            {
                "peak_date": episode_peak_date,
                "peak_price": episode_peak,
                "trough_date": episode_trough_date,
                "trough_price": episode_trough,
                "drawdown_pct": dd_pct,
                "duration_days": duration_days,
                "resolved": False,
            }
        )

    return pd.DataFrame(episodes)


def main():
    close = get_sp500_history()
    print(f"S&P 500 daily closes: {close.index[0].date()} -> {close.index[-1].date()} ({len(close)} rows)")

    episodes = find_drawdown_episodes(close)
    corrections = episodes[episodes["drawdown_pct"] <= -MIN_DRAWDOWN_PCT].copy()
    corrections["abs_drawdown_pct"] = corrections["drawdown_pct"].abs()

    print(f"\nTotal peak-to-trough episodes found: {len(episodes)}")
    print(f"Episodes with drawdown >= {MIN_DRAWDOWN_PCT}%: {len(corrections)}")

    print("\nAll qualifying corrections (peak date, trough date, drawdown %, duration days):")
    print(
        corrections[["peak_date", "trough_date", "drawdown_pct", "duration_days", "resolved"]]
        .sort_values("peak_date")
        .to_string(index=False)
    )

    p25, p50, p75 = np.percentile(corrections["abs_drawdown_pct"], [25, 50, 75])
    print(f"\n25th percentile drawdown: {p25:.2f}%")
    print(f"50th percentile (median) drawdown: {p50:.2f}%")
    print(f"75th percentile drawdown: {p75:.2f}%")

    dur25, dur50, dur75 = np.percentile(corrections["duration_days"], [25, 50, 75])
    print(f"\n25th percentile duration: {dur25:.1f} days")
    print(f"50th percentile (median) duration: {dur50:.1f} days")
    print(f"75th percentile duration: {dur75:.1f} days")

    print(f"\nANSWER Q3: Median drawdown of significant corrections = {p50:.2f}%")


if __name__ == "__main__":
    main()
