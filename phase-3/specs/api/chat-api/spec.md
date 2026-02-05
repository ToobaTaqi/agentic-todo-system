# Chat API Specification

## Overview
This specification defines the AI-powered chat API endpoint for the AI-ready full-stack todo app. The API follows the constitutional contract with specific endpoint and security requirements for natural language task management.

## API Contract (Immutable)
The following endpoint must be implemented exactly as specified:

### Chat Endpoint
- `POST /api/{user_id}/chat` - Process natural language task requests

## Authentication Requirements
- All endpoints require valid JWT authentication
- JWT must be provided in Authorization header: `Authorization: Bearer <jwt_token>`
- user_id in URL path MUST match user_id in JWT token
- Backend MUST NOT trust frontend input for user_id validation
- ALL queries MUST be filtered by authenticated user_id

## Request/Response Format

### Common Headers
```
Content-Type: application/json
Authorization: Bearer <jwt_token>
```

### Chat Endpoint Specification

#### POST /api/{user_id}/chat
**Description**: Process natural language request for task management and return AI-generated response

**Request Body**:
```json
{
  "conversation_id": "uuid-string (optional)",
  "message": "string (required, natural language request)"
}
```

**Success Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    "conversation_id": "uuid-string",
    "response": "string (AI-generated response)",
    "tool_calls": [
      {
        "tool_name": "string (MCP tool name)",
        "arguments": "object (tool arguments)",
        "result": "object (tool execution result)"
      }
    ]
  }
}
```

**Error Responses**:
- 400: Invalid request body
- 401: Unauthorized (invalid/missing JWT)
- 403: Forbidden (user_id mismatch)
- 422: Validation error (invalid fields or natural language processing error)
- 500: Internal Server Error (AI processing or tool execution failure)

## Security Requirements
- JWT verification must use shared secret (BETTER_AUTH_SECRET)
- user_id in URL path must match user_id in JWT
- All operations must be scoped to authenticated user
- No cross-user access allowed
- No admin bypass functionality
- AI prompt injection protection for natural language inputs
- Output sanitization for AI-generated responses
- Conversation isolation ensuring user data separation

## Performance Requirements
- API endpoint must support rate limiting
- Agent response times should be under 10 seconds for typical requests
- Conversation history loading must be paginated
- History window limits for performance optimization
- Agent timeout enforcement (max 30 seconds per request)
- Tool call quotas to prevent abuse
- Cost monitoring for AI usage

## Error Handling
- Consistent error response format:
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
- All inputs must be validated
- UUID format validation for user_id and conversation_id
- String length limits for message content (max 10000 chars)
- Natural language content must be non-empty
- Agent must validate all extracted parameters before MCP tool execution
- Tool parameters must conform to MCP tool specifications

## Rate Limiting
- API endpoint should implement rate limiting to prevent abuse
- Reasonable limits: 50 requests per minute per user for chat endpoint
- Proper HTTP headers for rate limit information
- Additional quota limits for AI usage: 100 tool calls per hour per user

## Conversation Management
- If conversation_id is provided, continue existing conversation
- If conversation_id is not provided, create new conversation
- Conversation history must be loaded and provided to agent
- User message must be persisted to conversation history
- Assistant response must be persisted to conversation history
- Conversation context must be maintained across requests