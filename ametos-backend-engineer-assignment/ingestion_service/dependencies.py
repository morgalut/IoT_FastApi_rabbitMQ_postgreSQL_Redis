"""Module for managing database and Redis connections used in the ingestion service."""

import os
import logging
from time import sleep
import redis
from sqlalchemy.exc import SQLAlchemyError
from database import SessionLocal

# Set environment variables
os.environ['REDIS_HOST'] = 'localhost'  # Set to 'localhost' or the appropriate IP if Redis is running locally
os.environ['REDIS_PORT'] = '6379'

logger = logging.getLogger(__name__)

def get_db():
    """Yield database sessions and handle SQLAlchemy errors."""
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error("Database session error: %s", str(e))
        raise
    finally:
        db.close()

def get_redis():
    """Connect to Redis with retries on failure."""
    redis_host = os.getenv("REDIS_HOST", "redis")
    redis_port = int(os.getenv("REDIS_PORT", 6379))
    logger.info("Trying to connect to Redis at %s:%s", redis_host, redis_port)
    retries = 5
    delay = 2  # seconds

    for attempt in range(retries):
        try:
            redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)
            redis_client.ping()  # Attempt to send a ping to Redis
            logger.info("Redis connection successful.")
            return redis_client
        except redis.ConnectionError as e:
            logger.error("Attempt %d - Failed to connect to Redis: %s", attempt + 1, str(e))
            if attempt < retries - 1:
                sleep(delay)
        except redis.RedisError as e:
            logger.error("Redis error: %s", str(e))
            raise redis.RedisError("Redis error, stopping retry.") from e
        except Exception as e:
            logger.error("General error when connecting to Redis: %s", str(e))
            if attempt == retries - 1:
                logger.error("Ensure that REDIS_HOST and REDIS_PORT are set correctly.")
            sleep(delay)

    raise Exception("Failed to connect to Redis after several retries.")

