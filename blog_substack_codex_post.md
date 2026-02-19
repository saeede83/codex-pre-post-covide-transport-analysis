# I Used Codex to Run an End-to-End Transit Data Analysis in One Chat
### From idea to datasets, analysis, visualizations, and publish-ready report

**By Codex (AI coding agent)**

I wanted to test whether Codex could handle a complete data project, not just code snippets.

I started with this prompt:

> “i want to explore the patterns of using public transport before and after covid in a few metro areas like new york , san fransisco . can you find publicly available datasets , plan a full analysis and once we are aligned execute on it to see what we find”

Then I refined scope:

> “if there is data available extend the pre covid baseline to few more years , maybe add one more city , chicago? do a full deep dive”

Then asked for a publishable deliverable:

> “create an html markdown report with key findings and appripriate visualizations for each insight shared, keep a tldr at the top and a few bullet points on nature and source of data and methodology followed by key insights, interpreattions and detailed findings and visualizations”

Codex executed the full pipeline end to end in one workflow.

## What Codex produced quickly

- A working analysis project folder and script
- Public dataset pull and processing (FTA NTD monthly ridership)
- Cross-city comparability logic for New York, San Francisco, and Chicago
- Recovery metrics and milestone calculations
- Multiple visuals tied directly to each key finding
- A narrative report in both Markdown and HTML

## Repository Links

All analysis artifacts are available here:

- Live HTML (GitHub Pages): `https://saeede83.github.io/codex-pre-post-covide-transport-analysis/`
- Repository: `https://github.com/saeede83/codex-pre-post-covide-transport-analysis`
- Analysis code: `https://github.com/saeede83/codex-pre-post-covide-transport-analysis/blob/codex/initial-analysis/src/analyze_transit.py`
- HTML report: `https://github.com/saeede83/codex-pre-post-covide-transport-analysis/blob/codex/initial-analysis/output/transit_deep_dive_report.html`
- Markdown report: `https://github.com/saeede83/codex-pre-post-covide-transport-analysis/blob/codex/initial-analysis/output/transit_deep_dive_report.md`
- Processed tables: `https://github.com/saeede83/codex-pre-post-covide-transport-analysis/tree/codex/initial-analysis/data/processed`
- Chart 1 (ridership index): `https://github.com/saeede83/codex-pre-post-covide-transport-analysis/blob/codex/initial-analysis/output/metro_ridership_index.png`
- Chart 2 (monthly trips): `https://github.com/saeede83/codex-pre-post-covide-transport-analysis/blob/codex/initial-analysis/output/metro_monthly_trips.png`
- Chart 3 (rail vs bus): `https://github.com/saeede83/codex-pre-post-covide-transport-analysis/blob/codex/initial-analysis/output/rail_bus_recovery_facets.png`
- Chart 4 (mode share shift): `https://github.com/saeede83/codex-pre-post-covide-transport-analysis/blob/codex/initial-analysis/output/mode_share_shift.png`

## Publishing on GitHub

I also used Codex to publish the full report online:

- The project was pushed to GitHub with code, processed data, charts, and reports.
- A `gh-pages` branch was created and deployed.
- The HTML report now renders as a normal website at:
  - `https://saeede83.github.io/codex-pre-post-covide-transport-analysis/`

This means the same assets used for analysis are now publicly inspectable and reproducible.

## Included Report (for Substack)

### TL;DR

- Ridership collapsed in all three metros in April 2020, to roughly `11%` to `20%` of baseline.
- By 2025, New York recovered most strongly, Chicago recovered moderately, and San Francisco lagged.
- Bus recovered better than rail in all three metros.
- The largest post-COVID mode-share shift toward bus happened in San Francisco.

### Data and Method

- Data: FTA NTD Monthly Modal Time Series (monthly unlinked passenger trips), `2014-01` to `2025-12`.
- Geographies: New York, San Francisco, Chicago.
- Baseline: same calendar month average during `2014-2019`.
- Metric: index where `100 = pre-COVID same-month baseline`.

### Key Insights with Visuals

1. Overall recovery diverged across cities after a shared April 2020 shock.  
   Visual: `https://raw.githubusercontent.com/saeede83/codex-pre-post-covide-transport-analysis/codex/initial-analysis/output/metro_ridership_index.png`

2. Absolute rider volume remains below pre-COVID annual totals across all three metros.  
   Visual: `https://raw.githubusercontent.com/saeede83/codex-pre-post-covide-transport-analysis/codex/initial-analysis/output/metro_monthly_trips.png`

3. Bus recovery outperformed rail recovery in each metro.  
   Visual: `https://raw.githubusercontent.com/saeede83/codex-pre-post-covide-transport-analysis/codex/initial-analysis/output/rail_bus_recovery_facets.png`

4. Mode share shifted toward bus relative to 2019, strongest in San Francisco.  
   Visual: `https://raw.githubusercontent.com/saeede83/codex-pre-post-covide-transport-analysis/codex/initial-analysis/output/mode_share_shift.png`

### Detailed Findings

- All three systems reached trough in April 2020.
- New York recovered fastest among the three and was closest to baseline by 2025.
- Chicago showed moderate recovery with a larger rail gap than bus.
- San Francisco had the slowest recovery, driven by persistent rail underperformance.

## Why this matters

This was not “AI gave me ideas.” This was execution:

- data source discovery
- analysis implementation
- visual production
- publish-ready write-up

Codex worked like a practical data analysis partner from problem statement to final assets.

## Attribution

This post is explicitly written by **Codex**, based on this chat session and the artifacts generated in this project.
