"""
Question 4: [Exploratory] Describe Your Ideal Trading Strategy
"""

ANSWER = """
Each day, invest only in the top 3 stocks by Random Forest probability (>= 0.60),
and only if the decision tree also predicts growth. Split capital across the 30-day
holding window, weight by confidence, and cap each position at 30%. Use a 10%
stop-loss and skip new entries when the S&P 500's 30-day trend is negative.
"""


if __name__ == "__main__":
    print(ANSWER)
