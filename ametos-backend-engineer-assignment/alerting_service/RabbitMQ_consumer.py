import json
import os
import pika
import psycopg2
from psycopg2.extras import RealDictCursor

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
        cursor.close()
        conn.close()
        print(f"Alert saved to database: {alert}")
    except Exception as e:
        print(f"Failed to save alert to database: {e}")

def process_event(event):
    """
    Processes an incoming event and determines if it should generate an alert.
    """
    alert = None
    try:
        if event.get('event_type') == 'access_attempt' and event.get('user_id') == 'unauthorized_user':
            alert = {
                'type': 'Unauthorized Access',
                'message': 'Unauthorized access attempt detected!',
                'details': event,
            }
        elif event.get('event_type') == 'speed_violation' and event.get('speed_kmh', 0) > 90:
            alert = {
                'type': 'Speed Violation',
                'message': 'Speed violation detected!',
                'details': event,
            }
        elif (event.get('event_type') == 'motion_detected' and 
              event.get('zone') == 'Restricted Area' and 
              event.get('confidence', 0) > 0.9):
            alert = {
                'type': 'Intrusion Detection',
                'message': 'Intrusion detected in a restricted area!',
                'details': event,
            }
    except Exception as ex:
        print(f"Error processing event: {ex}")
    return alert

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
                print(f"Received: {event}")
                alert = process_event(event)
                if alert:
                    save_alert_to_db(alert)
            except Exception as ex:
                print(f"Error processing message: {ex}")

        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        print(f"Connected to RabbitMQ on {host}, waiting for messages...")
        channel.start_consuming()
    except Exception as e:
        print(f"RabbitMQ connection error: {e}")
