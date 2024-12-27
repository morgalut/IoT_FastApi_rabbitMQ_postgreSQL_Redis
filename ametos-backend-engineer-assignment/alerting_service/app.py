from fastapi import FastAPI, BackgroundTasks, Query
from contextlib import asynccontextmanager
import threading
import psycopg2
from psycopg2.extras import RealDictCursor
from RabbitMQ_consumer import start_consumer

DB_CONFIG = {
    'dbname': 'iot_events',
    'user': 'admin',
    'password': '1234',
    'host': 'localhost',
    'port': 5432,
}

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
        cursor.close()
        conn.close()
        return {"alerts": alerts}
    except Exception as e:
        return {"error": str(e)}
