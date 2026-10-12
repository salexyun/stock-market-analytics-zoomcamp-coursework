"""
Question 3: Unique Correct Predictions from a 10-Level Decision Tree Classifier

What is the total number of records in the TEST dataset where the new
prediction pred5_clf_10 is correct, while all 'hand' rule predictions
(pred0 to pred4) are incorrect?
"""
from sklearn.tree import DecisionTreeClassifier

from prep import TARGET, build_new_df, clean_X, precision_by_prediction


def fit_and_predict_all(new_df, features, max_depth):
    """Fit on TRAIN+VALIDATION, predict on every row of new_df (same order)."""
    train = new_df.split.isin(["train", "validation"])
    clf = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
    clf.fit(clean_X(new_df[train], features), new_df.loc[train, TARGET])
    return clf, clf.predict(clean_X(new_df, features))


def only_correct(row, pred, predictions):
    """True when `pred` is correct and every other prediction is wrong."""
    return row[pred] == row[TARGET] and all(row[p] != row[TARGET] for p in predictions if p != pred)


def main():
    new_df, numerical, dummies = build_new_df()
    hand_rules = [k for k in new_df.keys() if k.startswith("pred")]

    _, new_df["pred5_clf_10"] = fit_and_predict_all(new_df, numerical + dummies, max_depth=10)
    predictions = hand_rules + ["pred5_clf_10"]
    print("TEST set precision:")
    print(precision_by_prediction(new_df, predictions))

    test = new_df[new_df.split == "test"].copy()
    test["only_pred5_is_correct"] = test.apply(only_correct, axis=1, args=("pred5_clf_10", predictions)).astype(int)
    print(f"\nANSWER Q3: {test['only_pred5_is_correct'].sum()} TEST rows where only pred5_clf_10 is correct")


if __name__ == "__main__":
    main()
