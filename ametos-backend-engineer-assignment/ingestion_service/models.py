"""This module defines the data models and Pydantic schemas used for handling events
and sensor data within the ingestion service of the IoT platform."""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, ForeignKey, Integer, String, JSON, TIMESTAMP
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, backref
from pydantic import BaseModel

Base = declarative_base()

class EventModel(BaseModel):
    """Schema for event data validation and serialization."""
    id: Optional[int] = None
    device_id: str
    event_type: str
    event_data: dict
    timestamp: datetime

    class Config:
        orm_mode = True

class EventCreateModel(BaseModel):
    """Schema for creating new events."""
    device_id: str
    event_type: str
    event_data: dict
    timestamp: datetime

    class Config:
        arbitrary_types_allowed = True

class Sensor(Base):
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, unique=True, nullable=False)  # Add unique constraint
    device_type = Column(String, nullable=False)
    events = relationship("Event", backref=backref("sensor", lazy="joined"))

class Event(Base):
    """Database model for events."""
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String(128), nullable=False)
    event_type = Column(String(50), nullable=False)
    event_data = Column(JSON, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)
    sensor_id = Column(Integer, ForeignKey("sensors.id"), nullable=True)


