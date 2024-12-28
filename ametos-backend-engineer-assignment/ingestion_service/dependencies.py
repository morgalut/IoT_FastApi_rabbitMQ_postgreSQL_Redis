import os

# Set environment variables
os.environ['REDIS_HOST'] = 'localhost'  # Set to 'localhost' or the appropriate IP if Redis is running locally
os.environ['REDIS_PORT'] = '6379'   
import redis
from sqlalchemy.exc import SQLAlchemyError
from database import SessionLocal

import logging
from time import sleep

logger = logging.getLogger(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Database session error: {str(e)}")
        raise
    finally:
        db.close()

def get_redis():
    redis_host = os.getenv("REDIS_HOST", "redis")
    redis_port = int(os.getenv("REDIS_PORT", 6379))
    logger.info(f"Trying to connect to Redis at {redis_host}:{redis_port}")  # Debugging line
    retries = 5
    delay = 2  # seconds

    for attempt in range(retries):
        try:
            redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)
            redis_client.ping()  # Attempt to send a ping to Redis
            logger.info("Redis connection successful.")
            return redis_client
        except redis.ConnectionError as e:
            logger.error(f"Attempt {attempt + 1} - Failed to connect to Redis: {e}")
            if attempt < retries - 1:
                sleep(delay)
        except redis.RedisError as e:
            logger.error(f"Redis error: {e}")
            raise Exception("Redis error, stopping retry.") from e
        except Exception as e:
            logger.error(f"General error when connecting to Redis: {e}")
            if attempt == retries - 1:
                logger.error("Ensure that REDIS_HOST and REDIS_PORT are set correctly.")
            sleep(delay)
    
    raise Exception("Failed to connect to Redis after several retries.")