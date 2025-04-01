# from pymongo import MongoClient
# import google.generativeai as genai
# import json
# from typing import List, Dict
# from tqdm import tqdm
# from bson import ObjectId
# # MongoDB Configuration (Replace with your actual credentials)
# MONGODB_URI = "mongodb+srv://mahekpatel2612:W1ZcEtXDJ03AOtht@datatrial.5fxil.mongodb.net/"  # Replace with your MongoDB URI
# DATABASE_NAME = "OriginalJSON"  # Replace with your database name
# COLLECTION_NAME = "JSONSIMPPL"  # Replace with your collection name

# # Gemini API Configuration (Replace with your API key)
# GOOGLE_API_KEY = "AIzaSyBmUfmA9alBsBgYARkekoeCbL2LGJsAY6k"
# genai.configure(api_key=GOOGLE_API_KEY)
# model = genai.GenerativeModel('gemini-2.0-flash')  # Use gemini-pro for text analysis


# BATCH_SIZE = 15



# class JSONEncoder(json.JSONEncoder):
#     """
#     Custom JSON encoder to handle MongoDB ObjectId.
#     """

#     def default(self, o):
#         if isinstance(o, ObjectId):
#             return str(o)
#         return super().default(o)


# def connect_to_mongodb(uri: str, db_name: str, collection_name: str):
#     """
#     Establishes a connection to MongoDB and returns the specified collection.

#     Args:
#         uri (str): The MongoDB connection URI.
#         db_name (str): The name of the database.
#         collection_name (str): The name of the collection.

#     Returns:
#         pymongo.collection.Collection: The MongoDB collection object.
#     """
#     client = MongoClient(uri)
#     db = client[db_name]
#     collection = db[collection_name]
#     return collection


# def fetch_data_batch(collection, batch_size: int, skip: int) -> List[Dict]:
#     """
#     Fetches a batch of data from MongoDB.

#     Args:
#         collection (pymongo.collection.Collection): The MongoDB collection object.
#         batch_size (int): The number of documents to fetch in each batch.
#         skip (int): The number of documents to skip from the beginning of the collection.

#     Returns:
#         List[Dict]: A list of dictionaries, where each dictionary represents a MongoDB document.
#     """
#     data = list(collection.find().skip(skip).limit(batch_size))
#     return data


# def analyze_posts_with_gemini(posts: List[Dict]) -> str:
#     """
#     Analyzes a batch of Reddit posts using the Gemini language model to identify
#     misleading information, sources, topics, and potential coordinated attacks.

#     Args:
#         posts (List[Dict]): A list of dictionaries, where each dictionary represents a Reddit post.

#     Returns:
#         str: A string containing the analysis results and insights.
#     """

#     prompt = f"""
#     Analyze the following Reddit posts to identify:

#     1. Sources and accounts involved in potentially misleading activity.
#     2. The topics of the potentially misleading posts.
#     3. Whether these actors have a history of similar behavior or if this appears to be a coordinated attack.
#     4. Identify any bad channels that consistently propagate such messages.

#     Provide your analysis in a narrative, highlighting potential misinformation campaigns,
#     coordinated efforts, and influential accounts driving these narratives. Focus on identifying trends,
#     patterns, and potential sources of misleading information. Also identify the topic that these
#     post convey.

#     Reddit Posts (JSON format):
#     ```json
#     {JSONEncoder().encode(posts)}
#     ```

#     Ensure that the story should be able to Track different popular trends to understand how public content is propagated on different social media platforms.
#     Identify posts containing misleading information with the use of claims verification mechanisms.
#     Analyze the trends across a large number of influential accounts over time in order to report on the influence of a narrative.
#     """

#     try:
#         response = model.generate_content(prompt)
#         return response.text
#     except Exception as e:
#         print(f"Error during Gemini analysis: {e}")
#         return "Analysis failed due to an error."


