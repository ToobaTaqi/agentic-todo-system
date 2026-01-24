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
    gmail_app_password = os.getenv("GMAIL_APP_PASSWORD")

    print("Testing email configuration...")
    print(f"SENDER_EMAIL: {sender_email}")
    print(f"GMAIL_APP_PASSWORD set: {'Yes' if gmail_app_password else 'No'}")

    if not sender_email or not gmail_app_password:
        print("ERROR: Email configuration is incomplete!")
        print("Please set SENDER_EMAIL and GMAIL_APP_PASSWORD in your .env file.")
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
        else:
            print("❌ FAILED: Could not send test email!")
            print(f"Error: {result['error']}")

    except Exception as e:
        print(f"❌ ERROR: Exception occurred while sending email: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_email_configuration())