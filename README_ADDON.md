# EpiScope-CEP: Remaining Work Add-on

This add-on is designed to be copied into the existing `E:\episcope` project. It does not replace existing files automatically.

## Important
- Generated records are synthetic. Do not present them as real Bangladesh surveillance data.
- The analytics use flexible column detection, but you must verify the actual CSV column names and validate outputs before submission.
- The D3 dashboard reads `data/gold/daily_disease_summary.csv` from the project root. If your file has different columns, adjust `dashboard-d3/app.js`.
- The generator defaults to a small development dataset. Do not generate 25 million rows on a low-memory laptop without testing smaller scales first.

## Copy into the project
Extract the ZIP, then copy the folders/files inside `EpiScope_remaining_work` into `E:\episcope`. Merge folders; do not delete your existing project files.

## Run analytics
From PowerShell:
```powershell
cd E:\episcope
python -m pip install -r requirements-addon.txt
python analytics\outbreak_detection.py --input data\gold\daily_disease_summary.csv --output reports\outbreak_alerts.csv
python analytics\forecasting.py --input data\gold\daily_disease_summary.csv --output reports\forecast.csv
python analytics\resource_optimizer.py --input data\gold\daily_disease_summary.csv --output reports\resource_allocation.csv
python analytics\preparedness_calendar.py --input data\gold\daily_disease_summary.csv --output reports\preparedness_calendar.csv
```
Check each output file and confirm the columns and values make sense.

## Run D3 dashboard
```powershell
cd E:\episcope
python -m http.server 8000
```
Open `http://localhost:8000/dashboard-d3/` in a browser. The dashboard expects the Gold CSV at `data/gold/daily_disease_summary.csv`.

## Run tests
```powershell
python -m pytest tests -v
```
Some tests may need adjustment to your actual schema. Record actual test output in the report.

## Still requires real project/team actions
- Verify 25-million-row synthetic generator requirement and runtime/memory before claiming it is satisfied.
- Obtain and cite public district boundary, population and weather data, or clearly mark missing sources.
- Run Spark pipeline and capture actual Spark UI optimisation evidence.
- Replace report placeholders with real measured results, member names/IDs and video link.
- Record a real 15–20 minute video; this ZIP cannot create or host it.
- Commit and push with all team members' real contributions; create `v1.0` only after verification.