# def main():
#     """
#     Main function to connect to MongoDB, fetch Reddit posts in batches,
#     analyze them using the Gemini language model, and generate a story
#     based on the analysis results.
#     """
#     collection = connect_to_mongodb(MONGODB_URI, DATABASE_NAME, COLLECTION_NAME)
#     total_posts = collection.count_documents({})
#     story_response = ""
#     posts_processed = 0  # Keep track of the number of posts processed

#     for i in tqdm(range(0, total_posts, BATCH_SIZE), desc="Analyzing Posts"):
#         posts_batch = fetch_data_batch(collection, BATCH_SIZE, i)
#         if not posts_batch:
#             break  # No more data

#         analysis_result = analyze_posts_with_gemini(posts_batch)
#         story_response += analysis_result + "\n\n"

#         posts_processed += len(posts_batch)  # Increment the counter

#         print(f"Posts Processed: {posts_processed}") # Print after processing each batch

#     # Print or save the complete story_response
#     print("Final Analysis Story:\n", story_response)

#     #  Ideally, here is where you would visualize insights and build your dashboard,
#     #  potentially using the 'story_response' to inform the content and presentation.


# if __name__ == "__main__":
#     main()



# # some more better pormptfrom pymongo import MongoClientfrom pymongo import MongoClient
import json
import os
from typing import List, Dict
from pymongo import MongoClient
from bson import ObjectId
import time
import re
import logging
from tqdm import tqdm
import random  # Import random for sampling
import chromadb
from chromadb.utils import embedding_functions
# import openai # REMOVE OPEN AI import
import google.generativeai as genai # ADD Gemini import
import datetime

