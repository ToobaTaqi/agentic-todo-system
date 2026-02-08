"""Schemas for verification-related functionality."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class VerificationTokenBase(BaseModel):
    user_id: UUID
    token: str
    expires_at: datetime
    is_used: bool = False


class VerificationTokenCreate(VerificationTokenBase):
    pass


class VerificationTokenResponse(VerificationTokenBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class VerifyEmailRequest(BaseModel):
    token: str