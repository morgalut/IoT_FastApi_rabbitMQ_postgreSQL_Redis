from typing import Optional
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Event, EventModel
from dependencies import get_redis, get_db
from device_management import DeviceManager
import logging
from datetime import datetime

app = FastAPI(title="IoT Event Ingestion Service")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.on_event("startup")
def startup_event():
    redis_client = get_redis()
    device_manager = DeviceManager(redis_client)
    try:
        device_manager.register_device("AA:BB:CC:DD:EE:FF", "Security Camera")
        device_manager.register_device("11:22:33:44:55:66", "Radar")
        logger.info("All devices registered successfully.")
    except Exception as e:
        logger.error(f"Failed to register devices: {str(e)}")

def process_event_for_alerts(event: Event, redis_client):
    # Example criteria: Alert if a security camera detects motion at night
    if event.event_type == "motion_detected" and redis_client.get(event.device_id) == "Security Camera":
        current_hour = datetime.now().hour
        if 18 <= current_hour or current_hour <= 6:
            send_alert(f"Motion detected by {event.device_id} during night hours.", redis_client)

def send_alert(message: str, redis_client):
    # Placeholder for alerting functionality
    logger.info(f"Alert: {message}")
    # Implement actual alert sending logic here

def handle_create_event(event: EventModel, db: Session, redis_client):
    device_manager = DeviceManager(redis_client)
    if not device_manager.is_device_registered(event.device_id):
        raise HTTPException(status_code=404, detail="Device not registered")
    new_event = Event(**event.dict())
    db.add(new_event)
    db.commit()
    logger.info("Event added successfully.")
    process_event_for_alerts(new_event, redis_client)
    return {"message": "Event added successfully"}

def handle_get_events(db: Session, from_timestamp: Optional[str], to_timestamp: Optional[str],
                      event_type: Optional[str], device_type: Optional[str]):
    query = db.query(Event)
    if from_timestamp:
        query = query.filter(Event.timestamp >= from_timestamp)
    if to_timestamp:
        query = query.filter(Event.timestamp <= to_timestamp)
    if event_type:
        query = query.filter(Event.event_type == event_type)
    if device_type:
        query = query.filter(Event.device_type == device_type)
    events = query.all()
    return events

def register_device_logic(device_id: str, device_type: str, redis_client):
    device_manager = DeviceManager(redis_client)
    if not device_manager.register_device(device_id, device_type):
        raise HTTPException(status_code=500, detail="Failed to register device")
    return {"message": "Device registered successfully"}
