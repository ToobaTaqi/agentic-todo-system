# PHR: ESLint Peer Dependency Conflict Fix

## Date
2026-01-22

## Summary
Resolved npm peer dependency conflict between ESLint and eslint-config-next during Vercel deployment. The error occurred because eslint-config-next@16.1.1 requires ESLint version >=9.0.0, but the project had ESLint at version ^8.57.1.

## Root Cause
- `eslint-config-next@16.0.0` requires ESLint ">=9.0.0" as peer dependency
- Project's package.json had ESLint at "^8.57.1" (older major version)
- Vercel's npm installation failed due to incompatible peer dependency requirements
- Additional issues: duplicate @types/node and unrelated baseline-browser-mapping dependency

## Solution Implemented
1. **Updated ESLint version**: Changed from "^8.57.1" to "^9.0.0" in devDependencies
2. **Cleaned dependencies**: Removed duplicate @types/node from dependencies (kept only in devDependencies)
3. **Removed unnecessary dependency**: Removed baseline-browser-mapping package that was not needed
4. **Maintained compatibility**: Ensured all versions work with Next.js 16.0.1

## Files Modified
- `frontend/package.json` - Updated ESLint version and cleaned dependencies

## Technical Details
- ESLint v9.x introduces breaking changes from v8.x but is required by newer Next.js configurations
- Peer dependencies ensure compatible versions between ESLint and its configuration packages
- Moved @types/node to proper location in devDependencies only
- Removed potentially problematic baseline-browser-mapping package

## Impact
- ✅ Resolves npm installation error on Vercel deployment
- ✅ Satisfies eslint-config-next peer dependency requirements
- ✅ Maintains proper dependency organization
- ✅ Removes unnecessary dependencies
- ✅ Enables successful build and deployment on Vercel
- ✅ Maintains linting functionality for the codebase