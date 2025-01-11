from flask import Blueprint
from controllers.route_controller import find_nearby_routes

# Create a Blueprint for route-related endpoints
route_blueprint = Blueprint('route', __name__)

# Define routes and link them to controller functions
route_blueprint.route('/find-nearby', methods=['POST'])(find_nearby_routes)
