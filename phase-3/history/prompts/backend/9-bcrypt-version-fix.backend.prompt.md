---
id: 9
title: "Bcrypt Version Compatibility Fix"
stage: backend
date_iso: "2026-01-14"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "authentication"
branch: "main"
user: "Claude"
command: "Fix bcrypt version compatibility issue with passlib"
labels: ["bug-fix", "auth", "password", "bcrypt", "todo-app"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "backend/models/models.py"
tests_yaml: []
---

# Bcrypt Version Compatibility Fix

## PROMPT_TEXT
Fix the bcrypt version compatibility issue: `(trapped) error reading bcrypt version - AttributeError: module 'bcrypt' has no attribute '__about__'`. This error occurs due to incompatibility between passlib and bcrypt versions. Need to update the password hashing implementation in the relevant files.

## RESOLUTION_SUMMARY

### Issue Identified:
The error `AttributeError: module 'bcrypt' has no attribute '__about__'` occurs when passlib tries to read the version of the bcrypt module. This is a known compatibility issue between certain versions of passlib and bcrypt.

### Root Cause:
The application was using passlib's CryptContext with bcrypt scheme, which tries to access `bcrypt.__about__.__version__` that doesn't exist in newer versions of bcrypt.

### Solution Implemented:
Updated the password hashing implementation in `backend/models/models.py` to use bcrypt directly instead of through passlib's CryptContext:

1. **Removed passlib dependency** for password hashing in the User model
2. **Implemented direct bcrypt usage** with proper encoding/decoding
3. **Updated hash_password method** to use `bcrypt.hashpw()` with proper byte encoding
4. **Updated verify_password method** to use `bcrypt.checkpw()` with proper byte encoding
5. **Added proper salt generation** with `bcrypt.gensalt()`

### Key Changes Made:

**In `backend/models/models.py`:**
- Replaced `from passlib.context import CryptContext` with `import bcrypt`
- Removed the `pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")` initialization
- Updated `hash_password()` method to use direct bcrypt operations with proper byte encoding
- Updated `verify_password()` method to use direct bcrypt verification with proper byte encoding

## RESPONSE_TEXT
Successfully resolved the bcrypt version compatibility issue by updating the password hashing implementation to use bcrypt directly instead of through passlib's CryptContext. The User model now properly handles password hashing and verification using bcrypt with correct byte encoding and decoding. The application starts without the version attribute error and password functionality works as expected.

## OUTCOME
The bcrypt version compatibility error has been completely resolved. Password hashing and verification now work properly using direct bcrypt operations. The application can start and handle authentication requests without encountering the AttributeError.

## EVALUATION
The fix successfully addresses the root cause of the compatibility issue by bypassing the problematic passlib-bcrypt interaction. The direct bcrypt implementation is more reliable and avoids version conflicts. Password security is maintained with proper salt generation and secure hashing. The solution is stable and production-ready.