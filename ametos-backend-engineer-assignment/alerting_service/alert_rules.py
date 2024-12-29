"""
This module contains functions that implement various alert rules based on different event types.
"""

def is_authorized_user(user_id, authorized_users):
    """
    Check if the user_id is in the list of authorized_users.

    :param user_id: str, the ID of the user.
    :param authorized_users: list, the list of authorized user IDs.
    :return: bool, True if user is authorized, otherwise False.
    """
    return user_id in authorized_users

def check_speed_violation(speed_kmh, speed_limit=90):
    """
    Check if the speed exceeds the speed limit.

    :param speed_kmh: float, the speed in km/h.
    :param speed_limit: int, the speed limit (default is 90 km/h).
    :return: bool, True if the speed exceeds the speed limit, otherwise False.
    """
    return speed_kmh > speed_limit

def check_intrusion(zone, confidence, restricted_zones):
    """
    Determine if an intrusion has occurred in restricted zones with a confidence level greater than 0.9.

    :param zone: str, the zone where activity was detected.
    :param confidence: float, the confidence level of the detection.
    :param restricted_zones: list, the list of restricted zones.
    :return: bool, True if intrusion is detected, otherwise False.
    """
    return zone in restricted_zones and confidence > 0.9

def process_event(event):
    """
    Process an event to determine if an alert should be generated based on predefined rules.

    :param event: dict, contains details of the event to be processed.
    :return: dict or None, alert information if an alert condition is met, otherwise None.
    """
    alert = None
    if event['event_type'] == 'access_attempt' and not is_authorized_user(event['user_id'], ['authorized_user']):
        alert = {
            'type': 'Unauthorized Access',
            'message': 'Unauthorized access attempt detected!',
            'details': event
        }
    elif event['event_type'] == 'speed_violation' and check_speed_violation(event['speed_kmh']):
        alert = {
            'type': 'Speed Violation',
            'message': 'Speed violation detected!',
            'details': event
        }
    elif event['event_type'] == 'motion_detected' and check_intrusion(event['zone'], event['confidence'], ['Restricted Area']):
        alert = {
            'type': 'Intrusion Detection',
            'message': 'Intrusion detected in a restricted area!',
            'details': event
        }
    return alert
