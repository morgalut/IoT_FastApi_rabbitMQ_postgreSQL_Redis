import os
from typing import Optional
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from datetime import datetime
import logging
from dependencies import get_redis
from device_management import DeviceManager
from models import Event, EventModel, Sensor
from sqlalchemy.orm import joinedload

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_event_for_alerts(event: Event, redis_client):
    """
    Process events to check if they meet alerting criteria.

    Args:
        event (Event): The event object.
        redis_client: The Redis client instance.
    """
    if event.event_type == "motion_detected" and redis_client.get(event.device_id) == "Security Camera":
        current_hour = datetime.now().hour
        if 18 <= current_hour or current_hour <= 6:
            send_alert(f"Motion detected by {event.device_id} during night hours.", redis_client)

def send_alert(message: str, redis_client):
    """
    Send an alert for critical events.

    Args:
        message (str): Alert message.
        redis_client: The Redis client instance.
    """
    logger.info(f"Alert: {message}")
    # Placeholder for alerting logic (e.g., email, SMS, etc.)

def handle_create_event(event: EventModel, db: Session, redis_client):
    """
    Handle creation of a new event.

    Args:
        event (EventModel): Event data.
        db (Session): Database session.
        redis_client: The Redis client instance.
    """
    device_manager = DeviceManager(redis_client)
    if not device_manager.is_device_registered(event.device_id):
        raise HTTPException(status_code=404, detail="Device not registered")
    
    new_event = Event(**event.dict())
    db.add(new_event)
    db.commit()
    logger.info(f"Event added successfully: {event.device_id}")
    process_event_for_alerts(new_event, redis_client)
    return {"message": "Event added successfully"}

def handle_get_events(db: Session, from_timestamp: Optional[str], to_timestamp: Optional[str],
                      event_type: Optional[str], device_type: Optional[str]):
    """
    Retrieve events from the database based on filters.
    """
    query = db.query(Event).options(joinedload(Event.sensor))
    if from_timestamp:
        query = query.filter(Event.timestamp >= from_timestamp)
    if to_timestamp:
        query = query.filter(Event.timestamp <= to_timestamp)
    if event_type:
        query = query.filter(Event.event_type == event_type)
    if device_type:
        # Now filtering through the related sensor's device_type
        query = query.filter(Sensor.device_type == device_type)
    events = query.all()
    return events

def register_device_logic(device_id: str, device_type: str, redis_client):
    """
    Register a new device in the system.

    Args:
        device_id (str): Device identifier.
        device_type (str): Type of the device.
        redis_client: The Redis client instance.
    """
    device_manager = DeviceManager(redis_client)
    if not device_manager.register_device(device_id, device_type):
        raise HTTPException(status_code=500, detail="Failed to register device")
    logger.info(f"Device registered: {device_id} ({device_type})")
    return {"message": "Device registered successfully"}
