# EpiScope: Public Health Dashboard

## Project Overview
EpiScope is a public health data project that processes health encounter data and displays daily disease summaries in a dashboard.

## Main Features
- Processes encounter data.
- Creates cleaned data in the Silver layer.
- Creates daily disease summaries in the Gold layer.
- Generates a data quality report.
- Displays disease data using a Streamlit dashboard.
- Runs basic automated tests using pytest.

## Technologies Used
- Python
- Pandas
- Streamlit
- Pytest
- CSV data files

## How to Run

1. Activate the virtual environment:
   .\.venv\Scripts\Activate.ps1

2. Run the data pipeline:
   python .\build_pipeline.py

3. Generate the data quality report:
   python .\quality_check.py

4. Run the automated tests:
   python -m pytest .\tests -v

5. Start the dashboard:
   python -m streamlit run .\dashboard\app.py

## Output Files
- data/silver/clean_encounters.csv
- data/gold/daily_disease_summary.csv
- reports/data_quality_report.csv
