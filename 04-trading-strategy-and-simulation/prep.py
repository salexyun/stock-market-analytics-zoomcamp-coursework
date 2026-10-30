"""
Shared pipeline for Module 4: reproduces the lesson notebook end to end
(features, dummies, temporal split, hand rules, Decision Tree / Random Forest
predictors, and the $100-per-signal trading simulation).

Knobs for the homework:
  - categorical: which columns get dummies (Q1 drops Ticker and month_wom)
  - target_threshold: growth_future_30d cut-off for the target (Q3 uses 1.022)
  - rf_thresholds: extra Random Forest decision rules (Q2)

The course parquet is shared with Module 3 (cached in 03-modeling/data/).
"""
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

# reuse Module 3's loader and feature lists (its file is also named prep.py)
_spec = importlib.util.spec_from_file_location("m3_prep", Path(__file__).parents[1] / "03-modeling" / "prep.py")
m3 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(m3)
MACRO, TECHNICAL_INDICATORS, load_df_full, temporal_split = m3.MACRO, m3.TECHNICAL_INDICATORS, m3.load_df_full, m3.temporal_split

TARGET = "is_positive_growth_30d_future"
CATEGORICAL = ["Month", "Weekday", "Ticker", "ticker_type", "month_wom"]
CUSTOM_NUMERICAL = ["SMA10", "SMA20", "growing_moving_average", "high_minus_low_relative",
                    "volatility", "ln_volume", "div_payout", "stock_split"]


def numerical_features(df):
    growth = [k for k in df.keys() if k.startswith("growth_") and "future" not in k]
    patterns = [k for k in df.keys() if "cdl" in k]
    return growth + TECHNICAL_INDICATORS + patterns + CUSTOM_NUMERICAL + MACRO


def build_new_df(categorical=CATEGORICAL, target_threshold=1.0):
    """Returns (new_df, features) like the lesson notebook."""
    df_full = load_df_full()
    df_full["ln_volume"] = np.log(df_full.Volume + 1e-6)
    df_full["div_payout"] = (df_full.Dividends > 0).astype(int)
    df_full["stock_split"] = (df_full["Stock Splits"] > 0).astype(int)
    df_full[TARGET] = (df_full.growth_future_30d > target_threshold).astype(int)

    df = df_full[df_full.Date >= "2000-01-01"].copy()
    df["Month"] = df.Month.dt.month_name()
    df["Weekday"] = df.Weekday.astype(str)
    df["month_wom"] = df.Month + "_w" + ((df.Date.dt.day - 1) // 7 + 1).astype(str)

    dummies = pd.get_dummies(df[categorical], dtype="int32")
    new_df = pd.concat([df, dummies], axis=1)
    new_df["split"] = temporal_split(new_df)

    new_df["pred0_manual_cci"] = (new_df.cci > 200).astype(int)
    new_df["pred1_manual_prev_g1"] = (new_df.growth_30d > 1).astype(int)
    new_df["pred2_manual_prev_g1_and_snp"] = ((new_df.growth_30d > 1) & (new_df.growth_snp500_30d > 1)).astype(int)
    new_df["pred3_manual_dgs10_5"] = ((new_df.DGS10 <= 4.5) & (new_df.DGS5 <= 4)).astype(int)
    new_df["pred4_manual_dgs10_fedfunds"] = ((new_df.DGS10 > 4) & (new_df.FEDFUNDS <= 4.795)).astype(int)
    return new_df.copy(), numerical_features(df_full) + dummies.columns.to_list()


def clean_X(df, features):
    return df[features].replace([np.inf, -np.inf], np.nan).fillna(0)


def add_model_predictions(new_df, features, rf_thresholds=()):
    """Fits the lesson's models on train+validation and adds pred5..pred11 (+ extra RF rules).

    Returns (rf_best, clf_best) for further analysis.
    """
    train_valid = new_df.split.isin(["train", "validation"])
    X_train_valid, y_train_valid = clean_X(new_df[train_valid], features), new_df.loc[train_valid, TARGET]
    X_all = clean_X(new_df, features)

    def tree(depth):
        return DecisionTreeClassifier(max_depth=depth, random_state=42).fit(X_train_valid, y_train_valid)

    new_df["pred5_clf_10"] = tree(10).predict(X_all)
    new_df["pred6_clf_4"] = tree(4).predict(X_all)
    clf_best = tree(7)
    new_df["pred7_clf_second_best"] = clf_best.predict(X_all)

    proba = clf_best.predict_proba(X_all)[:, 1]
    new_df["pred8_clf_second_best_rule_56"] = (proba >= 0.56).astype(int)
    new_df["pred9_clf_second_best_rule_66"] = (proba >= 0.66).astype(int)

    rf_best = RandomForestClassifier(n_estimators=100, max_depth=13, random_state=42, n_jobs=-1)
    rf_best.fit(X_train_valid, y_train_valid)
    proba = rf_best.predict_proba(X_all)[:, 1]
    new_df["pred10_rf_best_rule_55"] = (proba >= 0.55).astype(int)
    new_df["pred11_rf_best_rule_65"] = (proba >= 0.65).astype(int)
    for i, t in enumerate(rf_thresholds, start=12):
        new_df[f"pred{i}_rf_best_rule_{round(t * 100)}"] = (proba >= t).astype(int)
    return rf_best, clf_best


def simulate(new_df):
    """Lesson simulation: $100 per positive prediction on TEST, held 30 days, 0.2% fees."""
    test = new_df[new_df.split == "test"]
    rows = []
    for pred in [k for k in new_df.keys() if k.startswith("pred")]:
        trades = test[test[pred] == 1]
        gross = (100 * (trades.growth_future_30d - 1)).sum()
        fees = -0.2 * len(trades)
        net = (100 * (trades.growth_future_30d - 1) - 0.2).sum()  # like the notebook: skips NaN future growth
        daily = trades.groupby("Date")[pred].count()
        capital = 100 * 30 * daily.quantile(0.75)
        rows.append({
            "prediction": pred,
            "count_investments": len(trades),
            "gross_rev": gross,
            "fees": fees,
            "net_rev": net,
            "avg_investments_per_day": daily.mean(),
            "capital": capital,
            "CAGR": ((capital + net) / capital) ** (1 / 4) if capital else np.nan,
        })
    return pd.DataFrame(rows).set_index("prediction")
