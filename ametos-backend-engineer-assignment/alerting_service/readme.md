

# Ametos Alerting Service Setup Guide

This guide provides detailed steps to set up and run the Ametos Alerting Service which utilizes FastAPI, PostgreSQL, and RabbitMQ for handling IoT event alerts.

## Prerequisites

Ensure you have Docker, Python, and pip installed on your system to run the services and install dependencies.

## Installation

1. **Install Required Python Libraries**

   Navigate to the project directory and install the necessary Python libraries using pip:

   ```bash
   pip install -r Requirements.txt
   ```

## Running the Service

1. **Start the FastAPI server**

   Launch the FastAPI application with the following command:

   ```bash
   uvicorn app:app --reload
   ```

   The server will be available at `http://localhost:8000/`.

2. **Verify Server Operation**

   Test the connectivity to the server using:

   ```bash
   curl http://localhost:8000/
   ```

3. **Start Event Consumer**

   Initialize the event consumer to begin processing events:

   ```bash
   curl -X POST http://localhost:8000/start-consumer
   ```

## Interacting with the Service

1. **Create and Manage Alerts**

   - **Start Consumer**:

     Begin event consumption from RabbitMQ:

     ```bash
     curl -X POST "http://127.0.0.1:8000/start-consumer"
     ```

   - **Fetch Alerts**:

     Retrieve the latest alerts with a limit on the number of alerts:

     ```bash
     curl -X GET "http://localhost:8000/alerts?limit=10"
     ```

     This command requires a valid user in RabbitMQ. If you encounter errors, refer to the RabbitMQ User section below.

2. **Database Operations**

   - **Access PostgreSQL via Docker**:

     Connect to the PostgreSQL database:

     ```bash
     docker exec -it configs-postgres-1 psql -U admin -d iot_events
     ```

   - **Database Schema Setup**:

     Execute the following SQL commands to set up the database schema for sensors, events, and alerts:

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

   - **Query Alerts**:

     Check the saved alerts:

     ```sql
     SELECT * FROM alerts;
     ```

   - **Reload PostgreSQL Configuration**:

     If changes are made to `pg_hba.conf.sample`, reload the configuration:

     ```sql
     SELECT pg_reload_conf();
     ```

## Troubleshooting

1. **RabbitMQ User Issues**

   If you encounter a 403 user connection error, consult the detailed guide [here](https://docs.google.com/document/d/1uHlzu-p2eFq4PlwV05WQcxa274rIzSV63dcXWCC4xrE/edit?usp=sharing) for setting up RabbitMQ users, permissions, and resolving common issues.

2. **Database Column Error**

   If you see an error like `{"error":"Database error: column \"type\" does not exist\n...}`, refer to the troubleshooting guide [here](https://docs.google.com/document/d/16PatyEYmDUyZmu0ZGR-velZ343uX4Kclplq2ROpgboQ/edit?usp=sharing).

## Further Information

The service setup visuals and further details can be referenced in the project images shown [here](Img/image.png).

