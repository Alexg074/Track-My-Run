from flask import Blueprint
from controllers.workout_controller import save_workout, fetch_user_workouts

# Create a Blueprint for route-related endpoints
workout_blueprint = Blueprint('workout', __name__)

# Define routes and link them to controller functions
workout_blueprint.route('/save', methods=['POST'])(save_workout)
workout_blueprint.route('/user-workouts', methods=['GET'])(fetch_user_workouts)
