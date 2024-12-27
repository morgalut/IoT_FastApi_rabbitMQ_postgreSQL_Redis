import redis
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import SessionLocal
import os

def get_db():
    """
    Generator that yields database session and ensures it is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        print(f"Database session error: {str(e)}")
        raise
    finally:
        db.close()

def get_redis():
    """
    Retrieves a Redis client configured from environment variables or default values.
    """
    redis_host = os.getenv("REDIS_HOST", "redis")
    redis_port = int(os.getenv("REDIS_PORT", 6379))
    try:
        redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)
        # Attempt to ping Redis to check connection health
        redis_client.ping()
        return redis_client
    except redis.ConnectionError as e:
        print(f"Failed to connect to Redis: {str(e)}")
        raise

# Ensure environment configuration is picked up
if __name__ == "__main__":
    print("Testing database and Redis connections...")
    try:
        with get_db() as db:
            print("Database connection successful.")
    except Exception as e:
        print(f"Database connection failed: {str(e)}")
    
    try:
        redis_client = get_redis()
        print("Redis connection successful.")
    except Exception as e:
        print(f"Redis connection failed: {str(e)}")
