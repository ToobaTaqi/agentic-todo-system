import asyncio
import aiohttp
import json

async def test_registration():
    url = "http://localhost:8000/api/v1/register"

    # Sample user data
    user_data = {
        "email": "async_test@example.com",
        "password": "12345678",
        "first_name": "Async",
        "last_name": "Test"
    }

    headers = {
        "Content-Type": "application/json"
    }

    print(f"Sending registration request to {url}")
    print(f"User data: {json.dumps(user_data, indent=2)}")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=user_data, headers=headers) as response:
                print(f"Response Status Code: {response.status}")
                print(f"Response Headers: {dict(response.headers)}")

                response_text = await response.text()
                print(f"Response Body: {response_text}")

                if response.status == 200:
                    print("\n✓ Async registration successful!")
                    try:
                        response_data = json.loads(response_text)
                        print(f"Access Token: {response_data.get('access_token', 'Not found')}")
                        print(f"User ID: {response_data.get('user', {}).get('id', 'Not found')}")
                        print(f"User Email: {response_data.get('user', {}).get('email', 'Not found')}")
                    except json.JSONDecodeError:
                        print("Could not parse JSON response")
                elif response.status == 409:
                    print("\n⚠ User already exists (this is expected if running multiple times)")
                else:
                    print(f"\n✗ Registration failed with status code: {response.status}")

    except aiohttp.ClientConnectorError:
        print("✗ Could not connect to the server. Make sure it's running on http://localhost:8000")
    except Exception as e:
        print(f"✗ An error occurred: {str(e)}")

if __name__ == "__main__":
    print("Testing async registration endpoint...")
    asyncio.run(test_registration())