"""
Question 6: New Metrics Investigation (Optional)

Free-text answer identifying additional metrics or time series relevant to
your project, explaining their value and retrieval methods.
"""

ANSWER = """
A few extra metrics that could help the Korean market model:

- USD/KRW exchange rate (yfinance ticker "KRW=X") -- Korean exporters
  earn a lot of revenue overseas, so a weaker/stronger won can move their
  stock prices even without any change in the underlying business.
- Philadelphia Semiconductor Index (yfinance ticker "^SOX") -- Samsung and
  SK Hynix are semiconductor companies, so US chip-sector sentiment tends
  to spill over into how their stocks trade.
- VIX (yfinance ticker "^VIX") -- a simple proxy for global risk appetite;
  emerging markets like Korea tend to sell off more when it spikes.

All three are easy to pull with the same yf.download()/yf.Ticker() calls
used elsewhere in this homework.
"""


def main():
    print(ANSWER.strip())


if __name__ == "__main__":
    main()
