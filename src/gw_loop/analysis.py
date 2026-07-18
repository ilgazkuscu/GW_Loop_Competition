from __future__ import annotations

import numpy as np
import pandas as pd


DONATION_COLUMN = "Did you bring donations with you today?"
ITEM_COLUMNS = (
    "Tops",
    "Collared Shirts",
    "Sweaters",
    "Pants",
    "Skirts",
    "Shorts",
    "Dresses",
    "Outerwear",
    "Shoes",
    "Accessories",
)
DONATION_VALUES = {
    "yes": 1,
    "donated at blue bin": 1,
    "no": 0,
}


def normalize_donation(series: pd.Series) -> pd.Series:
    normalized = series.astype("string").str.strip().str.casefold()
    return normalized.map(DONATION_VALUES).astype("Int64")


def summarize_item_means(
    visits: pd.DataFrame,
    item_columns: tuple[str, ...] = ITEM_COLUMNS,
) -> pd.DataFrame:
    required = {DONATION_COLUMN, *item_columns}
    missing = required - set(visits.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

    frame = visits[[DONATION_COLUMN, *item_columns]].copy()
    frame["Donation"] = normalize_donation(frame.pop(DONATION_COLUMN))
    frame = frame.dropna(subset=["Donation"])
    for column in item_columns:
        frame[column] = pd.to_numeric(frame[column], errors="coerce").fillna(0)

    grouped = frame.groupby("Donation", observed=True)[list(item_columns)].mean().T
    grouped = grouped.rename(columns={0: "non_donor_mean", 1: "donor_mean"})
    for column in ("non_donor_mean", "donor_mean"):
        if column not in grouped:
            grouped[column] = np.nan
    denominator = grouped["non_donor_mean"].replace(0, np.nan)
    grouped["relative_change"] = grouped["donor_mean"] / denominator - 1
    return grouped.reset_index(names="item")[
        ["item", "non_donor_mean", "donor_mean", "relative_change"]
    ]
