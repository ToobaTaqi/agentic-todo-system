from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from auth.auth import security, verify_token, TokenData, get_current_user, create_access_token, authenticate_user
from database.db import get_db_session
from schemas.auth_schemas import UserRegistration, UserLogin, TokenResponse, UserResponse
from models.models import User
from models.verification_models import VerificationToken
from schemas.verification_schemas import VerificationTokenCreate
from utils.email_utils import generate_verification_token, generate_expiration_time, send_verification_email
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/register")
async def register_user(user_data: UserRegistration, db: AsyncSession = Depends(get_db_session)):
    """Register a new user with email verification"""
    print(f"Register endpoint hit with data: {user_data.email}")

    # Check if user already exists
    print(f"Checking if user with email {user_data.email} already exists")
    statement = select(User).where(User.email == user_data.email)
    result = await db.execute(statement)
    existing_user = result.scalar_one_or_none()
    print(f"User lookup result: {'found' if existing_user else 'not found'}")

    if existing_user:
        print(f"User with email {user_data.email} already exists")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )

    # Create new user with is_verified = False
    print(f"Creating new user with email: {user_data.email}")
    hashed_password = User.hash_password(user_data.password)
    user = User(
        email=user_data.email,
        password_hash=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        is_verified=False  # User is not verified initially
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)
    print(f"User {user.email} created successfully with ID: {user.id}")

    # Generate verification token
    verification_token = generate_verification_token()
    expires_at = generate_expiration_time(minutes=30)  # Token expires in 30 minutes

    print(f"Token generated for user {user.id}")

    # Create verification token record
    verification_token_record = VerificationToken(
        user_id=user.id,
        token=verification_token,
        expires_at=expires_at,
        is_used=False
    )

    db.add(verification_token_record)
    await db.commit()
    print(f"Verification token created for user: {user.id}")

    # Send verification email asynchronously
    try:
        email_result = await send_verification_email(user.email, verification_token)
        print(f"Email send result: {email_result}")

        if not email_result["success"]:
            print(f"Failed to send verification email: {email_result['error']}")
            # Still return success but log the email issue
            logger.warning(f"Could not send verification email to {user.email}: {email_result['error']}")
    except Exception as e:
        print(f"Error sending verification email: {str(e)}")
        logger.error(f"Error sending verification email to {user.email}: {str(e)}")
        # Continue with registration even if email fails, but log the error

    # Create JWT token for the new user (they can still login but will be unverified)
    token_data = {
        "user_id": str(user.id),
        "email": user.email
    }
    access_token = create_access_token(data=token_data)
    print(f"Generated access token for user: {user.id}")

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            id=str(user.id),
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            is_verified=user.is_verified,  # Will be False until verified
            created_at=user.created_at
        )
    )


@router.post("/login")
async def login_user(login_data: UserLogin, db: AsyncSession = Depends(get_db_session)):
    """Authenticate user and return JWT token"""
    print(f"Login endpoint hit with email: {login_data.email}")

    # Authenticate user
    user = await authenticate_user(db, login_data.email, login_data.password)
    if not user:
        print(f"Login failed for email: {login_data.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    print(f"User authenticated successfully: {user.id}")

    # Create JWT token
    token_data = {
        "user_id": str(user.id),
        "email": user.email
    }
    access_token = create_access_token(data=token_data)
    print(f"Generated access token for user: {user.id}")

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            id=str(user.id),
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            is_verified=user.is_verified,
            created_at=user.created_at
        )
    )


@router.post("/logout")
async def logout_user(user: TokenData = Depends(get_current_user)):
    """Logout user (client-side token invalidation)"""
    print(f"Logout endpoint hit for user: {user.user_id}")
    # In a real implementation, you might add the token to a blacklist
    # For now, just return success message
    return {"message": "Successfully logged out"}


@router.get("/session")
async def get_session(user: TokenData = Depends(get_current_user)):
    """Verify and return current session"""
    print(f"Session endpoint hit for user: {user.user_id}")
    return {
        "user_id": user.user_id,
        "email": user.email,
        "authenticated": True
    }


@router.post("/refresh")
async def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Refresh JWT token"""
    print(f"Refresh token endpoint hit")
    # Verify the current token
    token_data = verify_token(credentials.credentials)

    # Create a new token with extended expiry
    new_token_data = {
        "user_id": token_data.user_id,
        "email": token_data.email
    }
    new_access_token = create_access_token(data=new_token_data)

    return {
        "access_token": new_access_token,
        "token_type": "bearer",
        "expires_in": 7 * 24 * 60 * 60  # 7 days in seconds
    }


@router.post("/reset-password-request")
async def reset_password_request(email: str):
    """Request password reset (placeholder - would send email in real implementation)"""
    print(f"Reset password request endpoint hit for email: {email}")
    # In a real implementation, this would send an email with a reset link
    # For now, just return success
    return {"message": "Password reset email sent if account exists"}


@router.post("/reset-password")
async def reset_password(token: str, new_password: str, db: AsyncSession = Depends(get_db_session)):
    """Reset user password with token (placeholder - would validate token in real implementation)"""
    print(f"Reset password endpoint hit with token: {token}")
    # In a real implementation, this would validate the reset token and update the password
    # For now, just return success
    return {"message": "Password reset successful"}


@router.get("/verify-email")
async def verify_email(token: str, db: AsyncSession = Depends(get_db_session)):
    """Verify user email using the verification token"""
    print(f"Verify email endpoint hit with token: {token}")

    # Find the verification token in the database
    statement = select(VerificationToken).where(VerificationToken.token == token)
    result = await db.execute(statement)
    verification_token_record = result.scalar_one_or_none()

    if not verification_token_record:
        print("Invalid verification token")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification token"
        )

    # Check if token is already used
    if verification_token_record.is_used:
        print("Verification token already used")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification token already used"
        )

    # Check if token is expired
    from datetime import datetime
    if verification_token_record.expires_at < datetime.utcnow():
        print("Verification token has expired")
        # Mark token as used to prevent reuse
        verification_token_record.is_used = True
        db.add(verification_token_record)
        await db.commit()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification token has expired"
        )

    # Find the user associated with this token
    user_statement = select(User).where(User.id == verification_token_record.user_id)
    user_result = await db.execute(user_statement)
    user = user_result.scalar_one_or_none()

    if not user:
        print("User not found for verification token")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Update user verification status
    user.is_verified = True
    db.add(user)

    # Mark the verification token as used
    verification_token_record.is_used = True
    db.add(verification_token_record)

    await db.commit()
    await db.refresh(user)

    print(f"User {user.email} verified successfully")

    return {
        "message": "Email verified successfully",
        "user_id": str(user.id),
        "is_verified": user.is_verified
    }