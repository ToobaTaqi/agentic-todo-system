"""Quick test script to test Resend email functionality"""

import asyncio
import os
from dotenv import load_dotenv
from utils.email_utils import send_test_email

# Load environment variables
load_dotenv()

async def quick_test():
    """Quick test of Resend email functionality"""
    print("Testing Resend email functionality...")

    # Check if required environment variables are set
    resend_api_key = os.getenv("RESEND_API_KEY")
    sender_email = os.getenv("SENDER_EMAIL")

    print(f"RESEND_API_KEY set: {'Yes' if resend_api_key else 'No'}")
    print(f"SENDER_EMAIL: {sender_email}")

    if not resend_api_key:
        print("ERROR: RESEND_API_KEY not set in environment!")
        return

    # Test with your registered email (required for Resend test domain)
    test_email = "toobtq@gmail.com"  # Must be the same email used to register with Resend

    print(f"Sending test email to: {test_email}")

    try:
        result = await send_test_email(test_email)

        if result["success"]:
            print("[SUCCESS] Test email sent successfully!")
            print(f"Message: {result['message']}")
            if 'email_id' in result and result['email_id']:
                print(f"Email ID: {result['email_id']}")
        else:
            print("[FAILED] Could not send test email!")
            print(f"Error: {result['error']}")

    except Exception as e:
        print(f"[ERROR] Exception occurred while sending email: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(quick_test())