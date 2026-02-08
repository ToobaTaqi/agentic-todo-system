---
title: "Switch from Gmail SMTP to Resend for Email Verification"
date: "2026-02-03"
author: "Claude AI"
type: "enhancement"
component: "backend"
feature: "email-verification"
---

# Switch from Gmail SMTP to Resend for Email Verification

## Issue Description
The application was using Gmail SMTP for sending verification emails, which was causing timeout errors on Railway due to cloud platform restrictions on Gmail's SMTP service. The error was:
```
ERROR:utils.email_utils:Failed to send verification email to user@example.com: Timed out connecting to smtp.gmail.com on port 587
```

## Root Cause
- Gmail actively blocks connections from cloud platforms like Railway to prevent spam
- Cloud hosting providers often have outbound SMTP restrictions
- Gmail's security policies restrict access from known hosting provider IP ranges

## Solution Implemented
Replaced Gmail SMTP implementation with Resend transactional email service which is designed for cloud deployments.

### Files Modified
1. `backend/utils/email_utils.py` - Updated to use Resend API instead of aiosmtplib/Gmail SMTP
2. `backend/requirements.txt` - Replaced aiosmtplib with resend library
3. `backend/.env` - Updated configuration to use Resend API key instead of Gmail credentials
4. `backend/test_email_config.py` - Updated test script to check for Resend configuration

### Key Changes
- Replaced `aiosmtplib.send()` with `resend.Emails.send()`
- Updated environment variable requirements from GMAIL_APP_PASSWORD to RESEND_API_KEY
- Maintained same HTML email templates and functionality
- Preserved all error handling and logging

## Testing
- Email sending function updated to work with Resend
- Test email function updated accordingly
- Maintained backward compatibility for frontend verification flow

## Deployment Considerations
- Requires obtaining a Resend API key from resend.com
- For production, register a domain with Resend
- For development, Resend provides a test domain
- This resolves the Railway deployment SMTP timeout issue

## Environment Variables Required
- `RESEND_API_KEY` - API key from Resend dashboard
- `SENDER_EMAIL` - Email address registered with Resend (e.g., onboarding@yourdomain.com)

This change enables reliable email delivery on Railway while maintaining the same verification flow functionality.