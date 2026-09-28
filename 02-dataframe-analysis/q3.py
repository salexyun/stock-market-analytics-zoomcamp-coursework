"""
Question 3: [IPO] 'Fixed Months Holding Strategy'

What is the optimal number of months (1 to 12) to hold a newly IPO'd stock in
order to maximize the median growth value?

Reuses Q2's stocks_df (cached in data/stocks_df.csv -- run q2.py first, or
this will download it).
"""
import pandas as pd

from q2 import load_stocks_df

MONTHS = range(1, 13)
DAYS_PER_MONTH = 21


def add_future_growth(stocks_df):
    stocks_df = stocks_df.copy()
    close = stocks_df.groupby("Ticker")["Close"]
    for m in MONTHS:
        stocks_df[f"future_growth_{m}_m"] = close.shift(-m * DAYS_PER_MONTH) / stocks_df["Close"]
    return stocks_df


def main():
    stocks_df = add_future_growth(load_stocks_df())

    # entry point: each ticker's first trading day
    min_dates = stocks_df.groupby("Ticker")["Date"].min().reset_index().rename(columns={"Date": "min_date"})
    entries = min_dates.merge(
        stocks_df, left_on=["Ticker", "min_date"], right_on=["Ticker", "Date"], how="inner"
    )
    print(f"Entry rows (one per ticker): {len(entries)}")

    growth_cols = [f"future_growth_{m}_m" for m in MONTHS]
    stats = entries[growth_cols].describe()
    pd.set_option("display.width", 250)
    print(stats.T)

    medians = stats.loc["50%"]
    best = medians.idxmax()
    best_month = int(best.split("_")[2])
    print(f"\nANSWER Q3: hold {best_month} month(s) -> max median growth = {medians[best]:.4f}")


if __name__ == "__main__":
    main()
