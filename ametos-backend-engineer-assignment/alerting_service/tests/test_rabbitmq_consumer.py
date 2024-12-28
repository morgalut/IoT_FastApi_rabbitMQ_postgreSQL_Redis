import pytest
from alerting_service.RabbitMQ_consumer import process_event, save_alert_to_db

def test_process_event_unauthorized_access():
    event = {
        "event_type": "access_attempt",
        "user_id": "unauthorized_user",
        "device_id": "AA:BB:CC:DD:EE:FF",
        "timestamp": "2024-12-18T14:00:00Z"
    }
    alert = process_event(event)
    assert alert["type"] == "Unauthorized Access"
    assert alert["message"] == "Unauthorized access attempt detected!"
    assert alert["details"] == event

@pytest.mark.skip(reason="Requires live database connection")
def test_save_alert_to_db():
    alert = {
        "type": "Unauthorized Access",
        "message": "Unauthorized access attempt detected!",
        "details": {
            "event_type": "access_attempt",
            "user_id": "unauthorized_user"
        }
    }
    # This requires a running PostgreSQL instance
    save_alert_to_db(alert)
