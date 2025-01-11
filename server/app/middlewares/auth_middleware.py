from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify

# Middleware to protect routes
@jwt_required()
def protected_route():
    current_user = get_jwt_identity()
    return jsonify({"msg": "Protected route accessed", "user": current_user}), 200
