"""
Question 5: [Exploratory, Optional] Predicting a Positive-Return IPO

Free-text answer: how would you change the IPO strategy to increase
profitability?
"""

ANSWER = """
From Q2/Q3, buying every 2025 IPO and holding it loses money for the typical
stock: the median growth falls from ~0.93 after 1 month to ~0.5 after a
year. So the fix is mostly about being selective and not holding blindly:

- Filter before buying -- instead of buying every IPO, only take ones with
  signals known at IPO time: offer size (tiny $4-$5 microcap deals did
  worst), whether it priced above/within its range, first-day pop vs.
  offer price, industry, and the underwriters. Train a simple classifier
  (e.g. logistic regression or a tree model) on past years' IPOs to predict
  "positive 3-month return" and only buy the top-scored ones.
- Don't buy on day 1 -- IPOs tend to drift down after the first-day hype,
  so waiting for the price to settle (or for the lock-up expiry around
  6 months, when insiders can sell) could give a better entry.
- Exit rules instead of a fixed holding period -- use a stop-loss and a
  take-profit so the few big winners run while the many losers are cut
  early.
- Short or avoid the weakest group -- if the model can spot IPOs likely to
  fall, those can be skipped (or shorted, if borrow is available).
- Clean the data first -- drop pre-IPO OTC prices (like PPCB's $0.02 row)
  and SPAC units stuck around $10 so they don't distort the stats.
"""


def main():
    print(ANSWER.strip())


if __name__ == "__main__":
    main()
