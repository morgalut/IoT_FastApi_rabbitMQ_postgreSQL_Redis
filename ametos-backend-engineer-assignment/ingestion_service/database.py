import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from models import Base
from dotenv import load_dotenv
import logging

# Explicitly load environment variables from .env
env_path = os.path.join(os.path.dirname(__file__), '../configs/.env')
load_dotenv(dotenv_path=env_path)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load database configuration from environment variables
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB")

# Validate required environment variables
if not all([POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB]):
    logger.error("Missing required environment variables for database connection.")
    raise EnvironmentError("Ensure POSTGRES_USER, POSTGRES_PASSWORD, and POSTGRES_DB are set in the .env file.")

# Construct the SQLAlchemy database URL
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# Set up SQLAlchemy engine and sessionmaker
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def setup_database():
    """
    Set up the database by creating tables and checking the connection.
    """
    try:
        # Create tables defined in the Base metadata
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully.")

        # Verify the connection
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            logger.info(f"Connection successful, server returned: {result.scalar()}")
    except SQLAlchemyError as e:
        logger.error(f"SQLAlchemy error during database setup: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during database setup: {e}")
        raise

# If executed as a standalone script, run the setup
if __name__ == "__main__":
    setup_database()
