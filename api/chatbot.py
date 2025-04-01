# chatbot.py
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
import os
from pymongo import MongoClient
from dotenv import load_dotenv
import re

load_dotenv()

# Configuration
CHROMA_PATH = "chroma_db"
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME")

embeddings_model = OllamaEmbeddings(model="mistral")
llm = Ollama(model="mistral", temperature=0.5)

# MongoDB Connection
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION_NAME]

# ChromaDB Connection
vector_store = Chroma(
    collection_name="ollama_example_collection",
    embedding_function=embeddings_model,
    persist_directory=CHROMA_PATH,
)
retriever = vector_store.as_retriever(search_kwargs={'k': 5})


def extract_title(text):
    """Extracts a title enclosed in single or double quotes from the given text."""
    match = re.search(r"['\"](.*?)['\"]", text)
    return match.group(1) if match else None

def extract_author(text):
    """Extracts an author name from the text."""
    match = re.search(r"\b[A-Z][a-z]+\b", text)
    return match.group(0) if match else None

def get_response(message):
    """Handles user messages and generates responses, querying MongoDB directly for specific questions."""

    message_lower = message.lower()

    if "upvote ratio" in message_lower:
        title = extract_title(message)
        if not title:
            return "Could not extract the title from the query."

        post = collection.find_one({"data.title": title})
        if post:
            ratio = post["data"].get("upvote_ratio", "unknown")
            return f"The upvote ratio for the post '{title}' is {ratio}."
        else:
            return "Could not find a post with that title."

    elif "ups/downs" in message_lower or "upvotes/downvotes" in message_lower:
        title = extract_title(message)
        if not title:
            return "Could not extract the title from the query."

        post = collection.find_one({"data.title": title})
        if post:
            ups = post["data"].get("ups", "unknown")
            downs = post["data"].get("downs", "unknown")
            return f"The post '{title}' has {ups} upvotes and {downs} downvotes."
        else:
            return "Could not find a post with that title."

    elif "number of post" in message_lower and "author" in message_lower:
        author = extract_author(message)
        if not author:
            return "Could not extract the author's name from the query."
        count = collection.count_documents({"data.author": author})
        return f"The author '{author}' has {count} posts."

    elif ("number of comments" in message_lower or "number of upvotes" in message_lower) and "topic" in message_lower:
        title = extract_title(message)
        if not title:
            return "Could not extract the title from the query."
        post = collection.find_one({"data.title": title})
        if post:
            num_comments = post["data"].get("num_comments", "unknown")
            ups = post["data"].get("ups", "unknown")
            return f"The post '{title}' has {num_comments} comments and {ups} upvotes."
        else:
            return "Could not find a post with that title."

    elif "how many posts has these titles" in message_lower:
         title = extract_title(message)
         if not title:
            return "Could not extract the title from the query."
         count = collection.count_documents({"data.title": title})
         return f"There are {count} posts with the title '{title}'."


    else:
        # Standard RAG flow for other questions
        docs = retriever.invoke(message)
        knowledge = "".join([doc.page_content + "\n\n" for doc in docs])

        rag_prompt = f"""
        You are an assistent which answers questions based on knowledge which is provided to you.
        While answering, you don't use your internal knowledge, 
        but solely the information in the "The knowledge" section.
        You don't mention anything to the user about the provided knowledge.

        The question: {message}

        Conversation history: {history}

        The knowledge: {knowledge}
        """

        #return the model resposne
        return llm(rag_prompt)