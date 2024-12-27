from fastapi import FastAPI
from routers import router
from dependencies import get_redis
from device_management import DeviceManager

app = FastAPI(title="IoT Event Ingestion Service")

app.include_router(router)

@app.on_event("startup")
def startup_event():
    # Instantiate Redis client and device manager
    redis_client = get_redis()
    device_manager = DeviceManager(redis_client)
    
    # Device registrations, wrapped in try-except for improved error handling
    try:
        device_manager.register_device("AA:BB:CC:DD:EE:FF", "Security Camera")
        device_manager.register_device("11:22:33:44:55:66", "Radar")
        # Add more devices as needed
        print("All devices registered successfully.")
    except Exception as e:
        print(f"Failed to register devices: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "Welcome to the IoT Event Ingestion Service. Use /docs for API usage."}
