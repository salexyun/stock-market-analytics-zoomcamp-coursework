# Stock Markets Analytics Zoomcamp — Coursework

Coursework for the [DataTalksClub Stock Markets Analytics Zoomcamp (2026 cohort)](https://github.com/DataTalksClub/stock-markets-analytics-zoomcamp).

## Setup

Environment is managed with [uv](https://docs.astral.sh/uv/):

```bash
uv sync
```

## Module 1 — Intro and Data Sources

Lesson: [`Module01_Colab_Introduction_and_Data_Sources.ipynb`](https://github.com/DataTalksClub/stock-markets-analytics-zoomcamp/blob/main/01-intro-and-data-sources/Module01_Colab_Introduction_and_Data_Sources.ipynb)
Homework: [`cohorts/2026/homework1.md`](https://github.com/DataTalksClub/stock-markets-analytics-zoomcamp/blob/main/cohorts/2026/homework1.md)

See [`01-intro-and-data-sources/homework1.ipynb`](01-intro-and-data-sources/homework1.ipynb) for the full worked
analysis, or run the individual scripts:

```bash
uv run python 01-intro-and-data-sources/q1.py
uv run python 01-intro-and-data-sources/q2.py
uv run python 01-intro-and-data-sources/q3.py
uv run python 01-intro-and-data-sources/q4.py
uv run python 01-intro-and-data-sources/q5.py
uv run python 01-intro-and-data-sources/q6.py
```

## Module 2 — DataFrame Analysis

Homework: [`cohorts/2026/homework2.md`](https://github.com/DataTalksClub/stock-markets-analytics-zoomcamp/blob/main/cohorts/2026/homework2.md)

Run the scripts (Q3 reuses the stock data Q2 downloads and caches in `02-dataframe-analysis/data/`):

```bash
uv run python 02-dataframe-analysis/q1.py
uv run python 02-dataframe-analysis/q2.py
uv run python 02-dataframe-analysis/q3.py
uv run python 02-dataframe-analysis/q4.py
uv run python 02-dataframe-analysis/q5.py
```

Q5 tl;dr: only buy the IPOs a model trained on past deals scores well (using what's known at IPO time), wait out the post-IPO drift before buying, and use stop-loss and take-profit exits instead of holding for a fixed period.
