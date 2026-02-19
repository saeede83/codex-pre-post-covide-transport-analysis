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

Replace `<REPO_BASE>` with your GitHub repository URL (for example `https://github.com/<user>/<repo>`).

- Analysis code: `<REPO_BASE>/blob/main/src/analyze_transit.py`
- HTML report: `<REPO_BASE>/blob/main/output/transit_deep_dive_report.html`
- Markdown report: `<REPO_BASE>/blob/main/output/transit_deep_dive_report.md`
- Processed tables: `<REPO_BASE>/tree/main/data/processed`
- Chart 1 (ridership index): `<REPO_BASE>/blob/main/output/metro_ridership_index.png`
- Chart 2 (monthly trips): `<REPO_BASE>/blob/main/output/metro_monthly_trips.png`
- Chart 3 (rail vs bus): `<REPO_BASE>/blob/main/output/rail_bus_recovery_facets.png`
- Chart 4 (mode share shift): `<REPO_BASE>/blob/main/output/mode_share_shift.png`

## Why this matters

This was not “AI gave me ideas.” This was execution:

- data source discovery
- analysis implementation
- visual production
- publish-ready write-up

Codex worked like a practical data analysis partner from problem statement to final assets.

## Attribution

This post is explicitly written by **Codex**, based on this chat session and the artifacts generated in this project.
