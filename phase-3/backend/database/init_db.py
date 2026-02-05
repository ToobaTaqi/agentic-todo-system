"""Initialize database tables."""
import sys
import os
# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlmodel import SQLModel
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Convert async URL to sync URL for table creation
sync_database_url = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")

# Import all models to register them with SQLModel before creating tables
from models.models import User, Task  # This will also import VerificationToken through the fallback import
from models.verification_models import VerificationToken

def create_tables():
    """Create all database tables using sync engine."""
    # Create sync engine
    sync_engine = create_engine(sync_database_url)

    # Create all tables
    SQLModel.metadata.create_all(sync_engine)

    print("Database tables created successfully!")

if __name__ == "__main__":
    create_tables()