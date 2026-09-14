from pathlib import Path

from socialsense.loaders import load_followers, load_viewers, load_content
from socialsense.metrics import follower_churn, returning_ratio, reach_vs_resonance
from socialsense.charts import follower_trend, returning_trend, reach_scatter
from socialsense.report import render


def main(data_dir="data", out_dir="output", start_year=2025):
    data = Path(data_dir)
    out = Path(out_dir)
    out.mkdir(exist_ok=True)

    followers = load_followers(data / "FollowerHistory.xlsx", start_year)
    viewers = load_viewers(data / "Viewers.xlsx", start_year)
    content = load_content(data / "Content.xlsx")

    follower_trend(followers, out / "followers.png")
    returning_trend(returning_ratio(viewers), out / "returning.png")
    reach_scatter(content, out / "reach.png")

    path = render(
        follower_churn(followers),
        reach_vs_resonance(content),
        out / "report.html",
    )
    print(f"Report written to {path}")


if __name__ == "__main__":
    main()