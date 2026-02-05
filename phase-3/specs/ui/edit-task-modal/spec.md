# EditTaskModal Component Specification

## Overview
This specification defines the EditTaskModal component for the AI-ready full-stack todo app. The EditTaskModal provides a form interface for updating existing tasks, following the constitutional design system and UX requirements.

## Requirements
- Must follow the design system specified in the constitution
- Must be responsive and mobile-first
- Must include all task editing fields
- Must pre-populate with existing task data
- Must provide proper validation and error handling
- Must follow accessibility standards
- Must implement inline validation as per constitution

## Functional Requirements

### 1. Form Fields
- Title input field (required, with validation, pre-filled)
- Description textarea (optional, pre-filled)
- Priority selection dropdown (high, medium, low, pre-selected)
- Tags input with multi-selection capability (pre-populated)
- Due date picker with time selection (pre-filled)
- Recurring task toggle with pattern selection (pre-filled)
- Submit button (Update Task)
- Cancel/Close button
- Delete button (with confirmation)

### 2. Data Pre-population
- Automatically populate form fields with existing task data
- Set initial values for title, description, priority, tags, due date
- Set initial state for recurring task toggle and pattern
- Handle null/undefined values appropriately
- Maintain data integrity during pre-population

### 3. Validation
- Title field required validation (1-255 characters)
- Description length validation (0-1000 characters)
- Priority selection validation
- Tags validation (max 10 tags, each 1-50 characters)
- Due date validation (must be in future if provided)
- Recurring task pattern validation when enabled
- Inline validation messages for each field
- Form-level validation summary if needed

### 4. Visual Design
- Modal overlay with backdrop
- Modal content with 16px border radius as per constitution
- Consistent spacing and padding
- Follow constitutional color palette
- Appropriate visual hierarchy for form elements
- Consistent typography using Inter font
- Proper focus and hover states for all interactive elements

### 5. Interactive Elements
- Form submission handling for updates
- Cancel/Close functionality
- Delete task functionality with confirmation
- Dynamic field behavior (recurring pattern when toggle is on)
- Real-time validation feedback
- Loading state during update
- Success feedback after update
- Smooth animations for modal open/close

### 6. Priority Selection
- Dropdown or radio buttons for priority selection
- Visual indicators using constitutional colors
- Pre-selected value from existing task
- Clear visual feedback for selected option
- Options: High, Medium, Low

### 7. Tags Input
- Multi-tag input with add/remove capability
- Pre-populated with existing tags
- Tag suggestions based on existing tags
- Validation for tag format and count
- Visual display of selected tags
- Ability to add/remove tags during editing

### 8. Due Date Selection
- Date picker component
- Time selection capability
- Calendar integration for date selection
- Pre-populated with existing due date
- Validation to ensure future dates only
- Clear display of selected date/time

### 9. Recurring Task Options
- Toggle switch to enable recurring tasks
- Pre-set based on existing task's recurring status
- Pattern selection when enabled (daily, weekly, monthly)
- Pre-selected pattern from existing task
- Appropriate form layout when recurring is enabled
- Clear explanation of recurring task behavior

### 10. Delete Functionality
- Prominently placed delete button
- Confirmation dialog to prevent accidental deletion
- Clear warning about permanent deletion
- Appropriate styling for danger action
- Proper error handling for deletion

### 11. Responsive Design
- Full-screen modal on mobile devices
- Appropriately sized modal on desktop
- Proper touch targets for mobile interaction
- Adaptive layout for different screen sizes
- Maintained usability across devices

### 12. State Management
- Form data state management with initial values
- Validation state for each field
- Submission loading state
- Success/error state handling
- Modal open/close state management
- Delete confirmation state

## Design System Compliance
- Border Radius: Cards (16px), Buttons (12px), Inputs (10px)
- Colors: Follow constitutional color palette
- Typography: Inter for content, JetBrains Mono for monospace
- Spacing: Consistent with Tailwind spacing scale
- Shadows and depth: Consistent with design system
- Responsive breakpoints: Mobile-first approach

## Performance Requirements
- Fast modal rendering and display
- Minimal re-renders during form interaction
- Efficient validation without performance impact
- Smooth animations and transitions
- Quick response to user input
- Efficient data pre-population

## Accessibility Requirements
- Proper modal accessibility patterns (focus trapping)
- Keyboard navigation support (tab order, escape to close)
- Screen reader compatibility for form elements
- Proper ARIA labels and roles for all elements
- Focus management when modal opens/closes
- Color contrast compliance (WCAG AA minimum)
- Proper labeling for all form fields
- Clear identification of delete action as dangerous

## State Management
- Form field values state (with initial values from task)
- Validation errors state
- Submission loading state
- Modal visibility state
- Delete confirmation state
- Success/error feedback state

## Integration Points
- Must work with Next.js App Router
- Must integrate with API client for task updates
- Must work with DateTimePicker component
- Must work with TagChip component for tag display
- Must work with PriorityBadge component
- Must handle URL parameter updates if needed

## Error Handling
- Form validation error display
- API error handling for update failures
- Network error handling with appropriate messages
- Fallback UI for different error scenarios
- Graceful handling of invalid inputs
- Proper error handling for deletion operations

## UX Requirements (from Constitution)
- Mobile-first design approach
- Keyboard accessible navigation
- Inline validation (no separate validation steps)
- Smooth transitions and animations
- No full page reloads
- Proper feedback for user actions
- Optimistic UI updates (if applicable)

## Component Composition
- Should accept task data and callback functions as props
- Should emit events for task updates and deletions
- Should work with other UI components
- Should support dynamic content updates
- Should handle different form states appropriately