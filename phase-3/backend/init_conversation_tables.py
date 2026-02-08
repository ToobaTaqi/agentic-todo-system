#!/usr/bin/env python3
"""
Database initialization script to ensure all tables exist
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlmodel import SQLModel
from models.models import User, Task
from models.verification_models import VerificationToken
from models.conversation_models import Conversation, Message

# Load environment variables
load_dotenv()

def init_db():
    # Get database URL from environment
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is required")
    
    # Convert async URL to sync URL for table creation
    sync_database_url = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
    
    # Create sync engine and tables
    sync_engine = create_engine(sync_database_url)
    
    print("Creating all tables...")
    SQLModel.metadata.create_all(sync_engine)
    print("Tables created successfully!")
    
    # Verify tables exist by reflecting them
    from sqlalchemy import inspect
    inspector = inspect(sync_engine)
    tables = inspector.get_table_names()
    
    print("\nExisting tables:")
    for table in sorted(tables):
        print(f"  - {table}")
    
    required_tables = ['users', 'tasks', 'verification_tokens', 'conversations', 'messages']
    missing_tables = [table for table in required_tables if table not in tables]
    
    if missing_tables:
        print(f"\nWARNING: Missing tables: {missing_tables}")
    else:
        print(f"\nAll required tables exist!")

if __name__ == "__main__":
    init_db()