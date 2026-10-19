# EpiScope Proposal (Draft — team review required)

## Problem and stakeholders
EpiScope is a teaching-case decision-support platform for exploring district-level disease surveillance, short-term forecasting, and supply planning. Primary stakeholders are national health decision-makers, divisional teams, district health officers, facility reporting teams, and the public. All synthetic data must be labelled as synthetic; public data must be cited.

## Planned architecture
1. **Bronze:** immutable source drops with batch IDs and source metadata.
2. **Silver:** cleaned, standardised records; deduplication; salted patient identifiers; rejected records sent to quarantine with reason codes.
3. **Gold:** daily district/disease aggregates in Parquet/CSV for detection, forecasting, allocation, and dashboard views.
4. **Analytics:** a baseline outbreak detector, seasonal-naive forecasting comparison, constrained resource allocation, and preparedness calendar.
5. **Serving/dashboard:** D3.js coordinated views using aggregate data only.
6. **Evaluation:** quality-rule results, alert sensitivity/false-alert rate/detection delay, forecast MAE and 80% interval coverage, allocation comparison to a population-proportional baseline, and scalability measurements.

## Conflicts C1–C5 (draft)
- **C1 Sensitivity vs. false alarms:** tune thresholds on held-out synthetic outbreak labels and report both sensitivity and false-alert rate.
- **C2 Granularity vs. privacy:** show district aggregates only and suppress counts 1–4.
- **C3 Freshness vs. compute cost:** support incremental daily loads and compare full vs. incremental runtime.
- **C4 Efficiency vs. equity:** optimise estimated need while reserving a minimum share for every district.
- **C5 Model complexity vs. explainability:** use interpretable baselines first and report limitations.

## Methods (planned)
- Synthetic data generator with configurable scale and planted outbreak periods.
- Spark-based Bronze → Silver → Gold transformations, with Parquet output.
- At least 12 quality checks, quarantine reasons, batch lineage and hashed identifiers.
- CUSUM/EARS-style baseline detection; seasonal-naive forecasting baseline plus a second model if supported by data.
- Constrained allocation compared with a population-proportional baseline.
- Five linked D3 views: district map/overview, time series/forecast, seasonal heatmap, resource allocation, early-warning table.

## Risk register
| Risk | Impact | Mitigation |
|---|---|---|
| Synthetic data mistaken for real data | Invalid conclusions | Label every dataset and figure; document limitations |
| Missing or inconsistent source columns | Pipeline failure | Validate schemas and log rejected rows |
| Large generator overwhelms laptop | Long runtime/memory failure | Test scale factors incrementally; stream output in chunks |
| False outbreak alerts | Alert fatigue | Evaluate sensitivity and false alerts; human review |
| Privacy leakage from small counts | Patient inference | Suppress counts 1–4 and publish aggregates only |
| External data unavailable | Incomplete integration | Record source URL/date or explicitly mark limitation |
| Team contributions not traceable | Authorship concern | Each member commits their own work and signs contribution matrix |

## Roles (team must fill in)
- Member 1 / ID: [name, ID] — data generation and pipeline
- Member 2 / ID: [name, ID] — analytics and evaluation
- Member 3 / ID: [name, ID] — dashboard, testing, report/presentation

## Decisions still required
Choose two target diseases based on available data; add public source URLs and retrieval dates; confirm Spark/Java/Python versions; replace role placeholders; and review all methods with the full team.