# Configure logging
logging.basicConfig(filename='gemini_analysis.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

MONGO_URI = "mongodb+srv://mahekpatel2612:W1ZcEtXDJ03AOtht@datatrial.5fxil.mongodb.net/"
DATABASE_NAME = "OriginalJSON"
COLLECTION_NAME = "JSONSIMPPL"

GOOGLE_API_KEY = "AIzaSyA5Yx2Ro2yl6Obsos3XjOuU2qVUtUlRWPA"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class JSONEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle ObjectId."""

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)


def fetch_data_from_mongodb(batch_size: int, skip: int) -> List[Dict]:
    """
    Fetches a batch of posts from MongoDB.  This is now just used for initial data retrieval.

    Args:
        batch_size: The number of posts to fetch in each batch.
        skip: The number of posts to skip from the beginning of the collection.

    Returns:
        A list of dictionaries, where each dictionary represents a post.  Returns an empty list if no more posts are available.
    """
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    posts = list(collection.find({}, {'_id': 0}).skip(skip).limit(batch_size))
    return posts



def create_embeddings_and_store(posts: List[Dict], collection_name: str = "reddit_posts"):
    """
    Creates embeddings for the Reddit posts using OpenAI and stores them in ChromaDB.

    Args:
        posts: A list of Reddit post dictionaries.
        collection_name: The name of the ChromaDB collection.
    """
    chroma_client = chromadb.PersistentClient(path="./chroma_db")  # Store DB locally

    # Choose OpenAI embeddings
    # COMMENT OUT OPEN AI EMBEDDING FUNCITON
    # openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    #     api_key=os.environ["OPENAI_API_KEY"],
    #     model_name="text-embedding-ada-002"  # Or your preferred model
    # )

    # USE OPEN AI API's FOR ONLY CREATING EMBEDDDING
    def generate_embedding(text: str):
        response = openai.Embedding.create(
            input=[text],
            model="text-embedding-ada-002" # Or your preferred model
        )
        return response["data"][0]["embedding"]

    # Create a Chroma collection with no embedding function
    # This is because we will add embeddings manually
    collection = chroma_client.get_or_create_collection(name=collection_name)

    ids = [str(i) for i in range(len(posts))]  # Generate unique IDs

    # Prepare texts and metadata
    texts = [post.get("title", "") + " " + post.get("selftext", "") for post in posts]  # Combine title and selftext

    # Convert created_utc to datetime and format
    metadatas = []
    for post in posts:
        created_utc = post.get("created_utc", None)
        if created_utc:
            try:
                # Convert UTC timestamp to datetime object
                dt_object = datetime.datetime.fromtimestamp(created_utc)
                # Format datetime object to string (e.g., "YYYY-MM-DD HH:MM:SS")
                formatted_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")
            except Exception as e:
                logging.warning(f"Error converting created_utc: {e}")
                formatted_time = None  # Or some default value

        else:
            formatted_time = None

        metadata = {
            "subreddit": post.get("subreddit", None),
            "author_fullname": post.get("author_fullname", None),
            "title": post.get("title", None),
            "downs": post.get("downs", None),
            "name": post.get("name", None),
            "upvote_ratio": post.get("upvote_ratio", None),
            "subreddit_type": post.get("subreddit_type", None),
            "ups": post.get("ups", None),
            "is_original_content": post.get("is_original_content", None),
            "likes": post.get("likes", None),
            "author": post.get("author", None),
            "num_comments": post.get("num_comments", None),
            "url": post.get("url", None),
            "subreddit_subscribers": post.get("subreddit_subscribers", None),
            "created_utc": formatted_time,  # Store formatted time string
        }
        metadatas.append(metadata)


    # Add data to ChromaDB
    try:
        embeddings = [generate_embedding(text) for text in texts]
        collection.add(
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids,
            documents=texts
        )
        print(f"Successfully added {len(posts)} embeddings to ChromaDB.")
    except Exception as e:
        logging.error(f"Error adding embeddings to ChromaDB: {e}")
        print(f"Error adding embeddings: {e}")


def retrieve_relevant_posts(query: str, num_results: int = 10, collection_name: str = "reddit_posts") -> List[Dict]:
    """
    Retrieves the most relevant Reddit posts from ChromaDB based on a query.

    Args:
        query: The search query.
        num_results: The number of results to retrieve.
        collection_name: The name of the ChromaDB collection.

    Returns:
        A list of dictionaries, where each dictionary represents a retrieved Reddit post.
    """
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    collection = chroma_client.get_collection(name=collection_name)

    # USE OPEN AI API's FOR ONLY CREATING EMBEDDDING
    embedding = openai.Embedding.create(
            input=[query],
            model="text-embedding-ada-002" # Or your preferred model
        )["data"][0]["embedding"]

    results = collection.query(
        query_embeddings=[embedding],
        n_results=num_results,
        include=["metadatas", "documents", "embeddings"]  # Include metadata and documents
    )

    # Combine results into a list of dictionaries
    retrieved_posts = []
    for i in range(len(results["ids"][0])):
        # Extract document (title + selftext)
        full_document = results["documents"][0][i]
        title = full_document.split(" ")[0]  # Assuming title is the first word
        selftext = " ".join(full_document.split(" ")[1:])  # The rest is selftext

        metadata = results["metadatas"][0][i]  # Get the metadata

        # Create the retrieved post dictionary
        post = {
            "subreddit": metadata.get("subreddit", None),
            "selftext": selftext,
            "author_fullname": metadata.get("author_fullname", None),
            "title": title,
            "downs": metadata.get("downs", None),
            "name": metadata.get("name", None),
            "upvote_ratio": metadata.get("upvote_ratio", None),
            "subreddit_type": metadata.get("subreddit_type", None),
            "ups": metadata.get("ups", None),
            "is_original_content": metadata.get("is_original_content", None),
            "likes": metadata.get("likes", None),
            "author": metadata.get("author", None),
            "num_comments": metadata.get("num_comments", None),
            "url": metadata.get("url", None),
            "subreddit_subscribers": metadata.get("subreddit_subscribers", None),
            "created_utc": metadata.get("created_utc", None),  # Already formatted
        }
        retrieved_posts.append(post)
    return retrieved_posts


def analyze_relevant_posts(posts: List[Dict], query: str):
    """Analyzes relevant Reddit posts using Gemini and returns insights.

    Args:
        posts: A list of Reddit post dictionaries.
        query: The original search query that retrieved these posts.

    Returns:
        A string containing the analysis of the posts.
    """

    data_string = json.dumps(posts, indent=2, cls=JSONEncoder)

    prompt = f"""You are an expert data analyst specializing in social media trends and misinformation detection.
You have been provided with a set of Reddit posts that are relevant to the query: '{query}'.

Here's the data from the relevant Reddit posts:
{data_string}

Analyze these posts to identify key themes, potential misinformation, and user sentiment related to the query.  Consider ALL available data points for each post, including subreddit, selftext, author_fullname, title, downs, name, upvote_ratio, subreddit_type, ups, is_original_content, likes, author, num_comments, url, subreddit_subscribers, and created_utc.

Instructions:

*   Summarize the main topics and themes discussed in the posts, considering the context of the subreddits they were posted in.
*   Identify any potential misinformation or misleading narratives, paying attention to the content of the posts (selftext), the authors, and the voting patterns (ups, downs, upvote_ratio).
*   Analyze the sentiment expressed in the posts (positive, negative, neutral). Consider the number of comments and the upvote ratio as indicators of sentiment.
*   Identify any influential users or communities driving the conversation, based on author names, subreddit types, and subscriber counts.
*   Provide actionable insights and recommendations based on your analysis. Consider the created_utc timestamps to identify trends over time.

Output Format:

Your response should be structured as follows:

*   Summary of Key Insights: A short overview of the most important findings.
*   Topic Analysis: A detailed breakdown of the main topics and themes, with examples of posts from different subreddits.
*   Sentiment Analysis: An analysis of the sentiment expressed in the posts, including examples of positive, negative, and neutral posts.
*   Potential Misinformation: Examples of posts containing potential misinformation, with explanations of why they are flagged.
*   Influential Users and Communities: Identification of influential users and communities, with an analysis of their activity and impact.
*   Actionable Insights and Recommendations: Concrete steps that could be taken to mitigate the spread of misinformation or address other issues, based on the data and your analysis.  Include recommendations for further analysis.
    """

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            retry_delay = extract_retry_delay(str(e))
            logging.error(f"Attempt {attempt + 1} failed: {e}")
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print(f"Waiting {retry_delay} seconds before retrying...")
                time.sleep(retry_delay)  # Use the retry_delay from the error
            else:
                raise  # Re-raise the exception if all retries fail


def extract_retry_delay(error_message: str) -> int:
    """Extracts the retry delay from the error message."""
    match = re.search(r"retry_delay\s*{\s*seconds:\s*(\d+)\s*}", error_message)
    if match:
        return int(match.group(1))
    return 10  # Default retry delay if not found (10 seconds)


def main():
    """
    Fetches posts from MongoDB, creates embeddings, stores them in ChromaDB,
    retrieves relevant posts based on a query, and analyzes them using Gemini.
    """
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    all_posts = list(collection.find({}, {'_id': 0}))  # Exclude _id field

    # 1. Create Embeddings and Store in ChromaDB
    create_embeddings_and_store(all_posts)

    # 2. Define a Query
    query = "Summarize sentiment analysis from reddit data with a lot of negative comments."  # Replace with your actual query

    # 3. Retrieve Relevant Posts
    relevant_posts = retrieve_relevant_posts(query, num_results=10)  # Adjust num_results

    # 4. Analyze Relevant Posts
    try:
        analysis = analyze_relevant_posts(relevant_posts, query)
        print("\n\nAnalysis of Relevant Posts:")
        print(analysis)

    except Exception as e:
        retry_delay = extract_retry_delay(str(e))
        logging.error(f"Error during analysis: {e}")
        print(f"Error during analysis: {e}")
        print(f"Waiting {retry_delay} seconds before retrying...")
        time.sleep(retry_delay)
        print("Analysis failed.")

    client.close()


if __name__ == "__main__":
    main()

# # each inidividual analysis will be displayed


# from pymongo import MongoClient
# import google.generativeai as genai
# import json
# from typing import List, Dict
# from tqdm import tqdm
# import logging
# from datetime import datetime

# # Configure logging
# logging.basicConfig(filename='data_analysis.log', level=logging.ERROR,
#                     format='%(asctime)s - %(levelname)s - %(message)s')

# MONGO_URI = "mongodb+srv://mahekpatel2612:W1ZcEtXDJ03AOtht@datatrial.5fxil.mongodb.net/"
# DATABASE_NAME = "OriginalJSON"
# COLLECTION_NAME = "JSONSIMPPL"

# GOOGLE_API_KEY = "AIzaSyA5Yx2Ro2yl6Obsos3XjOuU2qVUtUlRWPA"
# genai.configure(api_key=GOOGLE_API_KEY)
# model = genai.GenerativeModel('gemini-2.0-flash')

# def fetch_data_from_mongodb() -> List[Dict]:
#     """
#     Fetches all posts from MongoDB.
#     """
#     client = MongoClient(MONGO_URI)
#     db = client[DATABASE_NAME]
#     collection = db[COLLECTION_NAME]

#     all_posts = list(collection.find({}, {'_id': 0}))  # Exclude _id field

#     client.close()
#     return all_posts


# def extract_data_and_analyze(posts: List[Dict]) -> str:
#     """
#     Extracts key data points from posts and generates a report using Gemini.
#     """
#     num_posts = len(posts)
#     subreddit_counts = {}
#     author_activity = {}
#     link_domain_counts = {}
#     keyword_counts = {}
#     time_of_day_counts = {}  # Track time of day of posts
#     comment_lengths = []  # Track lengths of comments
#     all_keywords = []
#     # Customize this part to extract the data you want
#     for post in posts:
#         # Access data from the inner 'data' dictionary
#         post_data = post.get('data', {})

#         # Subreddit Analysis
#         subreddit = post_data.get('subreddit', 'Unknown Subreddit')
#         subreddit_counts[subreddit] = subreddit_counts.get(subreddit, 0) + 1

#         # Author Activity
#         author = post_data.get('author', 'Unknown Author')
#         author_activity[author] = author_activity.get(author, 0) + 1

#         # Link Domain Analysis (for linked posts)
#         domain = post_data.get('domain')
#         if domain:
#             link_domain_counts[domain] = link_domain_counts.get(domain, 0) + 1

#         # Time of Day Analysis
#         created_utc = post_data.get('created_utc')
#         if created_utc:
#             try:
#                 # Convert timestamp to datetime object
#                 post_time = datetime.fromtimestamp(created_utc)
#                 hour = post_time.hour  # Get the hour of the day
#                 time_of_day = f"{hour:02d}:00 - {hour+1:02d}:00"  # Create time range
#                 time_of_day_counts[time_of_day] = time_of_day_counts.get(time_of_day, 0) + 1
#             except Exception as e:
#                 logging.error(f"Error parsing timestamp: {e}")

#         # Comment Length Analysis (Placeholder - Requires comment data)
#         # This is just a placeholder.  You'll need to adapt this part
#         # based on how your comment data is structured within the JSON.
#         num_comments = post_data.get('num_comments',0)
#         if num_comments:
#             comment_lengths.append(num_comments)

#         # Keyword Analysis (from selftext and title)
#         text = post_data.get('selftext', '') or post_data.get('title', '')
#         keywords = ['misinformation', 'election', 'attack', 'scam', 'fraud', 'conspiracy']  # Add more keywords
#         for keyword in keywords:
#             if keyword in text.lower():
#                 keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
#                 all_keywords.append(keyword)

#         all_keywords_string = ",".join(all_keywords)

#     # Find top subreddits and authors
#     top_subreddits = sorted(subreddit_counts.items(), key=lambda x: x[1], reverse=True)[:5]  # Top 5
#     top_authors = sorted(author_activity.items(), key=lambda x: x[1], reverse=True)[:5]  # Top 5

#     # Calculate Average Comment Length
#     avg_comment_length = sum(comment_lengths) / len(comment_lengths) if comment_lengths else 0

#     # Create a prompt for Gemini
#     prompt = f"""You are an expert in analyzing Reddit data. You have been given a dataset of {num_posts} Reddit posts in JSON format. Your goal is to generate a report that summarizes the overall activity and insights contained within the data.

#     Specifically, your report should include the following:

#     *   **Overall Activity:** Provide a high-level overview of the dataset.
#         *   Total number of posts: {num_posts}

#     *   **Subreddit Analysis:** Which are the most prevalent subreddits. and the topics that go around.
#         *   Top 5 Subreddits: {top_subreddits}
#         *   Discuss the activity in the subreddits and why these subreddits might be more prevalent.

#     *   **Author Analysis:** Identify and analyze key details about the top authors in the dataset:
#         *   Top 5 Active Authors: {top_authors}
#         *   Discuss the activity of these authors. Are there anything we can interpret why there are more active.

#     *   **Link Domain Analysis:** Analyze what domains are shared in the dataset.
#         *   Most Frequent Link Domains: {link_domain_counts}
#         *   What does this mean that domains are being posted, and what kind of activity is it telling.

#     *   **Keyword Analysis:** Find trends in what people are talking about and what are key discussion trends.
#         *   Key discussion trends are:{all_keywords_string}

#     *   **Time of Day Analysis:** Analyze what time are the most posts getting posted.
#         *   Time of Day Distribution: {time_of_day_counts}

#     *   **Comment Analysis:** Get the key trends going on the comments
#         *Average number of comments is: {avg_comment_length}

#     Objective: Analyze the given dataset to identify key discussion topics, voting patterns, potential misinformation, and influential groups.

# Instructions:

# Identify the most discussed topics:

# Determine the themes or categories that appear most frequently.

# Highlight keywords, hashtags, or recurring phrases.

# Analyze post and voting behavior:

# Identify what types of content receive the most upvotes/downvotes.

# Detect any bias in the voting system (e.g., do certain topics always get positive or negative reactions?).

# Detect misinformation or misleading narratives:

# Identify posts containing potential misinformation by comparing claims against verified sources (if available).

# Flag posts with sensationalized or emotionally charged language.

# Highlight patterns in misleading content (e.g., repeated false claims).

# Identify influential groups or coordinated activity:

# Detect accounts or communities driving conversations on certain topics.

# Identify clusters of users who post similar content or vote in a coordinated manner.

# Look for patterns suggesting manipulation (e.g., sudden spikes in engagement).

# Highlight ethical or harmful trends (if any):

# Identify discussions that might be harmful (e.g., hate speech, targeted harassment).

# Point out any unethical behavior observed in the dataset.

# Output Format:

# Summary of Key Insights (short overview of findings)

# Topic Analysis (most discussed themes)

# Voting & Engagement Trends (popular post patterns)

# Potential Misinformation (examples and explanations)

# Influential Groups & Coordinated Activity

# Ethical Concerns & Recommendations


#     Based on the overall activity, author activity, subreddit analysis, link domain analysis, time of day analysis, average length, and keyword analysis, generate a detailed report.  What kind of message does it give and what is the activity doing.
#     """

#     try:
#         response = model.generate_content(prompt)
#         return response.text
#     except Exception as e:
#         logging.error(f"Error during analysis: {e}")
#         return f"Analysis failed: {e}"


# def main():
#     """
#     Fetches posts from MongoDB, extracts data, analyzes it, and generates a report.
#     """
#     posts = fetch_data_from_mongodb()

#     if not posts:
#         print("No posts found in MongoDB.")
#         return

#     report = extract_data_and_analyze(posts)
#     print("\nData Analysis Report:\n", report)


# if __name__ == "__main__":
#     main()