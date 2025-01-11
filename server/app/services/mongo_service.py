import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')

# Initialize MongoDB Client
client = MongoClient(MONGO_URI)
db = client.trackmyrun

# Collections 
users_collection = db.users
workouts_collection = db.workouts
routes_collection = db.routes
messages_collection = db.messages
