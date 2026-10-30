"""
Question 1: Less Features is More

Find the CAGR for pred10_rf_best_rule_55 using the new setup
(Ticker and month_wom removed from CATEGORICAL before generating dummies).
"""
import pandas as pd

from prep import CATEGORICAL, add_model_predictions, build_new_df, simulate

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)


def run(categorical):
    new_df, features = build_new_df(categorical)
    print(f"Features: {len(features)}")
    add_model_predictions(new_df, features)
    return simulate(new_df)


def main():
    short = [c for c in CATEGORICAL if c not in ("Ticker", "month_wom")]
    results = {name: run(cats) for name, cats in [("original", CATEGORICAL), ("short", short)]}

    print(pd.concat(results, axis=1)[[(n, c) for c in ("CAGR", "avg_investments_per_day") for n in results]].round(4))
    # spec's 1.1195 is the original best ML predictor (pred5_clf_10 in the notebook's Colab run)
    best_original = results["original"].CAGR.idxmax()
    cagr = results["short"].loc["pred10_rf_best_rule_55", "CAGR"]
    print(f"\nOriginal best: {best_original} = {results['original'].CAGR.max():.4f} (Colab: pred5_clf_10 = 1.1196)")
    print(f"ANSWER Q1: pred10_rf_best_rule_55 CAGR = {cagr:.4f}")


if __name__ == "__main__":
    main()
