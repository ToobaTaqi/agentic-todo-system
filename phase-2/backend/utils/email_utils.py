"""Email utility functions for sending verification emails via Resend."""
import asyncio
import os
from typing import Dict, Any
from dotenv import load_dotenv
import logging
import secrets
from datetime import datetime, timedelta
import resend

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_verification_token() -> str:
    """Generate a secure verification token."""
    return secrets.token_urlsafe(32)


def generate_expiration_time(minutes: int = 30) -> datetime:
    """Generate expiration time for the token."""
    return datetime.utcnow() + timedelta(minutes=minutes)


async def send_verification_email(email: str, token: str) -> Dict[str, Any]:
    """
    Send verification email to the user asynchronously via Resend.

    Args:
        email: User's email address
        token: Verification token

    Returns:
        Dictionary with success status and message
    """
    try:
        # Get Resend API key from environment
        resend_api_key = os.getenv("RESEND_API_KEY")
        sender_email = os.getenv("SENDER_EMAIL", "onboarding@example.com")

        if not resend_api_key:
            logger.error("RESEND_API_KEY environment variable not set")
            return {
                "success": False,
                "error": "Email service not configured. Please set RESEND_API_KEY environment variable."
            }

        # Get the frontend base URL from environment, default to localhost for development
        frontend_base_url = os.getenv("FRONTEND_BASE_URL", "http://localhost:3000")
        verification_url = f"{frontend_base_url}/verify-email?token={token}"

        # Create HTML content
        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #4F46E5; text-align: center;">Welcome to AI-Ready Todo App!</h2>
            <p style="font-size: 16px; line-height: 1.5;">Thank you for registering. Please verify your email address to activate your account.</p>

            <div style="text-align: center; margin: 30px 0;">
                <a href="{verification_url}"
                   style="background-color: #4F46E5; color: white; padding: 14px 28px; text-decoration: none;
                          border-radius: 8px; display: inline-block; font-weight: bold; font-size: 16px;">
                    Verify Your Email Address
                </a>
            </div>

            <p style="font-size: 14px; color: #6B7280; margin: 20px 0;">
                This link will expire in 30 minutes. If you didn't create an account with us, please ignore this email.
            </p>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #E5E7EB;">
            <p style="font-size: 12px; color: #6B7280; text-align: center; margin-top: 20px;">
                AI-Ready Todo App<br>
                Secure Task Management
            </p>
        </div>
        """

        # Initialize Resend with API key
        resend.api_key = resend_api_key

        # Send email using Resend
        params = {
            "from": sender_email,
            "to": [email],
            "subject": "Verify Your Email Address - AI-Ready Todo App",
            "html": html_content,
        }

        email_response = resend.Emails.send(params)

        logger.info(f"Verification email sent successfully to {email}")
        return {
            "success": True,
            "message": "Verification email sent successfully",
            "email_id": email_response["id"] if isinstance(email_response, dict) and "id" in email_response else None
        }

    except Exception as e:
        logger.error(f"Failed to send verification email to {email}: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


async def send_test_email(email: str) -> Dict[str, Any]:
    """
    Send a test email to verify email configuration via Resend.

    Args:
        email: Test email address

    Returns:
        Dictionary with success status and message
    """
    try:
        # Get Resend API key from environment
        resend_api_key = os.getenv("RESEND_API_KEY")
        sender_email = os.getenv("SENDER_EMAIL", "onboarding@example.com")

        if not resend_api_key:
            logger.error("RESEND_API_KEY environment variable not set for test email")
            return {
                "success": False,
                "error": "Email service not configured. Please set RESEND_API_KEY environment variable."
            }

        # Create HTML content
        html_content = """
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #4F46E5; text-align: center;">Test Email</h2>
            <p style="font-size: 16px; line-height: 1.5;">This is a test email to verify your email configuration.</p>

            <p style="font-size: 14px; color: #6B7280; margin-top: 20px;">
                Email configuration is working correctly!
            </p>
        </div>
        """

        # Initialize Resend with API key
        resend.api_key = resend_api_key

        # Send email using Resend
        params = {
            "from": sender_email,
            "to": [email],
            "subject": "Test Email from AI-Ready Todo App",
            "html": html_content,
        }

        email_response = resend.Emails.send(params)

        logger.info(f"Test email sent successfully to {email}")
        return {
            "success": True,
            "message": "Test email sent successfully",
            "email_id": email_response["id"] if isinstance(email_response, dict) and "id" in email_response else None
        }

    except Exception as e:
        logger.error(f"Failed to send test email to {email}: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }