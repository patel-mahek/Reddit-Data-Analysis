import schedule
import time
from main import fetch_reddit_posts  # Import the function from your main script

# Schedule the function to run every 10 minutes
schedule.every(10).minutes.do(fetch_reddit_posts, subreddit_name="worldpolitics", limit=10)

if __name__ == "__main__":
    print("Scheduler started! Fetching posts every 10 minutes...")
    while True:
        schedule.run_pending()
        time.sleep(1)
