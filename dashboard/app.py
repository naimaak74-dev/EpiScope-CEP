
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(r"E:\episcope")
GOLD_FILE = ROOT / "data" / "gold" / "daily_disease_summary.csv"
SILVER_FILE = ROOT / "data" / "silver" / "clean_encounters.csv"

st.set_page_config(
    page_title="EpiScope Health Dashboard",
    page_icon="🩺",
    layout="wide"
)

st.title("EpiScope: Public Health Dashboard")
st.caption("Explore generated health encounter data and daily disease counts.")

if not GOLD_FILE.exists():
    st.warning(
        "Daily disease summary was not found. "
        "Run build_pipeline.py and check its output first."
    )
elif not SILVER_FILE.exists():
    st.warning("Clean encounter data was not found. Run the pipeline first.")
else:
    summary = pd.read_csv(GOLD_FILE)
    encounters = pd.read_csv(SILVER_FILE)

    st.subheader("Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total encounters", f"{len(encounters):,}")
    col2.metric("Disease categories", summary["disease"].nunique())
    col3.metric("Summary records", f"{len(summary):,}")

    st.subheader("Daily disease cases")

    if not summary.empty:
        summary["date"] = pd.to_datetime(summary["date"], errors="coerce")
        summary = summary.dropna(subset=["date"])

        diseases = sorted(summary["disease"].dropna().unique().tolist())
        selected = st.multiselect(
            "Select disease",
            diseases,
            default=diseases[:min(3, len(diseases))]
        )

        filtered = summary[summary["disease"].isin(selected)]

        if not filtered.empty:
            chart_data = filtered.pivot_table(
                index="date",
                columns="disease",
                values="case_count",
                aggfunc="sum",
                fill_value=0
            ).sort_index()

            st.line_chart(chart_data)
            st.dataframe(filtered, use_container_width=True)
        else:
            st.info("Select at least one disease to display the chart.")
    else:
        st.info("The daily summary file contains no records.")

    st.subheader("Encounter data preview")
    st.dataframe(encounters.head(100), use_container_width=True)
