import praw
import json
import os
from dotenv import load_dotenv
from datetime import datetime

# Load .env config
load_dotenv()

# Initialize Reddit client
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_SECRET"),
    username=os.getenv("REDDIT_USER"),
    password=os.getenv("REDDIT_PASS"),
    user_agent=os.getenv("USER_AGENT"),
)

# Subreddits to monitor
subreddits = ["CryptoMoonShots", "startups", "entrepreneur", "smallbusiness"]

def fetch_posts(limit=50):
    all_posts = []
    for sub in subreddits:
        print(f"Scraping r/{sub}...")
        subreddit = reddit.subreddit(sub)
        for post in subreddit.new(limit=limit):
            post_data = {
                "title": post.title,
                "upvotes": post.score,
                "comments": post.num_comments,
                "created_utc": post.created_utc,
                "created_human": datetime.utcfromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                "subreddit": sub,
                "url": post.url,
                "id": post.id,
            }
            all_posts.append(post_data)
    return all_posts

if __name__ == "__main__":
    posts = fetch_posts(limit=75)
    with open("data.json", "w") as f:
        json.dump(posts, f, indent=2)
    print(f"✅ {len(posts)} posts saved to data.json")
