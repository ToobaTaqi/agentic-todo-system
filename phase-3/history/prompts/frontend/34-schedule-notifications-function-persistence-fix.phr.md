# PHR: Schedule Notifications Function Persistence Fix

## Date
2026-01-22

## Summary
Fixed the "scheduleNotificationsForTasks is not a function" error and underlying functionality issues by correcting state management in the useNotification hook. The function was available but not working properly due to improper persistence of scheduled notifications.

## Root Cause
- scheduledNotifications was initialized as a regular variable in the useNotification hook
- On every render, a new empty Map was created, losing previously scheduled notifications
- The function existed but couldn't maintain state between calls
- This broke the notification scheduling functionality while appearing as if the function was missing

## Solution Implemented
1. **Changed state management**: Updated scheduledNotifications from a regular variable to useRef to maintain persistence
2. **Updated imports**: Added useRef to the React imports
3. **Maintained functionality**: Preserved all existing notification logic while fixing the persistence issue

## Files Modified
- `frontend/lib/hooks/useNotification.ts` - Fixed state management with useRef
- `history/prompts/frontend/34-schedule-notifications-function-persistence-fix.phr.md` - Documentation of the fix

## Technical Details
- Changed: `const [scheduledNotifications, setScheduledNotifications] = new Map<string, number>();`
- To: `const scheduledNotifications = useRef<Map<string, number>>(new Map()).current;`
- This ensures the Map persists across hook re-renders
- Function now properly maintains scheduled notification references
- All existing functionality preserved

## Impact
- ✅ Fixes the scheduleNotificationsForTasks functionality
- ✅ Maintains proper state management for scheduled notifications
- ✅ Enables browser notifications for upcoming task deadlines
- ✅ Preserves all existing notification features
- ✅ Follows React hooks best practices for state management
- ✅ No breaking changes to existing code