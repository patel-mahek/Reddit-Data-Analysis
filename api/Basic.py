from pymongo import MongoClient
import re

from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import numpy as np
import pandas as pd
from datetime import datetime
from statistics import mean, stdev
import spacy
from load_dotenv import load_dotenv
import os   
load_dotenv()
MONGO_USERNAME= os.environ.get("MONGO_USERNAME")
MONGO_PASSWORD= os.environ.get("MONGO_PASSWORD")

client = MongoClient(f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@datatrial.5fxil.mongodb.net/")
db = client["OriginalJSON"]
collection = db["JSONSIMPPL"]

# # Fetch 5 sample posts
# sample_posts = collection.find().limit(5)
# for post in sample_posts:
#     print(post)


# # ------------------------------------------------------------------------
# # Fetch all posts from the MongoDB collection
# json_data = list(collection.find())

# if not json_data:
#     print("No posts found in the collection.")
#     exit()

# # ------------------------------------------------------------------------
# # top trending post
# top_posts = sorted(json_data, key=lambda x: x.get("data", {}).get("ups", 0), reverse=True)[:5]

# print("\nTop Trending Posts:")
# for post in top_posts:
#     print(f"{post.get('data', {}).get('title', 'No Title')} ({post.get('data', {}).get('ups', 0)} upvotes)")


# # ------------------------------------------------------------------------
# # most discussed post by comments
# top_commented_posts = sorted(json_data, key=lambda x: x.get("data", {}).get("num_comments", 0), reverse=True)[:5]

# print("\nMost Discussed Posts:")
# for post in top_commented_posts:
#     print(f" {post.get('data', {}).get('title', 'No Title')} ({post.get('data', {}).get('num_comments', 0)} comments)")



# # ------------------------------------------------------------------------
# # top trending keywordsimport spacy
# from collections import Counter

# # Load spaCy's English NLP model
# nlp = spacy.load("en_core_web_sm")

# # Fetch post titles safely
# all_titles = " ".join(post.get("data", {}).get("title", "") for post in json_data if "data" in post)

# # Process text with spaCy
# doc = nlp(all_titles.lower())

# # Extract words that are nouns (skip stopwords & punctuation)
# filtered_words = [token.text for token in doc if token.is_alpha and not token.is_stop and token.pos_ in ("NOUN", "PROPN")]

# # Find most common words
# common_words = Counter(filtered_words).most_common(10)

# print("\nTop Trending Keywords:", common_words)




# # ------------------------------------------------------------------------
# # # detect possible miss-information
# # from statistics import mean, stdev

# # # Fetch all posts from MongoDB
# # all_posts = list(collection.find({}, {"data.title": 1, "data.upvote_ratio": 1, "data.num_comments": 1}))

# # # Extract numerical values
# # num_comments = [post["data"].get("num_comments", 0) for post in all_posts]
# # upvote_ratios = [post["data"].get("upvote_ratio", 1) for post in all_posts]

# # # Compute mean and standard deviation
# # mean_comments = mean(num_comments)
# # stdev_comments = stdev(num_comments) if len(num_comments) > 1 else 0  # Avoid division by zero

# # mean_upvotes = mean(upvote_ratios)
# # stdev_upvotes = stdev(upvote_ratios) if len(upvote_ratios) > 1 else 0

# # # Define thresholds
# # high_discussion_threshold = mean_comments + stdev_comments
# # low_upvote_threshold = mean_upvotes - stdev_upvotes




# # ----------------OR---------------------------
# import numpy as np
# # Extract numerical values from all posts
# num_comments = [post.get("data", {}).get("num_comments", 0) for post in json_data]
# upvote_ratios = [post.get("data", {}).get("upvote_ratio", 1) for post in json_data]  # Corrected key

# high_discussion_threshold = np.percentile(num_comments, 80)  # Top 20% most discussed
# low_upvote_threshold = np.percentile(upvote_ratios, 20)  # Bottom 20% upvote ratio


# print(f"Avg Comments: {mean_comments} | High Discussion Threshold: {high_discussion_threshold}")
# print(f"Avg Upvote Ratio: {mean_upvotes} | Low Upvote Threshold: {low_upvote_threshold}")

# # Detect misleading posts
# misleading_posts = [
#     post for post in all_posts
#     if post["data"].get("upvote_ratio", 1) < low_upvote_threshold
#     and post["data"].get("num_comments", 0) > high_discussion_threshold
# ]

# # Display results
# for post in misleading_posts:
#     print(f"Possible Misinformation: {post['data']['title']} (Upvote Ratio: {post['data'].get('upvote_ratio', 1)}, Comments: {post['data'].get('num_comments', 0)})")


json_data = list(collection.find())


def calculate_total_users():
    """
    Calculates the total number of unique users (authors) across all posts in the collection.
    """
    try:
        # Use aggregation to efficiently count distinct authors
        pipeline = [
            {"$group": {"_id": "$data.author"}},  # Group by author
            {"$count": "total_users"}  # Count the number of groups (distinct authors)
        ]

        result = list(collection.aggregate(pipeline))

        if result:
            total_users = result[0].get("total_users", 0)
        else:
            total_users = 0  # No documents found

        print(f"Total Number of Unique Users (Authors): {total_users}")

    except Exception as e:
        print(f"Error calculating total users: {e}")

    finally:
        client.close()  # Ensure client is closed even if there's an error


# Run the calculation
calculate_total_users()