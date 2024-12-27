from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from models import Sensor, Event
from dependencies import get_db, get_redis
from typing import Optional, List
from device_management import DeviceManager

router = APIRouter()

@router.post("/events", status_code=201)
def create_event(event: dict, db: Session = Depends(get_db), redis_client=Depends(get_redis)):
    device_id = event.get("device_id")
    device_manager = DeviceManager(redis_client)
    if not device_manager.is_device_registered(device_id):
        raise HTTPException(status_code=404, detail="Device not registered")
    
    new_event = Event(**event)
    db.add(new_event)
    db.commit()
    return {"message": "Event added successfully"}

@router.get("/events", response_model=List[Event])
def get_events(db: Session = Depends(get_db), 
               from_timestamp: Optional[str] = Query(None), 
               to_timestamp: Optional[str] = Query(None),
               event_type: Optional[str] = Query(None),
               device_type: Optional[str] = Query(None)):
    query = db.query(Event)
    if from_timestamp:
        query = query.filter(Event.timestamp >= from_timestamp)
    if to_timestamp:
        query = query.filter(Event.timestamp <= to_timestamp)
    if event_type:
        query = query.filter(Event.event_type == event_type)
    if device_type:
        query = query.join(Sensor).filter(Sensor.device_type == device_type)
    return query.all()

@router.post("/register_device")
def register_device_endpoint(device_id: str, device_type: str, redis_client=Depends(get_redis)):
    device_manager = DeviceManager(redis_client)
    if device_manager.register_device(device_id, device_type):
        return {"message": "Device registered successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to register device")
