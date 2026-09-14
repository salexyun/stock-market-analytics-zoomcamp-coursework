# Stock Markets Analytics Zoomcamp — Coursework

Coursework for the [DataTalksClub Stock Markets Analytics Zoomcamp (2026 cohort)](https://github.com/DataTalksClub/stock-markets-analytics-zoomcamp).

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Module 1 — Homework

Instructions: [homework1.md](https://github.com/DataTalksClub/stock-markets-analytics-zoomcamp/blob/main/cohorts/2026/homework1.md)
Submission form: https://courses.datatalks.club/sma-zoomcamp-2026/homework/hw01

See [`homework_01/homework1.ipynb`](homework_01/homework1.ipynb) for the full worked analysis, or run the
individual scripts:

```bash
python homework_01/q1_sp500_additions.py
python homework_01/q2_macro_indexes.py
python homework_01/q3_sp500_corrections.py
python homework_01/q4_amzn_earnings.py
```

### Answers

| # | Question | Answer |
|---|---|---|
| 1 | Year with the most S&P 500 additions (2020+) | **2025** (18 additions) |
| 1 (extra) | Current S&P 500 stocks in the index > 20 years | 224 |
| 2 | Indexes (of 10) beating the S&P 500 YTD as of 2026-08-21 | **2** (Nikkei 225, S&P/TSX Composite) |
| 3 | Median drawdown (%) of significant S&P 500 corrections (1950–present) | **~8%** (7.99%) |
| 4 | Median 2-day % change after positive AMZN earnings surprises | **0.35%** |

Notes on methodology:
- **Q1**: Wikipedia's "List of S&P 500 companies" page currently only exposes the
  live constituents table (with a `Date added` column) via `pandas.read_html()` —
  the separate historical "changes" table that used to sit below it is no longer
  present, so additions/removals before a stock's *current* stay in the index
  aren't captured.
- **Q3**: a "correction" = a decline of ≥5% from a running all-time high to the
  subsequent trough, before a new all-time high is made.
- **Q4**: for each of AMZN's last 24 earnings reports (since 2020-10-29) with
  surprise data, the "2-day return" is the % change from the close the trading
  day *before* the announcement to the close the trading day *after* it.
