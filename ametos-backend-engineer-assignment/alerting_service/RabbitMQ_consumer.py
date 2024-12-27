import logging
import json
import os
import pika
import psycopg2

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# PostgreSQL connection parameters
DB_CONFIG = {
    'dbname': os.getenv('POSTGRES_DB', 'iot_events'),
    'user': os.getenv('POSTGRES_USER', 'admin'),
    'password': os.getenv('POSTGRES_PASSWORD', '1234'),
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'port': os.getenv('POSTGRES_PORT', 5432),
}


def save_alert_to_db(alert):
    """
    Save an alert to the PostgreSQL database.
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO alerts (type, message, details)
            VALUES (%s, %s, %s)
            """,
            (alert['type'], alert['message'], json.dumps(alert['details']))
        )
        conn.commit()
        logging.info(f"Alert saved to database: {alert}")
    except Exception as e:
        logging.error(f"Failed to save alert to database: {e}")

def process_event(event):
    """
    Processes an incoming event and determines if it should generate an alert.
    """
    try:
        if event.get('event_type') == 'access_attempt' and event.get('user_id') == 'unauthorized_user':
            alert = {
                'type': 'Unauthorized Access',
                'message': 'Unauthorized access attempt detected!',
                'details': event,
            }
        # Add logging to show what event is being processed
        logging.info(f"Processing event: {event}")
        return alert
    except Exception as ex:
        logging.error(f"Error processing event: {ex}")
        return None

def start_consumer():
    """
    Starts the RabbitMQ consumer to listen for messages and process events.
    """
    host = os.getenv('RABBITMQ_HOST', 'localhost')
    queue_name = os.getenv('RABBITMQ_QUEUE', 'iot_events')
    credentials = pika.PlainCredentials(
        os.getenv('RABBITMQ_USER', 'guest'), 
        os.getenv('RABBITMQ_PASSWORD', 'guest')
    )
    parameters = pika.ConnectionParameters(host=host, credentials=credentials)

    try:
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)

        def callback(ch, method, properties, body):
            try:
                event = json.loads(body)
                logging.info(f"Received: {event}")
                alert = process_event(event)
                if alert:
                    save_alert_to_db(alert)
            except Exception as ex:
                logging.error(f"Error processing message: {ex}")

        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        logging.info(f"Connected to RabbitMQ on {host}, waiting for messages...")
        channel.start_consuming()
    except Exception as e:
        logging.error(f"RabbitMQ connection error: {e}")
