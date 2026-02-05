"""Conversation and Message models for AI-powered chat interface."""
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from pydantic import field_validator
from enum import Enum


class RoleType(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    user_id: uuid.UUID = Field(index=True)  # Foreign key to User
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    # Relationships would be defined here if needed
    # messages: List["Message"] = Relationship(back_populates="conversation")


class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    user_id: uuid.UUID = Field(index=True)  # Foreign key to User
    conversation_id: uuid.UUID = Field(index=True)  # Foreign key to Conversation
    role: str = Field(default="user", max_length=20, index=True)
    content: Optional[str] = Field(default=None, max_length=10000)  # Text content, nullable
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    # Validation using Pydantic's field_validator (newer version)
    @field_validator('role')
    @classmethod
    def validate_role(cls, v):
        if v not in ['user', 'assistant']:
            raise ValueError('Role must be either "user" or "assistant"')
        return v