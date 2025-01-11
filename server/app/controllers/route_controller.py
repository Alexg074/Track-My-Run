from flask import request, jsonify
from services.mongo_service import routes_collection
from flask_jwt_extended import get_jwt_identity, jwt_required
import geojson
from bson import ObjectId

# @jwt_required()
def find_nearby_routes(): # in functie de locatia curenta
    data = request.json
    longitude = data.get("longitude")
    latitude = data.get("latitude")
    max_distance = data.get("max_distance")

    if longitude is None or latitude is None:
        return jsonify({"error": "Longitude and latitude are required"}), 400

    # GeoJSON Point
    point = {
        "type": "Point",
        "coordinates": [longitude, latitude]
    }

    try:
        # Geospatial query
        routes = list(
            routes_collection.find({
                "geometry": {
                    "$near": {
                        "$geometry": point,
                        "$maxDistance": max_distance
                    }
                }
            })
        )

        # Serialize ObjectId
        for route in routes:
            route["_id"] = str(route["_id"])
            route["name"] = f"Route {route['_id']}"
            

        return jsonify({"routes": routes}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
