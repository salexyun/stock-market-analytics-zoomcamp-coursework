"""
Question 1: Dummies for Month and Week-of-Month

What is the ABSOLUTE CORRELATION VALUE of the most correlated dummy variable
<month>_w<week_of_month> with the binary outcome is_positive_growth_30d_future?
"""
import pandas as pd

from prep import TARGET, build_new_df


def main():
    new_df, numerical, dummies = build_new_df()
    wom_dummies = [d for d in dummies if d.startswith("month_wom_")]
    print(f"Dummies: {len(dummies)} total (spec ~115), {len(wom_dummies)} month_wom (spec ~60)")

    corr = new_df[numerical + dummies + [TARGET]].corr()[TARGET]
    corr_wom = pd.DataFrame(corr[wom_dummies])
    corr_wom["abs_corr"] = corr_wom[TARGET].abs()
    corr_wom = corr_wom.sort_values("abs_corr", ascending=False)
    print("\nTop 10 month_wom dummies by |corr|:")
    print(corr_wom.head(10))

    top = corr_wom.index[0]
    print(f"\nANSWER Q1: {top} -> |corr| = {corr_wom['abs_corr'].iloc[0]:.3f}")


if __name__ == "__main__":
    main()
