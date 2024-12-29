"""
This module handles the consumption of messages from RabbitMQ and processing those messages to generate and store alerts.
"""

import logging
import json
import os
import threading
import signal
import time
import pika
import psycopg2
from alert_rules import process_event

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# PostgreSQL connection parameters
DB_CONFIG = {
    'dbname': os.getenv('POSTGRES_DB', 'iot_events'),
    'user': os.getenv('POSTGRES_USER', 'new_admin'),
    'password': os.getenv('POSTGRES_PASSWORD', 'newer_password'),
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'port': int(os.getenv('POSTGRES_PORT', '5432'))
}

RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'new_user')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'new_password')
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', '5672'))
QUEUE_NAME = 'iot_events'

# Signal Handling
stop_thread = threading.Event()

def signal_handler(signum, _frame):
    """Handles incoming signals by logging and setting a stop event."""
    logging.info("Signal received, shutting down...")
    stop_thread.set()

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def connect_with_retry(max_retries=5):
    """Attempt to connect to RabbitMQ with a retry mechanism."""
    for attempt in range(max_retries):
        if stop_thread.is_set():
            logging.info("Shutdown signal received, stopping connection attempts.")
            return None
        try:
            credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
            parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)
            return pika.BlockingConnection(parameters)
        except pika.exceptions.AMQPConnectionError as e:
            wait_time = min(2 ** attempt, 30)
            logging.error("Connection attempt %d failed. Retrying in %d seconds...", attempt + 1, wait_time)
            time.sleep(wait_time)
    raise Exception("Failed to connect to RabbitMQ after several attempts.")

def save_alert_to_db(alert):
    """Save an alert to the PostgreSQL database."""
    logging.info("Attempting to save alert: %s", alert['message'])
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO alerts (type, message, details)
                    VALUES (%s, %s, %s)
                    """,
                    (alert['type'], alert['message'], json.dumps(alert['details']))
                )
                conn.commit()
                logging.info("Alert saved successfully.")
    except psycopg2.Error as e:
        logging.error("Failed to save alert to database: %s", str(e))

def start_consumer():
    """Start the RabbitMQ consumer."""
    connection = connect_with_retry()
    if connection is None:
        return
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_qos(prefetch_count=1)

def callback(ch, method, _properties, body):
    """Process incoming messages and generate alerts."""
    try:
        event = json.loads(body)
        logging.info("Received event: %s", event)
        alert = process_event(event)
        if alert:
            logging.info("Generated alert: %s", alert)
            save_alert_to_db(alert)
        else:
            logging.info("No alert generated for event: %s", event)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except json.JSONDecodeError as e:
        logging.error("Failed to process message: %s", str(e))
