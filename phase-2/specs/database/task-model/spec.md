# Task Database Model Specification

## Overview
This specification defines the database schema for the Task model in the AI-ready full-stack todo app. The model follows the constitutional requirements with specific field definitions, constraints, and indexing requirements.

## Data Model Requirements

### Core Fields
- `id` (UUID, Primary Key)
  - Type: UUID (universally unique identifier)
  - Constraints: Primary Key, Not Null, Unique
  - Generation: Auto-generated UUID4
  - Purpose: Unique identifier for each task

- `user_id` (UUID, Indexed)
  - Type: UUID (foreign key reference to user)
  - Constraints: Not Null, Indexed
  - Purpose: Links task to the user who owns it
  - Requirement: Must match authenticated user_id

### Essential Task Information
- `title` (String)
  - Type: String/VARCHAR
  - Constraints: Not Null, Length 1-255 characters
  - Purpose: Main description/title of the task
  - Requirement: Required field for all tasks

- `description` (String, Nullable)
  - Type: String/VARCHAR
  - Constraints: Nullable, Length 0-1000 characters
  - Purpose: Detailed description of the task
  - Requirement: Optional field

### Priority Management
- `priority` (String)
  - Type: String/ENUM
  - Values: "high", "medium", "low"
  - Constraints: Not Null, Default: "medium"
  - Purpose: Priority level of the task
  - Requirement: Must be one of the three values

### Tagging System
- `tags` (Array of Strings)
  - Type: JSON Array of Strings
  - Constraints: Not Null, Default: Empty Array []
  - Purpose: Categorization tags for the task
  - Requirement: Array of strings, each up to 50 characters

### Due Date Management
- `due_date` (DateTime, Nullable)
  - Type: DateTime/Timestamp with timezone
  - Constraints: Nullable
  - Purpose: Deadline for completing the task
  - Requirement: If set, must be in the future

### Completion Tracking
- `is_completed` (Boolean)
  - Type: Boolean
  - Constraints: Not Null, Default: False
  - Purpose: Completion status of the task
  - Requirement: Tracks whether task is completed

### Recurring Task Management
- `is_recurring` (Boolean)
  - Type: Boolean
  - Constraints: Not Null, Default: False
  - Purpose: Indicates if task is recurring
  - Requirement: True if task has recurrence pattern

- `recurrence_pattern` (String, Nullable)
  - Type: String/ENUM
  - Values: "daily", "weekly", "monthly", null
  - Constraints: Nullable
  - Purpose: Pattern for recurring tasks
  - Requirement: Must be null if is_recurring is false

### Timestamps
- `created_at` (DateTime)
  - Type: DateTime/Timestamp with timezone
  - Constraints: Not Null, Auto-generated on creation
  - Purpose: Timestamp when task was created
  - Requirement: Automatically set on creation

- `updated_at` (DateTime)
  - Type: DateTime/Timestamp with timezone
  - Constraints: Not Null, Auto-generated on update
  - Purpose: Timestamp when task was last updated
  - Requirement: Automatically updated on any change

## Constitutional Compliance Requirements

### Data Ownership Rules
- Every task belongs to exactly ONE user (enforced by user_id)
- Cross-user access is impossible (enforced by authentication)
- No admin bypass functionality
- No shared tasks between users

### Indexing Requirements
- Index on `user_id` (required for user-scoped queries)
- Index on `due_date` (required for date-based queries)
- Index on `priority` (required for priority-based queries)
- Index on `is_completed` (required for status-based queries)

### Database Rules
- No raw SQL operations (use ORM only)
- Migrations are required for schema changes
- Connection pooling must be implemented
- Async sessions must be used
- Soft deletes are forbidden (hard deletes only)

## Validation Rules

### Field Validation
- `title`: Required, 1-255 characters, no leading/trailing whitespace
- `description`: Optional, 0-1000 characters
- `priority`: Required enum value ("high", "medium", "low"), case-insensitive
- `tags`: Array of strings, max 10 items, each tag 1-50 alphanumeric/hyphen/underscore characters
- `due_date`: If provided, must be in the future, proper datetime format
- `recurrence_pattern`: If provided, must be one of ("daily", "weekly", "monthly")

### Business Logic Validation
- `is_recurring` and `recurrence_pattern` must be consistent
  - If `is_recurring` is true, `recurrence_pattern` must have a value
  - If `is_recurring` is false, `recurrence_pattern` must be null
- `due_date` must be in the future if provided
- `priority` must be one of the allowed values

## Database Constraints

### Primary Key Constraint
- `id` field must be unique and not null

### Foreign Key Constraint
- `user_id` must reference a valid user (implementation-dependent on user table)

### Check Constraints
- `title` length between 1 and 255 characters
- `description` length between 0 and 1000 characters
- `priority` in ("high", "medium", "low")
- `recurrence_pattern` in ("daily", "weekly", "monthly") when not null
- `due_date` in future when not null

### Default Values
- `priority`: "medium"
- `tags`: []
- `is_completed`: false
- `is_recurring`: false
- `recurrence_pattern`: null
- `created_at`: current timestamp
- `updated_at`: current timestamp

## Indexing Strategy

### Required Indexes (per constitution)
- Index on `user_id` - for user-scoped queries
- Index on `due_date` - for date-based queries and sorting
- Index on `priority` - for priority-based queries and sorting
- Index on `is_completed` - for status-based queries and filtering

### Potential Additional Indexes
- Composite index on (`user_id`, `is_completed`) - for user and status combined queries
- Composite index on (`user_id`, `due_date`) - for user and date combined queries
- Full-text index on (`title`, `description`) - for search functionality

## Performance Requirements

### Query Performance
- User-scoped queries must be efficient due to user_id index
- Date-based queries must be efficient due to due_date index
- Priority-based queries must be efficient due to priority index
- Status-based queries must be efficient due to is_completed index

### Storage Efficiency
- Use appropriate data types to minimize storage
- JSON for tags array should be efficiently stored
- UUIDs provide good distribution for indexing

## Security Requirements

### Data Isolation
- User data must be isolated by user_id
- No cross-user data access possible through database
- Proper indexing supports efficient user scoping

### Injection Prevention
- Use parameterized queries through ORM
- Validate all inputs before database operations
- Use proper escaping for all dynamic values

## Migration Strategy

### Initial Schema Creation
- Create Task table with all specified fields
- Add all required indexes
- Set up proper constraints and defaults
- Test schema creation on clean database

### Future Changes
- Use proper migration system for any schema changes
- Maintain backward compatibility where possible
- Test migrations on sample data
- Document all schema changes