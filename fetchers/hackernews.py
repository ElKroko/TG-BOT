# fetchers/hackernews.py
import feedparser

HN_RSS_URL = "https://hnrss.org/frontpage"

def fetch_hn_posts(limit: int = 5):
    """
    Recupera los primeros `limit` items del RSS de Hacker News.
    Devuelve una lista de dicts con: title, link, author (si existe), published.
    """
    feed = feedparser.parse(HN_RSS_URL)
    posts = []
    for entry in feed.entries[:limit]:
        posts.append({
            "title":     entry.title,
            "link":      entry.link,
            "author":    getattr(entry, "author", "unknown"),
            "published": entry.published
        })
    return posts
