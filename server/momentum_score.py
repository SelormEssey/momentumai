import json
from collections import defaultdict
import re
import math
from datetime import datetime

# Load scraped posts
with open("data.json", "r") as f:
    posts = json.load(f)

keyword_stats = defaultdict(lambda: {"mentions": 0, "total_upvotes": 0, "latest": 0})

# Basic keyword extractor
def extract_keywords(text):
    words = re.findall(r'\b[a-zA-Z0-9]{3,}\b', text.lower())  # Words 3+ characters
    return [word for word in words if word not in stopwords]

# Basic stopwords list (expand later)
stopwords = set([
    "the", "and", "for", "you", "this", "that", "with", "from", "your", "are", 
    "has", "was", "but", "about", "get", "not", "out", "just", "new", "now", "all"
])

# Analyze posts
for post in posts:
    keywords = extract_keywords(post["title"])
    for word in keywords:
        keyword_stats[word]["mentions"] += 1
        keyword_stats[word]["total_upvotes"] += post["upvotes"]
        keyword_stats[word]["latest"] = max(keyword_stats[word]["latest"], post["created_utc"])

# Score keywords
scored_keywords = []

for word, stats in keyword_stats.items():
    age_hours = (datetime.utcnow().timestamp() - stats["latest"]) / 3600
    recency_bonus = 1 / (1 + age_hours)  # newer = higher score
    score = (stats["mentions"] * 1.5) + (stats["total_upvotes"] * 0.1) + (recency_bonus * 5)
    scored_keywords.append({
        "keyword": word,
        "mentions": stats["mentions"],
        "upvotes": stats["total_upvotes"],
        "score": round(score, 2)
    })

# Sort and save top trending
top_keywords = sorted(scored_keywords, key=lambda x: x["score"], reverse=True)[:25]

with open("trending.json", "w") as f:
    json.dump(top_keywords, f, indent=2)

print("✅ trending.json generated")
