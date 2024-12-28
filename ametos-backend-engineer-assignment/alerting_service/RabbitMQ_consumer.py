"""
Module for consuming RabbitMQ messages and processing events to trigger alerts.
"""

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
    'port': int(os.getenv('POSTGRES_PORT', '5432')),  # Ensure the port is an integer
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
        logging.info("Alert saved to database: %s", alert)
    except Exception as e:
        logging.error("Failed to save alert to database: %s", e)


def process_event(event):
    """
    Processes an incoming event and determines if it should generate an alert.
    """
    alert = None  # Initialize alert to None to avoid use-before-assignment issues
    try:
        if event.get('event_type') == 'access_attempt' and event.get('user_id') == 'unauthorized_user':
            alert = {
                'type': 'Unauthorized Access',
                'message': 'Unauthorized access attempt detected!',
                'details': event,
            }
        logging.info("Processing event: %s", event)  # Use lazy % formatting
        return alert
    except Exception as ex:
        logging.error("Error processing event: %s", ex)
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
            """
            Callback function for handling messages.
            """
            try:
                event = json.loads(body)
                logging.info("Received: %s", event)
                alert = process_event(event)
                if alert:
                    save_alert_to_db(alert)
            except Exception as ex:
                logging.error("Error processing message: %s", ex)

        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        logging.info("Connected to RabbitMQ on %s, waiting for messages...", host)
        channel.start_consuming()
    except Exception as e:
        logging.error("RabbitMQ connection error: %s", e)

