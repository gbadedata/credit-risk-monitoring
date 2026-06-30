# Portfolio Credit Risk: Management Information Pack

**Reporting basis:** live consumer loan book at the latest snapshot
**Portfolio:** 907,904 active loans, $9.51bn exposure at default
**Prepared by:** Oluwagbade Odimayo

This pack summarises the credit health of the book for a risk committee: an early-warning dashboard, vintage performance, delinquency and impairment, model drift, and concentration. It is built from real loan data, with every figure reproducible.

---

## 1. Overall assessment: AMBER

The book is currently performing on a cash basis: delinquency and impairment are low and the portfolio is geographically well-diversified. Two forward-looking signals warrant attention. Origination quality has been deteriorating, with the 12-month-on-book default rate rising across recent vintages, and the scorecard's population has drifted far enough to merit a recalibration review. Neither is a present loss event; both are leading indicators that a committee should track.

### Early-warning dashboard

| Indicator | Current reading | Status |
|---|---|---|
| Vintage 12-month default trend | 6.8% on the latest mature vintage, up from 4.7% | RED |
| Live-book delinquency rate | 3.1% of active EAD | GREEN |
| Impaired (30+ days past due) share | 2.6% of active EAD | GREEN |
| Scorecard population drift (PSI) | 0.13 versus baseline | AMBER |
| Geographic concentration (HHI) | 0.051, top-5 states 41% | GREEN |
| Product concentration (largest purpose) | 58% of EAD | AMBER |

---

## 2. Vintage performance: RED

The clearest warning is in origination quality. Tracking each origination cohort by months on book, the 12-month-on-book default rate has risen steadily from 4.7% on the 2013 vintage to 6.8% on the 2016 vintage, roughly a third higher than the early-vintage average. The cohort curves show the 2015 and 2016 vintages sitting consistently above the 2012 to 2014 cohorts at every point in their life.

This pattern is consistent with either a loosening of underwriting standards or macroeconomic pressure on more recent borrowers. It is the single item most worth a committee's attention, because it feeds directly into future impairment.

*Recommendation: commission a thematic review of 2015 to 2016 underwriting against the credit policy, and confirm the ECL model's forward-looking assumptions reflect the rising vintage trend rather than the through-the-cycle average.*

## 3. Delinquency and impairment: GREEN

The live book is currently sound. Of $9.51bn active exposure, 3.1% sits in delinquency and 2.6% is impaired at 30 or more days past due. The bulk of exposure is current. This is a point-in-time strength, and it should be read alongside the vintage signal above: the back book is performing, while the more recent front book is the source of forward risk.

## 4. Model performance: AMBER

The application scorecard's score distribution has drifted relative to its 2013 to 2014 development baseline, with the Population Stability Index reaching 0.13 on the most recent vintage, inside the "moderate shift" band (0.10 to 0.25). Read together with the separate finding that the scorecard under-predicts default on recent vintages, the implication is that the central tendency is becoming stale.

*Recommendation: bring forward a recalibration review of the scorecard, and add a quarterly calibration check (predicted versus observed default) to monitoring so level drift is caught alongside population drift.*

## 5. Concentration: GREEN geography, AMBER product

Geographic concentration is low. The state-level Herfindahl-Hirschman Index is 0.051, well within a diversified range, with the top five states accounting for 41% of exposure. Product concentration is higher: the largest single loan purpose represents 58% of exposure, which is worth monitoring as a single-driver dependency even though it is typical of this asset class.

*Recommendation: set a product-concentration appetite limit and monitor it; no geographic action required.*

## 6. Watch items and actions

| # | Item | Status | Action | 
|---|---|---|---|
| 1 | Rising 12-month default on recent vintages | RED | Thematic review of 2015 to 2016 underwriting; confirm ECL forward assumptions |
| 2 | Scorecard population drift (PSI 0.13) and stale calibration | AMBER | Bring forward scorecard recalibration; add quarterly calibration check |
| 3 | Product concentration at 58% of EAD | AMBER | Set and monitor a product-concentration limit |
| 4 | Delinquency, impairment, geographic spread | GREEN | Continue routine monitoring |

---

## 7. A note on large exposures

This is a granular consumer book, so there are no single-name large exposures; the concentration analysis above is the appropriate lens. In an auto or captive-finance setting the same pack would add daily monitoring of single-counterparty large exposures on the dealer and wholesale (floorplan) side, against the large-exposure limits, which is a natural extension of the concentration monitoring shown here.

## 8. Caveats

The data is US unsecured consumer lending used to demonstrate the monitoring framework; the metrics and the dashboard transfer directly to an auto book. Vintage default timing is approximated from the last payment date, the most recent vintage is partly observed (right-censored) and is read with that in mind, and the scorecard drift is measured on origination cohorts as a model-monitoring proxy.

*Reproduce all metrics and figures with `python analysis.py`.*
