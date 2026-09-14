import pandas as pd
from datetime import date
import pandas as pd
from socialsense.dates import parse_dates
from socialsense.metrics import follower_churn
from socialsense.metrics import follower_churn


def test_follower_churn_separates_gains_from_losses():
    followers = pd.DataFrame({
        "date": pd.to_datetime(["2025-01-01", "2025-01-02", "2025-01-03"]),
        "followers": [1000, 1010, 980],
        "delta": [10, -30, 5],
    })

    result = follower_churn(followers)

    assert result["net"] == -15
    assert result["gained"] == 15
    assert result["lost"] == -30
    assert result["positive_days"] == 2
    assert result["total_days"] == 3




def test_parse_dates_increments_year_on_month_rollover():
    labels = ["December 30", "December 31", "January 1", "January 2"]

    result = parse_dates(labels, 2025)

    assert result == [
        date(2025, 12, 30),
        date(2025, 12, 31),
        date(2026, 1, 1),
        date(2026, 1, 2),
    ]


def test_parse_dates_keeps_year_when_month_does_not_go_back():
    labels = ["September 10", "October 1", "November 5"]

    result = parse_dates(labels, 2025)

    assert all(d.year == 2025 for d in result)