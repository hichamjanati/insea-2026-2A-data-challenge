"""Check a submission file, then upload it to Kaggle.

Usage: uv run python -m kit.submit submissions/<file>.csv "a short message describing the model"
You have 1 submission per day: the script shows what is left and asks for confirmation before uploading.
"""
import subprocess, sys
from kit.check_submission import check
from kit.data import competition
from kit.submissions_left import remaining_today

if len(sys.argv) != 3:
    sys.exit(__doc__)
path, message = sys.argv[1], sys.argv[2]
check(path)
left = remaining_today()
if left == 0:
    sys.exit("no submission left today: try again after midnight UTC")
answer = input(f"upload {path} to {competition()}? This uses one of today's submissions [y/N] ")
if answer.strip().lower() != "y":
    sys.exit("not uploaded")
cmd = ["kaggle", "competitions", "submit", "-c", competition(), "-f", path, "-m", message]
print(" ".join(cmd))
sys.exit(subprocess.run(cmd).returncode)
