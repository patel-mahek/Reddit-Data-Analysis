# # analyses ont he given criteria 
# from pymongo import MongoClient
# from collections import defaultdict
# import nltk
# from nltk.sentiment import SentimentIntensityAnalyzer
# import google.generativeai as genai
# import time
# import numpy as np
# from load_dotenv import load_dotenv
# import os
# load_dotenv()
# nltk.download("vader_lexicon")
# sia = SentimentIntensityAnalyzer()

# genai.configure(api_key= os.environ.get("GEMINI_API_KEY"))
# model = genai.GenerativeModel("gemini-1.5-flash")

# client = MongoClient(f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@datatrial.5fxil.mongodb.net/")
# db = client["OriginalJSON"]
# collection = db["JSONSIMPPL"]

# MISINFO_POST_THRESHOLD = 2  # Flag users with 2+ misleading posts
# SENSATIONAL_KEYWORDS = {"shocking", "exposed", "truth", "hidden", "cover-up", "scam", "hoax", "fraud", "lies"}


# def analyze_misleading_gemini(texts):
#     """Batch process text using Gemini to analyze misleading content with explanations."""
#     retries = 3
#     delay = 2
#     results = []  # Collect individual post results
#     for text in texts:
#         for attempt in range(retries):
#             try:
#                 prompt = f"""Determine if the following Reddit post contains misleading or false information. 
#                            If misleading, explain why in 1-2 sentences. Otherwise, say 'Not Misleading'.
#                            Post: '{text}'"""  # Single prompt for single post
#                 response = model.generate_content(prompt)
#                 results.append(response.text.strip()) #Append Result to text
#                 break # Break the retry loop
#             except Exception as e:
#                 print(f"Gemini API error (attempt {attempt+1} for post '{text[:50]}...'): {e}")  #Added post context
#                 if "429" in str(e):
#                     time.sleep(delay)
#                     delay *= 2
#                 else:
#                     results.append("Unknown")  # Append "Unknown" on permanent error
#                     break # Break the retry loop after a non-retryable error
#         else:  # If inner loop didn't break (all retries failed)
#             results.append("Unknown")  # Append "Unknown" if all retries failed

#     return results #return the whole set of  results


# # Fetch all posts from database
# all_posts = list(collection.find())
# num_comments = [p.get("data", {}).get("num_comments", 0) for p in all_posts]
# upvote_ratios = [p.get("data", {}).get("upvote_ratio", 1) for p in all_posts]

# # Define thresholds for high discussion & low upvotes
# high_discussion_threshold = np.percentile(num_comments, 80)
# low_upvote_threshold = np.percentile(upvote_ratios, 20)

# # Identify potential misleading posts
# potential_misleading_posts = []
# for post in all_posts:
#     data = post.get("data", {})
#     title = data.get("title", "").lower()
#     text = data.get("selftext", "").lower()

#     contains_sensational = any(word in title or word in text for word in SENSATIONAL_KEYWORDS)
#     low_upvotes = data.get("upvote_ratio", 1) < low_upvote_threshold
#     high_discussion = data.get("num_comments", 0) > high_discussion_threshold

#     if contains_sensational and low_upvotes and high_discussion:
#         potential_misleading_posts.append(post)

# print(f"Total Potential Misleading Posts Identified: {len(potential_misleading_posts)}")

# # Analyze misleading content with Gemini
# texts = [p["data"].get("title", "") + " " + p["data"].get("selftext", "") for p in potential_misleading_posts]
# misleading_evaluations = analyze_misleading_gemini(texts)

# # Debugging: Print Gemini's response for manual verification
# for text, eval in zip(texts, misleading_evaluations):
#     print(f"Text: {text[:100]}... | Evaluation: {eval}")

# # Confirm misleading posts based on Gemini's response
# misleading_posts = [
#     p for p, eval in zip(potential_misleading_posts, misleading_evaluations)
#     if "misleading" in eval.lower() and eval.lower() != "not misleading"
# ]

# print(f"Total Confirmed Misleading Posts: {len(misleading_posts)}")

# # Sort misleading posts by engagement (comments + upvotes)
# misleading_posts.sort(key=lambda p: (p["data"].get("num_comments", 0) + p["data"].get("ups", 0)), reverse=True)

# # Track user statistics
# user_stats = defaultdict(lambda: {"total_posts": 0, "misleading_posts": 0})
# for post in misleading_posts:
#     user = post["data"].get("author", "Unknown")
#     user_stats[user]["misleading_posts"] += 1
#     user_stats[user]["total_posts"] += 1

