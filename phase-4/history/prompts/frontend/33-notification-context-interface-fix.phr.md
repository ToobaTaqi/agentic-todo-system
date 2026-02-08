# PHR: Notification Context Interface and Type Fixes

## Date
2026-01-22

## Summary
Fixed TypeScript and runtime errors in the notification system by updating the NotificationContextType interface to include the missing scheduleNotificationsForTasks function. Also addressed type compatibility issues with the sort functionality in the dashboard.

## Root Causes
1. **Missing function in interface**: The NotificationContextType interface in NotificationProvider.tsx did not include scheduleNotificationsForTasks function
2. **Runtime error**: The dashboard was trying to call scheduleNotificationsForTasks but it wasn't available in the context
3. **Type compatibility**: Sort key type mismatches between SortDropdown component and dashboard state

## Solutions Implemented

### 1. Fixed Notification Context Interface
- Updated NotificationContextType interface to include scheduleNotificationsForTasks function signature
- Added proper type definition: `(tasks: Array<{ id: string; title: string; due_date?: string | null }>) => Map<string, number>`
- Ensured the function is properly passed from the useNotification hook to the provider value

### 2. Updated Notification Provider
- Added scheduleNotificationsForTasks to the destructuring from useNotification hook
- Included scheduleNotificationsForTasks in the provider value object
- Maintained all existing functionality while adding the missing function

### 3. Verified Sort Type Compatibility
- Confirmed that SortKey type ('due_date' | 'priority' | 'title' | 'created_at') is compatible with SortDropdown values
- The SortDropdown component provides exactly these string values, ensuring type safety

## Files Modified
- `frontend/components/Notifications/NotificationProvider.tsx` - Updated interface and provider implementation

## Technical Details
- The useNotification hook already exported scheduleNotificationsForTasks function
- The NotificationProvider was just not exposing it in the context interface/value
- Fixed both TypeScript compilation errors and runtime errors
- Maintained backward compatibility with existing code

## Impact
- ✅ Resolves "scheduleNotificationsForTasks is not a function" runtime error
- ✅ Fixes TypeScript error about property not existing on type
- ✅ Maintains all existing notification functionality
- ✅ Preserves proper type safety
- ✅ Enables browser notifications for upcoming task deadlines as designed
- ✅ No breaking changes to existing functionality