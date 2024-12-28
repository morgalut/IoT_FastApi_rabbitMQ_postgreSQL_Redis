import os
from fastapi import FastAPI, BackgroundTasks, Query
from contextlib import asynccontextmanager
import threading
import psycopg2
from psycopg2.extras import RealDictCursor
from RabbitMQ_consumer import start_consumer

DB_CONFIG = {
    'dbname': os.getenv('POSTGRES_DB', 'iot_events'),
    'user': os.getenv('POSTGRES_USER', 'admin'),
    'password': os.getenv('POSTGRES_PASSWORD', 'new_password'),  # Update this line
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'port': os.getenv('POSTGRES_PORT', 5432),
}


try:
    conn = psycopg2.connect(**DB_CONFIG)
    print("Connection successful!")
    conn.close()
except Exception as e:
    print(f"Error: {e}")

# Flag to track if the consumer is running
consumer_thread = None

@asynccontextmanager
async def lifespan(app: FastAPI):
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
    global consumer_thread
    if not consumer_thread or not consumer_thread.is_alive():
        consumer_thread = threading.Thread(target=start_consumer, daemon=True)
        consumer_thread.start()

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