# # Identify repeat offenders
# repeat_offenders = [(user, stats["misleading_posts"]) for user, stats in user_stats.items() if stats["misleading_posts"] >= MISINFO_POST_THRESHOLD]
# repeat_offenders.sort(key=lambda x: x[1], reverse=True)

# print("\nVerified Repeat Offenders:")
# for user, mis_posts in repeat_offenders[:10]:
#     print(f"{user}: {mis_posts} misleading posts")


# analyses all posts
from pymongo import MongoClient
from collections import defaultdict
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import google.generativeai as genai
import time
import numpy as np
from typing import List
from dotenv import load_dotenv 
import os
load_dotenv()
MONGO_USERNAME= os.environ.get("MONGO_USERNAME")
MONGO_PASSWORD= os.environ.get("MONGO_PASSWORD")

nltk.download("vader_lexicon")
sia = SentimentIntensityAnalyzer()

# Replace with your actual API key! DO NOT HARDCODE IN PRODUCTION!
genai.configure(api_key= os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

MONGO_USERNAME = os.environ.get("MONGO_USERNAME")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")
client = MongoClient(f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@datatrial.5fxil.mongodb.net/")
db = client["OriginalJSON"]
collection = db["JSONSIMPPL"]



MISINFO_POST_THRESHOLD = 2  # Flag users with 2+ misleading posts
# SENSATIONAL_KEYWORDS = {"shocking", "exposed", "truth", "hidden", "cover-up", "scam", "hoax", "fraud", "lies"}  # REMOVED

BATCH_SIZE = 10  # Define the batch size


def analyze_misleading_gemini_batch(texts: List[str]) -> List[str]:
    """Batch process text using Gemini to analyze misleading content.

    Args:
        texts: A list of post texts to analyze.

    Returns:
        A list of analysis results, one for each post.
    """
    results = []
    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i:i + BATCH_SIZE]
        retries = 3
        delay = 2
        for attempt in range(retries):
            try:
                prompts = [
                    f"""Determine if the following Reddit post contains misleading or false information.
                    If misleading, explain why in 1-2 sentences. Otherwise, say 'Not Misleading'.
                    Post: '{text}'"""
                    for text in batch
                ]
                responses = model.generate_content(prompts)
                results.extend([resp.text.strip() for resp in responses])
                break  # Success, move to the next batch
            except Exception as e:
                print(f"Gemini API error (attempt {attempt+1} for batch starting with '{batch[0][:50]}...'): {e}") #First Element for Batch
                if "429" in str(e):
                    time.sleep(delay)
                    delay *= 2
                else:
                    # Non-retryable error, fill with "Unknown" for this batch
                    results.extend(["Unknown"] * len(batch))
                    break # Stop retrying this batch
        else:
            # All retries failed, fill with "Unknown" for this batch
            results.extend(["Unknown"] * len(batch))

    return results


# Fetch all posts from database
all_posts = list(collection.find())

# Extract texts for analysis
texts = [p["data"].get("title", "") + " " + p["data"].get("selftext", "") for p in all_posts]

# Analyze all posts in batches
misleading_evaluations = analyze_misleading_gemini_batch(texts)

# Debugging: Print Gemini's response for manual verification
for text, eval in zip(texts, misleading_evaluations):
    print(f"Text: {text[:100]}... | Evaluation: {eval}")

# Confirm misleading posts based on Gemini's response
misleading_posts = [
    p for p, eval in zip(all_posts, misleading_evaluations)
    if "misleading" in eval.lower() and eval.lower() != "not misleading"
]

print(f"Total Confirmed Misleading Posts: {len(misleading_posts)}")

# Track user statistics
user_stats = defaultdict(lambda: {"total_posts": 0, "misleading_posts": 0})
for post in misleading_posts:
    user = post["data"].get("author", "Unknown")
    user_stats[user]["misleading_posts"] += 1
    user_stats[user]["total_posts"] += 1

# Identify repeat offenders
repeat_offenders = [(user, stats["misleading_posts"]) for user, stats in user_stats.items() if stats["misleading_posts"] >= MISINFO_POST_THRESHOLD]
repeat_offenders.sort(key=lambda x: x[1], reverse=True)

print("\nVerified Repeat Offenders:")
for user, mis_posts in repeat_offenders[:10]:
    print(f"{user}: {mis_posts} misleading posts")