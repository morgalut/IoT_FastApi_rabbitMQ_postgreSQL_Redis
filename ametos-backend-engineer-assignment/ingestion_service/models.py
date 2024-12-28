# models.py
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, JSON, TIMESTAMP
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class EventModel(BaseModel):
    id: Optional[int] = None  # Make `id` optional
    device_id: str
    event_type: str
    event_data: dict
    timestamp: datetime

    class Config:
        from_attributes = True  # Replace orm_mode

class EventCreateModel(BaseModel):
    device_id: str
    event_type: str
    event_data: dict
    timestamp: datetime

    class Config:
        arbitrary_types_allowed = True

class Sensor(Base):
    __tablename__ = "sensors"
    id = Column(Integer, primary_key=True)
    device_id = Column(String(128), unique=True, nullable=False)
    device_type = Column(String(50), nullable=False)

    # Establish relationship
    events = relationship("Event", backref=backref("sensor", lazy="joined"))

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String(128), nullable=False)
    event_type = Column(String(50), nullable=False)
    event_data = Column(JSON, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)

    # Explicit relationship to Sensor
    sensor_id = Column(Integer, ForeignKey("sensors.id"), nullable=True)