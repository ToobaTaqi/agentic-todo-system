"""Verification-related models."""
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID


class VerificationToken(SQLModel, table=True):
    __tablename__ = "verification_tokens"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(index=True)
    token: str = Field(unique=True, index=True)
    expires_at: datetime
    is_used: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship with User model will be handled via foreign key
    # user: Optional["User"] = Relationship(back_populates="verification_tokens")