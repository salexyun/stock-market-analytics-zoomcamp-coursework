"""
Question 3: Redefining the Growth Target

With is_positive_growth_30d_future = growth_future_30d > 1.022 (original
dummies), what is the number of trades for the best predictor pred5_clf_10?
"""
import pandas as pd

from prep import TARGET, add_model_predictions, build_new_df, simulate

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)


def main():
    new_df, features = build_new_df(target_threshold=1.022)
    print(f"Class 1 share: {new_df[TARGET].mean():.3f} (spec ~0.50)")
    add_model_predictions(new_df, features)

    results = simulate(new_df).sort_values("CAGR", ascending=False)
    print(results[["count_investments", "avg_investments_per_day", "CAGR"]].round(4))

    pred5 = results.loc["pred5_clf_10"]
    print(f"\nANSWER Q3: pred5_clf_10 avg trades per day = {pred5.avg_investments_per_day:.2f} "
          f"(rounded {round(pred5.avg_investments_per_day)}), total {int(pred5.count_investments)}")


if __name__ == "__main__":
    main()
