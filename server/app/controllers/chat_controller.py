from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from services.mongo_service import messages_collection
from services.rabbit_service import send_group_message, start_group_consumer

# Send a group message to all participants
@jwt_required()
def send_message():
    user_id = get_jwt_identity()
    data = request.json

    message = data.get("message")
    if not message:
        return jsonify({"error": "Message content is required"}), 400

    try:
        # Send message using RabbitMQ - handles both MongoDB storage and RabbitMQ publishing
        rabbit_response = send_group_message(user_id, message)

        if rabbit_response["status"] == "success":
            return jsonify({"message": "Message sent successfully"}), 200
        else:
            return jsonify({"error": rabbit_response["message"]}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get chat history for the group chat
@jwt_required()
def get_chat_history():
    try:
        messages = list(messages_collection.find().sort("timestamp", 1)) # cursor that returns all messages sorted by timestamp
        
        for message in messages:
            message["_id"] = str(message["_id"])

        return jsonify({"messages": messages}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Start listening to group messages for a specific user
def listen_to_group_messages(username):
    def callback(message):
        print(f"[{username}] Received message: {message}")

    start_group_consumer(username, callback)
