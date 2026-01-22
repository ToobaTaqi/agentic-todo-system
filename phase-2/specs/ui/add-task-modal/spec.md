# AddTaskModal Component Specification

## Overview
This specification defines the AddTaskModal component for the AI-ready full-stack todo app. The AddTaskModal provides a form interface for creating new tasks, following the constitutional design system and UX requirements.

## Requirements
- Must follow the design system specified in the constitution
- Must be responsive and mobile-first
- Must include all task creation fields
- Must provide proper validation and error handling
- Must follow accessibility standards
- Must implement inline validation as per constitution

## Functional Requirements

### 1. Form Fields
- Title input field (required, with validation)
- Description textarea (optional)
- Priority selection dropdown (high, medium, low)
- Tags input with multi-selection capability
- Due date picker with time selection
- Recurring task toggle with pattern selection
- Submit button
- Cancel/Close button

### 2. Validation
- Title field required validation (1-255 characters)
- Description length validation (0-1000 characters)
- Priority selection validation
- Tags validation (max 10 tags, each 1-50 characters)
- Due date validation (must be in future if provided)
- Recurring task pattern validation when enabled
- Inline validation messages for each field
- Form-level validation summary if needed

### 3. Visual Design
- Modal overlay with backdrop
- Modal content with 16px border radius as per constitution
- Consistent spacing and padding
- Follow constitutional color palette
- Appropriate visual hierarchy for form elements
- Consistent typography using Inter font
- Proper focus and hover states for all interactive elements

### 4. Interactive Elements
- Form submission handling
- Cancel/Close functionality
- Dynamic field behavior (recurring pattern when toggle is on)
- Real-time validation feedback
- Loading state during submission
- Success feedback after creation
- Smooth animations for modal open/close

### 5. Priority Selection
- Dropdown or radio buttons for priority selection
- Visual indicators using constitutional colors
- Default selection to "medium" priority
- Clear visual feedback for selected option

### 6. Tags Input
- Multi-tag input with add/remove capability
- Tag suggestions based on existing tags
- Validation for tag format and count
- Visual display of selected tags
- Ability to remove tags before submission

### 7. Due Date Selection
- Date picker component
- Time selection capability
- Calendar integration for date selection
- Validation to ensure future dates only
- Clear display of selected date/time

### 8. Recurring Task Options
- Toggle switch to enable recurring tasks
- Pattern selection when enabled (daily, weekly, monthly)
- Appropriate form layout when recurring is enabled
- Clear explanation of recurring task behavior

### 9. Responsive Design
- Full-screen modal on mobile devices
- Appropriately sized modal on desktop
- Proper touch targets for mobile interaction
- Adaptive layout for different screen sizes
- Maintained usability across devices

### 10. State Management
- Form data state management
- Validation state for each field
- Submission loading state
- Success/error state handling
- Modal open/close state management

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

## Accessibility Requirements
- Proper modal accessibility patterns (focus trapping)
- Keyboard navigation support (tab order, escape to close)
- Screen reader compatibility for form elements
- Proper ARIA labels and roles for all elements
- Focus management when modal opens/closes
- Color contrast compliance (WCAG AA minimum)
- Proper labeling for all form fields

## State Management
- Form field values state
- Validation errors state
- Submission loading state
- Modal visibility state
- Success/error feedback state

## Integration Points
- Must work with Next.js App Router
- Must integrate with API client for task creation
- Must work with DateTimePicker component
- Must work with TagChip component for tag display
- Must work with PriorityBadge component
- Must handle URL parameter updates if needed

## Error Handling
- Form validation error display
- API error handling for creation failures
- Network error handling with appropriate messages
- Fallback UI for different error scenarios
- Graceful handling of invalid inputs

## UX Requirements (from Constitution)
- Mobile-first design approach
- Keyboard accessible navigation
- Inline validation (no separate validation steps)
- Smooth transitions and animations
- No full page reloads
- Proper feedback for user actions
- Optimistic UI updates (if applicable)

## Component Composition
- Should accept callback functions for form submission and cancellation
- Should emit events for successful task creation
- Should work with other UI components
- Should support dynamic content updates
- Should handle different form states appropriately