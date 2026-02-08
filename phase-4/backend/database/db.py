from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create async engine with proper connection pooling and resilience
engine = create_async_engine(
    DATABASE_URL,
    poolclass=AsyncAdaptedQueuePool,
    pool_pre_ping=True,      # Verify connections before use to handle stale connections
    pool_recycle=300,        # Recycle connections every 5 minutes to prevent timeouts
    pool_size=20,            # Number of connections to maintain in the pool
    max_overflow=30,         # Additional connections beyond pool_size during high load
    pool_timeout=30,         # Timeout for getting a connection from the pool
    echo=False,              # Set to True for SQL debugging (production: False)
    connect_args={
        "server_settings": {
            "application_name": "agentic-todo-app",
        }
    }
)

# Create async session factory
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db_session():
    """
    Dependency to provide database session for FastAPI endpoints.
    Each request gets its own session which is automatically closed.
    This ensures proper connection lifecycle management and prevents "connection is closed" errors.
    """
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            # Session is automatically closed when exiting the context manager
            # No need to explicitly close in finally block as context manager handles it
            pass