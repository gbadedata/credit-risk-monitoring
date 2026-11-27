"""Build the modelling table used by the affordability, scorecard and monitoring repos.

Every accepted loan is kept, finished or not, with fixed-window outcomes (see lending_club.py):
  obs_12 / bad_12  default within 12 months of issue, and whether that is observable
  obs_24 / bad_24  default within 24 months of issue, and whether that is observable
Earlier versions kept only finished loans, which over-represents defaults in recent vintages.

Usage:  python build_dataset.py [path/to/accepted_2007_to_2018Q4.csv.gz]
        (or set LENDING_CLUB_CSV). Writes data/lending_affordability.parquet.
"""
import os
import sys
import warnings

import numpy as np
import pandas as pd

import lending_club as lc

warnings.filterwarnings("ignore")
RAW = sys.argv[1] if len(sys.argv) > 1 else lc.DEFAULT_RAW
OUT = os.environ.get("AFFORDABILITY_PARQUET", "data/lending_affordability.parquet")

USECOLS = ["annual_inc", "dti", "installment", "loan_amnt", "purpose", "home_ownership", "emp_length",
           "verification_status", "application_type", "annual_inc_joint", "dti_joint", "fico_range_low",
           "fico_range_high", "delinq_2yrs", "inq_last_6mths", "revol_util", "open_acc", "pub_rec",
           "total_acc", "earliest_cr_line", "grade", "out_prncp"]
EMP = {"< 1 year": 0, "1 year": 1, "2 years": 2, "3 years": 3, "4 years": 4, "5 years": 5,
       "6 years": 6, "7 years": 7, "8 years": 8, "9 years": 9, "10+ years": 10}

df = lc.load(RAW, usecols=USECOLS)
print(lc.describe(df))
snapshot_m = df.attrs["snapshot_m"]

joint = df["application_type"] == "Joint App"
num = lambda c: pd.to_numeric(df[c], errors="coerce")
df["annual_inc_eff"] = np.where(joint & df["annual_inc_joint"].notna(), num("annual_inc_joint"), num("annual_inc"))
df["dti_eff"] = np.where(joint & df["dti_joint"].notna(), num("dti_joint"), num("dti"))
df["fico"] = (num("fico_range_low") + num("fico_range_high")) / 2
df["payment_to_income"] = num("installment") * 12 / df["annual_inc_eff"]
df["loan_to_income"] = num("loan_amnt") / df["annual_inc_eff"]
df["emp_length_num"] = df["emp_length"].map(EMP)
df["revol_util"] = pd.to_numeric(df["revol_util"].astype(str).str.replace("%", ""), errors="coerce")
ecl_m = lc.month_index(df["earliest_cr_line"])
df["credit_history_yrs"] = (df["issue_m"] - ecl_m) / 12
for w in (12, 24):
    obs, bad = lc.window_outcome(df, w)
    df[f"obs_{w}"] = obs
    df[f"bad_{w}"] = bad
df["default"] = df["charged_off"].astype("int8")          # ever charged off by the snapshot (legacy target)

before = len(df)
df = df[(df["annual_inc_eff"] >= 2000) & df["annual_inc_eff"].notna()].copy()
df["payment_to_income"] = df["payment_to_income"].clip(0, 2)
df["loan_to_income"] = df["loan_to_income"].clip(0, 5)
df["dti_eff"] = df["dti_eff"].clip(0, 100)
df["revol_util"] = df["revol_util"].clip(0, 200)
print(f"Dropped {before - len(df):,} rows with missing or implausible income; {len(df):,} loans kept")

OUTCOLS = ["issue_m", "issue_year", "loan_status", "grade", "completed", "charged_off", "default",
           "obs_12", "bad_12", "obs_24", "bad_24", "annual_inc_eff", "dti_eff", "payment_to_income",
           "loan_to_income", "installment", "loan_amnt", "term_months", "emp_length_num", "home_ownership",
           "purpose", "verification_status", "fico", "delinq_2yrs", "inq_last_6mths", "revol_util",
           "open_acc", "pub_rec", "total_acc", "credit_history_yrs"]
out = df[OUTCOLS].copy()
for c in out.select_dtypes("float64").columns:
    if c not in ("issue_m",):
        out[c] = out[c].astype("float32")
for c in ["loan_status", "grade", "home_ownership", "purpose", "verification_status"]:
    out[c] = out[c].astype("category")
out.attrs = {"snapshot_m": float(snapshot_m)}
os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
out.to_parquet(OUT, index=False)
o24 = out["obs_24"]
print(f"Saved {OUT}: {len(out):,} loans | snapshot {lc.month_label(snapshot_m)} | "
      f"24-month window observable for {int(o24.sum()):,} loans issued up to "
      f"{lc.month_label(out.loc[o24, 'issue_m'].max())}, bad rate {out.loc[o24, 'bad_24'].mean():.1%}")
