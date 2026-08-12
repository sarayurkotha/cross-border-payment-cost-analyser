"""
Trims the full World Bank Remittance Prices Worldwide raw workbook (41-74 columns,
~247k rows, 49MB) down to only the columns this analysis actually uses, and writes
a single combined CSV to data/.

Run this once against your own copy of data/raw/remittance_prices_raw.xlsx
(not committed to git - see README) to regenerate data/remittance_prices_selected_columns.csv.
"""

import pandas as pd

RAW_PATH = "data/raw/remittance_prices_raw.xlsx"
OUTPUT_PATH = "data/remittance_prices_selected_columns.csv"

# Only what analysis.py needs:
#   period              - quarter label, e.g. "2016_2Q" -> trend chart, slicer
#   source_name         - sending country -> corridor grouping, heatmap
#   destination_name    - receiving country -> corridor grouping, heatmap
#   destination_code    - ISO 3166-1 alpha-3 code -> choropleth map (plotly needs
#                         a country code, not a name, to place shading correctly)
#   firm_type           - Bank / Money Transfer Operator / etc. -> provider comparison
#   corridor            - source+destination code -> convenience key
#   cc1 total cost %    - total cost sending the equivalent of $200 (the World Bank's
#                         own headline SDG 10.c indicator basis); cc2 (the $500 figure)
#                         is dropped since cc1 alone is enough for this analysis.
COLUMNS = [
    "period",
    "source_name",
    "destination_name",
    "destination_code",
    "firm_type",
    "corridor",
    "cc1 total cost %",
]

SHEETS = ["Dataset (up to Q1 2016)", "Dataset (from Q2 2016)"]


def main() -> None:
    frames = [
        pd.read_excel(RAW_PATH, sheet_name=sheet, usecols=COLUMNS)
        for sheet in SHEETS
    ]
    df = pd.concat(frames, ignore_index=True)
    df = df.rename(columns={"cc1 total cost %": "total_cost_pct"})
    df = df.dropna(subset=["total_cost_pct"])

    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Wrote {len(df):,} rows x {len(df.columns)} columns to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
