from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from auth.auth import get_current_user, TokenData
from database.db import get_db_session
from models.models import User
from schemas.auth_schemas import UserResponse

router = APIRouter()

@router.get("/profile", response_model=UserResponse)
async def get_profile(
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """Get current user's profile information"""
    print(f"Get profile endpoint hit for user: {current_user.user_id}")
    statement = select(User).where(User.id == current_user.user_id)
    result = await db.execute(statement)
    user = result.scalar_one_or_none()

    if not user:
        print(f"User {current_user.user_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    print(f"Found user profile for: {user.email}")
    return user

@router.put("/profile")
async def update_profile(
    first_name: str = None,
    last_name: str = None,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """Update current user's profile information"""
    print(f"Update profile endpoint hit for user: {current_user.user_id}")
    statement = select(User).where(User.id == current_user.user_id)
    result = await db.execute(statement)
    user = result.scalar_one_or_none()

    if not user:
        print(f"User {current_user.user_id} not found for update")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if first_name is not None:
        print(f"Updating first name from '{user.first_name}' to '{first_name}'")
        user.first_name = first_name
    if last_name is not None:
        print(f"Updating last name from '{user.last_name}' to '{last_name}'")
        user.last_name = last_name

    await db.commit()
    await db.refresh(user)
    print(f"Updated profile for user: {user.id}")

    return user