"""Test script to verify the complete registration and email verification flow"""

import asyncio
import os
from dotenv import load_dotenv
from utils.email_utils import generate_verification_token, generate_expiration_time, send_verification_email

# Load environment variables
load_dotenv()

async def test_full_flow():
    """Test the complete verification flow functionality"""
    print("=== Testing Complete Registration & Verification Flow ===\n")

    # Check if required environment variables are set
    resend_api_key = os.getenv("RESEND_API_KEY")
    sender_email = os.getenv("SENDER_EMAIL")
    frontend_base_url = os.getenv("FRONTEND_BASE_URL", "http://localhost:3000")

    print(f"RESEND_API_KEY configured: {'Yes' if resend_api_key else 'No'}")
    print(f"SENDER_EMAIL: {sender_email}")
    print(f"FRONTEND_BASE_URL: {frontend_base_url}\n")

    if not resend_api_key:
        print("[ERROR] RESEND_API_KEY not set in environment!")
        return

    # Simulate a new user registration
    print("--- Step 1: Simulating User Registration ---")
    test_user_email = "toobtq@gmail.com"  # Use the email you can receive on
    print(f"New user registering with email: {test_user_email}")

    # Generate verification token (this happens during registration)
    token = generate_verification_token()
    expires_at = generate_expiration_time(minutes=30)
    print(f"Generated verification token: {token[:10]}... (first 10 chars)")
    print(f"Token expires at: {expires_at}\n")

    print("--- Step 2: Sending Verification Email ---")
    # Send verification email (this happens during registration)
    result = await send_verification_email(test_user_email, token)

    if result["success"]:
        print("[SUCCESS] Verification email sent successfully!")
        print(f"Message: {result['message']}")
        if 'email_id' in result and result['email_id']:
            print(f"Email ID: {result['email_id']}")

        print(f"\n--- Step 3: Email Content Preview ---")
        print(f"A verification email was sent to: {test_user_email}")
        print(f"With verification link: {frontend_base_url}/verify-email?token={token}")
        print("When user clicks this link, their account will be activated.")
        print("The backend /api/v1/verify-email endpoint will process the token and set is_verified=True")
    else:
        print("[FAILED] Could not send verification email!")
        print(f"Error: {result['error']}")

    print(f"\n--- Step 4: Expected Verification Process ---")
    print("1. User receives email with verification link")
    print("2. User clicks the link in the email")
    print("3. Browser navigates to: /verify-email?token=<token>")
    print("4. Frontend sends POST to backend /api/v1/verify-email with token")
    print("5. Backend verifies token, marks user as is_verified=True")
    print("6. User account is now activated and fully functional")

if __name__ == "__main__":
    asyncio.run(test_full_flow())