---
id: 1
title: "AI-Ready Todo App Constitution Creation"
stage: constitution
date_iso: "2026-01-08"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "none"
branch: "main"
user: "Claude"
command: "Create constitution.md for AI-Ready Full-Stack Todo App"
labels: ["constitution", "setup", "todo-app"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - ".specify/memory/constitution.md"
tests_yaml: []
---

# AI-Ready Todo App Constitution Creation

## PROMPT_TEXT
You are a Staff+ level Full-Stack Architect, Principal Frontend Engineer, Senior Backend Architect,
and an expert in Spec-Driven Development (Spec-Kit Plus compatible).

Your task is to generate a SINGLE, COMPLETE, FINAL, NON-NEGOTIABLE `constitution.md`
for a Full-Stack Todo Web Application.

This document will act as:
- The ONLY source of truth
- The ROOT authority for frontend + backend
- A strict spec-driven contract
- A zero-assumption, zero-freedom document

You must NOT:
- Ask questions
- Leave TODOs
- Defer decisions
- Say “implementation dependent”
- Leave anything to developer or Claude judgment

====================================================
SECTION 1: PROJECT OVERVIEW
====================================================

Project Name: AI-Ready Full-Stack Todo App

Architecture:
- Frontend: Next.js 16+ (App Router)
- Backend: FastAPI (Python 3.11+)
- Database: Neon Serverless PostgreSQL
- ORM: SQLModel
- Auth: Better Auth (Frontend) + JWT Verification (Backend)
- API Style: REST (User-scoped, JWT-secured)

====================================================
SECTION 2: CORE FUNCTIONAL FEATURES (MANDATORY)
====================================================

1. Add Task
2. Delete Task
3. Update Task
4. View Task List
5. Mark Task as Complete
6. Priorities (High / Medium / Low)
7. Tags / Categories (Work / Home / Custom)
8. Search (keyword-based)
9. Filter (status / priority / date)
10. Sort (due date / priority / alphabetical)
11. Recurring Tasks (daily / weekly / monthly)
12. Due Dates & Time Reminders
13. Browser Notifications

====================================================
SECTION 3: AUTHENTICATION & SECURITY (NON-NEGOTIABLE)
====================================================

- Better Auth runs ONLY on frontend
- JWT plugin MUST be enabled
- JWT payload MUST include:
  - user_id
  - email
  - issued_at
  - expiry (maximum 7 days)

Frontend:
- JWT MUST be attached to every API request
- Header format:
  Authorization: Bearer <token>

Backend:
- MUST verify JWT using shared secret
- MUST reject missing/invalid token with 401
- MUST enforce task ownership on EVERY operation

Shared Secret:
- Environment variable: BETTER_AUTH_SECRET
- MUST be identical in frontend & backend

====================================================
SECTION 4: API CONTRACT (IMMUTABLE)
====================================================

GET    /api/{user_id}/tasks
POST   /api/{user_id}/tasks
GET    /api/{user_id}/tasks/{id}
PUT    /api/{user_id}/tasks/{id}
DELETE /api/{user_id}/tasks/{id}
PATCH  /api/{user_id}/tasks/{id}/complete

Rules:
- user_id in URL MUST match JWT user_id
- Backend MUST NOT trust frontend input
- ALL queries filtered by authenticated user_id

====================================================
SECTION 5: DATA OWNERSHIP RULES
====================================================

- Every task belongs to exactly ONE user
- Cross-user access is impossible
- No admin bypass
- No shared tasks

====================================================
SECTION 6: FRONTEND CONSTITUTION
====================================================

Tech:
- Next.js 16+ (App Router)
- TypeScript
- Tailwind CSS
- Better Auth (JWT enabled)

Design System (LOCKED):

Colors:
- Primary: #4F46E5
- Secondary: #22C55E
- Danger: #EF4444
- Warning: #F59E0B
- Background: #F9FAFB
- Surface: #FFFFFF
- Text Primary: #111827
- Text Secondary: #6B7280
- Border: #E5E7EB

Fonts:
- Inter (headings & body)
- JetBrains Mono (monospace)

Radius:
- Cards: 16px
- Buttons: 12px
- Inputs: 10px

Mandatory UI Components:
- AppShell
- Navbar (auth-aware)
- TaskList
- TaskCard
- AddTaskModal
- EditTaskModal
- PriorityBadge
- TagChip
- SearchBar
- FilterPanel
- SortDropdown
- DateTimePicker
- RecurringSelector
- EmptyState
- LoadingSkeleton
- ErrorBoundary
- Toast Notifications

UX Rules:
- Mobile-first
- Keyboard accessible
- Optimistic UI updates
- Skeleton loaders (NO spinners)
- Inline validation
- No full page reloads

State Management:
- Server Components → server data
- Client Components → UI interactions
- URL params → search / filter / sort
- Redux is FORBIDDEN

Performance:
- Code splitting REQUIRED
- Dynamic imports for modals
- Memoized task lists
- Debounced search (300ms)
- Pagination or infinite scroll

Forbidden:
- Inline styles
- Hardcoded colors
- UI decisions outside this file
- Auth logic outside Better Auth

====================================================
SECTION 7: BACKEND CONSTITUTION
====================================================

Tech:
- Python 3.11+
- FastAPI
- SQLModel
- Neon Serverless PostgreSQL
- Async-first architecture

Data Models:

Task:
- id (UUID, PK)
- user_id (UUID, indexed)
- title (required)
- description (optional)
- priority (high | medium | low)
- tags (array[string])
- due_date (datetime, nullable)
- is_completed (boolean)
- is_recurring (boolean)
- recurrence_pattern (daily | weekly | monthly | null)
- created_at
- updated_at

API Rules:
- JWT required for ALL endpoints
- user_id in path MUST match token
- 401 for auth errors
- 403 for ownership violations
- 404 for missing resources

Middleware:
- JWT verification
- Request timing
- Global error handler

Business Logic:
- Recurring tasks auto-reschedule on completion
- Soft deletes NOT allowed
- Completion is toggle-based
- Filtering & sorting server-side

Database Rules:
- Async sessions
- Connection pooling
- Indexes REQUIRED on:
  - user_id
  - due_date
  - priority
  - is_completed
- No raw SQL
- Migrations REQUIRED

Performance:
- Pagination mandatory
- Query limits enforced
- Max payload size enforced

Forbidden:
- Trusting frontend user_id
- Storing auth sessions
- Cross-user queries
- Silent failures

====================================================
SECTION 8: SPEC-DRIVEN DEVELOPMENT RULES
====================================================

- No feature without spec
- No UI without component definition
- No API without request/response schema
- No styling without tokens
- No undocumented decisions

====================================================
SECTION 9: QUALITY GATES
====================================================

- update phr after executing this prompt as you're already claude and specs kit plus expert and know where should be the location or phr and constitution.md

## RESPONSE_TEXT
Created the complete constitution.md file for the AI-Ready Full-Stack Todo App with all the specified sections and requirements. The constitution includes project overview, functional features, authentication & security, API contracts, data ownership rules, frontend and backend constitutions, spec-driven development rules, and quality gates. The file has been saved to .specify/memory/constitution.md and follows all the specified requirements without leaving anything to interpretation.

## OUTCOME
Successfully created the complete constitution.md file with all required sections and specifications for the AI-Ready Full-Stack Todo App.

## EVALUATION
The constitution file has been created with all nine sections as specified in the requirements. All technical details, including API contracts, data models, authentication requirements, and design system specifications, have been properly implemented. The file serves as the immutable source of truth for the project as required.