from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_db, get_redis
from typing import List, Optional
from models import EventModel
import app  # Import functions from app.py to handle logic

router = APIRouter()

@router.post("/events", status_code=201, response_model=dict)
def create_event(event: EventModel, db: Session = Depends(get_db), redis_client=Depends(get_redis)):
    return app.handle_create_event(event, db, redis_client)

@router.get("/events", response_model=List[EventModel])
def get_events(db: Session = Depends(get_db), from_timestamp: Optional[str] = None, to_timestamp: Optional[str] = None,
               event_type: Optional[str] = None, device_type: Optional[str] = None):
    return app.handle_get_events(db, from_timestamp, to_timestamp, event_type, device_type)

@router.post("/register_device")
def register_device(device_id: str, device_type: str, redis_client=Depends(get_redis)):
    return app.register_device(device_id, device_type, redis_client)
