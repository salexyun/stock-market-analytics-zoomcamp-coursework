"""
Question 2: Most Efficient Random Forest Decision Rule

On the Q1 setup (no Ticker / month_wom dummies), add RF rules for thresholds
0.56..0.64. Which threshold gives the best CAGR with < 5 average trades per day?
"""
import numpy as np
import pandas as pd

from prep import CATEGORICAL, TARGET, add_model_predictions, build_new_df, simulate

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)


def main():
    short = [c for c in CATEGORICAL if c not in ("Ticker", "month_wom")]
    new_df, features = build_new_df(short)
    add_model_predictions(new_df, features, rf_thresholds=np.arange(56, 65) / 100)

    results = simulate(new_df).filter(like="_rf_", axis=0)
    test = new_df[new_df.split == "test"]
    results["precision"] = [test.loc[test[p] == 1, TARGET].mean() for p in results.index]
    results = results.sort_values("CAGR", ascending=False)
    print(results[["count_investments", "precision", "avg_investments_per_day", "CAGR"]].round(4))

    best = results[results.avg_investments_per_day < 5].index[0]
    print(f"\nANSWER Q2: {best} -> threshold 0.{best.split('_')[-1]}")


if __name__ == "__main__":
    main()
