"""
Question 5: Capstone Project Brainstorm (Optional)

Free-text answer describing your capstone project idea, including asset
class, geography, industry focus, investment horizon, and proposed
methodology.
"""

ANSWER = """
I want to build a short-to-medium-term prediction model for the Korean
stock market (KOSPI and KOSDAQ), with a first focus on large, liquid
exporters -- semiconductors and electronics (Samsung Electronics, SK
Hynix), autos (Hyundai, Kia), and shipbuilding/battery names -- since
these dominate index performance and are especially sensitive to global
demand cycles. Investment horizon: roughly 5-30 trading days (short swing
to short-term positioning, not intraday or long-term buy-and-hold).

Proposed methodology:
- Price/technical features: returns, volatility, RSI, MACD, moving-average
  crossovers, and volume trends per ticker.
- Korea-specific macro drivers: KRW/USD exchange rate, the semiconductor
  price/demand cycle, foreign investor net buy/sell flows on the KRX, and
  spillover from US tech earnings (given how correlated KOSPI is with
  Nasdaq semiconductor names).
- Target: next-N-day forward return (classification: up/down beyond a
  threshold, or regression on the return itself).
- Models: start with gradient boosting (XGBoost/LightGBM) on engineered
  features as a baseline, then compare against a simple LSTM/temporal
  model if the baseline shows signal.
- Evaluation: walk-forward/expanding-window backtesting (not a random
  train/test split, to avoid look-ahead bias), with a simple long-only
  strategy simulation to translate model accuracy into a Sharpe-ratio-like
  metric.
"""


def main():
    print(ANSWER.strip())


if __name__ == "__main__":
    main()
