import requests
import json

# Test the registration endpoint
def test_registration():
    url = "http://localhost:8000/api/v1/register"

    # Sample user data
    user_data = {
        "email": "testuser@example.com",
        "password": "12345678",
        "first_name": "Test",
        "last_name": "User"
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        print(f"Sending registration request to {url}")
        print(f"User data: {json.dumps(user_data, indent=2)}")

        response = requests.post(url, json=user_data, headers=headers)

        print(f"Response Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text}")

        if response.status_code == 200:
            print("\n✓ Registration successful!")
            response_data = response.json()
            print(f"Access Token: {response_data.get('access_token', 'Not found')}")
            print(f"User ID: {response_data.get('user', {}).get('id', 'Not found')}")
            print(f"User Email: {response_data.get('user', {}).get('email', 'Not found')}")
        elif response.status_code == 409:
            print("\n⚠ User already exists (this is expected if running multiple times)")
        else:
            print(f"\n✗ Registration failed with status code: {response.status_code}")

    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to the server. Make sure it's running on http://localhost:8000")
    except Exception as e:
        print(f"✗ An error occurred: {str(e)}")

if __name__ == "__main__":
    test_registration()