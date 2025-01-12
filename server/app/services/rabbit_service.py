import pika
import threading
from datetime import datetime, timezone
import pytz
from services.mongo_service import messages_collection
import os
from dotenv import load_dotenv

# Load environment variables for RabbitMQ config
load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")
GROUP_CHAT_EXCHANGE = os.getenv("RABBITMQ_EXCHANGE", "group_chat_exchange")

def get_rabbitmq_connection():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    return pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            credentials=credentials
        )
    )

# Sends a message to the group chat exchange and also stores it in MongoDB 
def send_group_message(username, message):
    try:
        # Connect to RabbitMQ
        connection = get_rabbitmq_connection()
        channel = connection.channel()

        # Declare fanout exchange
        channel.exchange_declare(exchange=GROUP_CHAT_EXCHANGE, exchange_type='fanout')

        # Message timestamp 
        tz_romania = pytz.timezone("Europe/Bucharest")
        utc_time = datetime.now(timezone.utc)
        timestamp = utc_time.astimezone(tz_romania).strftime("%Y-%m-%d %H:%M:%S")
        full_message = f"{timestamp} | {username}: {message}"

        # Publish the message
        channel.basic_publish(exchange=GROUP_CHAT_EXCHANGE, routing_key='', body=full_message)

        # Persist the message in Mongo
        messages_collection.insert_one({
            "username": username,
            "message": message,
            "timestamp": timestamp
        })
        
        # Close connection
        connection.close()

        return {"status": "success", "message": "Message sent successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# Starts a consumer that listens to group messages for a specific user
def start_group_consumer(username, callback):
    """
    1. Declares a unique queue for the user.
    2. Binds the queue to the fanout exchange.
    3. Starts consuming messages and calls the callback function whenever a new message arrives.
    4. Runs the consumer in a separate thread for non-blocking operation.
    """
    def listen_to_messages():
        try:
            # Connect to RabbitMQ
            connection = get_rabbitmq_connection()
            channel = connection.channel()

            # Declare the fanout exchange
            channel.exchange_declare(exchange=GROUP_CHAT_EXCHANGE, exchange_type='fanout')

            # Declare a unique queue for the user
            queue_name = f"groupChat.{username}"
            channel.queue_declare(queue=queue_name, exclusive=True)
            channel.queue_bind(exchange=GROUP_CHAT_EXCHANGE, queue=queue_name)

            # Define the callback for consuming messages
            def on_message(ch, method, properties, body):
                callback(body.decode())

            # Start consuming messages
            channel.basic_consume(queue=queue_name, on_message_callback=on_message, auto_ack=True)
            print(f"{username} is now listening to group messages...")
            channel.start_consuming()
            
        except Exception as e:
            print(f"Error starting consumer for {username}: {e}")

    # Run the consumer in a separate thread to keep it non-blocking
    threading.Thread(target=listen_to_messages, daemon=True).start()
