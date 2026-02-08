"""Simple script to initialize database tables including new conversation models."""
import asyncio
import os
from sqlalchemy import create_engine
from sqlmodel import SQLModel
from models.models import User, Task, VerificationToken
from models.conversation_models import Conversation, Message

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

# Convert async URL to sync URL for table creation
sync_database_url = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")

# Create sync engine and tables
sync_engine = create_engine(sync_database_url)
SQLModel.metadata.create_all(sync_engine)

print("Database tables created successfully!")
print("- Users table")
print("- Tasks table")
print("- VerificationTokens table")
print("- Conversations table")
print("- Messages table")