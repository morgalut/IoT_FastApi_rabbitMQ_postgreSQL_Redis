import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from ingestion_service.app import app
from ingestion_service.database import Base
from ingestion_service.dependencies import get_db
import asyncio
import os

# Environment variables
POSTGRES_USER = os.getenv("POSTGRES_USER", "test_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "test_password")
POSTGRES_DB = os.getenv("POSTGRES_DB", "test_db")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:{POSTGRES_PORT}/{POSTGRES_DB}"

# Database setup
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

@pytest.fixture(scope="module")
def event_loop():
    """Create a new event loop for tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function", autouse=True)
async def setup_database():
    """Reset the database before each test."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@pytest.fixture
def client():
    """Test client for FastAPI app."""
    def override_get_db():
        session = SessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client

# Tests
def test_register_device_success(client):
    """Test device registration."""
    response = client.post("/register_device", json={
        "device_id": "00:11:22:33:44:55",
        "device_type": "Thermal Camera"
    })
    assert response.status_code == 200
    assert response.json() == {"message": "Device registered successfully"}



def test_create_event_success(client):
    """Test event creation."""
    client.post("/register_device", json={
        "device_id": "AA:BB:CC:DD:EE:FF",
        "device_type": "Camera"
    })
    response = client.post("/events", json={
        "device_id": "AA:BB:CC:DD:EE:FF",
        "event_type": "motion_detected",
        "event_data": {"motion": "detected"},
        "timestamp": "2024-12-29T00:00:00"
    })
    assert response.status_code == 201
    assert response.json() == {"message": "Event added successfully"}

def test_get_events_filter(client):
    """Test fetching events with filters."""
    client.post("/register_device", json={
        "device_id": "AA:BB:CC:DD:EE:FF",
        "device_type": "Camera"
    })
    client.post("/events", json={
        "device_id": "AA:BB:CC:DD:EE:FF",
        "event_type": "motion_detected",
        "event_data": {"motion": "detected"},
        "timestamp": "2024-12-29T00:00:00"
    })
    response = client.get("/events", params={"event_type": "motion_detected"})
    assert response.status_code == 200
    events = response.json()
    assert len(events) == 1
    assert events[0]["event_type"] == "motion_detected"
