# TaskCard Component Specification

## Overview
This specification defines the TaskCard component for the AI-ready full-stack todo app. The TaskCard displays an individual task with all its details in a card format, following the constitutional design system and UX requirements.

## Requirements
- Must follow the design system specified in the constitution
- Must be responsive and mobile-first
- Must display all task details clearly
- Must support task interaction (completion, editing)
- Must follow accessibility standards
- Must implement optimistic UI updates as per constitution

## Functional Requirements

### 1. Task Information Display
- Display task title prominently
- Show task description (with expand/collapse if long)
- Display priority level with visual indicators
- Show tags as TagChip components
- Display due date with appropriate visual indicators
- Show completion status with checkmark or similar indicator
- Display creation/modification timestamps

### 2. Visual Design
- Card layout with 16px border radius as per constitution
- Consistent spacing and padding
- Follow constitutional color palette for priority indicators
- Appropriate visual hierarchy for different elements
- Consistent typography using Inter font
- Subtle shadows for depth perception

### 3. Interactive Elements
- Completion toggle (checkbox or similar)
- Edit button/icon
- Delete button/icon
- Expand/collapse for long descriptions
- Smooth animations for interactions
- Visual feedback for user actions
- Support for keyboard navigation

### 4. Priority Visualization
- Visual indicators for different priority levels (high, medium, low)
- Use constitutional colors: High (#EF4444), Medium (#4F46E5), Low (#22C55E)
- Consistent styling for priority display
- Clear differentiation between priority levels
- Accessible color contrast

### 5. Tag Display
- Display tags as TagChip components
- Proper spacing between tags
- Responsive layout for multiple tags
- Clickable tags if needed for filtering
- Consistent styling with design system

### 6. Due Date Display
- Clear due date presentation
- Visual indicators for overdue, today, tomorrow, etc.
- Appropriate icons or symbols for due dates
- Time display if needed
- Relative date display (e.g., "Today", "Tomorrow")

### 7. Responsive Design
- Compact layout for mobile devices
- Expanded layout for desktop
- Proper touch targets for mobile interaction
- Adaptive spacing for different screen sizes
- Maintained readability across devices

### 8. State Management
- Visual indication of loading states
- Feedback for optimistic updates
- Error states if needed
- Hover and focus states for interactive elements
- Disabled states if needed

## Design System Compliance
- Border Radius: Cards (16px), Buttons (12px), Inputs (10px)
- Colors: Follow constitutional color palette
- Typography: Inter for content, JetBrains Mono for monospace
- Spacing: Consistent with Tailwind spacing scale
- Shadows and depth: Consistent with design system
- Responsive breakpoints: Mobile-first approach

## Performance Requirements
- Fast rendering of individual task cards
- Minimal re-renders when possible
- Efficient handling of interactive elements
- Smooth animations and transitions
- Optimistic UI updates as per constitution

## Accessibility Requirements
- Semantic HTML structure for task content
- Proper ARIA labels and roles for interactive elements
- Keyboard navigation support (tab order, space/enter for actions)
- Screen reader compatibility
- Focus management and indicators
- Color contrast compliance (WCAG AA minimum)
- Proper labeling for all interactive elements

## State Management
- Completion state (checked/unchecked)
- Loading state (during optimistic updates)
- Error state (if update fails)
- Hover state for interactive elements
- Focus state for keyboard navigation
- Expanded/collapsed state for long descriptions

## Integration Points
- Must work with Next.js App Router
- Must integrate with API client for updates
- Must work with TaskList component
- Must work with TagChip component
- Must work with PriorityBadge component
- Must handle optimistic updates properly

## Error Handling
- Graceful degradation when API is unavailable
- Proper error messages for update failures
- Fallback UI for different error scenarios
- Network error handling with revert functionality
- Invalid data handling from API

## UX Requirements (from Constitution)
- Mobile-first design approach
- Keyboard accessible navigation
- Optimistic UI updates
- Inline validation
- Smooth transitions and animations
- No full page reloads
- Proper feedback for user actions

## Component Composition
- Should accept task data as props
- Should emit events for user interactions
- Should work with other UI components
- Should support dynamic content updates
- Should handle different task states appropriately