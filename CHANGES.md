# Changes

## Corrected default dating, observable windows and drift population (Nov 2026)

**Why.** Three problems in the earlier version:
1. **Default dated too early.** A charged-off loan's default month was its last payment month. A borrower who stops paying is about 90 days past due roughly four months later, so the 12-month default rate counted defaults that happened up to month 16.
2. **Unobservable loans counted.** The 12-month rate for recent vintages included loans issued too late for their 12 months to have passed by the snapshot.
3. **Drift measured on finished loans only.** The PSI population was the finished-loans table, so recent vintages (where mostly early defaults and early repayments had finished) looked like drift. PSI needs only application data, so every issued loan should be scored.
It also labelled the 31+ days past due share "impaired", which in IFRS 9 terms means credit-impaired (Stage 3); it is now called arrears.

**What changed.**
- `lending_club.py` (new, shared with the other credit projects) dates default at last payment plus four months, records the snapshot (March 2019) and computes observable outcome windows.
- `analysis.py`: 12-month default uses only loans whose window (plus a six-month charge-off allowance) had passed; partly observable vintages are marked; each vintage is also restated at the 2013 grade mix. The drift model is trained on loans issued up to 2014 with a 24-month outcome and scores all 2.26M issued loans. Arrears labels now follow Lending Club's status definitions.
- `analysis.py` is written in notebook cell format; `make_notebook.py` rebuilds and executes the notebook from it.
- README and MI_PACK.md updated; `results.json` holds every quoted number.

**Numbers.**

| | Before | After |
|---|---|---|
| 12-month default, 2013 vintage | 4.7% | 2.7% |
| 12-month default, 2016 vintage | 6.8% | 4.0% (4.3% at 2013 grade mix) |
| Vintage trend RAG | RED | RED (37% above 2012-13 average) |
| PSI, 2018 vintage vs 2013-14 | 0.13 (finished loans) | 0.15 (all issued loans) |
| Delinquency 16+ dpd | 3.1% ("delinquency rate") | 3.1% |
| 31+ dpd share | 2.6% ("impaired") | 2.6% ("arrears 31+ dpd") |
| Active book | 907,904 loans, $9.51bn | unchanged |

The overall assessment (AMBER, with the vintage trend RED) is unchanged. The deterioration is smaller in absolute terms than previously reported but persists after holding the grade mix constant.
