from flask import Blueprint
from controllers.chat_controller import send_message, get_chat_history

chat_blueprint = Blueprint('chat', __name__)

# Define routes and link them to controller functions
chat_blueprint.route('/send', methods=['POST'])(send_message)
chat_blueprint.route('/history', methods=['GET'])(get_chat_history)
