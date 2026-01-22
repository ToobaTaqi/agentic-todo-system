# PHR: PostgreSQL Driver Missing Dependency Fix

## Date
2026-01-22

## Summary
Fixed ModuleNotFoundError for psycopg2 module during Railway deployment. The error occurred because the application uses both async and sync database connections, but only had async drivers installed. Added psycopg2-binary dependency to requirements.txt to provide the PostgreSQL adapter needed for synchronous database operations during startup.

## Root Cause
- Application creates both async (asyncpg) and sync (psycopg2) database connections
- Startup event in main.py uses SQLAlchemy's create_engine() which requires psycopg2 for PostgreSQL sync operations
- requirements.txt only included asyncpg for async operations but missing psycopg2-binary for sync operations
- Railway deployment failed with "ModuleNotFoundError: No module named 'psycopg2'"
- Sync engine created on line 43 of main.py requires psycopg2 driver: `sync_engine = create_engine(sync_database_url)`

## Solution Implemented
1. **Added missing dependency**: Added `psycopg2-binary==2.9.10` to requirements.txt
2. **Maintained compatibility**: Kept existing asyncpg for async operations
3. **Ensured complete PostgreSQL support**: Both async and sync operations now supported
4. **Version stability**: Used specific version for reproducible builds

## Files Modified
- `backend/requirements.txt` - Added psycopg2-binary dependency
- `history/prompts/backend/40-postgres-driver-missing-dependency-fix.phr.md` - Documentation of the fix

## Technical Details
- Application uses hybrid approach with both async (FastAPI, asyncpg) and sync (startup table creation) operations
- Startup event creates sync engine using SQLAlchemy's create_engine() which requires psycopg2 for PostgreSQL
- asyncpg handles async operations during runtime
- psycopg2-binary provides the sync PostgreSQL adapter needed during startup
- Both drivers can coexist in the same application
- PostgreSQL URL conversion happens in startup_event: `sync_database_url = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")`

## Impact
- ✅ Resolves ModuleNotFoundError during Railway deployment
- ✅ Enables successful application startup on Railway
- ✅ Maintains both async and sync database functionality
- ✅ Preserves existing async operations with asyncpg
- ✅ Enables sync operations needed for table creation during startup
- ✅ Ensures compatibility with PostgreSQL database
- ✅ Enables successful deployment to Railway
- ✅ Maintains application functionality and performance