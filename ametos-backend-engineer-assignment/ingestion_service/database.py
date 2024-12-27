from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Define SessionLocal at the module level to be imported elsewhere
SQLALCHEMY_DATABASE_URL = "postgresql://admin:1234@localhost:5432/iot_events"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def setup_database():
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Connection check at startup
    try:
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("Connection successful, server returned:", result.scalar())
    except Exception as e:
        print(f"Error connecting to the database: {e}")

# This allows the function to run if the module is executed as a script, useful for setting up DB in a new environment
if __name__ == "__main__":
    setup_database()
