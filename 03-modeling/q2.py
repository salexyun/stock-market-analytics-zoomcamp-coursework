"""
Question 2: Define New "Hand" Rules on Macro and Technical Indicator Variables

What is the precision score for the best of the NEW predictions (pred3 or
pred4), rounded to 3 digits after the comma?
"""
from prep import build_new_df, precision_by_prediction


def main():
    new_df, _, _ = build_new_df()
    predictions = [k for k in new_df.keys() if k.startswith("pred")]

    stats = precision_by_prediction(new_df, predictions)
    print("TEST set precision of hand rules:")
    print(stats)

    new = stats.loc[["pred3_manual_dgs10_5", "pred4_manual_dgs10_fedfunds"]].dropna()
    best = new["precision"].idxmax()
    print(f"\nANSWER Q2: {best} -> precision = {new.loc[best, 'precision']:.3f}")


if __name__ == "__main__":
    main()
