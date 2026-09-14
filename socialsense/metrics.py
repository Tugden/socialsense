
import numpy as np




def follower_churn(followers):
    """Net change, gross gains and losses from a follower history table."""
    delta = followers["delta"]
    return {
        "net": int(delta.sum()), #farkın toplamı
        "gained": int(delta[delta > 0].sum()), #kazanılan takipçi toplam delta sütununda deltanın pozitif olan yerlerini seç boolean masking filtreleme
        "lost": int(delta[delta < 0].sum()), #kaybedilen takipçiler toplam
        "positive_days": int((delta > 0).sum()),# kaç gün takipçi pozitifti(kaç gün takipöi kazandı sayar)
        "total_days": len(followers), #satır uzunluğu 365 days için 
    }





def returning_ratio(viewers, block_days=30):
    """Share of viewers who are returning, in blocks of days.

    viewers: table with date, total_viewers, new_viewers, returning_viewers
    """
    df = viewers.dropna(subset=["total_viewers"]).copy() #boş olan verileri dropna ile düşür copy de gerçek veriyi etkilememek sadece kopyasını almak için kullanıldı
    df["block"] = df.index // block_days # block adında bir sutün oluştur = ile bu sütuna yaz, // tam böl ve küçüğe yuvarla, 

    grouped = df.groupby("block").agg(
        start=("date", "first"),
        total=("total_viewers", "sum"),
        returning=("returning_viewers", "sum"),
    )
    grouped["ratio"] = grouped["returning"] / grouped["total"] * 100
    return grouped






def reach_vs_resonance(content):
    """Relationship between how far a video travels and how much it engages.

    content: table with views, likes, shares, comments
    """
    df = content.copy()
    df["engagement"] = (df["likes"] + df["comments"] + df["shares"]) / df["views"] * 100

    correlation = np.corrcoef(np.log10(df["views"]), df["engagement"])[0, 1]







    return {
        "correlation": round(float(correlation), 3),
        "median_engagement": round(float(df["engagement"].median()), 2),
        "videos": len(df),
    }






if __name__ == "__main__":
    from pathlib import Path
    from socialsense.loaders import load_followers, load_viewers

    followers = load_followers(Path("data/FollowerHistory.xlsx"), 2025)
    print(follower_churn(followers))

    viewers = load_viewers(Path("data/Viewers.xlsx"), 2025)
    print(returning_ratio(viewers))

    from socialsense.loaders import load_content
    content = load_content(Path("data/Content.xlsx"))
    print(reach_vs_resonance(content))