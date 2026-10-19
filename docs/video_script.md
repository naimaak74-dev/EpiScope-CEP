# Video Presentation Plan (15–20 minutes)

**Before recording:** use the final `v1.0` code, readable 1080p screen recording, show real terminal output, and ensure the public link works without sign-in. Each of the three members must speak for at least four minutes and show their name.

- **00:00–02:00 — Problem and stakeholders:** explain the case, C1–C5 conflicts, and why synthetic data are labelled.
- **02:00–05:00 — Architecture:** show repository folders and Bronze → Silver → Gold flow.
- **05:00–08:00 — Pipeline run:** run a clean pipeline, ingest one incremental day, rerun it and show that no duplicate rows were introduced. Show one quarantined invalid row and its reason code.
- **08:00–11:00 — Analytics:** show outbreak alerts, forecasting vs. seasonal-naive baseline, MAE/interval coverage, allocation vs. population-proportional baseline, and seasonal calendar.
- **11:00–15:00 — D3 dashboard:** demonstrate all five views and linked filtering; explain count suppression, uncertainty and freshness.
- **15:00–18:00 — Evaluation and ethics:** show actual scaling table and two Spark optimisation comparisons; explain limitations and privacy.
- **18:00–20:00 — Recommendations and close:** top recommendations, future work and member contributions.

Add actual timestamps after editing the video. Do not claim a step succeeded unless it is shown and verified.
