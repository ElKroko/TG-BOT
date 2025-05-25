# fetchers/reddit.py
import praw
from config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

def fetch_subreddit_posts(subreddit_name: str, limit: int = 3):
    """
    Obtiene los posts top 'hot' de un subreddit.
    Devuelve lista de dicts con: title, author, url, score.
    """
    posts = []
    try:
        sub = reddit.subreddit(subreddit_name)
        for submission in sub.hot(limit=limit):
            posts.append({
                "title":  submission.title,
                "author": submission.author.name if submission.author else "[deleted]",
                "url":    submission.url,
                "score":  submission.score
            })
    except Exception as e:
        print(f"Error fetching /r/{subreddit_name}: {e}")
    return posts
