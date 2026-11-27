"""Shared Lending Club loader, used identically by the credit-risk portfolio repos.

Why this exists
---------------
The Lending Club "accepted 2007-2018Q4" file is a single snapshot. Loans issued in 2016-2018
had mostly not finished by then, and the ones that had finished are mostly early defaults and
early repayments. Training or validating only on finished ("completed") loans therefore
over-represents defaults in recent vintages, which distorts calibration, drift (PSI) and
out-of-time results.

The fix used here is the standard one in credit scoring: a fixed outcome window. A loan is
"bad" if it charged off with its default dated within `months` of issue, and it is only used
when that whole window, plus time for a defaulted loan to be charged off, had passed by the
snapshot. Active and finished loans are treated alike, so no vintage is selected by outcome.

Default timing
--------------
The file has no default or charge-off date. Default is dated `DEFAULT_LAG_MONTHS` after the
last payment received (three missed monthly payments, about 90 days past due), or after issue
for loans that never paid. Lending Club charged loans off at about 150 days past due, so a
loan is treated as observable only if `SETTLE_MONTHS` more had passed by the snapshot. Recovery
payments made after charge-off can move last_pymnt_d later for some loans, which would date
their default later than it happened; this is a known limitation of the proxy.

Data
----
Kaggle dataset "wordsforthewise/lending-club", file accepted_2007_to_2018Q4.csv.gz. Point to
it with the LENDING_CLUB_CSV environment variable or pass the path explicitly; the default is
data/raw/accepted_2007_to_2018Q4.csv.gz. The file is not redistributed in these repos.
"""
from __future__ import annotations

import os

import numpy as np
import pandas as pd

DEFAULT_RAW = os.environ.get("LENDING_CLUB_CSV", "data/raw/accepted_2007_to_2018Q4.csv.gz")

CHARGED = {"Charged Off", "Default", "Does not meet the credit policy. Status:Charged Off"}
PAID = {"Fully Paid", "Does not meet the credit policy. Status:Fully Paid"}
ACTIVE_STATUSES = {"Current", "In Grace Period", "Late (16-30 days)", "Late (31-120 days)", "Default"}

DEFAULT_LAG_MONTHS = 4   # last payment -> about 90 days past due
SETTLE_MONTHS = 6        # time for a 90+ dpd loan to be charged off (~150 dpd) before the snapshot

BASE_COLS = ["issue_d", "loan_status", "last_pymnt_d", "term"]


def month_index(s: pd.Series) -> pd.Series:
    """'Dec-2015' -> 2015*12 + 11. Missing or malformed values become NaN."""
    d = pd.to_datetime(s, format="%b-%Y", errors="coerce")
    return (d.dt.year * 12 + d.dt.month - 1).astype("float64")


def month_label(m: float) -> str:
    m = int(m)
    return pd.Timestamp(year=m // 12, month=m % 12 + 1, day=1).strftime("%b %Y")


def load(raw: str | os.PathLike | None = None, usecols=(), chunksize: int = 300_000) -> pd.DataFrame:
    """Read the loan tape with the timing fields every repo needs.

    Adds: issue_m, issue_year, last_pymnt_m, term_months, charged_off, completed, active,
    default_m (dated default for charged-off loans, NaN otherwise) and mob_default
    (months on book at default). The snapshot month is stored in df.attrs["snapshot_m"].
    """
    raw = raw or DEFAULT_RAW
    if not os.path.exists(raw):
        raise FileNotFoundError(
            f"Lending Club file not found: {raw}\n"
            "Download accepted_2007_to_2018Q4.csv.gz from Kaggle (wordsforthewise/lending-club) "
            "and set LENDING_CLUB_CSV to its path.")
    cols = list(dict.fromkeys(BASE_COLS + list(usecols)))
    parts = []
    for ch in pd.read_csv(raw, usecols=cols, chunksize=chunksize, low_memory=False):
        ch = ch[ch["loan_status"].notna() & ch["issue_d"].notna()].copy()
        ch["issue_m"] = month_index(ch["issue_d"])
        ch["last_pymnt_m"] = month_index(ch["last_pymnt_d"])
        ch["term_months"] = ch["term"].astype(str).str.extract(r"(\d+)", expand=False).astype("float64")
        parts.append(ch)
    df = pd.concat(parts, ignore_index=True)
    df = df[df["issue_m"].notna()].reset_index(drop=True)
    df["issue_year"] = (df["issue_m"] // 12).astype("float64")

    snapshot_m = float(np.nanmax(df["last_pymnt_m"]))
    df.attrs["snapshot_m"] = snapshot_m

    df["charged_off"] = df["loan_status"].isin(CHARGED)
    df["completed"] = df["loan_status"].isin(CHARGED | PAID)
    df["active"] = df["loan_status"].isin(ACTIVE_STATUSES)
    if "out_prncp" in df.columns:
        df["active"] &= pd.to_numeric(df["out_prncp"], errors="coerce").fillna(0) > 0
    anchor = df["last_pymnt_m"].where(df["last_pymnt_m"].notna(), df["issue_m"])
    df["default_m"] = np.where(df["charged_off"], anchor + DEFAULT_LAG_MONTHS, np.nan)
    df["mob_default"] = df["default_m"] - df["issue_m"]
    return df


def window_outcome(df: pd.DataFrame, months: int):
    """(observable, bad) for a fixed outcome window of `months` from issue.

    observable: the whole window plus SETTLE_MONTHS had passed by the snapshot.
    bad: charged off, with default dated within the window.
    """
    snapshot_m = df.attrs["snapshot_m"]
    observable = (df["issue_m"] + months + SETTLE_MONTHS) <= snapshot_m
    bad = (df["charged_off"] & (df["mob_default"] <= months)).astype("int8")
    return observable, bad


def describe(df: pd.DataFrame) -> str:
    s = df.attrs["snapshot_m"]
    return (f"{len(df):,} loans issued {month_label(df['issue_m'].min())} - {month_label(df['issue_m'].max())}; "
            f"snapshot (latest payment in file) {month_label(s)}")
