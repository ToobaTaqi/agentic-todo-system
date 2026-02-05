# MCP Task Operations Specification

## Overview
This specification defines the MCP (Model Context Protocol) tools for task operations in the AI-ready full-stack todo app. These tools enable the AI agent to perform task management operations securely and consistently with the constitutional requirements.

## Requirements
- All tools must enforce user authentication and ownership
- Tools must maintain data integrity and consistency
- Tools must follow the same business logic as traditional API endpoints
- Tools must provide standardized input/output schemas
- Tools must include proper error handling and validation

## Functional Requirements

### 1. add_task Tool
- Tool must create a new task for the authenticated user
- Tool must accept parameters: title (required), description, priority, tags, due_date, is_recurring, recurrence_pattern
- Tool must validate all input parameters
- Tool must associate task with authenticated user_id
- Tool must return the created task object
- Tool must enforce all validation rules from the constitutional Task model

### 2. list_tasks Tool
- Tool must retrieve tasks for the authenticated user
- Tool must accept optional parameters: status, priority, search, sort, order
- Tool must enforce user ownership filtering
- Tool must support pagination parameters
- Tool must return array of task objects
- Tool must apply all constitutional filtering and sorting rules

### 3. complete_task Tool
- Tool must toggle completion status of a specific task
- Tool must accept task_id parameter
- Tool must verify task ownership by authenticated user
- Tool must handle recurring task auto-rescheduling
- Tool must return updated task object
- Tool must enforce constitutional completion behavior

### 4. delete_task Tool
- Tool must permanently delete a specific task
- Tool must accept task_id parameter
- Tool must verify task ownership by authenticated user
- Tool must validate task exists before deletion
- Tool must return success confirmation
- Tool must enforce constitutional deletion rules (no soft deletes)

### 5. update_task Tool
- Tool must update properties of a specific task
- Tool must accept task_id and update parameters
- Tool must verify task ownership by authenticated user
- Tool must validate all update parameters
- Tool must return updated task object
- Tool must enforce all constitutional validation rules

## Security Requirements
- All tools require valid JWT authentication
- user_id in tool context must match JWT user_id
- Tools must NOT trust frontend input for user_id validation
- ALL operations filtered by authenticated user_id
- Cross-user access is impossible
- No admin bypass
- Tool misuse prevention with parameter validation
- Output sanitization for all returned data

## Tool Contracts

### add_task Tool Contract
- **Input Schema**:
  ```json
  {
    "title": "string (required, max 255 chars)",
    "description": "string (optional, max 1000 chars)",
    "priority": "string (high|medium|low, optional)",
    "tags": "array of strings (optional, max 10 items)",
    "due_date": "ISO 8601 datetime string (optional)",
    "is_recurring": "boolean (optional)",
    "recurrence_pattern": "string (daily|weekly|monthly, optional if is_recurring is true)"
  }
  ```
- **Output Schema**:
  ```json
  {
    "success": "boolean",
    "data": "{Complete task object as defined in constitutional Task model}"
  }
  ```
- **Error Codes**:
  - INVALID_INPUT: Input validation failed
  - AUTHORIZATION_ERROR: User not authorized for operation
  - NOT_FOUND: Referenced item not found
  - SERVER_ERROR: Internal server error

### list_tasks Tool Contract
- **Input Schema**:
  ```json
  {
    "status": "string (completed|incomplete, optional)",
    "priority": "string (high|medium|low, optional)",
    "search": "string (keyword search, optional)",
    "sort": "string (due_date|priority|title, optional)",
    "order": "string (asc|desc, optional)",
    "page": "number (pagination page, optional)",
    "limit": "number (items per page, optional, max 100)"
  }
  ```
- **Output Schema**:
  ```json
  {
    "success": "boolean",
    "data": "[Array of task objects]",
    "pagination": "{Pagination metadata}"
  }
  ```
- **Error Codes**:
  - AUTHORIZATION_ERROR: User not authorized for operation
  - VALIDATION_ERROR: Invalid parameter values
  - SERVER_ERROR: Internal server error

### complete_task Tool Contract
- **Input Schema**:
  ```json
  {
    "task_id": "string (required, UUID format)"
  }
  ```
- **Output Schema**:
  ```json
  {
    "success": "boolean",
    "data": "{Updated task object with toggled completion status}"
  }
  ```
- **Error Codes**:
  - INVALID_INPUT: Invalid task_id format
  - AUTHORIZATION_ERROR: User not authorized for operation
  - NOT_FOUND: Task not found
  - SERVER_ERROR: Internal server error (especially for recurring task handling)

### delete_task Tool Contract
- **Input Schema**:
  ```json
  {
    "task_id": "string (required, UUID format)"
  }
  ```
- **Output Schema**:
  ```json
  {
    "success": "boolean",
    "message": "string (confirmation message)"
  }
  ```
- **Error Codes**:
  - INVALID_INPUT: Invalid task_id format
  - AUTHORIZATION_ERROR: User not authorized for operation
  - NOT_FOUND: Task not found
  - SERVER_ERROR: Internal server error

### update_task Tool Contract
- **Input Schema**:
  ```json
  {
    "task_id": "string (required, UUID format)",
    "title": "string (optional, max 255 chars)",
    "description": "string (optional, max 1000 chars)",
    "priority": "string (high|medium|low, optional)",
    "tags": "array of strings (optional, max 10 items)",
    "due_date": "ISO 8601 datetime string (optional)",
    "is_recurring": "boolean (optional)",
    "recurrence_pattern": "string (daily|weekly|monthly, optional)"
  }
  ```
- **Output Schema**:
  ```json
  {
    "success": "boolean",
    "data": "{Updated task object}"
  }
  ```
- **Error Codes**:
  - INVALID_INPUT: Invalid task_id format or parameter validation failed
  - AUTHORIZATION_ERROR: User not authorized for operation
  - NOT_FOUND: Task not found
  - SERVER_ERROR: Internal server error

## Validation Rules
- All UUID parameters must be valid UUID format
- String length limits enforced (title: 255, description: 1000)
- Array length limits enforced (tags: 10 items max)
- Priority must be one of: high, medium, low
- Recurrence pattern must be one of: daily, weekly, monthly, or null
- Due dates must be valid ISO 8601 datetime strings
- Future date validation for due_date where applicable

## Error Handling
- Consistent error response format across all tools
- Proper HTTP-like error codes for different failure scenarios
- Human-readable error messages for debugging
- No sensitive information in error responses
- Graceful handling of edge cases

## Performance Requirements
- Tool execution must complete within 5 seconds
- Database operations must use proper indexing
- Query limits must be enforced (max 100 items per request)
- Response times should be under 2 seconds for typical operations
- Connection pooling must be utilized for database operations

## Business Logic Compliance
- Recurring tasks must auto-reschedule on completion (as per constitution)
- Soft deletes must NOT be allowed (as per constitution)
- Completion must be toggle-based (as per constitution)
- Filtering & sorting must happen server-side (as per constitution)
- All constitutional data model requirements must be enforced