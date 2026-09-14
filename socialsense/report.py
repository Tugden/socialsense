from pathlib import Path


TEMPLATE = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>socialsense report</title>
<style>
  body {{ font-family: -apple-system, Segoe UI, sans-serif;
         max-width: 820px; margin: 40px auto; padding: 0 20px;
         color: #1a1a1a; line-height: 1.6; }}
  h1 {{ margin-bottom: 4px; }}
  .sub {{ color: #666; margin-top: 0; }}
  .grid {{ display: flex; gap: 32px; margin: 24px 0; }}
  .stat .n {{ font-size: 30px; font-weight: 600; }}
  .stat .l {{ color: #666; font-size: 13px; }}
  img {{ width: 100%; margin: 8px 0 32px; }}
  .note {{ background: #f6f6f6; padding: 14px 18px; font-size: 14px; }}
</style>
</head>
<body>

<h1>Account report</h1>
<p class="sub">{days} days of data</p>

<div class="grid">
  <div class="stat"><div class="n">{net:+,}</div><div class="l">Net followers</div></div>
  <div class="stat"><div class="n">{gained:+,}</div><div class="l">Gross gained</div></div>
  <div class="stat"><div class="n">{lost:+,}</div><div class="l">Gross lost</div></div>
  <div class="stat"><div class="n">{positive_days}</div><div class="l">Positive days</div></div>
</div>

<img src="followers.png">

<h2>Returning viewers</h2>
<img src="returning.png">

<h2>Reach against engagement</h2>
<img src="reach.png">

<div class="note">
Correlation between log views and engagement rate: <b>{correlation}</b>
across {videos} videos. Median engagement rate {median_engagement}%.
Videos that travel furthest engage least.
</div>

</body>
</html>
"""


def render(churn, reach, out_path):
    """Write an HTML report from computed metrics."""
    html = TEMPLATE.format(
        days=churn["total_days"],
        net=churn["net"],
        gained=churn["gained"],
        lost=churn["lost"],
        positive_days=churn["positive_days"],
        correlation=reach["correlation"],
        videos=reach["videos"],
        median_engagement=reach["median_engagement"],
    )
    Path(out_path).write_text(html, encoding="utf-8")
    return out_path



if __name__ == "__main__":
    from socialsense.loaders import load_followers, load_content
    from socialsense.metrics import follower_churn, reach_vs_resonance

    followers = load_followers(Path("data/FollowerHistory.xlsx"), 2025)
    content = load_content(Path("data/Content.xlsx"))

    print(render(
        follower_churn(followers),
        reach_vs_resonance(content),
        "output/report.html",
    ))