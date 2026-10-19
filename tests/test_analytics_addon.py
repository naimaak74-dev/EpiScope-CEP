import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analytics"))
import pandas as pd
from outbreak_detection import detect
from resource_optimizer import allocate
from preparedness_calendar import make_calendar

def sample():
    return pd.DataFrame({
        "date":pd.date_range("2025-01-01",periods=12),
        "cases":[10,11,9,10,12,11,10,11,10,12,50,13],
        "district":["D1"]*12,"disease":["Dengue"]*12
    })

def test_detector_has_alert_column():
    out=detect(sample())
    assert "alert" in out.columns
    assert out["alert"].dtype == bool

def test_allocator_total_units_and_equity():
    df=sample()
    out=allocate(df,total_units=100,min_share=0.01)
    assert int(out["allocated_units"].sum()) == 100
    assert (out["allocated_units"] >= 0).all()

def test_calendar_has_month_and_action():
    out=make_calendar(sample())
    assert {"month","month_name","preparedness_action"} <= set(out.columns)
