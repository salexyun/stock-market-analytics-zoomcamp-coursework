"""
Question 5: [Exploratory] What data is missing?

Free-text answer: which new indicators would you add to the dataset, and why?
"""

ANSWER = """
The trees (Q4's depth-4 tree splits on cpi_core_yoy, FEDFUNDS, DGS10,
growth_btc_usd_365d and growth_wti_oil_365d first) lean almost entirely on
macro LEVELS. Those mostly identify the time period rather than the stock:
pred3/pred4 are 100%/0% positive on the whole validation window, and a
10-level tree beats depth 4 on train but loses on test. So the gaps are:

- Macro changes instead of levels -- 1/3/6-month deltas of DGS10, FEDFUNDS
  and CPI, plus the yield-curve slope (FRED T10Y2Y / T10Y3M). These carry
  the "rates are falling / curve is steepening" signal without memorising
  which years had 4% yields.
- Regional macro -- a third of the tickers are Indian or EU, but every macro
  feature is US. Add RBI repo rate + India CPI (RBI DBIE / FRED
  INDCPIALLMINMEI), ECB deposit rate + euro area HICP + Bund yield (ECB Data
  Portal / FRED IRLTLT01DEM156N), and the FX rates INR=X / EURUSD=X (yfinance)
  since a USD investor's return depends on them.
- Risk sentiment -- VIX (^VIX), India VIX (^INDIAVIX), VSTOXX, and the high-
  yield credit spread (FRED BAMLH0A0HYM2). Fear spikes tend to precede
  30-day rebounds, which is exactly the target.
- Relative strength -- each stock's growth_30d/90d MINUS its home index's
  (^NSEI, ^STOXX50E, ^GSPC), and its cross-sectional rank among the 33
  tickers on that date. These are about the stock, not the regime.
- Fundamentals/events -- days to next earnings date, last earnings surprise,
  forward P/E vs. its own history (yfinance .earnings_dates / .info, or
  Financial Modeling Prep for history), plus dividend/ex-dates.
- Seasonality, but compact -- Q1 shows Oct/Nov weeks carry the strongest
  calendar signal; a "days to month end" / "turn of month" flag and a
  "Q4 (Oct-Dec)" flag capture it in 2 columns instead of 60 sparse dummies.
"""


if __name__ == "__main__":
    print(ANSWER)
