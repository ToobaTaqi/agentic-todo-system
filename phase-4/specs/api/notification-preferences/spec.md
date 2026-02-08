# Notification Preferences API Specification

## Overview
This specification defines the API endpoints for managing user notification preferences in the AI-ready full-stack todo app. The API allows users to configure their browser notification settings, following the constitutional requirements for time reminders and browser notifications.

## Requirements
- All endpoints require valid JWT authentication
- All operations must be user-scoped and enforce ownership
- Must support user preference storage for notification settings
- Must follow the constitutional API contract rules
- Must integrate with browser notification functionality

## API Contract

### Notification Preferences Endpoints
- `GET    /api/{user_id}/notification-preferences` - Retrieve user's notification preferences
- `PUT    /api/{user_id}/notification-preferences` - Update user's notification preferences
- `DELETE /api/{user_id}/notification-preferences` - Reset user's notification preferences to defaults

## Authentication Requirements
- All endpoints require valid JWT authentication
- JWT must be provided in Authorization header: `Authorization: Bearer <token>`
- user_id in URL path MUST match user_id in JWT token
- Backend MUST verify JWT and enforce user_id validation
- ALL operations filtered by authenticated user_id

## Request/Response Format

### Common Headers
```
Content-Type: application/json
Authorization: Bearer <jwt_token>
```

### Notification Preferences Object Structure
```json
{
  "id": "uuid-string (preference record id)",
  "user_id": "uuid-string",
  "enabled": "boolean (whether notifications are enabled)",
  "timing_minutes_before": "integer (minutes before due date to notify, e.g., 60 for 1 hour)",
  "due_soon_reminder_enabled": "boolean (notify for upcoming due tasks)",
  "overdue_reminder_enabled": "boolean (notify for overdue tasks)",
  "recurring_task_reminder_enabled": "boolean (notify for recurring tasks)",
  "custom_notification_times": "array of specific times for custom notifications",
  "do_not_disturb_start": "string (HH:MM format, optional)",
  "do_not_disturb_end": "string (HH:MM format, optional)",
  "created_at": "ISO 8601 datetime string",
  "updated_at": "ISO 8601 datetime string"
}
```

## Endpoint Specifications

### GET /api/{user_id}/notification-preferences
**Description**: Retrieve the user's current notification preferences

**Success Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    // Complete notification preferences object as defined above
  }
}
```

**Error Responses**:
- 401: Unauthorized (invalid/missing JWT)
- 403: Forbidden (user_id mismatch)
- 404: Not Found (preferences not set for user, return defaults)

### PUT /api/{user_id}/notification-preferences
**Description**: Update the user's notification preferences

**Request Body**:
```json
{
  "enabled": "boolean (optional)",
  "timing_minutes_before": "integer (optional, 1-1440 for 1 minute to 24 hours)",
  "due_soon_reminder_enabled": "boolean (optional)",
  "overdue_reminder_enabled": "boolean (optional)",
  "recurring_task_reminder_enabled": "boolean (optional)",
  "custom_notification_times": "array of specific times (optional)",
  "do_not_disturb_start": "string (HH:MM format, optional)",
  "do_not_disturb_end": "string (HH:MM format, optional)"
}
```

**Success Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    // Updated notification preferences object
  }
}
```

**Error Responses**:
- 400: Invalid request body
- 401: Unauthorized (invalid/missing JWT)
- 403: Forbidden (user_id mismatch)
- 422: Validation error (invalid field values)

### DELETE /api/{user_id}/notification-preferences
**Description**: Reset the user's notification preferences to default values

**Success Response (200 OK)**:
```json
{
  "success": true,
  "message": "Notification preferences reset to defaults"
}
```

**Error Responses**:
- 401: Unauthorized (invalid/missing JWT)
- 403: Forbidden (user_id mismatch)

## Security Requirements
- JWT verification must use shared secret (BETTER_AUTH_SECRET)
- user_id in URL path must match user_id in JWT
- All operations must be scoped to authenticated user
- No cross-user access allowed
- No admin bypass functionality
- Input validation for all preference fields

## Validation Rules
- `timing_minutes_before`: Integer between 1 and 1440 (1 minute to 24 hours)
- `do_not_disturb_start` and `do_not_disturb_end`: Valid HH:MM format
- `do_not_disturb_end` must be after `do_not_disturb_start` if both are set
- `custom_notification_times`: Array of valid HH:MM format times
- All boolean fields must be valid booleans
- `user_id` must be a valid UUID matching the authenticated user

## Performance Requirements
- Efficient database queries for preference retrieval
- Fast response times for preference updates
- Proper indexing on user_id field
- Minimal payload sizes

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

## Default Values
When user preferences don't exist or are reset, use these defaults:
- `enabled`: true
- `timing_minutes_before`: 60 (1 hour before due date)
- `due_soon_reminder_enabled`: true
- `overdue_reminder_enabled`: true
- `recurring_task_reminder_enabled`: true
- `custom_notification_times`: []
- `do_not_disturb_start`: null
- `do_not_disturb_end`: null