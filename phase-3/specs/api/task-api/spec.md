# Task API Specification

## Overview
This specification defines the complete API contract for task management in the AI-ready full-stack todo app. The API follows the immutable contract defined in the project constitution with specific endpoints and security requirements.

## API Contract (Immutable)
The following endpoints must be implemented exactly as specified:

### Task Endpoints
- `GET    /api/{user_id}/tasks` - Retrieve user's tasks
- `POST   /api/{user_id}/tasks` - Create a new task
- `GET    /api/{user_id}/tasks/{id}` - Retrieve a specific task
- `PUT    /api/{user_id}/tasks/{id}` - Update a task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task
- `PATCH  /api/{user_id}/tasks/{id}/complete` - Toggle task completion

## Authentication Requirements
- All endpoints require valid JWT authentication
- JWT must be provided in Authorization header: `Authorization: Bearer <token>`
- user_id in URL path MUST match user_id in JWT token
- Backend MUST NOT trust frontend input for user_id validation
- ALL queries MUST be filtered by authenticated user_id

## Request/Response Format

### Common Headers
```
Content-Type: application/json
Authorization: Bearer <jwt_token>
```

### Task Object Structure
```json
{
  "id": "uuid-string",
  "user_id": "uuid-string",
  "title": "string (required)",
  "description": "string (optional)",
  "priority": "string (high|medium|low, default: medium)",
  "tags": "array of strings",
  "due_date": "ISO 8601 datetime string (nullable)",
  "is_completed": "boolean (default: false)",
  "is_recurring": "boolean (default: false)",
  "recurrence_pattern": "string (daily|weekly|monthly|null, default: null)",
  "created_at": "ISO 8601 datetime string",
  "updated_at": "ISO 8601 datetime string"
}
```

## Endpoint Specifications

### POST /api/{user_id}/tasks
**Description**: Create a new task for the specified user

**Request Body**:
```json
{
  "title": "string (required)",
  "description": "string (optional)",
  "priority": "string (high|medium|low, optional)",
  "tags": "array of strings (optional)",
  "due_date": "ISO 8601 datetime string (optional)",
  "is_recurring": "boolean (optional)",
  "recurrence_pattern": "string (daily|weekly|monthly, optional if is_recurring is true)"
}
```

**Success Response (201 Created)**:
```json
{
  "success": true,
  "data": {
    // Complete task object as defined above
  }
}
```

**Error Responses**:
- 400: Invalid request body
- 401: Unauthorized (invalid/missing JWT)
- 403: Forbidden (user_id mismatch)
- 422: Validation error (invalid fields)

### GET /api/{user_id}/tasks
**Description**: Retrieve tasks for the specified user

**Query Parameters**:
- `page`: Page number for pagination (default: 1)
- `limit`: Items per page for pagination (default: 20, max: 100)
- `search`: Keyword search in title/description (optional)
- `status`: Filter by completion status (completed|incomplete, optional)
- `priority`: Filter by priority (high|medium|low, multiple allowed)
- `due_status`: Filter by due date status (overdue|today|tomorrow|week|month, optional)
- `sort`: Sort field (due_date|priority|title, default: due_date)
- `order`: Sort order (asc|desc, default: asc)

**Success Response (200 OK)**:
```json
{
  "success": true,
  "data": [
    // Array of task objects
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

**Error Responses**:
- 401: Unauthorized (invalid/missing JWT)
- 403: Forbidden (user_id mismatch)

### GET /api/{user_id}/tasks/{id}
**Description**: Retrieve a specific task

**Success Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    // Complete task object as defined above
  }
}
```

**Error Responses**:
- 401: Unauthorized (invalid/missing JWT)
- 403: Forbidden (user_id mismatch or task doesn't belong to user)
- 404: Not Found (task doesn't exist)

### PUT /api/{user_id}/tasks/{id}
**Description**: Update a specific task

**Request Body**:
```json
{
  "title": "string (optional)",
  "description": "string (optional)",
  "priority": "string (high|medium|low, optional)",
  "tags": "array of strings (optional)",
  "due_date": "ISO 8601 datetime string (optional)",
  "is_recurring": "boolean (optional)",
  "recurrence_pattern": "string (daily|weekly|monthly, optional)"
}
```

**Success Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    // Updated task object as defined above
  }
}
```

**Error Responses**:
- 400: Invalid request body
- 401: Unauthorized (invalid/missing JWT)
- 403: Forbidden (user_id mismatch or task doesn't belong to user)
- 404: Not Found (task doesn't exist)
- 422: Validation error (invalid fields)

### DELETE /api/{user_id}/tasks/{id}
**Description**: Delete a specific task

**Success Response (200 OK)**:
```json
{
  "success": true,
  "message": "Task deleted successfully"
}
```

**Error Responses**:
- 401: Unauthorized (invalid/missing JWT)
- 403: Forbidden (user_id mismatch or task doesn't belong to user)
- 404: Not Found (task doesn't exist)

### PATCH /api/{user_id}/tasks/{id}/complete
**Description**: Toggle task completion status

**Request Body**:
```json
{
  "is_completed": "boolean (optional, if provided will set to this value, otherwise toggle)"
}
```

**Success Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    // Updated task object with toggled completion status
  }
}
```

**Special Behavior**: If the task is recurring, this endpoint should also handle auto-rescheduling by creating a new instance of the recurring task.

**Error Responses**:
- 401: Unauthorized (invalid/missing JWT)
- 403: Forbidden (user_id mismatch or task doesn't belong to user)
- 404: Not Found (task doesn't exist)
- 500: Internal Server Error (auto-rescheduling failure for recurring tasks)

## Security Requirements
- JWT verification must use shared secret (BETTER_AUTH_SECRET)
- user_id in URL path must match user_id in JWT
- All operations must be scoped to authenticated user
- No cross-user access allowed
- No admin bypass functionality

## Performance Requirements
- All endpoints must support pagination
- Query limits must be enforced (max 100 items per request)
- Max payload size must be enforced
- Database indexes must be used for filtering/sorting
- Response times should be under 500ms for typical requests

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
- UUID format validation for user_id and task id
- String length limits for title (max 255 chars) and description (max 1000 chars)
- Array length limits for tags (max 10 items)
- Future date validation for due_date
- Enum validation for priority and recurrence_pattern

## Rate Limiting
- API endpoints should implement rate limiting to prevent abuse
- Reasonable limits: 100 requests per minute per user
- Proper HTTP headers for rate limit information