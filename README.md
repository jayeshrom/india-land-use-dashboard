# India Land Use Dashboard

Interactive Streamlit dashboard for India's historical land-use trends using the official Nine-Fold Land Use Classification data from 1950-51 to 2023-24.

## Features

- KPI cards for net sown area, forest cover, and non-agricultural land change.
- Interactive year range filter and category toggles.
- Multi-line historical trend chart.
- Donut chart for selected-year land-use share.
- Stacked decade chart comparing cultivated and uncultivated land.

## Run Locally

```powershell
pip install -r requirements.txt
streamlit run app.py
```

## Data

The source table is hardcoded in `app.py` as a CSV string to preserve exact historical values.
