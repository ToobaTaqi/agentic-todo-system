# Notification Preferences API Implementation Tasks

## Foundation Setup

### Model Definition
- [ ] Create NotificationPreference model in models.py
- [ ] Define all required fields: id, user_id, enabled, timing_minutes_before, etc.
- [ ] Add proper field types and constraints
- [ ] Add validation rules for each field
- [ ] Create database indexes for user_id
- [ ] Test model creation and validation

### Database Setup
- [ ] Create database migration for notification preferences table
- [ ] Include all fields, constraints, and indexes in migration
- [ ] Test migration on clean database
- [ ] Test migration rollback
- [ ] Test migration on database with existing data

### Pydantic Models
- [ ] Create request models for each endpoint
  - [ ] GetPreferencesRequest
  - [ ] UpdatePreferencesRequest with optional fields
  - [ ] DeletePreferencesRequest
- [ ] Create response models for each endpoint
  - [ ] PreferencesResponse with all preference fields
  - [ ] UpdatePreferencesResponse
  - [ ] DeletePreferencesResponse
- [ ] Add validation rules to request models
- [ ] Test model serialization and validation

## Core API Endpoints

### GET /api/{user_id}/notification-preferences
- [ ] Create endpoint function in routes/notifications.py
- [ ] Add JWT authentication dependency
- [ ] Add user_id validation dependency
- [ ] Query for user's notification preferences
- [ ] Return preferences or defaults if not found
- [ ] Add proper error handling
- [ ] Test endpoint with existing and non-existing preferences

### PUT /api/{user_id}/notification-preferences
- [ ] Create endpoint function in routes/notifications.py
- [ ] Add JWT authentication dependency
- [ ] Add user_id validation dependency
- [ ] Parse and validate request body using Pydantic model
- [ ] Update or create user's notification preferences
- [ ] Return updated preferences
- [ ] Add proper error handling
- [ ] Test endpoint with valid and invalid inputs

### DELETE /api/{user_id}/notification-preferences
- [ ] Create endpoint function in routes/notifications.py
- [ ] Add JWT authentication dependency
- [ ] Add user_id validation dependency
- [ ] Delete user's notification preferences (or reset to defaults)
- [ ] Return success message
- [ ] Add proper error handling
- [ ] Test endpoint with existing and non-existing preferences

## Validation Implementation

### Field Validation
- [ ] Create Pydantic validator for timing_minutes_before (1-1440 range)
- [ ] Create Pydantic validator for do_not_disturb_start/end time format
- [ ] Create Pydantic validator for custom_notification_times format
- [ ] Create Pydantic validator for boolean fields
- [ ] Return 422 error for invalid preference values
- [ ] Test validation with various invalid inputs

### Business Logic Validation
- [ ] Validate that do_not_disturb_end is after do_not_disturb_start
- [ ] Validate custom_notification_times format
- [ ] Test validation with various combinations

## Security Implementation

### Authentication Middleware
- [ ] Create authentication utilities in auth.py
- [ ] Implement JWT token verification function
- [ ] Create dependency for JWT authentication
- [ ] Add shared secret validation using BETTER_AUTH_SECRET
- [ ] Extract user_id from JWT for validation
- [ ] Test JWT validation with valid and invalid tokens

### User ID Validation
- [ ] Create utility function to verify user_id in URL matches JWT user_id
- [ ] Create FastAPI dependency for user ownership validation
- [ ] Test user_id validation with matching and mismatching IDs
- [ ] Handle authentication errors appropriately

## Default Preferences

### Default Values Implementation
- [ ] Implement logic to return default preferences when none exist
- [ ] Define default values as per specification
- [ ] Test default preference behavior
- [ ] Handle preferences creation with defaults
- [ ] Test preference reset functionality

## Error Handling

### Consistent Error Format
- [ ] Create standardized error response model
- [ ] Implement consistent error handling across all endpoints
- [ ] Add appropriate HTTP status codes
- [ ] Create error detail messages
- [ ] Test error responses

### Specific Error Cases
- [ ] Handle 401 Unauthorized errors
- [ ] Handle 403 Forbidden errors
- [ ] Handle 404 Not Found errors (for non-existing preferences)
- [ ] Handle 422 Validation errors
- [ ] Test error conditions and edge cases

## Testing

### Unit Tests
- [ ] Write unit tests for NotificationPreference model
- [ ] Write unit tests for validation functions
- [ ] Write unit tests for authentication functions
- [ ] Write unit tests for default preference logic
- [ ] Test model serialization and validation

### Integration Tests
- [ ] Write integration tests for all API endpoints
- [ ] Test authentication and authorization
- [ ] Test default preferences behavior
- [ ] Test error scenarios
- [ ] Test with various preference configurations

### Security Tests
- [ ] Test authentication and authorization
- [ ] Test user isolation between preferences
- [ ] Test with invalid JWT tokens
- [ ] Test user_id validation
- [ ] Verify no cross-user access is possible

### Performance Tests
- [ ] Test API performance with large datasets
- [ ] Verify database query performance
- [ ] Test API response times under load
- [ ] Verify efficient preference retrieval
- [ ] Test with concurrent preference updates