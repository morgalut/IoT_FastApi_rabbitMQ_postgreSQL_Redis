from pydantic import BaseModel, Field
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, JSON, TIMESTAMP, Index

Base = declarative_base()

class EventModel(BaseModel):
    id: int
    device_id: str
    event_type: str
    event_data: dict  # Use dict type here for JSON data
    timestamp: datetime

    class Config:
        #orm_mode = True  # Old setting for Pydantic v1, now commented out as per Pydantic v2 requirements
        from_attributes = True  # Enabled as required for Pydantic v2

class Sensor(Base):
    __tablename__ = "sensors"
    id = Column(Integer, primary_key=True)
    device_id = Column(String(128), unique=True, nullable=False)
    device_type = Column(String(50), nullable=False)

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    device_id = Column(String(128), nullable=False, index=True)
    event_type = Column(String(50), nullable=False, index=True)
    event_data = Column(JSON, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False, index=True)
    __table_args__ = (Index('idx_device_id_timestamp', 'device_id', 'timestamp'),)
