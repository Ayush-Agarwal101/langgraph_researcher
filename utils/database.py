# FILE: utils/database.py

import pymongo
from pymongo import errors
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

try:
    client = pymongo.MongoClient(MONGO_URI)
    client.admin.command('ping')
    print("✅ MongoDB connection successful.")
    db = client["autonomous_researcher_db"]
    knowledge_graph_collection = db["knowledge_graph"]
except errors.ConnectionFailure as e:
    print(f"❌ Could not connect to MongoDB: {e}")
    db = None
    knowledge_graph_collection = None
    knowledge_graph_collection = None