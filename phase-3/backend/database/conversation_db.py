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

    conversation = Conversation(user_id=user_id)
    db_session.add(conversation)
    await db_session.commit()
    await db_session.refresh(conversation)
    return conversation


async def get_conversation_by_id(db_session: AsyncSession, conversation_id: str, user_id: str):
    """Get a conversation by ID for a specific user (with ownership validation)."""
    from sqlmodel import select
    from models.conversation_models import Conversation

    statement = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    )
    result = await db_session.exec(statement)
    return result.first()


async def create_message(db_session: AsyncSession, conversation_id: str, user_id: str, role: str, content: str):
    """Create a new message in a conversation."""
    from models.conversation_models import Message

    message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role=role,
        content=content
    )
    db_session.add(message)
    await db_session.commit()
    await db_session.refresh(message)
    return message


async def get_messages_for_conversation(db_session: AsyncSession, conversation_id: str, user_id: str, limit: int = 50, offset: int = 0):
    """Get messages for a specific conversation with user ownership validation."""
    from sqlmodel import select
    from models.conversation_models import Message

    statement = select(Message).where(
        Message.conversation_id == conversation_id,
        Message.user_id == user_id
    ).order_by(Message.created_at).offset(offset).limit(limit)

    result = await db_session.exec(statement)
    return result.all()


async def validate_conversation_ownership(db_session: AsyncSession, conversation_id: str, user_id: str) -> bool:
    """Validate that a conversation belongs to the specified user."""
    from sqlmodel import select
    from models.conversation_models import Conversation

    statement = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    )
    result = await db_session.exec(statement)
    return result.first() is not None