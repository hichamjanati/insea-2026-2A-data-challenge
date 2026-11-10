# INSEA 2026 FSML data challenge: starter kit

How much will the buyer negotiate? Each row is a used car sold on a Moroccan marketplace: the car, the asking price,
the seller, where and when the ad was posted. You predict the discount the buyer obtained, in percent of the asking
price; submissions are scored with the mean absolute error (MAE).
Competition page, data description and rules: [https://www.kaggle.com/competitions/predictive-ml-2-a-2026](https://www.kaggle.com/competitions/predictive-ml-2-a-2026)

This repository is a starting point: an environment, the data download, a weak baseline, a submission checker, a
command that tells you how many submissions you have left, and the upload command. Everything in it is meant to be
replaced by your own work.

## 1. Create your team repository

1. Click **Use this template** (top right), then **Create a new repository**. Make it **private** and give it your team's name.
  Do not fork: a fork of a public repository cannot be private.
2. In your repository, **Settings > Collaborators**, add the instructor.
3. Clone your repository and work in it. Everything below runs from its root folder.



## 2. Environment

The kit uses [uv](https://docs.astral.sh/uv/) for the environment and [just](https://just.systems/) to run its commands. Follow the instructions for your system.

### Windows

Open **PowerShell** (Start menu, type "PowerShell"). Install uv:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Close PowerShell, open a new one, go to your repository folder, then install just and create the environment:

```powershell
uv tool install rust-just
just setup
```

If PowerShell says `just` is not recognized, run `uv tool update-shell`, then close and reopen PowerShell.

### macOS

Open **Terminal** (Applications > Utilities). Install uv:

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Close Terminal, open a new one, go to your repository folder, then install just and create the environment:

```sh
uv tool install rust-just
just setup
```

If the terminal says `just: command not found`, run `uv tool update-shell`, then close and reopen the terminal.

### Linux

Open a terminal. Install uv (if `curl` is missing, use `wget -qO- https://astral.sh/uv/install.sh | sh`):

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Close the terminal, open a new one, go to your repository folder, then install just and create the environment:

```sh
uv tool install rust-just
just setup
```

If the terminal says `just: command not found`, run `uv tool update-shell`, then close and reopen the terminal.

### On all systems

`just setup` creates `.venv` with numpy, scipy, pandas, scikit-learn, xgboost, lightgbm, matplotlib, kaggle and
jupyterlab. From here on, every command in this README is the same on Windows, macOS and Linux.

Add packages with `uv add <package>` (for example `uv add seaborn`); `pyproject.toml` records them, so the instructor
can rebuild your environment with `uv sync`. Run anything with `uv run python ...` or `uv run jupyter lab`.

## 3. Kaggle access

Each team member needs a Kaggle account. Log the command line in, once:

```sh
uv run kaggle auth login            # opens a browser, recommended
```

And login on the browser. Your credential token will automatically be saved in your home folder ~/.kaggle: keep it private from both humans (and agents !). 

## 4. Join the competition

1. Open the **competition invitation link** shared by the host, while logged in to your Kaggle account.
2. Click **Join Competition** and **accept the rules**. Without this, every download and submission is refused.
3. Form your team on Kaggle: one member opens the **Team** tab of the competition and invites the others.

The rules on the competition page are the ones that apply.

## 5. From data to submission

Run `just` alone to list the commands. Each one is a single line in `justfile`.

### Step 1: get the data

```sh
just data
```

Downloads `train.csv`, `test.csv` and `sample_submission.csv` into `data/` (a few MB, gitignored). Run it once.

### Step 2: train a model

```sh
just train
```

This runs `kit/train.py`: it trains the baseline, prints its cross-validated MAE and writes the predictions for the
test ads to `submissions/baseline.csv`. Edit `kit/train.py`, write your own scripts, or work in notebooks
(`uv run jupyter lab`): what matters is that your repository reproduces your final submission.

### Step 3: check the submission file

```sh
just check submissions/baseline.csv
```

Validates the file the way Kaggle does, and warns about predictions that cannot be right. Use the path of your own
file.

### Step 4: see how many submissions you have left

```sh
just left
```

Asks Kaggle how many submissions your team has made today and in total, and how many are left today. The daily count
resets at midnight UTC.

### Step 5: submit

```sh
just submit submissions/baseline.csv "baseline: OLS on the table"
```

Checks the file again, shows how many submissions you have left, asks for confirmation, then uploads it with your
message. **Careful: you have one submission per day per team**, so make sure the file is the one you want before
typing `y`. On Windows, keep `$` out of the message: PowerShell would replace it.

Submission files are gitignored: keep the code that produced them instead.

## 6. What is in the kit


| file                      | role                                                                               |
| ------------------------- | ---------------------------------------------------------------------------------- |
| `kit/data.py`             | paths, the competition name, loaders for the tables                                |
| `kit/download_data.py`    | `just data`                                                                        |
| `kit/train.py`            | the baseline: OLS with default settings on a few table columns, complete rows only |
| `kit/check_submission.py` | the format checks Kaggle applies, plus warnings on predictions that cannot be right |
| `kit/submissions_left.py` | `just left`                                                                        |
| `kit/submit.py`           | `just submit`                                                                      |
| `REPORT.md`               | the report skeleton to fill in for the oral evaluation                             |
