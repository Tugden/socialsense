from pathlib import Path
import pandas as pd
from socialsense.dates import parse_dates


def load_followers(path_yol, start_year):
    """FollowerHistory.xlsx -> date, followers, delta table."""
    df = pd.read_excel(path_yol)
    df = df.rename(columns={
        "Date": "date",
        "Followers": "followers",
        "Difference in followers from previous day": "delta",
    })
    df["date"] = pd.to_datetime(parse_dates(df["date"], start_year))
    return df[["date", "followers", "delta"]]


def load_overview(path_yol, start_year):
    """Overview.xlsx -> daily totals table."""
    df = pd.read_excel(path_yol)
    df = df.rename(columns={
        "Date": "date",
        "Video Views": "views",
        "Profile Views": "profile_views",
        "Likes": "likes",
        "Comments": "comments",
        "Shares": "shares",
    })
    df["date"] = pd.to_datetime(parse_dates(df["date"], start_year))
    return df[["date", "views", "profile_views", "likes", "comments", "shares"]]


def load_viewers(path_yol, start_year):
    """Viewers.xlsx -> daily viewer breakdown."""
    df = pd.read_excel(path_yol)
    df = df.rename(columns={
        "Date": "date",
        "Total Viewers": "total_viewers",
        "New Viewers": "new_viewers",
        "Returning Viewers": "returning_viewers",
    })
    df["total_viewers"] = pd.to_numeric(df["total_viewers"], errors="coerce")
    df["date"] = pd.to_datetime(parse_dates(df["date"], start_year))
    return df[["date", "total_viewers", "new_viewers", "returning_viewers"]]


def load_content(path_yol):
    """Content.xlsx -> per-video table.

    Post dates have no year and rows are not chronological, so the date
    is left as text for now.
    """
    df = pd.read_excel(path_yol)
    df = df.rename(columns={
        "Video title": "title",
        "Total views": "views",
        "Total likes": "likes",
        "Total shares": "shares",
        "Total comments": "comments",
        "Post time": "posted",
    })
    return df[["title", "posted", "views", "likes", "shares", "comments"]]


if __name__ == "__main__":
    print(load_followers(Path("data/FollowerHistory.xlsx"), 2025).head(2))
    print(load_overview(Path("data/Overview.xlsx"), 2025).head(2))
    print(load_viewers(Path("data/Viewers.xlsx"), 2025).head(2))
    print(load_content(Path("data/Content.xlsx")).head(2))