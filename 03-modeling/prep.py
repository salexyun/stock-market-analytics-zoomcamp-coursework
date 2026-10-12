"""
Shared data prep for Module 3: reproduces the lesson notebook's new_df
(dummies, temporal split, hand-rule predictions) with the homework extensions:
the month_wom dummies (Q1) and hand rules pred3/pred4 (Q2).

The course parquet is cached to data/ after the first download.
"""
from pathlib import Path

import gdown
import numpy as np
import pandas as pd

FILE_ID = "1oQSUMCs2DyQQIh8Y62UhrT00cIsE9Sr5"
DATA = Path(__file__).parent / "data" / "stocks_df_combined.parquet.brotli"

TARGET = "is_positive_growth_30d_future"

OHLCV = ["Open", "High", "Low", "Close", "Adj Close_x", "Volume"]
CATEGORICAL = ["Month", "Weekday", "Ticker", "ticker_type", "month_wom"]
CUSTOM_NUMERICAL = ["SMA10", "SMA20", "growing_moving_average", "high_minus_low_relative", "volatility", "ln_volume"]
TECHNICAL_INDICATORS = [
    "adx", "adxr", "apo", "aroon_1", "aroon_2", "aroonosc",
    "bop", "cci", "cmo", "dx", "macd", "macdsignal", "macdhist", "macd_ext",
    "macdsignal_ext", "macdhist_ext", "macd_fix", "macdsignal_fix",
    "macdhist_fix", "mfi", "minus_di", "mom", "plus_di", "dm", "ppo",
    "roc", "rocp", "rocr", "rocr100", "rsi", "slowk", "slowd", "fastk",
    "fastd", "fastk_rsi", "fastd_rsi", "trix", "ultosc", "willr",
    "ad", "adosc", "obv", "atr", "natr", "ht_dcperiod", "ht_dcphase",
    "ht_phasor_inphase", "ht_phasor_quadrature", "ht_sine_sine", "ht_sine_leadsine",
    "ht_trendmod", "avgprice", "medprice", "typprice", "wclprice",
]
MACRO = ["gdppot_us_yoy", "gdppot_us_qoq", "cpi_core_yoy", "cpi_core_mom", "FEDFUNDS", "DGS1", "DGS5", "DGS10"]


def load_df_full():
    if not DATA.exists():
        DATA.parent.mkdir(exist_ok=True)
        gdown.download(f"https://drive.google.com/uc?id={FILE_ID}", str(DATA), quiet=False)
    return pd.read_parquet(DATA)


def numerical_features(df):
    growth = [k for k in df.keys() if k.startswith("growth_") and "future" not in k]
    patterns = [k for k in df.keys() if "cdl" in k]
    return growth + TECHNICAL_INDICATORS + patterns + CUSTOM_NUMERICAL + MACRO


def temporal_split(df, train_prop=0.7, val_prop=0.15):
    min_date, max_date = df["Date"].min(), df["Date"].max()
    days = (max_date - min_date).days
    train_end = min_date + pd.Timedelta(days=days * train_prop)
    val_end = train_end + pd.Timedelta(days=days * val_prop)
    return np.where(df["Date"] <= train_end, "train", np.where(df["Date"] <= val_end, "validation", "test"))


def add_hand_rules(df):
    df["pred0_manual_cci"] = (df.cci > 200).astype(int)
    df["pred1_manual_prev_g1"] = (df.growth_30d > 1).astype(int)
    df["pred2_manual_prev_g1_and_snp"] = ((df.growth_30d > 1) & (df.growth_snp500_30d > 1)).astype(int)
    df["pred3_manual_dgs10_5"] = ((df.DGS10 <= 4.5) & (df.DGS5 <= 4)).astype(int)
    df["pred4_manual_dgs10_fedfunds"] = ((df.DGS10 > 4) & (df.FEDFUNDS <= 4.795)).astype(int)
    return df


def build_new_df():
    """Returns (new_df, NUMERICAL, DUMMIES) like the lesson notebook, plus month_wom dummies."""
    df_full = load_df_full()
    df_full["ln_volume"] = df_full.Volume.replace(0, np.nan).fillna(1e-9).apply(np.log)
    df = df_full[df_full.Date >= "2000-01-01"].copy()

    df["Weekday"] = df["Weekday"].astype(str)
    df["Month"] = df["Month"].dt.month.astype(str)
    df["month_wom"] = df["Date"].dt.month_name() + "_w" + ((df["Date"].dt.day - 1) // 7 + 1).astype(str)

    dummies = pd.get_dummies(df[CATEGORICAL], dtype="int32")
    new_df = pd.concat([df, dummies], axis=1)
    new_df["split"] = temporal_split(new_df)
    new_df = add_hand_rules(new_df.copy())
    return new_df, numerical_features(df_full), dummies.columns.to_list()


def clean_X(df, features):
    """Same cleaning as the lesson: +-inf -> NaN -> 0."""
    return df[features].replace([np.inf, -np.inf], np.nan).fillna(0)


def precision_by_prediction(new_df, predictions, split="test"):
    """Lesson-style precision: share of correct outcomes among rows where pred == 1."""
    sub = new_df[new_df.split == split]
    rows = []
    for p in predictions:
        positives = sub[sub[p] == 1]
        precision = (positives[TARGET] == 1).mean() if len(positives) else np.nan
        rows.append({"prediction": p, "positives": len(positives), "precision": precision})
    return pd.DataFrame(rows).set_index("prediction")
