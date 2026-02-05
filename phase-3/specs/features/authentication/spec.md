# Authentication Feature Specification

## Overview
This specification defines the authentication system for the AI-ready full-stack todo app. The authentication system must follow Better Auth with JWT configuration as mandated by the project constitution. All API operations must be secured with JWT tokens.

## Requirements
- Better Auth must be used for authentication (runs only on frontend)
- JWT plugin must be enabled with specific payload requirements
- JWT must be attached to every API request
- Backend must verify JWT using shared secret
- All operations must be user-scoped and enforce task ownership

## Functional Requirements

### 1. Better Auth Configuration
- Better Auth runs ONLY on frontend as per constitution
- JWT plugin MUST be enabled
- JWT payload MUST include:
  - user_id (UUID)
  - email (string)
  - issued_at (timestamp)
  - expiry (maximum 7 days)
- Shared secret must be identical in frontend & backend (BETTER_AUTH_SECRET)

### 2. Frontend Authentication
- JWT MUST be attached to every API request in Authorization header
- Header format: `Authorization: Bearer <token>`
- Token must be refreshed automatically before expiry
- Authentication state must persist across sessions

### 3. Backend Authentication
- MUST verify JWT using shared secret
- MUST reject missing/invalid token with 401 status
- MUST enforce task ownership on EVERY operation
- MUST validate user_id in JWT matches user_id in URL path
- MUST NOT trust frontend input for user_id

### 4. API Security
- ALL endpoints require valid JWT authentication
- ALL queries filtered by authenticated user_id
- Cross-user access must be impossible
- No admin bypass functionality
- No shared tasks between users

### 5. Session Management
- Automatic JWT refresh before expiry
- Secure token storage (HTTP-only cookies or secure local storage)
- Proper logout functionality
- Session timeout handling

## Security Requirements
- All API requests must include valid JWT
- JWT validation must use shared secret (BETTER_AUTH_SECRET)
- Token expiration maximum 7 days as per constitution
- No plaintext password storage
- Secure transmission over HTTPS
- Prevention of JWT replay attacks

## API Contract Compliance
- user_id in URL MUST match JWT user_id (immutable rule)
- Backend MUST NOT trust frontend input (immutable rule)
- ALL queries filtered by authenticated user_id (immutable rule)

## Data Ownership Rules
- Every task belongs to exactly ONE user
- Cross-user access is impossible
- No admin bypass
- No shared tasks

## Integration Points
- Frontend: Better Auth integration with JWT plugin
- Backend: JWT verification middleware
- Database: User association via user_id foreign key
- All task operations must validate user ownership

## Error Handling
- 401 Unauthorized: Missing or invalid JWT
- 403 Forbidden: User attempting to access resources they don't own
- Proper error messages without sensitive information disclosure
- Consistent error response format across all endpoints

## Performance Requirements
- Efficient JWT validation without impacting performance
- Minimal overhead for authentication checks
- Caching considerations for repeated validations
- Proper cleanup of expired sessions

## User Experience Requirements
- Seamless authentication flow
- Automatic login persistence
- Clear error messaging for authentication failures
- Smooth transition between authenticated/unauthenticated states