# Authentication API Specification

## Overview
This specification defines the authentication API endpoints for the AI-ready full-stack todo app. The API follows the constitutional requirements for Better Auth with JWT configuration and ensures all operations are properly secured.

## Authentication Requirements (Constitutional)
- Better Auth runs ONLY on frontend
- JWT plugin MUST be enabled
- JWT payload MUST include: user_id, email, issued_at, expiry (maximum 7 days)
- JWT MUST be attached to every API request
- Header format: `Authorization: Bearer <token>`
- Backend MUST verify JWT using shared secret
- Backend MUST reject missing/invalid token with 401
- Backend MUST enforce task ownership on EVERY operation
- Shared secret: BETTER_AUTH_SECRET (identical in frontend & backend)

## API Contract

### Authentication Endpoints
- `GET /api/auth/session` - Verify and return current session
- `POST /api/auth/refresh` - Refresh JWT token (if needed)

## Endpoint Specifications

### GET /api/auth/session
**Description**: Verify the current session and return user information

**Headers**:
```
Authorization: Bearer <jwt_token>
```

**Success Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    "user_id": "uuid-string",
    "email": "user@example.com",
    "expires_at": "ISO 8601 datetime string",
    "authenticated": true
  }
}
```

**Error Response (401 Unauthorized)**:
```json
{
  "success": false,
  "error": {
    "code": "INVALID_TOKEN",
    "message": "Invalid or expired JWT token"
  }
}
```

### POST /api/auth/refresh
**Description**: Refresh the JWT token if nearing expiration

**Headers**:
```
Authorization: Bearer <current_jwt_token>
```

**Request Body**:
```json
{}
```

**Success Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    "token": "new_jwt_token",
    "expires_at": "ISO 8601 datetime string"
  }
}
```

**Error Response (401 Unauthorized)**:
```json
{
  "success": false,
  "error": {
    "code": "INVALID_TOKEN",
    "message": "Invalid or expired JWT token, please log in again"
  }
}
```

## Security Requirements
- All endpoints require valid JWT authentication
- JWT verification must use shared secret (BETTER_AUTH_SECRET)
- user_id in JWT must be validated for all operations
- All API requests must be authenticated via JWT
- Token expiration maximum 7 days as per constitution
- Proper validation of JWT signature and claims

## Request/Response Format
### Common Headers
```
Content-Type: application/json
Authorization: Bearer <jwt_token>
```

### Common Success Response
```json
{
  "success": true,
  "data": {}
}
```

### Common Error Response
```json
{
  "success": false,
  "error": {
    "code": "error_code",
    "message": "Human-readable error message",
    "details": {} // Optional details about the error
  }
}
```

## Validation Rules
- JWT token must be present in Authorization header
- JWT signature must be valid
- JWT must not be expired
- JWT claims must include required fields (user_id, email, issued_at, expiry)
- All requests must be from authenticated users

## Error Handling
- 401 Unauthorized: Invalid or missing JWT token
- 403 Forbidden: Insufficient permissions (though not typically used for auth endpoints)
- 500 Internal Server Error: Server-side authentication failure

## Integration Requirements
- Must work seamlessly with Better Auth frontend implementation
- Must validate tokens using the same shared secret
- Must enforce user_id validation across all protected endpoints
- Must maintain consistency with task API authentication