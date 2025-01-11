import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
from pymongo import MongoClient
from routes.auth_routes import auth_blueprint
from routes.route_routes import route_blueprint
from routes.workout_routes import workout_blueprint

# Load environment variables
load_dotenv()

# Verify JWT_SECRET_KEY is loaded
print("JWT_SECRET_KEY:", os.getenv('JWT_SECRET_KEY'))

# Initialize Flask app
app = Flask(__name__)

# Configure app
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY', 'your_secret_key')
JWTManager(app)
CORS(app)

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["trackmyrun"]
routes_collection = db["routes"]

def preprocess_routes():
    # Drop existing indexes to avoid GeoJSON validation errors
    routes_collection.drop_indexes()
    print("Dropped all indexes on the routes collection.")

    # Preprocess routes
    for route in routes_collection.find():
        try:
            if "features" in route:
                geometry = route["features"][0].get("geometry", {})
                if geometry.get("type") == "MultiLineString":
                    processed_coordinates = [
                        [[coord[0], coord[1]] for coord in line]
                        for line in geometry.get("coordinates", [])
                    ]

                    # Update the route document with geometry and distance
                    routes_collection.update_one(
                        {"_id": route["_id"]},
                        {
                            "$set": {
                                "geometry": {
                                    "type": "MultiLineString",
                                    "coordinates": processed_coordinates,
                                },
                            },
                            "$unset": {"features": ""}
                        }
                    )
                    print(f"Processed route with _id: {route['_id']}")
            else:
                print(f"Skipping route with _id: {route['_id']} - No features found.")
        except Exception as e:
            print(f"Error processing route with _id: {route['_id']}: {e}")

    print("All routes have been preprocessed.")

    # Recreate geospatial index
    routes_collection.create_index([("geometry", "2dsphere")])
    print("Geospatial index created on geometry field.")

# Preprocess routes before starting the server
print("Preprocessing routes...")
preprocess_routes()
print("Preprocessing completed.")

# Create geospatial index
routes_collection.create_index([("geometry", "2dsphere")])
print("Geospatial index created on geometry field.")

# Register blueprints
app.register_blueprint(auth_blueprint, url_prefix='/api/auth')
app.register_blueprint(route_blueprint, url_prefix='/api/routes')
app.register_blueprint(workout_blueprint, url_prefix='/api/workouts')

# Root route
@app.route('/')
def home():
    return "Welcome to the Flask API!"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
