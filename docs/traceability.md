# Requirement Traceability — starter
| Requirement | Implementation / evidence | Report section | Status |
|---|---|---|---|
| Bronze/Silver/Gold | `pipeline/spark_bronze_silver_gold.py` | §3–4 | Needs local run and schema validation |
| Synthetic generator | `generator/generate_synthetic.py` | §4 | Starter only; confirm required scale/outbreak ground truth |
| Outbreak detection | `analytics/outbreak_detection.py` | §5.1–6 | Baseline only; backtest required |
| Forecasting | `analytics/forecasting.py` | §5.2–6 | Seasonal-naive baseline; second model/backtest required |
| Allocation | `analytics/resource_optimizer.py` | §5.3–6 | Heuristic starter; population baseline comparison required |
| Preparedness calendar | `analytics/preparedness_calendar.py` | §5.4 | Starter; review with domain context |
| D3 coordinated dashboard | `dashboard-d3/` | §7 | Needs local run and data schema check |
| Quality/privacy/lineage | Existing quality code + pipeline additions | §4 | Add missing rules, quarantine and privacy tests |
| Scaling + Spark optimisation | `docs/scaling_template.csv` | §6 | Must be measured |
| Proposal | `docs/proposal.md` | §1–3 | Replace placeholders and approve as team |
| Policy brief | `docs/policy_brief.md` | Appendix A | Format to exactly two pages |
| Contribution matrix | `docs/contribution_matrix.md` | Appendix B | Team must sign |
| Video | `docs/video_script.md` | README | Must record and host |
