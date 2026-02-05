# Conversation Model Specification

## Overview
This specification defines the Conversation and Message database models for the AI-ready full-stack todo app. These models store persistent conversation history for the AI-powered chat interface, following constitutional requirements for data ownership and security.

## Requirements
- Conversation data must be securely tied to authenticated user
- All conversations must be isolated by user ownership
- Models must support efficient querying for conversation history
- Models must follow constitutional database rules
- Proper indexing must be implemented for performance

## Data Model Requirements

### Conversation Model
- id (UUID, Primary Key, indexed)
- user_id (UUID, indexed, foreign key to User)
- created_at (datetime, indexed)
- updated_at (datetime, indexed)

### Message Model
- id (UUID, Primary Key, indexed)
- user_id (UUID, indexed, foreign key to User)
- conversation_id (UUID, indexed, foreign key to Conversation)
- role (string: "user" | "assistant", indexed)
- content (text, nullable)
- created_at (datetime, indexed)

## Database Rules Compliance
- Async sessions must be used for all operations
- Connection pooling must be utilized
- Indexes REQUIRED on all specified fields
- No raw SQL - all operations through SQLModel
- Migrations REQUIRED for schema changes
- All operations must be user-scoped

## Security Requirements
- User isolation at database level
- No cross-user access to conversations
- JWT validation required for all access
- user_id in operations must match JWT user_id
- No admin bypass for conversation access
- Proper foreign key relationships enforced

## Performance Requirements
- Proper indexing for efficient queries
- Foreign key constraints for data integrity
- Async operations for concurrency
- Connection pooling for efficiency
- Pagination support for large histories
- Query optimization for conversation loading

## Validation Rules
- UUID format validation for all ID fields
- Role field must be one of: "user", "assistant"
- Content field length validation (max 10000 characters)
- Required fields must be validated
- Foreign key relationships must be enforced
- Timestamps must be properly formatted

## Relationships
- Conversation has many Messages (one-to-many)
- Message belongs to Conversation (many-to-one)
- Conversation belongs to User (many-to-one)
- Message belongs to User (many-to-one)
- Cascade delete for conversation (deleting conversation deletes messages)

## Indexing Strategy
- Conversation.id: Primary key index
- Conversation.user_id: B-tree index for user-based queries
- Conversation.created_at: B-tree index for chronological queries
- Conversation.updated_at: B-tree index for freshness queries
- Message.id: Primary key index
- Message.user_id: B-tree index for user-based queries
- Message.conversation_id: B-tree index for conversation-based queries
- Message.role: B-tree index for role-based queries
- Message.created_at: B-tree index for chronological queries

## Query Patterns
- Retrieve all conversations for a user (filtered by user_id)
- Retrieve conversation by ID (filtered by id and user_id for ownership)
- Retrieve messages for a conversation (filtered by conversation_id and user_id)
- Retrieve recent conversations (ordered by updated_at)
- Retrieve messages by role (filtered by role field)

## API Integration Points
- Chat API endpoint will access these models for conversation persistence
- Agent will load conversation history from these models
- Message persistence will occur through these models
- Conversation creation/deletion will use these models

## Error Handling
- Database constraint violations must be handled gracefully
- Invalid data must trigger appropriate validation errors
- Ownership violations must return 403 Forbidden
- Missing conversations must return 404 Not Found
- Database connectivity issues must return 500 Server Error

## Migration Requirements
- Initial migration must create both Conversation and Message tables
- Proper foreign key constraints must be established
- Indexes must be created as specified
- Downgrade migration must safely remove tables
- Migration must be tested in development environment

## Audit Trail
- All conversation operations must be logged
- Access patterns must be monitored for security
- Performance metrics must be collected
- Error logs must be captured for debugging