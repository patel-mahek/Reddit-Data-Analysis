import praw
import pymongo
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv  
import os
load_dotenv()
MONGO_USERNAME= os.environ.get("MONGO_USERNAME")
MONGO_PASSWORD= os.environ.get("MONGO_PASSWORD")

# Connect to MongoDB

client = MongoClient(f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@datatrial.5fxil.mongodb.net/")
db = client["OriginalJSON"]
collection = db["JSONSIMPPL"]

# Configure Reddit API (Replace with your credentials)
reddit = praw.Reddit(
    client_id="9DliHvg8Kd9i7WXLpBNrQQ",
    client_secret="kNIr1Vby84IsUTz-PfIkQMSm1ASmKg",
    user_agent="script:Webscrap:v1.0 (by u/AnyEnvironment3975)"
)
# 🔹 Fetch & Store New Reddit Posts
def fetch_reddit_posts(subreddit_name="worldpolitics", limit=10):
    subreddit = reddit.subreddit(subreddit_name)
    new_posts = []

    for post in subreddit.new(limit=limit):  
        if not collection.find_one({"id": post.id}):  # Avoid duplicates
            new_posts.append({
                "id": post.id,
                "title": post.title,
                "text": post.selftext,
                "url": post.url,
                "author": str(post.author),
                "created_utc": datetime.utcfromtimestamp(post.created_utc),
                "upvotes": post.score,
                "num_comments": post.num_comments
            })

    if new_posts:
        collection.insert_many(new_posts)
        print(f"{len(new_posts)} new posts added!")

# 🔹 Run the function every 10 minutes
if __name__ == "__main__":
    fetch_reddit_posts("worldpolitics", limit=10)