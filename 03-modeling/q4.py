"""
Question 4: Hyperparameter tuning for a Decision Tree

What is the optimal tree depth (from 1 to 12) for a DecisionTreeClassifier?

Reuses fit_and_predict_all() from q3.py.
"""
import pandas as pd
from sklearn.metrics import precision_score
from sklearn.tree import export_text

from prep import TARGET, build_new_df, precision_by_prediction
from q3 import fit_and_predict_all

DEPTHS = range(1, 13)


def main():
    new_df, numerical, dummies = build_new_df()
    features = numerical + dummies
    is_test = new_df.split == "test"

    rows = []
    for depth in DEPTHS:
        clf, y_pred = fit_and_predict_all(new_df, features, max_depth=depth)
        if depth <= 3:
            print(f"--- depth {depth} tree head ---")
            print(export_text(clf, feature_names=features, max_depth=3))
        rows.append({
            "max_depth": depth,
            "train_val_precision": precision_score(new_df.loc[~is_test, TARGET], y_pred[~is_test]),
            "test_precision": precision_score(new_df.loc[is_test, TARGET], y_pred[is_test], zero_division=0),
            "test_positives": int(y_pred[is_test].sum()),
        })
    scores = pd.DataFrame(rows).set_index("max_depth")
    print(scores)

    best_max_depth = scores["test_precision"].idxmax()
    _, new_df["pred5_clf_10"] = fit_and_predict_all(new_df, features, max_depth=10)
    _, new_df["pred6_clf_best"] = fit_and_predict_all(new_df, features, max_depth=best_max_depth)

    predictions = [k for k in new_df.keys() if k.startswith("pred")]
    print("\nTEST set precision, all predictions:")
    print(precision_by_prediction(new_df, predictions))

    print(f"\nANSWER Q4: best_max_depth = {best_max_depth} "
          f"(test precision = {scores.loc[best_max_depth, 'test_precision']:.4f})")


if __name__ == "__main__":
    main()
