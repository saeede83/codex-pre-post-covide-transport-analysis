# Transit Ridership Recovery Analysis (NYC, San Francisco, Chicago)

This repository contains an end-to-end transit ridership analysis built with Codex, including:

- analysis code
- processed analysis tables
- generated figures
- Markdown and HTML reports

## Project Structure

- `src/analyze_transit.py`: main analysis script
- `data/processed/*.csv`: processed outputs and summary tables
- `output/*.png`: visualizations
- `output/transit_deep_dive_report.md`: narrative report in Markdown
- `output/transit_deep_dive_report.html`: publish-ready HTML report

## Data Source

- FTA NTD Monthly Modal Time Series:  
  https://data.transportation.gov/Public-Transit/Monthly-Modal-Time-Series-by-Mode-of-Transportation-/5ti2-5uiv

## Reproducing

1. Create a Python virtual environment.
2. Install dependencies:
   - `pandas`
   - `matplotlib`
   - `seaborn`
   - `tabulate`
3. Run:
   - `MPLCONFIGDIR=.mplconfig python src/analyze_transit.py`

The script writes outputs into `data/processed/` and `output/`.
