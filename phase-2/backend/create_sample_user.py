#!/usr/bin/env python3
"""
Script to create a sample user in the database for testing purposes.
"""

import asyncio
import uuid
from datetime import datetime
from sqlalchemy import create_engine
from sqlmodel import Session, select
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Import the User model
from models.models import User

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set in .env file")

# Convert async URL to sync URL for direct database operations
sync_database_url = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")

def create_sample_user():
    """Create a sample user for testing."""

    # Create sync engine
    sync_engine = create_engine(sync_database_url)

    # Sample user data
    sample_user = User(
        id=uuid.uuid4(),  # Generate a new UUID
        email="test@example.com",
        password_hash=User.hash_password("TestPass123!"),  # Hash the password
        first_name="Test",
        last_name="User",
        is_active=True,
        is_verified=True,  # Set to True so user doesn't need email verification
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    # Add user to database
    with Session(sync_engine) as session:
        # Check if user already exists
        existing_user = session.exec(select(User).where(User.email == "test@example.com")).first()

        if existing_user:
            print(f"Sample user already exists with ID: {existing_user.id}")
            print(f"Email: {existing_user.email}")
            print(f"First Name: {existing_user.first_name}")
            print(f"Last Name: {existing_user.last_name}")
            return existing_user

        # Add the new user
        session.add(sample_user)
        session.commit()
        session.refresh(sample_user)

        print(f"Sample user created successfully!")
        print(f"ID: {sample_user.id}")
        print(f"Email: {sample_user.email}")
        print(f"Password: TestPass123! (hashed in database)")
        print(f"First Name: {sample_user.first_name}")
        print(f"Last Name: {sample_user.last_name}")
        print(f"Verified: {sample_user.is_verified}")
        print(f"Active: {sample_user.is_active==True}")

        return sample_user

if __name__ == "__main__":
    print("Creating sample user for testing...")
    user = create_sample_user()
    print("\nSample user is ready for testing!")
    print("You can now login with:")
    print("  Email: test@example.com")
    print("  Password: TestPass123!")