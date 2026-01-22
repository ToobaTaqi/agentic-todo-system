#!/usr/bin/env python3
"""
Script to reset the sample user in the database and create a fresh one.
"""

import asyncio
import uuid
from datetime import datetime
from sqlalchemy import create_engine, delete
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

def reset_sample_user():
    """Reset the sample user and create a fresh one."""

    # Create sync engine
    sync_engine = create_engine(sync_database_url)

    with Session(sync_engine) as session:
        # Delete existing sample user
        result = session.exec(select(User).where(User.email == "test@example.com"))
        existing_users = result.all()

        if existing_users:
            for user in existing_users:
                print(f"Deleting existing user: {user.email} (ID: {user.id})")
                session.delete(user)

            session.commit()
            print(f"Deleted {len(existing_users)} existing sample user(s)")
        else:
            print("No existing sample user found to delete")

        # Create a new sample user
        new_sample_user = User(
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

        # Add the new user
        session.add(new_sample_user)
        session.commit()
        session.refresh(new_sample_user)

        print(f"\nNew sample user created successfully!")
        print(f"ID: {new_sample_user.id}")
        print(f"Email: {new_sample_user.email}")
        print(f"Password: TestPass123! (hashed in database)")
        print(f"First Name: {new_sample_user.first_name}")
        print(f"Last Name: {new_sample_user.last_name}")
        print(f"Verified: {new_sample_user.is_verified}")
        print(f"Active: {new_sample_user.is_active}")

        return new_sample_user

if __name__ == "__main__":
    print("Resetting sample user...")
    user = reset_sample_user()
    print("\nNew sample user is ready for testing!")
    print("You can now login with:")
    print("  Email: test@example.com")
    print("  Password: TestPass123!")