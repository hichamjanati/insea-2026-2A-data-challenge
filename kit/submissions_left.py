"""How many submissions your team has left today, as Kaggle counts them.

Usage: uv run python -m kit.submissions_left
The daily count resets at midnight UTC. Needs a logged-in Kaggle CLI and the competition rules accepted.
"""
import re, subprocess, sys
from kit.data import competition


def remaining_today() -> int | None:
    """Submissions left for the rest of today (UTC); None when Kaggle could not be asked."""
    r = subprocess.run(["kaggle", "competitions", "submission-limits", competition()], capture_output=True, text=True)
    m = re.search(r"Remaining today:\s*(\d+)", r.stdout)
    if r.returncode != 0 or m is None:
        print((r.stdout + r.stderr).strip())
        return None
    print(r.stdout.strip())
    return int(m.group(1))


if __name__ == "__main__":
    if remaining_today() is None:
        sys.exit("could not read the submission limits: are you logged in (uv run kaggle auth login), "
                 "did you accept the rules, and are you in a team on the competition page?")
    print("(the daily count resets at midnight UTC)")
