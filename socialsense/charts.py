import matplotlib

matplotlib.use("Agg") #matplotlip pencere açmaya çalışır pencere yok dosya yaz
import matplotlib.pyplot as plt


def follower_trend(followers, out_path):
    """Line chart of follower count over time."""
    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.plot(followers["date"], followers["followers"], linewidth=1.5) #x ekseni date y ekseni followers
    ax.set_title("Follower count")
    ax.set_ylabel("Followers")
    ax.grid(alpha=0.3)
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path

def returning_trend(ratio_table, out_path):
    """Bar chart of returning viewer share per block."""
    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.bar(range(len(ratio_table)), ratio_table["ratio"])
    ax.set_title("Returning viewers as share of total")
    ax.set_ylabel("Percent")
    ax.set_xlabel("30-day block")
    ax.grid(alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def reach_scatter(content, out_path):
    """Scatter of view count against engagement rate."""
    engagement = (
        (content["likes"] + content["comments"] + content["shares"])
        / content["views"] * 100
    )

    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.scatter(content["views"], engagement, s=40)
    ax.set_xscale("log")
    ax.set_title("Reach against engagement rate")
    ax.set_xlabel("Total views (log scale)")
    ax.set_ylabel("Engagement rate %")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


if __name__ == "__main__":
    from pathlib import Path
    from socialsense.loaders import load_followers, load_viewers, load_content
    from socialsense.metrics import returning_ratio

    Path("output").mkdir(exist_ok=True)

    followers = load_followers(Path("data/FollowerHistory.xlsx"), 2025)
    print(follower_trend(followers, "output/followers.png"))

    viewers = load_viewers(Path("data/Viewers.xlsx"), 2025)
    print(returning_trend(returning_ratio(viewers), "output/returning.png"))

    content = load_content(Path("data/Content.xlsx"))
    print(reach_scatter(content, "output/reach.png"))