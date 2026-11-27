# Portfolio Credit Risk: Management Information Pack

**Reporting basis:** live consumer loan book at the data snapshot (March 2019, the latest payment date in the file)
**Portfolio:** 907,904 active loans, $9.51bn exposure at default
**Prepared by:** Oluwagbade Odimayo

This pack summarises the credit health of the book for a risk committee: an early-warning dashboard, vintage performance, arrears, application-score drift, and concentration. It is built from real loan data, with every figure reproducible from `analysis.py` and recorded in `results.json`.

**Definitions.** Default is dated at a charged-off loan's last payment plus four months (about 90 days past due). A vintage's 12-month default rate is the share of its loans that defaulted within 12 months of issue, counting only loans whose full 12 months (plus a six-month allowance for charge-off to be recorded) had passed by the reporting date. Arrears buckets follow Lending Club's loan status; its "Default" status means 121+ days past due.

---

## 1. Overall assessment: AMBER

The book is currently performing on a cash basis: arrears are low and the portfolio is geographically well-diversified. Two forward-looking signals warrant attention. Origination quality has been deteriorating, with the 12-month default rate rising across recent vintages even at a constant grade mix, and the newest applicants' risk profile has drifted far enough to merit a scorecard review. Neither is a present loss event; both are leading indicators that a committee should track.

### Early-warning dashboard

| Indicator | Current reading | Status |
|---|---|---|
| Vintage 12-month default trend | 4.0% on the 2016 vintage (latest fully observed), up from 2.7% on 2013; 4.3% at 2013 grade mix | RED |
| Live-book delinquency (16+ days past due) | 3.1% of active EAD | GREEN |
| Arrears 31+ days past due | 2.6% of active EAD | GREEN |
| Application-score drift (PSI) | 0.15, 2018 vintage versus 2013-14 | AMBER |
| Geographic concentration (HHI) | 0.051, top-5 states 41% | GREEN |
| Product concentration (largest purpose) | 58% of EAD | AMBER |

---

## 2. Vintage performance: RED

The clearest warning is in origination quality. The share of each vintage defaulting within 12 months of issue has risen from 2.7% on the 2013 vintage to 3.4% on 2015 and 4.0% on 2016, about 37% above the 2012-13 average (the RED trigger is 25%). Restating every vintage at the 2013 grade mix makes the rise slightly larger (2.7% to 4.3%), so it is not explained by lending more in riskier grades: loans of the same grade are defaulting more. The cohort curves agree: by 24 months on book, 11.9% of the 2016 vintage had defaulted against 8.8% of 2013. The partly observed 2017 vintage (early-2017 issues only) reads 3.8%.

This pattern is consistent with either a loosening of underwriting standards within grades or pressure on more recent borrowers. It is the single item most worth a committee's attention, because it feeds directly into future impairment.

*Recommendation: commission a thematic review of 2015 to 2016 underwriting against the credit policy, and confirm the ECL model's forward-looking assumptions reflect the rising vintage trend rather than the through-the-cycle average.*

## 3. Arrears: GREEN

The live book is currently sound. Of $9.51bn active exposure, 3.1% is 16 or more days past due and 2.6% is 31 or more days past due (the 31-120 day and 121+ day buckets). The bulk of exposure is current. This is a point-in-time strength, and it should be read alongside the vintage signal above: the back book is performing, while the more recent front book is the source of forward risk.

## 4. Application-score drift: AMBER

A PD model fitted on loans issued up to 2014 scores every issued loan, and each vintage's score distribution is compared with 2013-14. The Population Stability Index stays low through 2016 (0.03) and 2017 (0.08) and reaches 0.15 on the 2018 vintage, inside the "moderate shift" band (0.10 to 0.25). Separately, loans in the same PD band defaulted more often in 2016-17 than in 2013-14, in every band (figure 7), which matches the independent validation's finding that the scorecard under-predicts default on recent vintages. The applicant mix is starting to move, and the score-to-default relationship has already moved.

*Recommendation: bring forward a recalibration review of the scorecard, and add a quarterly calibration check (predicted versus observed default) to monitoring so level drift is caught alongside population drift.*

## 5. Concentration: GREEN geography, AMBER product

Geographic concentration is low. The state-level Herfindahl-Hirschman Index is 0.051, well within a diversified range, with the top five states accounting for 41% of exposure. Product concentration is higher: the largest single loan purpose represents 58% of exposure, which is worth monitoring as a single-driver dependency even though it is typical of this asset class.

*Recommendation: set a product-concentration appetite limit and monitor it; no geographic action required.*

## 6. Watch items and actions

| # | Item | Status | Action | 
|---|---|---|---|
| 1 | Rising 12-month default on recent vintages | RED | Thematic review of 2015 to 2016 underwriting; confirm ECL forward assumptions |
| 2 | Application-score drift (PSI 0.15 on 2018) and stale calibration | AMBER | Bring forward scorecard recalibration; add quarterly calibration check |
| 3 | Product concentration at 58% of EAD | AMBER | Set and monitor a product-concentration limit |
| 4 | Arrears, geographic spread | GREEN | Continue routine monitoring |

---

## 7. A note on large exposures

This is a granular consumer book, so there are no single-name large exposures; the concentration analysis above is the appropriate lens. In an auto or captive-finance setting the same pack would add daily monitoring of single-counterparty large exposures on the dealer and wholesale (floorplan) side, against the large-exposure limits, which is a natural extension of the concentration monitoring shown here.

## 8. Caveats

The data is US unsecured consumer lending used to demonstrate the monitoring framework; the metrics and the dashboard transfer directly to an auto book. Default timing is approximated from the last payment date (plus four months), because the file has no delinquency history, so roll rates between buckets are not available. Each vintage's 12-month rate uses only loans whose full window had passed, and the 2017 vintage is shown as partly observed. Application-score drift is measured on origination cohorts as a model-monitoring proxy. The RAG limits are illustrative, not a calibrated risk appetite. An earlier version of this pack reported 12-month default of 4.7% to 6.8% and PSI of 0.13. Those dated each default at the last payment rather than about 90 days past due (so a loan that stopped paying in month 12 counted as a month-12 default, four months early), and scored only finished loans for PSI. They are superseded (see `CHANGES.md`).

*Reproduce all metrics and figures with `python build_dataset.py` then `python analysis.py` (see the README).*
