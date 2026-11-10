"""Check a submission file before uploading it.

Usage: uv run python -m kit.check_submission submissions/<file>.csv
Exits with an error on anything Kaggle would reject; prints warnings for predictions that cannot be right.
"""
import sys
import numpy as np, pandas as pd
from kit.data import DATA, TARGET, N_TEST


def check(path) -> pd.DataFrame:
    errors, warnings = [], []
    sub = pd.read_csv(path)
    test_ids = pd.read_csv(DATA / "test.csv", usecols=["id"]).id

    if list(sub.columns) != ["id", TARGET]:
        errors.append(f"columns must be exactly ['id', '{TARGET}'], got {list(sub.columns)}")
    else:
        if len(sub) != N_TEST:
            errors.append(f"{len(sub):,} rows, expected {N_TEST:,}")
        if sub.id.duplicated().any():
            errors.append(f"{sub.id.duplicated().sum()} duplicated ids")
        if set(sub.id) != set(test_ids):
            errors.append(f"ids differ from test.csv: {len(set(test_ids) - set(sub.id))} missing, {len(set(sub.id) - set(test_ids))} unknown")
        d = pd.to_numeric(sub[TARGET], errors="coerce")
        if d.isna().any():
            errors.append(f"{d.isna().sum()} missing or non-numeric predictions")
        elif not np.isfinite(d).all():
            errors.append("infinite predictions")
        else:
            if (d < 0).any():
                warnings.append(f"{(d < 0).sum()} negative predictions: a discount is never below 0")
            if (d > 100).any():
                warnings.append(f"{(d > 100).sum()} predictions above 100: the discount is in percent of the asking price")
            if d.nunique() == 1:
                warnings.append("every prediction is the same value")
            mean = pd.read_csv(DATA / "train.csv", usecols=[TARGET])[TARGET].mean()
            print(f"{len(sub):,} rows; mean prediction {d.mean():.2f} (train mean {mean:.2f}); min {d.min():.2f}, max {d.max():.2f}")

    for w in warnings:
        print(f"WARNING: {w}")
    for e in errors:
        print(f"ERROR: {e}")
    if errors:
        sys.exit(1)
    print(f"OK: {path} is a valid submission")
    return sub


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    check(sys.argv[1])
