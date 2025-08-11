india_trends_dashboard - Full Development Bundle

Contents:
- app.py (Streamlit app)
- utils/ (data loaders + pdf export)
- data/ (sample CSVs)
- raw/ (place large raw CSVs here or run get_and_prepare_data.py)
- geo/ (sample geojson; get_and_prepare_data.py will download full geojson)
- get_and_prepare_data.py (fetches Census CSV, GeoJSON, and PLFS table)
- export/ (output PDF reports)

Quick start:
1. Create venv and install deps:
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
2. (Optional) Fetch full data:
   python get_and_prepare_data.py
3. Run the app:
   streamlit run app.py

PDF reports are saved in export/ by default.
