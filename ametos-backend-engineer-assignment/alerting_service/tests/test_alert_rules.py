import pytest
from alerting_service.alert_rules import is_authorized_user, check_speed_violation, check_intrusion

def test_is_authorized_user():
    assert is_authorized_user("authorized_user", ["authorized_user", "admin"]) is True
    assert is_authorized_user("unauthorized_user", ["authorized_user", "admin"]) is False

def test_check_speed_violation():
    assert check_speed_violation(100, 90) is True
    assert check_speed_violation(80, 90) is False

def test_check_intrusion():
    assert check_intrusion("Restricted Area", 0.95, ["Restricted Area"]) is True
    assert check_intrusion("Safe Zone", 0.95, ["Restricted Area"]) is False
    assert check_intrusion("Restricted Area", 0.85, ["Restricted Area"]) is False
