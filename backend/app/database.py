
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get MongoDB connection URI
MONGODB_URI = os.getenv("MONGODB_URI")

if not MONGODB_URI:
    raise ValueError("MONGODB_URI is missing from .env file")

# Connect to MongoDB
client = MongoClient(
    MONGODB_URI,
    serverSelectionTimeoutMS=5000
)

# Select database
db = client["ai_career_agent"]

# Select collection
learning_progress_collection = db["learning_progress"]


def check_database_connection():
    client.admin.command("ping")
    print("MongoDB connected successfully!")
