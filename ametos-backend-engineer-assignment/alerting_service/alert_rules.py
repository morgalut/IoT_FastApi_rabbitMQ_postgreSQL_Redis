# alert_rules.py

def is_authorized_user(user_id, authorized_users):
    """
    Check if the user_id is in the list of authorized users.
    """
    return user_id in authorized_users

def check_speed_violation(speed_kmh, speed_limit=90):
    """
    Check if the speed exceeds the speed limit.
    """
    return speed_kmh > speed_limit

def check_intrusion(zone, confidence, restricted_zones):
    """
    Check if there is an intrusion in a restricted area with high confidence.
    """
    return zone in restricted_zones and confidence > 0.9

def process_event(event):
    """
    Process the incoming event and generate alerts based on event type.
    """
    alert = None
    if event['event_type'] == 'access_attempt':
        if not is_authorized_user(event['user_id'], ['authorized_user']):
            alert = {
                'type': 'Unauthorized Access',
                'message': 'Unauthorized access attempt detected!',
                'details': event
            }

    elif event['event_type'] == 'speed_violation':
        if check_speed_violation(event['speed_kmh']):
            alert = {
                'type': 'Speed Violation',
                'message': 'Speed violation detected!',
                'details': event
            }

    elif event['event_type'] == 'motion_detected':
        if check_intrusion(event['zone'], event['confidence'], ['Restricted Area']):
            alert = {
                'type': 'Intrusion Detection',
                'message': 'Intrusion detected in a restricted area!',
                'details': event
            }

    return alert