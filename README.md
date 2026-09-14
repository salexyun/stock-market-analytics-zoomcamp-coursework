# Stock Markets Analytics Zoomcamp — Coursework

Coursework for the [DataTalksClub Stock Markets Analytics Zoomcamp (2026 cohort)](https://github.com/DataTalksClub/stock-markets-analytics-zoomcamp).

## Setup

Environment is managed with [uv](https://docs.astral.sh/uv/):

```bash
uv sync
```

## Module 1 — Intro and Data Sources

Lesson: [`Module01_Colab_Introduction_and_Data_Sources.ipynb`](https://github.com/DataTalksClub/stock-markets-analytics-zoomcamp/blob/main/01-intro-and-data-sources/Module01_Colab_Introduction_and_Data_Sources.ipynb)
Homework questions: https://courses.datatalks.club/sma-zoomcamp-2026/homework/hw01

See [`01-intro-and-data-sources/homework1.ipynb`](01-intro-and-data-sources/homework1.ipynb) for the full worked
analysis, or run the individual scripts:

```bash
uv run python 01-intro-and-data-sources/q1.py
uv run python 01-intro-and-data-sources/q2.py
uv run python 01-intro-and-data-sources/q3.py
uv run python 01-intro-and-data-sources/q4.py
```

`q5.py` and `q6.py` hold the two optional free-text questions (capstone
project brainstorm, new metrics investigation) — fill in your own answer in
each before submitting:

```bash
uv run python 01-intro-and-data-sources/q5.py
uv run python 01-intro-and-data-sources/q6.py
```

### Answers

| # | Question | Answer |
|---|---|---|
| 1 | Year with the most S&P 500 additions (2020+) | **2025** (18 additions) |
| 1 (extra) | Current S&P 500 stocks in the index > 20 years | 224 |
| 2 | Indexes (of 10) beating the S&P 500 YTD as of 2026-08-21 | **2** (Nikkei 225, S&P/TSX Composite) |
| 3 | Median drawdown (%) of significant S&P 500 corrections (1950–present) | **~8%** (7.99%) |
| 4 | Median 2-day % change after positive AMZN earnings surprises | **0.35%** |
| 5 | Capstone project brainstorm (optional, free text) | see `q5.py` |
| 6 | New metrics investigation (optional, free text) | see `q6.py` |

Verified against the [homework spec](https://github.com/DataTalksClub/stock-markets-analytics-zoomcamp/blob/main/cohorts/2026/homework1.md):
- **Q1**: Wikipedia's "List of S&P 500 companies" page currently only exposes the
  live constituents table (with a `Date added` column) via `pandas.read_html()` —
  the separate historical "changes" table that used to sit below it is no longer
  present, so additions/removals before a stock's *current* stay in the index
  aren't captured. Direct requests get a 403, so the page is fetched with a
  browser `User-Agent` first (as the spec's hint suggests) and the HTML is
  handed to `pandas.read_html()`.
- **Q3**: a "correction" = a decline of ≥5% from a running all-time high to the
  subsequent trough, before a new all-time high is made. The spec ships a
  reference list of the 10 largest S&P 500 corrections by drawdown — `q3.py`
  cross-checks against it, and all 10 match exactly (dates, drawdown %, and
  duration in days).
- **Q4**: `get_earnings_dates()` with no `limit` returns exactly the 25 AMZN
  entries from 2020-10-29 the spec describes (1 future one has no surprise
  data yet, leaving 24). For each 3-day (Day1/Day2/Day3) window around each
  announcement, the 2-day return is `Close_Day3 / Close_Day1 - 1`.
