# Sample User Creation for Testing - PHR

## Overview
This PHR documents the creation of a sample user in the AI-Ready Full-Stack Todo App database for testing purposes. This enables immediate testing of the application without requiring new user registration.

## Sample User Details
A sample user has been created with the following credentials:

- **Email**: test@example.com
- **Password**: TestPass123!
- **Full Name**: Test User
- **Account Status**: Active and Verified (no email verification required)
- **User ID**: 60f568ab-027f-4278-bdd9-eae70779e987

## Implementation Details
- Created using a dedicated Python script: `create_sample_user.py`
- Password is properly hashed using the application's password hashing mechanism
- User is marked as verified to avoid email verification requirements
- User is marked as active for immediate access
- Database connection uses the same configuration as the main application

## Testing Instructions
To test the application with the sample user:

1. Start the backend server: `cd backend && uvicorn main:app --reload`
2. Start the frontend server: `cd frontend && npm run dev`
3. Navigate to the frontend application (typically http://localhost:3000)
4. Click on "Login" or navigate to /auth/login
5. Use the following credentials:
   - Email: test@example.com
   - Password: TestPass123!

## Security Notes
- This sample user is intended for testing purposes only
- The password "TestPass123!" is publicly documented in this PHR
- For production use, create new users with secure passwords
- The sample user can be safely deleted from the database if needed

## Script Details
The `create_sample_user.py` script:
- Connects to the database using the same connection string as the main app
- Checks if a test user already exists to prevent duplicates
- Uses proper password hashing via the User model's hash_password method
- Sets is_verified=True to bypass email verification
- Logs the created user's details for easy access

## Date
2026-01-19