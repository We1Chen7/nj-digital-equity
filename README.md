# New Jersey Digital Equity: a step-by-step Colab notebook

[Open in Google Colab](https://colab.research.google.com/github/We1Chen7/nj-digital-equity/blob/main/NJ_Digital_Equity_Colab.ipynb)

[Public Drive notebook](https://colab.research.google.com/drive/15W7wUe0KhY7C4_XvfAfH95xV91sP1BHQ)

The notebook contains **36 code cells**. Each cell has an English explanation
and a visible checkpoint: a table, sample rows, a chart, or a status message.
Run cells in order with **Shift + Enter**, or choose **Runtime → Run all**.
A standard CPU runtime is enough. Colab's preinstalled pandas, numpy and
matplotlib are used; the GIS cells install GeoPandas from PyPI if needed.

## Data

- ACS 2024 five-year estimates represent **2020–2024**, covering **2,181 NJ
  census tracts, 21 counties and one state row**.
- Tables: B28002, B28003, B19013, C17002 and B01002.
- NJ Office of Broadband Connectivity asset directory: **614 raw records**.
- `NJ_Digital_Equity_Data.zip` contains raw NJ source rows, source metadata,
  download provenance and the initial processed CSVs. The notebook recreates
  processed indicators from the raw files.
- Source downloads were collected on October 6, 2026. Cached files were checked
  again on October 7; the directory's combined JSON was reassembled from those
  cached pages. The manifest identifies the concatenation method separately.

The notebook downloads the public ZIP automatically and checks its SHA-256 hash.
No Census API key, Drive sign-in or new questionnaire is needed for the default
analysis. The optional `drive` input mode reads the same ZIP from
`MyDrive/NJ_Digital_Equity/`. The optional final Drive cell asks for authorization
and copies the results ZIP to that folder.

## Files

| File | Purpose |
|---|---|
| `NJ_Digital_Equity_Colab.ipynb` | Editable notebook with saved visual outputs |
| `NJ_Digital_Equity_Data.zip` | Verified input snapshot |
| `NJ_Digital_Equity_Results.zip` | Processed tables, summaries, PNG charts and joined GIS GeoPackage |
| `NJ_Digital_Equity_Colab_Walkthrough.html` | Downloadable reading version |
| `download_data.py` | Collect another official-source snapshot in a new dated folder |
| `snapshot_info.json` | Input ZIP hash |
| `tl_2024_34_tract.zip` | Official 2024 NJ tract shapefile and companion files |

Saved notebook outputs were initially verified locally. Re-running in Colab
replaces them with outputs from the Colab runtime.

## Initial description

Using the official statewide estimates, 5.39% of households had no internet
access, 4.06% had no computing device, and 10.34% had cellular-only subscriptions.
All joining, checksum and category-total checks passed. Fifteen tracts had zero
household denominators and therefore missing household percentages.

These findings are descriptive. The directory includes 99 records explicitly
stating that no direct digital inclusion program is available. A directory record
is not automatically a verified service site or a capacity measure. Recorded
office locations can differ from service areas. Census margins of error are
retained, but derived percentage confidence intervals have not been calculated.
FCC network availability has not been downloaded. No causal model is included.

## Official sources

- [Census ACS summary files](https://www.census.gov/programs-surveys/acs/data/summary-file.2024.html)
- [B28002 definitions](https://api.census.gov/data/2024/acs/acs5/groups/B28002.html)
- [B28003 definitions](https://api.census.gov/data/2024/acs/acs5/groups/B28003.html)
- [NJ OBC directory data](https://data.nj.gov/resource/yjm4-bujw.json)
- [NJ mapping hub](https://www.nj.gov/connect/resources/mapping/)

Keep this snapshot unchanged for reproducibility. Use the downloader in a new
dated folder to collect a new snapshot. Public source data remain subject to
their source terms; no new blanket license is assigned here.

## Tract maps

Cells 29–36 display source descriptions, variable definitions, descriptive statistics, shapefile provenance and join checks inside code outputs. All 2,181 tract GEOIDs match one-to-one. Maps compare no internet access, poverty and median income; a bivariate map combines relative poverty and no-access terciles. Small denominators and missing estimates are flagged. Terciles describe relative rankings, not policy thresholds or causal effects.

The boundaries come from [2024 Census TIGER/Line](https://www2.census.gov/geo/tiger/TIGER2024/TRACT/tl_2024_34_tract.zip). The ZIP is checked against SHA-256 `6aa58cfd7b8563383a0104bc7363d9de9daeac0ad524a12ed0d4fd473a03c38e`.
