-- Create Database
CREATE DATABASE iot_events;

-- Connect to Database
\c iot_events;

-- Create Tables
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
