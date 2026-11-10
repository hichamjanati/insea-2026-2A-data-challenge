"""Download the competition data into data/ with the Kaggle API.

Needs a logged-in Kaggle CLI (uv run kaggle auth login) and the competition rules accepted on the website.
Usage: uv run python -m kit.download_data
"""
import subprocess, sys, zipfile
from kit.data import DATA, competition

CSVS = ["train.csv", "test.csv", "sample_submission.csv"]

DATA.mkdir(exist_ok=True)
if all((DATA / f).exists() for f in CSVS):
    print(f"data/ already populated ({DATA}); delete it to download again"); sys.exit(0)

cmd = ["kaggle", "competitions", "download", "-c", competition(), "-p", str(DATA)]
print(" ".join(cmd))
if subprocess.run(cmd).returncode != 0:
    sys.exit("download failed: are you logged in (uv run kaggle auth login), and did you accept the rules on the competition page?")

# the API delivers one archive with every competition file
for z in sorted(DATA.glob("*.zip")):
    print(f"extracting {z.name}")
    with zipfile.ZipFile(z) as zf:
        zf.extractall(DATA)
    z.unlink()

missing = [f for f in CSVS if not (DATA / f).exists()]
if missing:
    sys.exit(f"something is missing: {missing}; look at the content of data/")
print(f"files: {', '.join(CSVS)}\ndone")
