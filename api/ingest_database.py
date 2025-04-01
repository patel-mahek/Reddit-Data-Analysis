# ingest_database.py
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from pymongo import MongoClient
from uuid import uuid4
import os

# configuration
CHROMA_PATH = "chroma_db"
MONGO_URI = os.getenv("MONGO_URI")  # Ensure this is set in your .env file
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")  # Ensure this is set in your .env file
MONGO_COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME") # Ensure this is set in your .env file

# embeddings_model = OpenAIEmbeddings(model="text-embedding-3-large")  # Removed OpenAI dependency
embeddings_model = OllamaEmbeddings(model="mistral") # Using ollama embeddings instead

# connecting to MongoDB
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION_NAME]

# retrieving all documents from MongoDB
documents = list(collection.find())

# Extracting text content from MongoDB documents
# Adjust the key based on your JSON structure
texts = []
for doc in documents:
    try:
        # Prioritize 'selftext' if it exists, otherwise use 'title'
        if 'selftext' in doc['data'] and doc['data']['selftext']:
            texts.append(doc['data']['selftext'])
        elif 'title' in doc['data']:
            texts.append(doc['data']['title'])
        else:
            texts.append("")  # Add an empty string if neither field exists
    except KeyError as e:
        print(f"Error extracting text from document: {doc}.  Missing key: {e}")
        texts.append("") # Append an empty string to avoid breaking the process

# initiate the vector store
vector_store = Chroma(
    collection_name="ollama_example_collection", # changed the collection name
    embedding_function=embeddings_model,
    persist_directory=CHROMA_PATH,
)

# splitting the document
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=100,
    length_function=len,
    is_separator_regex=False,
)

# creating the chunks
chunks = text_splitter.create_documents(texts)

# creating unique ID's
uuids = [str(uuid4()) for _ in range(len(chunks))]

# adding chunks to vector store
vector_store.add_documents(documents=chunks, ids=uuids)

vector_store.persist() #important

print("Data ingested and stored in ChromaDB.")