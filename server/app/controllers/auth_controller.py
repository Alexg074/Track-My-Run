from flask import request, jsonify
from flask_jwt_extended import create_access_token
from services.mongo_service import users_collection
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

def register_user():
    try:
        data = request.json
        email = data['email']
        password = data['password']
        username = data['username']

        # Check if user already exists
        if users_collection.find_one({"email": email}):
            return jsonify({"error": "User already exists"}), 400

        # Hash the password
        password_hash = generate_password_hash(password)

        # Save user to database
        user_id = users_collection.insert_one({
            "email": email,
            "password": password_hash,
            "username": username
        }).inserted_id

        return jsonify({"message": "User registered", "user_id": str(user_id)}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def login_user():
    try:
        data = request.json
        email = data['email']
        password = data['password']

        # Fetch user from database
        user = users_collection.find_one({"email": email})

        if not user or not check_password_hash(user['password'], password):
            return jsonify({"error": "Invalid email or password"}), 401

        # Generate JWT token at login
        token = create_access_token(identity=str(user['_id']), additional_claims={"email": user['email']})
        
        return jsonify({"token": token, "username": user['username']}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
