from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["trackmyrun"]
routes_collection = db["routes"]

# Update all routes with a default name
routes = routes_collection.find()
for route in routes:
    route_name = f"Route {route['_id']}"  # Generate route name
    routes_collection.update_one(
        {"_id": route["_id"]},  
        {"$set": {"name": route_name}} 
    )
    print(f"Updated route {route['_id']} with name '{route_name}'")
