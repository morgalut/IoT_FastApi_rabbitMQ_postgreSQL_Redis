

# Ingestion Service Setup Guide

This guide provides instructions for setting up and operating the ingestion service for the Ametos backend engineer assignment. It includes steps for configuring environment variables, activating the service, and verifying operations through various `curl` commands.

## Prerequisites

Ensure you have Docker installed for managing containers and Python for running the service.

## Environment Setup

### Creating an Environment Variables File

1. **Navigate to the configs directory**:
   ```
   cd ametos-backend-engineer-assignment\configs\
   ```

2. **Create a `.env` file**:
   Create a `.env` file in the directory with the following content. This file contains necessary configuration settings for the databases and services used by the ingestion service.
   ```plaintext
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

## Service Activation

### Start the Ingestion Service

Run the service using Uvicorn with live reload enabled to apply code changes without restarting the service:

```
uvicorn app:app --reload
```

## Database Setup

### Initialize PostgreSQL Database

Ensure that the PostgreSQL database is set up and configured correctly:

1. **Access the PostgreSQL instance**:
   ```bash
   docker exec -it configs-postgres-1 psql -U admin -d iot_events
   ```

2. **Create necessary tables**:
   Execute the following SQL commands to create the database schema required for the ingestion service:
   ```sql
   CREATE DATABASE iot_events;

   CREATE TABLE sensors (
       id SERIAL PRIMARY KEY,
       device_id VARCHAR(128) UNIQUE NOT NULL,
       device_type VARCHAR(50) NOT NULL
   );

   CREATE TABLE events (
       id SERIAL PRIMARY KEY,
       device_id VARCHAR(255) NOT NULL,
       event_type VARCHAR(255) NOT NULL,
       event_data JSONB NOT NULL,
       timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       FOREIGN KEY (device_id) REFERENCES sensors(device_id) ON DELETE CASCADE
   );

   CREATE TABLE alerts (
       id SERIAL PRIMARY KEY,
       type VARCHAR(255),
       message TEXT,
       details JSONB,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

## Device Registration

Use the following `curl` commands to register devices within the system:

- **Security Camera**:
  ```bash
  curl -X POST "http://127.0.0.1:8000/register_device" -H "Content-Type: application/json" -d "{\"device_id\": \"AA:BB:CC:DD:EE:FF\", \"device_type\": \"Security Camera\"}"
  ```

[View Example Security Camera Registration](Img/1.png)

- **Motion Sensor** and **Radar**:
  ```bash
  curl -X POST "http://127.0.0.1:8000/register_device" -H "Content-Type: application/json" -d "{\"device_id\": \"77:88:99:AA:BB:CC\", \"device_type\": \"Motion Sensor\"}"
  curl -X POST "http://127.0.0.1:8000/register_device" -H "Content-Type: application/json" -d "{\"device_id\": \"11:22:33:44:55:66\", \"device_type\": \"Radar\"}"
  ```

## Posting and Retrieving Events

### Post Events

Post event data using `curl`:

```bash
curl -X POST "http://127.0.0.1:8000/events" -H "Content-Type: application/json" -d "{\"device_id\": \"AA:BB:CC:DD:EE:FF\", \"timestamp\": \"2024-12-18T14:00:00Z\", \"event_type\": \"access_attempt\", \"event_data\": {\"user_id\": \"unauthorized_user\"}}"
```

### Retrieve Events

Retrieve posted events with various filters:

- **Get All Events**:
  ```bash
  curl -X GET "http://127.0.0.1:8000/events"
  ```

- **Filter by Timestamp and Event Type**:
  ```bash
  curl -X GET "http://127.0.0.1:8000/events?from_timestamp=2024-12-18T14:00:00Z&to_timestamp=2024-12-18T15:00:00Z"
  curl -X GET "http://127.0.0.1:8000/events?event_type=motion_detected"
  curl -X GET "http://127.0.0.1:8000/events?device_type=Motion%20Sensor"
  ```

[View Example of Event Retrieval](Img/e.png)

### Example of Posting an Event with an Image in Base64

```bash
curl -X POST "http://127.0.0.1:8000/events" -H "Content-Type: application/json" -d "{\"device_id\": \"77:88:99:AA:BB:CC\", \"timestamp\": \"2024-12-18T14:10:00Z\", \"event_type\": \"motion_detected\", \"event_data\": {\"zone\": \"Restricted Area\", \"confidence\": 0.95, \"photo_base64\": \"/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDACgcHiMeGSgjISMtKygwPGRBPDc3PHtYXUlkkYCZlo+AjIqgtObDoKrarYqMyP/L2u71////m8H////6/+b9//j/2wBDASstLTw1PHZBQXb4pYyl+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj/wAARCAIgB4ADASIAAhEBAxEB/8QAGgAAAwEBAQEAAAAAAAAAAAAAAAECAwQFBv/EAEYQAAICAQMDAgQEBAMECQQBBQECABEDEiExBEFRImETMnGBBUKRoRQjUrFiwdEVM3LhNDVDRXOCwvDxJFOEkgZEVKLig//EABcBAQEBAQAAAAAAAAAAAAAAAAABAgP/xAAgEQEBAQADAQEBAQADAAAAAAAAARECITESQVFhAxNx/9oADAMBAAIRAxEAPwD2YSE3G/MagWRAqEQAB2ju4BCLVIJOriA8jhAGbiWNxObqVVsRBUn6GXhYfCSrFiEbQi38xwoiIB5EAQSaMcDk6lSrqaZ9W2ntDB/JynEqnSd9vyzqYEqQNjIKhE9K2RAGyhWqiT7SywCaroTlHTvrL6hq9x2mzMfhkaLIHBgcWTK2TICCQtczZchTC1EajuDUwGQOArnV6uK3mmNEZjjALdyR2hHnZyhya19LH5lPYzK51dcAH0utODt7jtOPeUPiUmwJPeSBewlXSfaB3fhILZ2bsFnrTx/w/OMOpaJuuJ7ANgGKohCEgIRE0Cf7TmPWIHG5A8EQOqEQNgHzHAInICm4FlXkgTiz9SWJGMX/AJyW4M+qyY6NH1dqnnmjvdA+01yE3TE3MSaU8+ZlFBQG2P3uLOqrpKj0ng95GqjcbsNOkG95RHeUORvUkX4lDapVNsjA7HY+0lVDPV1BmJW2IlooUDkMfPiRAXAtV3FeZnZUgN2mqkoTjBbc70OYihtq3XvARYsTpHI23muPK2um\"}}"
```

[View Example Motion Detection Event](Img/age.png)

