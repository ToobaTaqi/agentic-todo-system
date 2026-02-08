# PHR-76: GROQ API Model Decommission Error Resolution

## Issue Summary

The AI chat functionality in the agentic-todo-system is experiencing a failure due to a decommissioned GROQ API model. When users attempt to interact with the AI chat, they receive the error message: "Sorry, there's an issue with the AI service configuration. Please contact the administrator."

## Root Cause Analysis

### Error Details
- **API Endpoint**: `/api/{user_id}/chat`
- **Error Code**: 400 Bad Request
- **Error Message**: "The model llama3-70b-8192 has been decommissioned and is no longer supported"
- **Error Type**: `invalid_request_error`
- **Error Code**: `model_decommissioned`

### Technical Stack Trace
1. Step 1: Authentication and validation successful
2. Step 2: Conversation creation successful
3. Step 3: User message saving successful
4. Step 4: Conversation history preparation successful (but with database exec error)
5. Step 5: GROQ API initialization successful
6. Step 6: **FAILURE** - GROQ API call fails due to decommissioned model

### Database Issue Observed
There's also a secondary issue noted in the logs: `'AsyncSession' object has no attribute 'exec'` which suggests SQLAlchemy version compatibility issues with the database query methods.

## Impact Assessment

- **User Experience**: AI chat functionality is completely non-functional
- **System Health**: Backend API is operational but returning error responses
- **Business Impact**: Users cannot leverage AI features for task management
- **Severity**: High - Critical functionality is broken

## Solution Required

### Immediate Fix
1. Update the GROQ API model reference from `llama3-70b-8192` to a currently supported model
2. According to GROQ documentation, recommended replacements could be:
   - `llama-3.1-70b-versatile`
   - `llama-3.1-8b-instant`
   - `mixtral-8x7b-32768`
   - `gemma2-9b-it`

### Secondary Fix
Address the database compatibility issue where `AsyncSession.exec()` method is not available, likely due to SQLAlchemy version differences.

## Implementation Plan

1. Locate the GROQ API integration code in the backend
2. Update the model parameter to use a supported model
3. Test the API call with the new model
4. Address the database session execution method
5. Verify end-to-end functionality

## Files Likely Affected

- Backend chat API implementation (likely in `/backend/routes/chat/chat_api.py`)
- Database query methods for retrieving conversation history
- GROQ API client configuration

## Verification Steps

1. Send a test message through the chat interface
2. Verify that the AI responds appropriately
3. Confirm that conversation history is maintained
4. Ensure no further deprecation errors occur

## Business Context

This issue blocks the core AI functionality that differentiates this todo system as "agentic". Resolving this quickly is essential for maintaining the value proposition of AI-assisted task management.