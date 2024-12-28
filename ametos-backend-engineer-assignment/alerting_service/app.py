"""
FastAPI application for IoT event alerting and RabbitMQ message processing.
"""

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
CONSUMER_THREAD = None

@asynccontextmanager
async def lifespan(_):
    """
    Lifespan context manager for managing startup and shutdown events.
    """
    yield

# Initialize FastAPI with lifespan
app = FastAPI(title="IoT Alerting Service", lifespan=lifespan)

def run_consumer():
    """
    Wrapper function to start the RabbitMQ consumer in a thread.
    """
    global CONSUMER_THREAD
    if not CONSUMER_THREAD or not CONSUMER_THREAD.is_alive():
        CONSUMER_THREAD = threading.Thread(target=start_consumer, daemon=True)
        CONSUMER_THREAD.start()

@app.get("/")
def root():
    """
    Root endpoint to check the service status.
    """
    return {"message": "Welcome to the IoT Alerting Service"}

@app.post("/start-consumer")
def start_consumer_endpoint(background_tasks: BackgroundTasks):
    """
    Endpoint to manually start the RabbitMQ consumer.
    """
    background_tasks.add_task(run_consumer)
    return {"message": "RabbitMQ consumer is starting in the background."}

@app.get("/alerts")
def get_alerts(event_type: str = Query(None), limit: int = Query(10)):
    """
    Retrieve alerts from the database with optional filters.
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        query = "SELECT * FROM alerts"
        params = []

        if event_type:
            query += " WHERE type = %s"
            params.append(event_type)

        query += " ORDER BY id DESC LIMIT %s"
        params.append(limit)

        cursor.execute(query, params)
        alerts = cursor.fetchall()
        return {"alerts": alerts}
    except psycopg2.Error as db_error:
        return {"error": f"Database error: {db_error}"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()
