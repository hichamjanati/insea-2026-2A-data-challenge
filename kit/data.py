"""Paths, competition constants and loaders shared by the scripts."""
from pathlib import Path
import sys
import pandas as pd

COMPETITION = "predictive-ml-2-a-2026"     # the end of the competition URL, kaggle.com/competitions/<slug>
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SUBMISSIONS = ROOT / "submissions"

TARGET = "discount"
N_TEST = 3_000


def competition() -> str:
    """The competition slug; stops with a clear message while it is not set."""
    if COMPETITION.startswith("TODO"):
        sys.exit("the competition name is not set: put the end of the competition URL in COMPETITION, in kit/data.py")
    return COMPETITION


def load_train() -> pd.DataFrame:
    return pd.read_csv(DATA / "train.csv")


def load_test() -> pd.DataFrame:
    return pd.read_csv(DATA / "test.csv")
