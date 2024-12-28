uvicorn app:app --reload


# Need create .env 
You need to create a file inside the "ametos-backend-engineer-assignment\configs\.env"
with the following details so that everything is correct
```
POSTGRES_PORT=5432
POSTGRES_PASSWORD=newer_password
POSTGRES_USER=new_admin
POSTGRES_DB=iot_events
RABBITMQ_USER=user
RABBITMQ_PASSWORD=guest
REDIS_HOST=redis
REDIS_PORT=6379
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
```

## Check curl register_device
``` curl -X POST "http://127.0.0.1:8000/register_device" -H "Content-Type: application/json" -d "{\"device_id\": \"AA:BB:CC:DD:EE:FF\", \"device_type\": \"Security Camera\"}" ```

``` curl -X POST "http://127.0.0.1:8000/register_device" -H "Content-Type: application/json" -d "{\"device_id\": \"77:88:99:AA:BB:CC\", \"device_type\": \"Motion Sensor\"}" ```

``` curl -X POST "http://127.0.0.1:8000/register_device" -H "Content-Type: application/json" -d "{\"device_id\": \"11:22:33:44:55:66\", \"device_type\": \"Radar\"}" ```

## Check curl events

``` curl -X POST "http://127.0.0.1:8000/events" -H "Content-Type: application/json" -d "{\"device_id\": \"AA:BB:CC:DD:EE:FF\", \"timestamp\": \"2024-12-18T14:00:00Z\", \"event_type\": \"access_attempt\", \"event_data\": {\"user_id\": \"unauthorized_user\"}}" ```

``` curl -X POST "http://127.0.0.1:8000/events" -H "Content-Type: application/json" -d "{\"device_id\": \"AA:BB:CC:DD:EE:FF\", \"timestamp\": \"2024-12-18T14:05:00Z\", \"event_type\": \"access_attempt\", \"event_data\": {\"user_id\": \"authorized_user\"}}" ```

## Check with img curl commnd 

```curl -X POST "http://127.0.0.1:8000/events" -H "Content-Type: application/json" -d "{\"device_id\": \"77:88:99:AA:BB:CC\", \"timestamp\": \"2024-12-18T14:10:00Z\", \"event_type\": \"motion_detected\", \"event_data\": {\"zone\": \"Restricted Area\", \"confidence\": 0.95, \"photo_base64\": \"/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDACgcHiMeGSgjISMtKygwPGRBPDc3PHtYXUlkkYCZlo+AjIqgtObDoKrarYqMyP/L2u71////m8H////6/+b9//j/2wBDASstLTw1PHZBQXb4pYyl+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj/wAARCALQBQADASIAAhEBAxEB/8QAGgABAQEBAQEBAAAAAAAAAAAAAAECAwQFBv/EAD0QAAICAQMCBQMCBQQBAwQCAwABAhEhAxIxQVEEImFxgRMykUKhBSMzUrEUYnLB0YLh8CQ0Q5IlovFT8v/EABgBAQEBAQEAAAAAAAAAAAAAAAABAgME/8QAJxEBAQACAgICAgICAwEAAAAAAAECEQMxITISQVFhEyIzcSNCkVL/2gAMAwEAAhEDEQA/APAAU6MABQCQBQBCgCMBgihCvkgFfJCvkUBHyOpSAKBXyAI8EK/+iAVcHVcI5Lg6rhAAUEVCgAAAQQAoEKAQAAAC5YC5YAMpl8gQ0ZNBQoAGdX+mznp/cvc6av8ATkY0/uj7iI5y++Xuywi5SUV1E/6kvc7eFSTc5ccI6zpl9DwfhVLSctVLb0j/AOT5kmpeIe3ht1+GfS8T4qGj4JacZfzJRXwfM1GktOUPX5Mq67L0owlzSR52mnT5R2Ws5xm4xSlHKRmS+pprUjyuRKU8P/Ufseg82h/V+D1Gc+1xQFBhQAAAefXcvqUn0Oe2XV59+TUxNvWOhnR/ox9jZOhiXDMSXmfsjpLCfsYbTk/ZAc9RVF+//RdLMIjU+2Xv/wBDR/pr3KhS+n/6TlPGpI7/AKPhnCf9SQHdpbuCNc46f+Sv7iOSznp/5Axp5b9jRjTai89v+zVqqvKAzJ+b8DuR9SgJcGDb4MAAClApCoCgllsgFsgA0aTMFRR0TNKRyWDVkHVSLv59+TjYsqO0p3ZYa0oT\"}}" ```

``` curl -X POST "http://127.0.0.1:8000/events" -H "Content-Type: application/json" -d "{\"device_id\": \"77:88:99:AA:BB:CC\", \"timestamp\": \"2024-12-18T14:10:00Z\", \"event_type\": \"motion_detected\", \"event_data\": {\"zone\": \"Restricted Area\", \"confidence\": 0.95, \"photo_base64\": \"/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDACgcHiMeGSgjISMtKygwPGRBPDc3PHtYXUlkkYCZlo+AjIqgtObDoKrarYqMyP/L2u71////m8H////6/+b9//j/2wBDASstLTw1PHZBQXb4pYyl+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj/wAARCAIgB4ADASIAAhEBAxEB/8QAGgAAAwEBAQEAAAAAAAAAAAAAAAECAwQFBv/EAEYQAAICAQMDAgQEBAMECQQBBQECABEDEiExBEFRImETMnGBBUKRoRQjUrFiwdEVM3LhNDVDRXOCwvDxJFOEkgZEVKLig//EABcBAQEBAQAAAAAAAAAAAAAAAAABAgP/xAAgEQEBAQADAQEBAQADAAAAAAAAARECITESQVFhAxNx/9oADAMBAAIRAxEAPwD2YSE3G/MagWRAqEQAB2ju4BCLVIJOriA8jhAGbiWNxObqVVsRBUn6GXhYfCSrFiEbQi38xwoiIB5EAQSaMcDk6lSrqaZ9W2ntDB/JynEqnSd9vyzqYEqQNjIKhE9K2RAGyhWqiT7SywCaroTlHTvrL6hq9x2mzMfhkaLIHBgcWTK2TICCQtczZchTC1EajuDUwGQOArnV6uK3mmNEZjjALdyR2hHnZyhya19LH5lPYzK51dcAH0utODt7jtOPeUPiUmwJPeSBewlXSfaB3fhILZ2bsFnrTx/w/OMOpaJuuJ7ANgGKohCEgIRE0Cf7TmPWIHG5A8EQOqEQNgHzHAInICm4FlXkgTiz9SWJGMX/AJyW4M+qyY6NH1dqnnmjvdA+01yE3TE3MSaU8+ZlFBQG2P3uLOqrpKj0ng95GqjcbsNOkG95RHeUORvUkX4lDapVNsjA7HY+0lVDPV1BmJW2IlooUDkMfPiRAXAtV3FeZnZUgN2mqkoTjBbc70OYihtq3XvARYsTpHI23muPK2um\"}}" ```