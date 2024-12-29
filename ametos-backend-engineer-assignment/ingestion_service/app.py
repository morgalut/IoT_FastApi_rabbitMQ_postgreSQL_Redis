from fastapi import FastAPI
from routers import router
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI(title="IoT Event Ingestion Service")
app.include_router(router)

# Example of using .env variables
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

@app.on_event("startup")
async def startup_event():
    print(f"Connecting to database: {POSTGRES_USER}@{POSTGRES_PORT}")
    # Add other startup logic here
    
