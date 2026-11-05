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

Lesson: [`[2026]_Module_01_Colab_Introduction_and_Data_Sources.ipynb`](https://github.com/DataTalksClub/stock-markets-analytics-zoomcamp/blob/main/01-intro-and-data-sources/%5B2026%5D_Module_01_Colab_Introduction_and_Data_Sources.ipynb)
Homework: [`cohorts/2026/homework1.md`](https://github.com/DataTalksClub/stock-markets-analytics-zoomcamp/blob/main/cohorts/2026/homework1.md)

Scripts `q1.py`–`q6.py` in [`01-intro-and-data-sources/`](01-intro-and-data-sources/), plus the full worked analysis in [`homework1.ipynb`](01-intro-and-data-sources/homework1.ipynb).

## Module 2 — DataFrame Analysis

Lesson: [`[2026]_Module_02_Colab_Working_with_the_data.ipynb`](https://github.com/DataTalksClub/stock-markets-analytics-zoomcamp/blob/main/02-dataframe-analysis/%5B2026%5D_Module_02_Colab_Working_with_the_data.ipynb)
Homework: [`cohorts/2026/homework2.md`](https://github.com/DataTalksClub/stock-markets-analytics-zoomcamp/blob/main/cohorts/2026/homework2.md)

Scripts `q1.py`–`q5.py` in [`02-dataframe-analysis/`](02-dataframe-analysis/), plus the full worked analysis in [`homework2.ipynb`](02-dataframe-analysis/homework2.ipynb). Q3 reuses the stock data Q2 downloads and caches in `02-dataframe-analysis/data/`.

## Module 3 — Modeling

Lesson: [`[2026]_Module_03_Colab_Time_Series_Modeling.ipynb`](https://github.com/DataTalksClub/stock-markets-analytics-zoomcamp/blob/main/03-modeling/%5B2026%5D_Module_03_Colab_Time_Series_Modeling.ipynb)
Homework: [`cohorts/2026/homework3.md`](https://github.com/DataTalksClub/stock-markets-analytics-zoomcamp/blob/main/cohorts/2026/homework3.md)

Scripts `q1.py`–`q5.py` in [`03-modeling/`](03-modeling/), plus the full worked analysis in [`homework3.ipynb`](03-modeling/homework3.ipynb). Shared data prep lives in `prep.py`; the course parquet is cached in `03-modeling/data/`.

## Module 4 — Trading Strategy and Simulation

Lesson: [`[2026]_Module_04_Colab_Trading_Simulations.ipynb`](https://github.com/DataTalksClub/stock-markets-analytics-zoomcamp/blob/main/04-trading-strategy-and-simulation/%5B2026%5D_Module_04_Colab_Trading_Simulations.ipynb)
Homework: [`cohorts/2026/homework4.md`](https://github.com/DataTalksClub/stock-markets-analytics-zoomcamp/blob/main/cohorts/2026/homework4.md)

Scripts `q1.py`–`q4.py` in [`04-trading-strategy-and-simulation/`](04-trading-strategy-and-simulation/), plus the full worked analysis in [`homework4.ipynb`](04-trading-strategy-and-simulation/homework4.ipynb). `prep.py` reproduces the lesson pipeline and simulation, reusing Module 3's cached data.

## Module 5 — Deployment and Automation

Homework: [`cohorts/2026/homework5.md`](https://github.com/DataTalksClub/stock-markets-analytics-zoomcamp/blob/main/cohorts/2026/homework5.md)

Free-text research proposals in [`homework5.md`](05-deployment-and-automation/homework5.md).
