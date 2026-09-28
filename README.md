# Stock Markets Analytics Zoomcamp — Coursework

Coursework for the [DataTalksClub Stock Markets Analytics Zoomcamp (2026 cohort)](https://github.com/DataTalksClub/stock-markets-analytics-zoomcamp).

## Setup

Environment is managed with [uv](https://docs.astral.sh/uv/):

```bash
uv sync
```

Each homework question is a standalone script:

```bash
uv run python <module-folder>/q<N>.py   # e.g. uv run python 02-dataframe-analysis/q1.py
```

## Module 1 — Intro and Data Sources

Lesson: [`Module01_Colab_Introduction_and_Data_Sources.ipynb`](https://github.com/DataTalksClub/stock-markets-analytics-zoomcamp/blob/main/01-intro-and-data-sources/Module01_Colab_Introduction_and_Data_Sources.ipynb)
Homework: [`cohorts/2026/homework1.md`](https://github.com/DataTalksClub/stock-markets-analytics-zoomcamp/blob/main/cohorts/2026/homework1.md)

Scripts `q1.py`–`q6.py` in [`01-intro-and-data-sources/`](01-intro-and-data-sources/), plus the full worked analysis in [`homework1.ipynb`](01-intro-and-data-sources/homework1.ipynb).

## Module 2 — DataFrame Analysis

Homework: [`cohorts/2026/homework2.md`](https://github.com/DataTalksClub/stock-markets-analytics-zoomcamp/blob/main/cohorts/2026/homework2.md)

Scripts `q1.py`–`q5.py` in [`02-dataframe-analysis/`](02-dataframe-analysis/). Q3 reuses the stock data Q2 downloads and caches in `02-dataframe-analysis/data/`.
