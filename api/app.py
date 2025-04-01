from pymongo import MongoClient
import json
from datetime import datetime
from collections import defaultdict, Counter
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from dotenv import load_dotenv
import os
load_dotenv()
MONGO_USERNAME= os.environ.get("MONGO_USERNAME")
MONGO_PASSWORD= os.environ.get("MONGO_PASSWORD")

client = MongoClient(f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@datatrial.5fxil.mongodb.net/")
db = client["OriginalJSON"]
collection = db["JSONSIMPPL"]

posts = list(collection.find())
filtered_posts = []

def remove_automoderator_post(posts):
    """
    Remove posts that are automoderator posts.
    """
    return [post for post in posts if post.get("data", {}).get("author") != "AutoModerator"]
filtered_posts = remove_automoderator_post(posts)
def convert_to_normal_time(filtered_posts):
    """
    Convert the time from Unix timestamp to normal time format.
    """
    for post in filtered_posts:
        created_utc = post.get("data", {}).get("created_utc")
        if isinstance(created_utc, (int, float)):  # Check if it's a valid timestamp
            post["data"]["created_utc"] = datetime.utcfromtimestamp(created_utc).strftime('%Y-%m-%d %H:%M:%S')
    return filtered_posts


def top_trending_keywords(filtered_posts):
    nlp = spacy.load("en_core_web_sm")
    all_titles = " ".join(post.get("data", {}).get("title", "") for post in posts if "data" in post)
    doc = nlp(all_titles.lower())
    filtered_words = [token.text for token in doc if token.is_alpha and not token.is_stop and token.pos_ in ("NOUN", "PROPN")]
    common_words = Counter(filtered_words).most_common(10)
    print("\nTop Trending Keywords:", common_words)


# # notsogood results
# def top_words_using_TFIDF(filtered_posts):
#     """
#     Extracts the top trending keywords using TF-IDF from post titles and selftext.
#     """
#     text_data = [
#         f"{post.get('data', {}).get('title', '')} {post.get('data', {}).get('selftext', '')}".strip()
#         for post in filtered_posts
#     ]
    
#     if not any(text_data):
#         print("No valid text data available for TF-IDF analysis.")
#         return []

#     vectorizer = TfidfVectorizer(stop_words="english", max_features=10)
#     tfidf_matrix = vectorizer.fit_transform(text_data)
#     keywords = vectorizer.get_feature_names_out()

#     print("Top trending keywords:", keywords)
#     return keywords

# trending_words_2 = top_words_using_TFIDF(filtered_posts)

# for post in filtered_posts:
#     data = post.get("data", {})
#     print(f"Title: {data.get('title', 'No Title')}")
#     print(f"Created At:  {data.get('created_utc', 'Unknown Time')}")
#     print(f"Text: {data.get('selftext', 'No Text')}")
#     print(f"Comments: {data.get('num_comments', 0)} | Upvotes: {data.get('ups', 0)}")
#     print("-" * 50)

def post_frequency_per_subreddit(filtered_posts):
    """
    Calculate the number of posts per subreddit.
    """
    subreddit_count = Counter(post.get("data", {}).get("subreddit", "Unknown") for post in filtered_posts)
    return subreddit_count


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

# filtered_posts = convert_to_normal_time(filtered_posts)
# treding_word = top_trending_keywords(filtered_posts)
# post_freq = post_frequency_per_subreddit(filtered_posts)
# engagement = engagement_metrics(filtered_posts)
# keywords = top_trending_keywords(filtered_posts)

# # Display results
# print("\nPost Frequency Per Subreddit:")
# for sub, count in post_freq.items():
#     print(f"{sub}: {count} posts")

# print("\nEngagement Metrics (Upvotes & Comments):")
# for sub, stats in engagement.items():
#     print(f"{sub}: {stats['post_count']} posts, {stats['total_upvotes']} upvotes, {stats['total_comments']} comments")

# # visvalisation
# import matplotlib.pyplot as plt

# df["date"] = df["created_utc"].dt.date
# trend = df.groupby("date").size()

# plt.figure(figsize=(12, 5))
# plt.plot(trend.index, trend.values, marker="o", linestyle="-")
# plt.xlabel("Date")
# plt.ylabel("Number of Posts")
# plt.title("Post Activity Over Time")
# plt.xticks(rotation=45)
# plt.show()
