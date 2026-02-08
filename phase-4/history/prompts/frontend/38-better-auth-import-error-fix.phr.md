# PHR: Better Auth Import Error Fix

## Date
2026-01-22

## Summary
Fixed TypeScript error in unused Better Auth client file where `createAuth` was incorrectly imported instead of `createAuthClient`. The error occurred because `createAuth` is not exported from the main "better-auth" package for client-side usage. The project uses a custom JWT authentication system, making this file unused but potentially problematic if imported.

## Root Cause
- Better Auth package exports `createAuthClient` for frontend usage from "better-auth/client", not `createAuth` from main package
- File `lib/auth/better-auth-client.ts` had incorrect import causing TypeScript compilation error
- While the file was currently unused in the codebase, it would cause build errors if ever imported
- Project currently uses custom JWT implementation instead of Better Auth

## Solution Implemented
1. **Fixed import statement**: Changed `import { createAuth } from "better-auth"` to `import { createAuthClient } from "better-auth/client"`
2. **Updated function call**: Changed `createAuth({...})` to `createAuthClient({...})`
3. **Adjusted configuration**: Removed server-side plugins from client configuration since plugins are typically server-side only
4. **Updated types**: Changed type export from custom type to standard Better Auth Session type

## Files Modified
- `frontend/lib/auth/better-auth-client.ts` - Fixed import and configuration
- `history/prompts/frontend/38-better-auth-import-error-fix.phr.md` - Documentation of the fix

## Technical Details
- Better Auth has different exports for client vs server usage
- Client-side uses `createAuthClient` from "better-auth/client"
- Server-side uses `createAuth` from "better-auth" (not used in this project)
- Client configuration should not include server-side plugins
- Project uses custom JWT auth system (not Better Auth) as indicated in AuthContext.tsx comment

## Impact
- ✅ Resolves TypeScript compilation error for Better Auth import
- ✅ Makes unused Better Auth client file syntactically correct
- ✅ Prevents future build errors if file is ever imported
- ✅ Maintains compatibility with existing custom JWT auth system
- ✅ Follows Better Auth client-side usage patterns
- ✅ No changes to currently working authentication functionality
- ✅ Enables potential future Better Auth integration if desired