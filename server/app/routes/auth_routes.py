from flask import Blueprint
from controllers.auth_controller import register_user, login_user
from middlewares.auth_middleware import protected_route

# Flask Blueprint to group all authentication-related endpoints
auth_blueprint = Blueprint('auth', __name__) 

auth_blueprint.route('/register', methods=['POST'])(register_user)
auth_blueprint.route('/login', methods=['POST'])(login_user)
auth_blueprint.route('/protected', methods=['GET'])(protected_route)

