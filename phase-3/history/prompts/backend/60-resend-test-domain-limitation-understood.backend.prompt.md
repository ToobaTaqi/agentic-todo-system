---
title: "Understanding Resend Test Domain Limitation for User Registration"
date: "2026-02-03"
author: "Claude AI"
type: "documentation"
component: "backend"
feature: "email-verification"
---

# Understanding Resend Test Domain Limitation for User Registration

## Issue Clarification
The application code is correctly implemented to send verification emails to each user's specific email address during registration. The apparent issue is not with the application logic, but with Resend's test domain limitations.

## Root Cause
- **Application Code**: Properly sends emails to the user's provided email address (user.email)
- **Resend Test Domain**: Free test domain (resend.dev) only allows sending emails TO the email address used to register with Resend
- **Misunderstanding**: Appears that all emails go to one address, but it's due to test domain restrictions

## Application Implementation is Correct
✅ Registration flow correctly captures user's email address
✅ Verification email is sent to user.email (the address they provided)
✅ Verification token and link are personalized for each user
✅ Backend verification endpoint processes tokens correctly

## Test Domain vs. Verified Domain Behavior
### With Test Domain (resend.dev):
- Can only send TO: your registered email address (toobtq@gmail.com)
- FROM: onboarding@resend.dev
- Works for: Testing and development purposes

### With Verified Domain (yourdomain.com):
- Can send TO: ANY email address
- FROM: noreply@yourdomain.com (or any address from your domain)
- Works for: Production with multiple users

## Solution for Production
To enable email verification for users with different email addresses:
1. Verify your own domain with Resend
2. Update SENDER_EMAIL to use your verified domain
3. Same application code will work for all users

## Verification
- Application code: `await send_verification_email(user.email, verification_token)`
- user.email = the specific email address each user provides during registration
- This is working correctly and will scale to any number of users when using a verified domain

## Documentation
Created RESOLVE_EMAIL_SETUP.md to explain the difference between test domain limitations and production setup.

The application is properly implemented for multi-user registration and verification; it just requires a verified domain for production use.