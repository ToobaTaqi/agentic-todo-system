# Tagging Feature Specification

## Overview
This specification defines the tagging system for tasks in the AI-ready full-stack todo app. The tagging feature is mandatory as per the project constitution and must support predefined tags (Work, Home) and custom tags with proper UI representation and filtering capabilities.

## Requirements
- Tasks must support tags as an array of strings
- Support for predefined tags: Work, Home
- Support for custom tags (user-defined)
- Tags must be selectable during task creation and updates
- Tags must be displayed in the UI with appropriate visual indicators
- Tasks must be filterable by tags
- Tag data must be stored in the database as specified in constitution

## Functional Requirements

### 1. Tag Types
- Predefined tags: Work, Home
- Custom tags: User-defined tags
- Tags are optional during task creation
- Multiple tags per task allowed
- Tag names must be unique within a task

### 2. Task Creation with Tags
- Users can select tags during task creation
- Users can add custom tags during task creation
- Multiple tags can be added to a single task
- Tag validation occurs before saving to database
- Predefined tags are suggested to users

### 3. Task Updates with Tags
- Users can add tags to existing tasks
- Users can remove tags from existing tasks
- Users can modify tags on existing tasks
- Tag changes must be validated
- Updated tags must be saved to database

### 4. Tag Display
- Tags must be displayed on TaskCard component
- Visual indicators for different tags (TagChip component)
- Tags must be distinguishable in both light and dark modes
- Support for multiple tags per task
- Follow design system color specifications

### 5. Tag Filtering
- Users must be able to filter tasks by tags
- Filter options: All, Work, Home, Custom tags
- Multiple tag filters should be supported
- Filtered results must be displayed in TaskList
- Tag filters should be combinable with other filters

### 6. Custom Tag Creation
- Users can create custom tags during task creation
- Users can create custom tags during task updates
- Custom tags should be validated for length and characters
- Custom tags should be case-insensitive for uniqueness
- Suggested tags based on user's previously used tags

### 7. Tag Validation
- Tag names must not exceed 50 characters
- Tag names must not be empty or whitespace-only
- Tag names must contain only alphanumeric characters, hyphens, and underscores
- Duplicate tags within a single task should be prevented
- Validation must occur on both frontend and backend

## Data Model Requirements
- Field name: `tags`
- Type: Array of strings
- Default value: Empty array []
- Nullable: No (defaults to empty array)
- Storage: JSON array in database
- Indexed: No specific index required

## API Requirements
- Tags must be included in all task operations
- POST `/api/{user_id}/tasks`: Accept tags in request body
- GET `/api/{user_id}/tasks`: Include tags in response
- PUT `/api/{user_id}/tasks/{id}`: Allow tags updates
- GET `/api/{user_id}/tasks`: Support filtering by tags
- Tags array must be properly validated and sanitized

## UI Component Requirements
- TagChip component to display individual tags with visual indicators
- Tag input system in AddTaskModal and EditTaskModal
- Tag suggestion system for common tags
- Tag filtering controls in FilterPanel
- Tag management interface for custom tags

## Security Requirements
- Tag operations must be authenticated
- Users can only modify tags of their own tasks
- Tag validation must occur server-side
- No cross-user tag modifications allowed
- Prevent injection attacks through tag names

## Performance Requirements
- Tag filtering must be efficient
- Tag display must not impact UI performance
- Tag operations should have minimal latency
- Tag suggestions should load quickly

## Accessibility Requirements
- Tag indicators must be accessible to screen readers
- Color contrast must meet WCAG standards
- Keyboard navigation must work with tag elements
- Proper labeling for tag inputs and selections

## Validation Rules
- Tag names must be 1-50 characters long
- Tag names must contain only alphanumeric, hyphens, underscores
- No duplicate tags within a single task
- Empty or whitespace-only tags not allowed
- Tags must be validated on both frontend and backend

## Error Handling
- 422 Unprocessable Entity: Invalid tag format
- 422 Unprocessable Entity: Tag too long (>50 chars)
- 422 Unprocessable Entity: Empty or whitespace-only tag
- 401 Unauthorized: Unauthenticated tag operation
- 403 Forbidden: Attempt to modify another user's task tags
- 404 Not Found: Task does not exist for tag update