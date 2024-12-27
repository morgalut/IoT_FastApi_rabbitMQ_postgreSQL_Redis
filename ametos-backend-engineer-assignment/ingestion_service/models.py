from sqlalchemy import Column, String, Integer, JSON, TIMESTAMP, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Sensor(Base):
    __tablename__ = "sensors"
    id = Column(Integer, primary_key=True)
    device_id = Column(String(128), unique=True, nullable=False)  # Assumed max length for device IDs
    device_type = Column(String(50), nullable=False)  # Assumed reasonable max length for device types

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    device_id = Column(String(128), nullable=False, index=True)  # Added length and kept the index
    event_type = Column(String(50), nullable=False, index=True)  # Added length and kept the index
    event_data = Column(JSON, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False, index=True)  # Keeping the index for timestamp queries

    # Adding a composite index for frequent query patterns, e.g., querying by device_id and timestamp
    __table_args__ = (Index('idx_device_id_timestamp', 'device_id', 'timestamp'),)
