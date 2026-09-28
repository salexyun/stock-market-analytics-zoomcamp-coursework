"""
Question 1: [IPO] Withdrawn IPOs by Company Type

What is the total withdrawn IPO value (in $ millions) for the company class
with the highest total withdrawal value?

Note: the iposcoop "recently filed" table is a rolling list, so it keeps
growing after the homework was written. We keep only withdrawn rows with a
File Date before 2026-09-11 to match the question's "before Sep 11, 2026".
"""
import io

import numpy as np
import pandas as pd
import requests

URL = "https://www.iposcoop.com/ipos-recently-filed/"
CUTOFF = pd.Timestamp("2026-09-11")

# order matters -- first match wins
COMPANY_TYPE_RULES = [
    (["Technologies"], "Technologies"),
    (["Acquisition Corp", "Acquisition Corporation", "Corp"], "Acquisition Corp"),
    (["Inc", "Incorporated"], "Inc."),
    (["Group"], "Group"),
    (["Ltd", "Limited"], "Limited"),
    (["Holdings", "Holding"], "Holdings"),
]


def load_filed_ipos():
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(URL, headers=headers, timeout=30)
    resp.raise_for_status()
    return pd.read_html(io.StringIO(resp.text))[0]


def classify_company(name):
    for patterns, label in COMPANY_TYPE_RULES:
        if any(p in name for p in patterns):
            return label
    return "Other"


def parse_price(value):
    # '$8.00' -> 8.0, '-' / NaN -> NaN
    if pd.isna(value) or str(value).strip() == "-":
        return np.nan
    return float(str(value).replace("$", "").replace(",", ""))


def to_numeric(series):
    return pd.to_numeric(
        series.astype(str).str.replace("$", "", regex=False).str.replace(",", "", regex=False),
        errors="coerce",
    )


def main():
    df = load_filed_ipos()
    df["File Date"] = pd.to_datetime(df["File Date"])

    withdrawn = df[(df["Expected To Trade"] == "Withdrawn") & (df["File Date"] < CUTOFF)].copy()
    print(f"Withdrawn IPOs filed before {CUTOFF.date()}: {len(withdrawn)} (spec expects ~32)")

    withdrawn["Company Type"] = withdrawn["Company"].apply(classify_company)
    withdrawn["Avg_price"] = (
        withdrawn["Price Low"].apply(parse_price) + withdrawn["Price High"].apply(parse_price)
    ) / 2
    withdrawn["Shares (millions)"] = to_numeric(withdrawn["Shares (millions)"])
    withdrawn["Est $ Vol (millions)"] = to_numeric(withdrawn["Est $ Vol (millions)"])

    withdrawn["Shares_offered_value"] = (
        withdrawn["Shares (millions)"] * withdrawn["Avg_price"]
    ).fillna(withdrawn["Est $ Vol (millions)"])

    print(
        withdrawn[["Company", "Company Type", "Shares (millions)", "Avg_price",
                   "Est $ Vol (millions)", "Shares_offered_value"]].to_string(index=False)
    )

    by_type = withdrawn.groupby("Company Type")["Shares_offered_value"].agg(["count", "sum"])
    by_type = by_type.sort_values("sum", ascending=False)
    print("\nWithdrawn value by Company Type ($M):")
    print(by_type)

    top = by_type.index[0]
    print(f"\nANSWER Q1: {top} with ${by_type.loc[top, 'sum']:,.2f}M withdrawn")


if __name__ == "__main__":
    main()
