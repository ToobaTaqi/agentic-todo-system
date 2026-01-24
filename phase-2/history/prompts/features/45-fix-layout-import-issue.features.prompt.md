# Fix Layout Import Issue

## Issue Identified
The auth layout had an import error where `./globals.css` could not be resolved because the path was incorrect.

## Root Cause
The `globals.css` file is located in the root of the app directory (`app/globals.css`), but the auth layout was trying to import it as `./globals.css` instead of `../../globals.css` (going up two directories from `app/(auth)/layout.tsx`).

Additionally, the layout was marked as a 'use client' directive when it should be a server component since it's a layout.

## Solution Implemented

### 1. Fixed Import Path
- Changed import from `./globals.css` to `../../globals.css` to correctly reference the root globals.css file

### 2. Removed Client Directive
- Removed `'use client'` directive since layouts should be server components
- This is the proper Next.js 14+ App Router pattern

## Files Modified
- `frontend/app/(auth)/layout.tsx` - Fixed import path and removed client directive

## Expected Outcome
- The auth layout will properly import the global styles
- No more module resolution errors
- Proper server component behavior for the layout

## Testing Steps
1. Verify that the verification page loads without import errors
2. Check that global styles are applied to the verification page
3. Ensure other pages remain unaffected