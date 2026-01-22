# Task CRUD Feature Specification

## Overview
This specification defines the core functionality for creating, reading, updating, and deleting tasks in the AI-ready full-stack todo app. This feature is mandatory as per the project constitution and must follow all security and data ownership rules.

## Requirements
- Users must be able to add new tasks
- Users must be able to view their task list
- Users must be able to update existing tasks
- Users must be able to delete tasks
- Users must be able to mark tasks as complete/incomplete
- All operations must be authenticated and user-scoped
- Data ownership rules must be enforced (no cross-user access)

## Functional Requirements

### 1. Add Task
- User can create a new task with required fields
- Task must include user_id from authenticated session
- Required fields: title
- Optional fields: description, priority, tags, due_date, is_recurring, recurrence_pattern
- Task is associated with the authenticated user
- Task creation must be validated against user authentication

### 2. View Task List
- User can retrieve all tasks associated with their user_id
- Tasks must be filtered by authenticated user_id
- Support for pagination (mandatory for performance)
- Support for filtering, sorting, and search (as per constitution)

### 3. Update Task
- User can modify existing task properties
- User can only update tasks associated with their user_id
- Backend must verify JWT and enforce ownership
- Validation must be performed on all updates

### 4. Delete Task
- User can permanently delete tasks associated with their user_id
- Soft deletes are not allowed (as per constitution)
- Backend must verify JWT and enforce ownership

### 5. Mark Task as Complete
- User can toggle task completion status
- Backend must verify JWT and enforce ownership
- Completion is toggle-based (as per constitution)

## Security Requirements
- All operations require valid JWT authentication
- User_id in URL must match JWT user_id
- Backend must NOT trust frontend input
- ALL queries filtered by authenticated user_id
- Cross-user access is impossible
- No admin bypass
- No shared tasks

## Data Model Requirements
- id (UUID, Primary Key)
- user_id (UUID, indexed)
- title (required, string)
- description (optional, string)
- priority (high | medium | low)
- tags (array[string])
- due_date (datetime, nullable)
- is_completed (boolean)
- is_recurring (boolean)
- recurrence_pattern (daily | weekly | monthly | null)
- created_at (timestamp)
- updated_at (timestamp)

## API Endpoints
- POST `/api/{user_id}/tasks` - Create task
- GET `/api/{user_id}/tasks` - Get user's tasks
- GET `/api/{user_id}/tasks/{id}` - Get specific task
- PUT `/api/{user_id}/tasks/{id}` - Update task
- DELETE `/api/{user_id}/tasks/{id}` - Delete task
- PATCH `/api/{user_id}/tasks/{id}/complete` - Toggle completion

## Validation Rules
- All requests must include valid JWT in Authorization header
- user_id in URL path must match JWT user_id
- Title is required for task creation
- Task ID must exist and belong to authenticated user
- Priority must be one of: high, medium, low
- Recurrence pattern must be one of: daily, weekly, monthly, or null

## Error Handling
- 401 Unauthorized: Invalid or missing JWT
- 403 Forbidden: User attempting to access another user's task
- 404 Not Found: Task does not exist
- 422 Unprocessable Entity: Validation errors

## Performance Requirements
- Pagination mandatory for task lists
- Query limits enforced (as per constitution)
- Max payload size enforced
- Optimistic UI updates (as per constitution)