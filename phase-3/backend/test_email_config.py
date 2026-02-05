"""Test script to verify email configuration and send a test email."""

import asyncio
import os
from dotenv import load_dotenv
from utils.email_utils import send_test_email

# Load environment variables
load_dotenv()

async def test_email_configuration():
    """Test the email configuration by sending a test email."""

    # Check if required environment variables are set
    sender_email = os.getenv("SENDER_EMAIL")
    resend_api_key = os.getenv("RESEND_API_KEY")

    print("Testing email configuration...")
    print(f"SENDER_EMAIL: {sender_email}")
    print(f"RESEND_API_KEY set: {'Yes' if resend_api_key else 'No'}")

    if not resend_api_key:
        print("ERROR: Email configuration is incomplete!")
        print("Please set RESEND_API_KEY in your .env file.")
        return

    # Test with a sample email (replace with your test email)
    test_recipient = input("Enter the email address to send test to: ").strip()

    if not test_recipient:
        print("No recipient email provided. Using default test email.")
        test_recipient = "test@example.com"

    print(f"Sending test email to: {test_recipient}")

    try:
        result = await send_test_email(test_recipient)

        if result["success"]:
            print("✅ SUCCESS: Test email sent successfully!")
            print(f"Message: {result['message']}")
            if 'email_id' in result and result['email_id']:
                print(f"Email ID: {result['email_id']}")
        else:
            print("❌ FAILED: Could not send test email!")
            print(f"Error: {result['error']}")

    except Exception as e:
        print(f"❌ ERROR: Exception occurred while sending email: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_email_configuration())