"""
FastAPI application for IoT event alerting and RabbitMQ message processing.
"""

import logging
import os
import threading
from contextlib import asynccontextmanager
from fastapi import FastAPI, BackgroundTasks, Query
import psycopg2
from psycopg2.extras import RealDictCursor
from RabbitMQ_consumer import start_consumer

# PostgreSQL connection parameters
DB_CONFIG = {
    'dbname': os.getenv('POSTGRES_DB', 'iot_events'),
    'user': os.getenv('POSTGRES_USER', 'new_admin'),
    'password': os.getenv('POSTGRES_PASSWORD', 'newer_password'),  # Ensure this is consistent across all scripts
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'port': int(os.getenv('POSTGRES_PORT', '5432')),  # Ensure the port is an integer
}

try:
    conn = psycopg2.connect(**DB_CONFIG)
    print("Connection successful!")
    conn.close()
except Exception as e:
    print(f"Error: {e}")

# Flag to track if the consumer is running

@asynccontextmanager
async def lifespan(_):
    """
    Lifespan context manager for managing startup and shutdown events.
    """
    yield

# Initialize FastAPI with lifespan
app = FastAPI(title="IoT Alerting Service", lifespan=lifespan)
consumer_thread = None

def run_consumer():
    global consumer_thread
    if not consumer_thread or not consumer_thread.is_alive():
        consumer_thread = threading.Thread(target=start_consumer, daemon=True)
        consumer_thread.start()

@app.get("/")
def root():
    return {"message": "Welcome to the IoT Alerting Service"}

@app.post("/start-consumer")
def start_consumer_endpoint(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_consumer)
    return {"message": "RabbitMQ consumer is starting in the background."}

@app.get("/alerts")
def get_alerts(event_type: str = Query(None), limit: int = Query(10)):
    try:
        logging.info("Querying alerts with event_type: %s, limit: %d", event_type, limit)
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = "SELECT * FROM alerts"
                params = []
                if event_type:
                    query += " WHERE type = %s"
                    params.append(event_type)
                query += " ORDER BY id DESC LIMIT %s"
                params.append(limit)
                logging.info("Executing query: %s with params: %s", query, params)
                cursor.execute(query, params)
                results = cursor.fetchall()
                logging.info("Query results: %s", results)
                return {"alerts": results}
    except Exception as e:
        logging.error("Error querying alerts: %s", e)
        return {"error": str(e)}
