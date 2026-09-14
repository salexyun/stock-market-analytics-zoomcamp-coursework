"""
Question 1: S&P 500 Stocks Added to the Index

Main Task: Which year had the highest number of additions (starting from 2020)?
Additional Task: How many current S&P 500 stocks have been in the index for
more than 20 years?

Note: Wikipedia's "List of S&P 500 companies" page used to also carry a
separate "Selected changes to the list of components" history table, but as
of this run only the current-constituents table (with a "Date added" column)
is present, so that's the one we use.
"""
import io

import pandas as pd
import requests

WIKI_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"


def load_sp500_current():
    # can't call pd.read_html() directly on this URL (403) -- same trick as
    # the course notebook's "Web Scraping for Macro" section: fetch with a
    # browser-like User-Agent first, then hand the HTML to pandas.
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    resp = requests.get(WIKI_URL, headers=headers, timeout=30)
    resp.raise_for_status()
    tables = pd.read_html(io.StringIO(resp.text))
    current = tables[0]  # current constituents, has "Date added"
    return current


def main():
    current = load_sp500_current().copy()
    current["Date added"] = pd.to_datetime(current["Date added"], errors="coerce")
    current["year_added"] = current["Date added"].dt.year

    # --- Main task: additions per year from 2020 onward ---
    additions_by_year = (
        current[current["year_added"] >= 2020]
        .groupby("year_added")
        .size()
        .sort_index()
    )
    print("Additions by year (2020+):")
    print(additions_by_year)

    top_year = additions_by_year.idxmax()
    top_count = additions_by_year.max()
    print(f"\nANSWER Q1 (main): Year with most additions = {top_year} ({top_count} additions)")

    # --- Additional task: how many current stocks in index > 20 years ---
    today = pd.Timestamp.today()
    current["years_in_index"] = (today - current["Date added"]).dt.days / 365.25
    over_20 = current[current["years_in_index"] > 20]
    print(f"\nANSWER Q1 (additional): Stocks in index for more than 20 years = {len(over_20)}")
    print(
        over_20[["Symbol", "Security", "Date added", "years_in_index"]]
        .sort_values("years_in_index", ascending=False)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()
