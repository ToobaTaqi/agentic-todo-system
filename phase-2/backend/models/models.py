from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid
from sqlalchemy import JSON
from sqlalchemy.dialects.postgresql import UUID
import bcrypt

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @classmethod
    def hash_password(cls, password: str) -> str:
        # Encode the password to bytes, then hash it
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')

    def verify_password(self, password: str) -> bool:
        # Encode the password to bytes and verify against the stored hash
        password_bytes = password.encode('utf-8')
        stored_hash_bytes = self.password_hash.encode('utf-8')
        return bcrypt.checkpw(password_bytes, stored_hash_bytes)


class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(index=True)
    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None)
    priority: str = Field(default="medium")  # high, medium, low
    tags: list = Field(default=[], sa_type=JSON)  # Stored as JSON
    label: Optional[str] = Field(default=None)  # Label for categorization (work, home, etc.)
    due_date: Optional[datetime] = Field(default=None)
    is_completed: bool = Field(default=False)
    is_recurring: bool = Field(default=False)
    recurrence_pattern: Optional[str] = Field(default=None)  # daily, weekly, monthly, null
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# Import VerificationToken from separate file to ensure all models are available
try:
    from .verification_models import VerificationToken
except ImportError:
    # Fallback for when running in certain contexts
    from verification_models import VerificationToken