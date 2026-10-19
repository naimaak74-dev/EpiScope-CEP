# Policy Brief: Using EpiScope for District Preparedness
**Audience:** Health-sector decision-makers  
**Status:** Draft for review — results must be replaced with measured project findings.

## What this tool is
EpiScope is a teaching-case decision-support prototype. It organises daily district-level disease counts, flags unusual changes, shows short-term baseline forecasts and suggests how a limited stock of supplies could be distributed. Synthetic data are not real case reports and must never be used to make real operational decisions.

## Three recommendations
1. **Review unusual increases with district teams before action.** An alert means the observed count differs from the selected baseline; it does not prove an outbreak. Check facility reporting completeness, recent changes in reporting, and local clinical evidence.
2. **Prepare supplies ahead of historically higher-risk periods.** Use the seasonal calendar as a planning prompt, then combine it with current stock, population, travel time, facility capacity and local knowledge.
3. **Keep allocation both needs-based and equitable.** Direct extra supplies toward higher estimated need while maintaining a minimum fair share for each district. Review the result with district officers before final approval.

## How to read the dashboard
- **District overview:** compare aggregate counts across districts; it is not a patient-level map.
- **Trend and forecast:** distinguish observed counts from forecasts and uncertainty ranges. Longer horizons are less certain.
- **Seasonal heatmap:** identify months with historically higher average counts.
- **Resource allocation:** compare the proposed distribution with the simple baseline. The proposal is a model output, not an automatic order.
- **Early-warning table:** review alerts with date, disease, district and threshold context.

## Confidence and limitations
Confidence depends on reporting completeness, historical data quality, and the assumptions in the detector and forecast. Late reports, duplicated records, changes in facility participation and unusual events can create misleading signals. Forecast intervals are approximate and should not be treated as guarantees. The prototype needs independent validation before operational use.

## Data protection
The dashboard should display aggregated data only. Suppress district/disease counts from 1 to 4, do not expose names or direct identifiers, and use hashed identifiers only for internal deduplication. A hash is not a substitute for access control or a lawful data-governance process.

## Expected impact
Potential benefits include earlier review of unusual changes, more structured seasonal preparation and transparent comparison of allocation options. Quantitative impact must be stated only after backtesting and evaluation against baselines.
