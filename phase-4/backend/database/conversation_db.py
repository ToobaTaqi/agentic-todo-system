"""Database session management and utilities for conversation operations."""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
import os
from typing import AsyncGenerator
from contextlib import asynccontextmanager


# Create async database engine
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

engine = create_async_engine(DATABASE_URL)


# Create async session maker
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session for dependency injection."""
    async with AsyncSessionLocal() as session:
        yield session


# Utility functions for conversation operations
async def create_conversation(db_session: AsyncSession, user_id: str):
    """Create a new conversation for a user."""
    from models.conversation_models import Conversation
    import uuid

    # Convert string user_id to UUID object
    user_uuid = uuid.UUID(user_id)
    conversation = Conversation(user_id=user_uuid)
    db_session.add(conversation)
    await db_session.commit()
    await db_session.refresh(conversation)
    return conversation


async def get_conversation_by_id(db_session: AsyncSession, conversation_id: str, user_id: str):
    """Get a conversation by ID for a specific user (with ownership validation)."""
    from sqlmodel import select
    from models.conversation_models import Conversation
    import uuid

    try:
        # Convert string IDs to UUID objects with validation
        conv_uuid = uuid.UUID(conversation_id)
        user_uuid = uuid.UUID(user_id)

        statement = select(Conversation).where(
            Conversation.id == conv_uuid,
            Conversation.user_id == user_uuid
        )
        result = await db_session.execute(statement)
        return result.scalar_one_or_none()
    except ValueError as ve:
        # Handle invalid UUID format
        print(f"Invalid UUID format in get_conversation_by_id: conversation_id={conversation_id}, user_id={user_id}, error={str(ve)}")
        return None  # Return None instead of crashing
    except Exception as e:
        # Handle any other database errors
        print(f"Database error in get_conversation_by_id: {str(e)}")
        return None  # Return None instead of crashing


async def create_message(db_session: AsyncSession, conversation_id: str, user_id: str, role: str, content: str):
    """Create a new message in a conversation."""
    from models.conversation_models import Message
    import uuid

    try:
        # Convert string IDs to UUID objects with validation
        conv_uuid = uuid.UUID(conversation_id)
        user_uuid = uuid.UUID(user_id)

        message = Message(
            conversation_id=conv_uuid,
            user_id=user_uuid,
            role=role,
            content=content
        )
        db_session.add(message)
        await db_session.commit()
        await db_session.refresh(message)
        return message
    except ValueError as ve:
        # Handle invalid UUID format
        print(f"Invalid UUID format in create_message: conversation_id={conversation_id}, user_id={user_id}, error={str(ve)}")
        raise  # Re-raise since this is a critical error for creating a message
    except Exception as e:
        # Handle any other database errors
        print(f"Database error in create_message: {str(e)}")
        raise  # Re-raise since this is a critical error


async def get_messages_for_conversation(db_session: AsyncSession, conversation_id: str, user_id: str, limit: int = 50, offset: int = 0):
    """Get messages for a specific conversation with user ownership validation."""
    from sqlmodel import select
    from models.conversation_models import Message
    import uuid

    try:
        # Convert string IDs to UUID objects with validation
        conv_uuid = uuid.UUID(conversation_id)
        user_uuid = uuid.UUID(user_id)

        statement = select(Message).where(
            Message.conversation_id == conv_uuid,
            Message.user_id == user_uuid
        ).order_by(Message.created_at).offset(offset).limit(limit)

        result = await db_session.execute(statement)
        messages = result.scalars().all()

        # Additional validation to ensure messages are properly formed
        validated_messages = []
        for msg in messages:
            # Ensure the message object has required attributes
            if hasattr(msg, 'role') and hasattr(msg, 'content'):
                validated_messages.append(msg)
            else:
                print(f"Warning: Invalid message object found in database: {msg}")

        return validated_messages

    except ValueError as ve:
        # Handle invalid UUID format
        print(f"Invalid UUID format: conversation_id={conversation_id}, user_id={user_id}, error={str(ve)}")
        return []  # Return empty list instead of crashing
    except Exception as e:
        # Handle any other database errors
        print(f"Database error in get_messages_for_conversation: {str(e)}")
        return []  # Return empty list instead of crashing


async def validate_conversation_ownership(db_session: AsyncSession, conversation_id: str, user_id: str) -> bool:
    """Validate that a conversation belongs to the specified user."""
    from sqlmodel import select
    from models.conversation_models import Conversation
    import uuid

    # Convert string IDs to UUID objects
    conv_uuid = uuid.UUID(conversation_id)
    user_uuid = uuid.UUID(user_id)

    statement = select(Conversation).where(
        Conversation.id == conv_uuid,
        Conversation.user_id == user_uuid
    )
    result = await db_session.execute(statement)
    return result.scalar_one_or_none() is not None