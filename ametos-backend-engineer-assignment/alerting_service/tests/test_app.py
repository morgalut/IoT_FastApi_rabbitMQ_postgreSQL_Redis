from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from alerting_service.app import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the IoT Alerting Service"}

def test_start_consumer():
    response = client.post("/start-consumer")
    assert response.status_code == 200
    assert response.json() == {"message": "RabbitMQ consumer is starting in the background."}

def test_get_alerts_empty():
    response = client.get("/alerts?event_type=Unauthorized Access&limit=5")
    assert response.status_code == 200
    assert "alerts" in response.json()
