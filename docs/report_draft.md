# EpiScope Technical Report — Draft Structure

> **Not submission-ready until completed with actual evidence.** Add group number, all member names/IDs, final repository URL, and shareable video link. Replace every bracketed placeholder. Do not invent performance results.

## Abstract
This project develops a teaching-case pipeline for district-level disease surveillance, short-term forecasting and resource planning. The implementation combines layered data processing, quality checks, aggregate analytics and a coordinated D3 dashboard. Results must be reported only after the team runs the tagged code and validates the generated outputs.

## 1. Introduction and problem analysis
Describe the decision problem, national/divisional/district stakeholders, and the need to balance early warning, false alarms, equity, freshness and privacy.

## 2. CEP attributes P1–P7 and conflicts C1–C5
Explain how the implementation addresses each attribute from the assignment. Include concrete design decisions and evidence; do not merely repeat definitions.

## 3. Architecture and design decisions
Insert architecture diagram. Explain Bronze/Silver/Gold, Spark, Parquet, incremental ingestion, serving layer, dashboard and alternatives considered.

## 4. Data generation, quality, lineage and privacy
Document generator schema, scale factor, outbreak injection, public data sources and retrieval dates. Report all quality rules, quarantine counts/reason codes, batch lineage, hashing method and suppression of counts 1–4.

## 5. Analytics methods
### 5.1 Outbreak detection
Explain selected detector and threshold. Compare against planted ground truth.
### 5.2 Forecasting
Evaluate at 1–4 week horizons. Compare at least two diseases and seasonal-naive baseline; report MAE and 80% interval coverage.
### 5.3 Resource allocation
Describe objective, constraints and equity floor. Compare with population-proportional allocation.
### 5.4 Preparedness calendar
Summarise seasonal risk windows and actions.

## 6. Evaluation
Report detection sensitivity, false-alert rate and detection delay; forecasting MAE and interval coverage; allocation metrics; scaling factors SF=0.25/0.5/1; hardware/software; runtime and output size; two Spark optimisations with before/after evidence. **Fill with measured results only.**

## 7. Dashboard design and usability
Describe all five views, linked interactions, uncertainty, freshness and small-count suppression. Include screenshots and brief usability findings from real testing.

## 8. Ethics, society and sustainability
Discuss synthetic/public-data labelling, privacy, equity, limitations of reporting, risks of alert fatigue, resource trade-offs and modest-infrastructure design.

## 9. Limitations and future work
State actual missing sources, modelling assumptions, scale limits, schema issues and deployment limitations.

## References
Cite the assignment, public data sources, methods papers and official health-data guidance used.

## Appendix A — Two-page policy brief
Use `docs/policy_brief.md`; expand/edit to exactly two pages in final report.

## Appendix B — Contribution matrix
Complete and sign `docs/contribution_matrix.md`.

## Appendix C — Individual reflections
Each member writes their own half-page reflection in their own words.
