from flask import request, jsonify
from services.mongo_service import workouts_collection, routes_collection
from flask_jwt_extended import get_jwt_identity, jwt_required
from bson import ObjectId
from datetime import datetime, timezone, timedelta
import pytz

@jwt_required()
def save_workout():
    user_id = get_jwt_identity() 
    data = request.json

    # Validate input
    if not data.get("route_id") or not data.get("duration"):
        return jsonify({"error": "route_id and duration are required"}), 400

    # Validate duration format (minutes and seconds)
    duration = data["duration"]
    if not isinstance(duration, dict) or "minutes" not in duration or "seconds" not in duration:
        return jsonify({"error": "Duration must include 'minutes' and 'seconds' fields"}), 400

    # Get the route from Mongo based on route_id
    route = routes_collection.find_one({"_id": ObjectId(data["route_id"])})
    if not route:
        return jsonify({"error": "Route not found"}), 404

    # Get the coordinates from the retrieved route
    coordinates = route.get("geometry", {}).get("coordinates", [])
    if not coordinates:
        return jsonify({"error": "Coordinates not found for the given route"}), 404
    
    # Adjust to Romania's time zone (UTC+2)
    tz_romania = pytz.timezone("Europe/Bucharest")
    utc_time = datetime.now(timezone.utc)
    romania_time = utc_time.astimezone(tz_romania)
    
    # Default workout name if not provided
    romania_time_str = romania_time.strftime("%Y-%m-%d %H:%M")
    default_workout_name = f"Workout {romania_time.strftime('%Y-%m-%d')} at {romania_time.strftime('%H:%M')}"
    workout_name = data.get("workout_name", default_workout_name)

    workout = {
        "user_id": user_id, # Retrieve user ID from JWT token
        "workout_name": workout_name,
        "route_id": ObjectId(data["route_id"]),  # Store route ID together with its coordinates
        "coordinates": coordinates,
        "date": data.get("date", romania_time_str), # YYYY-MM-DD HH:MM
        "distance": data["distance"],  # kilometers // TODO: CALCULEZ DE PE KAMOOT
        "duration": {
            "minutes": duration["minutes"],
            "seconds": duration["seconds"]
        }
    }

    workouts_collection.insert_one(workout)
    return jsonify({"message": "Workout saved successfully"}), 201

@jwt_required()
def fetch_user_workouts():
    user_id = get_jwt_identity()
    workouts = list(workouts_collection.find({"user_id": user_id}))
    
    # Serialize ObjectId
    for workout in workouts:
        workout["_id"] = str(workout["_id"])
        workout["route_id"] = str(workout["route_id"])

    return jsonify({"workouts": workouts}), 200

