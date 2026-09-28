"""
Question 4: [Strategy] Simple RSI-Based Trading Strategy

What is the total profit (in $ thousands) you would have earned by investing
$1000 every time a stock was oversold (RSI < 30)?

The parquet file is cached to data/data.parquet after the first download.
"""
from pathlib import Path

import gdown
import pandas as pd

FILE_ID = "1grCTCzMZKY5sJRtdbLVCXg8JXA8VPyg-"
DATA = Path(__file__).parent / "data" / "data.parquet"

RSI_THRESHOLD = 30
START, END = "2000-01-01", "2025-06-01"
BET = 1000


def load_data():
    if not DATA.exists():
        DATA.parent.mkdir(exist_ok=True)
        gdown.download(f"https://drive.google.com/uc?id={FILE_ID}", str(DATA), quiet=False)
    return pd.read_parquet(DATA, engine="pyarrow")


def main():
    df = load_data()

    selected_df = df[
        (df["rsi"] < RSI_THRESHOLD) & (df["Date"] >= START) & (df["Date"] <= END)
    ]
    returns = selected_df["growth_future_30d"]

    print(f"Trades (RSI < {RSI_THRESHOLD}, {START} to {END}): {len(selected_df)} (spec: 5,206)")
    print(f"Average 30d return: {(returns.mean() - 1) * 100:.2f}% (spec: 1.26%)")
    print(f"Win rate: {(returns > 1).mean() * 100:.2f}% (spec: 55.13%)")

    net_income = BET * (returns - 1).sum()
    print(f"\nANSWER Q4: net income = ${net_income:,.2f} (~{net_income / 1000:.1f}K)")


if __name__ == "__main__":
    main()
