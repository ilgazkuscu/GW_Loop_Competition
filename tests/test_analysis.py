import pandas as pd
import pytest

from gw_loop.analysis import DONATION_COLUMN, normalize_donation, summarize_item_means


def test_donation_values_are_normalized_explicitly():
    result = normalize_donation(pd.Series(["Yes", "No", "Donated at blue bin", "Unknown"]))
    assert result.iloc[:3].tolist() == [1, 0, 1]
    assert pd.isna(result.iloc[3])


def test_summary_compares_donor_and_non_donor_means():
    visits = pd.DataFrame(
        {
            DONATION_COLUMN: ["No", "No", "Yes", "Donated at blue bin"],
            "Tops": [1, 3, 4, 6],
            "Shoes": [0, 0, 1, 1],
        }
    )
    summary = summarize_item_means(visits, item_columns=("Tops", "Shoes")).set_index("item")
    assert summary.loc["Tops", "non_donor_mean"] == 2
    assert summary.loc["Tops", "donor_mean"] == 5
    assert summary.loc["Tops", "relative_change"] == 1.5
    assert pd.isna(summary.loc["Shoes", "relative_change"])


def test_summary_rejects_incomplete_schema():
    with pytest.raises(ValueError, match="Missing required columns"):
        summarize_item_means(pd.DataFrame({DONATION_COLUMN: ["Yes"]}), ("Tops",))
