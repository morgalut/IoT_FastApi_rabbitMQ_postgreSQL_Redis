"""API routers for the ingestion service, handling routes for event and device management."""

import logging
from typing import List, Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from dependencies import get_db, get_redis
from models import EventCreateModel, EventModel
import handlers  # Corrected to import from handlers instead of app

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize APIRouter
router = APIRouter()

@router.post("/events", status_code=201, response_model=dict)
def create_event(event: EventCreateModel, db: Session = Depends(get_db), redis_client=Depends(get_redis)):
    """
    Endpoint to create a new event.
    Args:
        event (EventCreateModel): The event data to create.
        db (Session): Database session dependency.
        redis_client: Redis client dependency.
    Returns:
        dict: Success message.
    """
    logger.info("Creating event for device: %s", event.device_id)
    return handlers.handle_create_event(event, db, redis_client)

class EventQueryModel(BaseModel):
    """Model for querying events with optional filters."""
    from_timestamp: Optional[str] = None
    to_timestamp: Optional[str] = None
    event_type: Optional[str] = None
    device_type: Optional[str] = None

@router.get("/events", response_model=List[EventModel])
def get_events(query: EventQueryModel = Depends(), db: Session = Depends(get_db)):
    """
    Endpoint to fetch events based on optional filters.
    Args:
        query (EventQueryModel): Query parameters for filtering events.
        db (Session): Database session dependency.
    Returns:
        List[EventModel]: List of events matching the filters.
    """
    logger.info("Fetching events with filters: %s", query)
    return handlers.handle_get_events(
        db,
        from_timestamp=query.from_timestamp,
        to_timestamp=query.to_timestamp,
        event_type=query.event_type,
        device_type=query.device_type,
    )

class RegisterDeviceModel(BaseModel):
    """Model for registering a new device."""
    device_id: str
    device_type: str

@router.post("/register_device")
def register_device(device: RegisterDeviceModel, redis_client=Depends(get_redis)):
    """
    Endpoint to register a new device.
    Args:
        device (RegisterDeviceModel): Device details.
        redis_client: Redis client dependency.
    Returns:
        dict: Success message.
    """
    logger.info("Registering device: %s as type: %s", device.device_id, device.device_type)
    return handlers.register_device_logic(device.device_id, device.device_type, redis_client)
