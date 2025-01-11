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

# Indexes to ensure data integrity and query efficiency
# def initialize_indexes():
#     # Users Collection Indexes
#     users_collection.create_index("email", unique=True)
#     users_collection.create_index("username", unique=True)

#     # Workouts Collection Indexes
#     workouts_collection.create_index("user_id")
#     workouts_collection.create_index("date")

#     # Routes Collection Indexes
#     routes_collection.create_index("user_id")

#     # Messages Collection Indexes
#     messages_collection.create_index("sender_id")
#     messages_collection.create_index("receiver_id")

#     print("Indexes have been initialized.")

# # Call this function to ensure indexes are created
# initialize_indexes()

# # Testing
# def insert_mock_data():
#     users_collection.insert_one({
#         "username": "testuser",
#         "email": "test@example.com",
#         "password_hash": "hashedpassword123",
#         "profile_details": {"age": 30, "bio": "Runner"}
#     })

#     workouts_collection.insert_one({
#         "user_id": "some_user_id",
#         "date": "2024-12-15",
#         "duration": 45,
#         "distance": 10.5,
#         "route": "Park Route",
#         "statistics": {"calories": 300, "pace": "4:30"}
#     })

#     routes_collection.insert_one({
#         "user_id": "some_user_id",
#         "name": "Evening Run",
#         "coordinates": [[40.7128, -74.0060], [40.7138, -74.0070]],
#         "popularity": 100
#     })

#     messages_collection.insert_one({
#         "sender_id": "user1",
#         "receiver_id": "user2",
#         "message": "Let's run tomorrow!",
#         "timestamp": "2024-12-15T08:00:00Z"
#     })

#     print("Mock data inserted.")

# # Call this function to add sample data
# insert_mock_data()
