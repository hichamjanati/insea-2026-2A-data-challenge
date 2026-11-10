"""Baseline: an ordinary least squares regression (OLS) on a few table columns, trained on the complete rows only.

Usage: uv run python -m kit.train
Writes submissions/baseline.csv. Reported score: 5-fold cross-validated MAE on the training rows used.

This is a starting point, not a recommendation. Two of its choices are worth questioning on day one:
  - it drops every training ad with a missing value in the columns it uses;
  - at prediction time, a test ad with a missing value gets the train median, since the model never saw such ads.
"""
from datetime import date
import numpy as np, pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from kit.data import SUBMISSIONS, TARGET, load_train, load_test

NUMERIC = ["reg_year", "km", "engine_l", "price_mad", "n_photos", "desc_length"]
CATEGORICAL = ["make", "gearbox", "fuel", "body_type", "city", "seller_type"]
# we use only some of the columns to keep the baseline short

train, test = load_train(), load_test()
median = train[TARGET].median()
cols = NUMERIC + CATEGORICAL
complete = train[cols].notna().all(axis=1)
print(f"train: {len(train):,} ads, {complete.sum():,} complete on the {len(cols)} columns used ({complete.mean():.1%})")
X, y = train.loc[complete, cols], train.loc[complete, TARGET]

# numeric columns as they are, categorical columns one-hot encoded, then OLS: no scaling, no tuning
model = Pipeline([
    ("prep", ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL)],
                               remainder="passthrough")),
    ("reg", LinearRegression()),
])
cv = -cross_val_score(model, X, y, cv=5, scoring="neg_mean_absolute_error")
print(f"5-fold MAE on the complete training rows: {cv.mean():.3f} (+/- {cv.std():.3f})")
model.fit(X, y)

test_complete = test[cols].notna().all(axis=1)
pred = np.full(len(test), median)
pred[test_complete.values] = model.predict(test.loc[test_complete, cols])
print(f"test: {len(test):,} ads, {(~test_complete).sum():,} with a missing value get the train median {median:.1f}")

SUBMISSIONS.mkdir(exist_ok=True)
out = SUBMISSIONS / "baseline.csv"
pd.DataFrame({"id": test.id, TARGET: pred}).to_csv(out, index=False)
print(f"written {out}  ({date.today()})")
