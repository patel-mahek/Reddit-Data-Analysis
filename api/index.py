from fastapi import FastAPI
from typing import List
from datetime import datetime, timedelta
from pymongo import MongoClient
from collections import defaultdict, Counter
import spacy
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

client = MongoClient("mongodb+srv://mahekpatel2612:W1ZcEtXDJ03AOtht@datatrial.5fxil.mongodb.net/")
db = client["OriginalJSON"]
collection = db["JSONSIMPPL"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change to your frontend domain for security)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def remove_automoderator_post(posts):
    """
    Remove posts that are automoderator posts.
    """
    return [post for post in posts if post.get("data", {}).get("author") != "AutoModerator"]

def engagement_metrics(filtered_posts):
    """
    Compute engagement metrics - total upvotes & comments per subreddit.
    """
    metrics = defaultdict(lambda: {"post_count": 0, "total_upvotes": 0, "total_comments": 0})

    for post in filtered_posts:
        subreddit = post.get("data", {}).get("subreddit", "Unknown")
        upvotes = post.get("data", {}).get("ups", 0)
        comments = post.get("data", {}).get("num_comments", 0)

        metrics[subreddit]["post_count"] += 1
        metrics[subreddit]["total_upvotes"] += upvotes
        metrics[subreddit]["total_comments"] += comments

    return {sub: {"posts": data["post_count"], "comments": data["total_comments"], "upvotes": data["total_upvotes"]} for sub, data in metrics.items()}

def extract_keywords(posts):
    nlp = spacy.load("en_core_web_sm")
    all_titles = " ".join(post.get("data", {}).get("title", "") for post in posts if "data" in post)
    doc = nlp(all_titles.lower())
    filtered_words = [token.text for token in doc if token.is_alpha and not token.is_stop and token.pos_ in ("NOUN", "PROPN")]
    common_words = Counter(filtered_words).most_common(10)  
    print("\nTop Trending Keywords:", common_words)
    return [word[0] for word in common_words]


def count_keywords_by_month(posts):
    """Count occurrences of trending keywords per month."""
    monthly_trends = defaultdict(lambda: defaultdict(int))  

    top_keywords = extract_keywords(posts)  

    for post in posts:
        created_utc = post["data"].get("created_utc")
        if created_utc:
            month = datetime.utcfromtimestamp(created_utc).strftime("%Y-%m")

            # Check if title contains any top keywords
            title = post["data"].get("title", "").lower()
            for keyword in top_keywords:
                if keyword in title:
                    monthly_trends[month][keyword] += 1  

    # Convert to list format
    keyword_counts = [
        {"month": month, "keyword": keyword, "count": count}
        for month, keywords in monthly_trends.items()
        for keyword, count in keywords.items()
    ]

    return keyword_counts


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/engagement-metrics")
def get_engagement_metrics():
    posts = list(collection.find({})) 
    filtered_posts = remove_automoderator_post(posts)
    return engagement_metrics(filtered_posts)

@app.get("/trending-keyword-counts")
def fetch_trending_keyword_counts():
    six_months_ago = datetime.utcnow() - timedelta(days=180)
    posts = list(collection.find({"data.created_utc": {"$gte": six_months_ago.timestamp()}}))

    filtered_posts = remove_automoderator_post(posts)
    return count_keywords_by_month(filtered_posts)