# AI-Ready Full-Stack Todo App Constitution

## PROJECT OVERVIEW

**Project Name**: AI-Ready Full-Stack Todo App

**Architecture**:
- Frontend: Next.js 16+ (App Router)
- Backend: FastAPI (Python 3.11+)
- Database: Neon Serverless PostgreSQL
- ORM: SQLModel
- Auth: Better Auth (Frontend) + JWT Verification (Backend)
- API Style: REST (User-scoped, JWT-secured)

## CORE FUNCTIONAL FEATURES (MANDATORY)

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

## AUTHENTICATION & SECURITY (NON-NEGOTIABLE)

**Better Auth Configuration**:
- Better Auth runs ONLY on frontend
- JWT plugin MUST be enabled
- JWT payload MUST include:
  - user_id
  - email
  - issued_at
  - expiry (maximum 7 days)

**Frontend Authentication**:
- JWT MUST be attached to every API request
- Header format: `Authorization: Bearer <token>`

**Backend Authentication**:
- MUST verify JWT using shared secret
- MUST reject missing/invalid token with 401
- MUST enforce task ownership on EVERY operation

**Shared Secret**:
- Environment variable: BETTER_AUTH_SECRET
- MUST be identical in frontend & backend

## API CONTRACT (IMMUTABLE)

**Endpoints**:
- GET    `/api/{user_id}/tasks`
- POST   `/api/{user_id}/tasks`
- GET    `/api/{user_id}/tasks/{id}`
- PUT    `/api/{user_id}/tasks/{id}`
- DELETE `/api/{user_id}/tasks/{id}`
- PATCH  `/api/{user_id}/tasks/{id}/complete`

**Rules**:
- user_id in URL MUST match JWT user_id
- Backend MUST NOT trust frontend input
- ALL queries filtered by authenticated user_id

## DATA OWNERSHIP RULES

- Every task belongs to exactly ONE user
- Cross-user access is impossible
- No admin bypass
- No shared tasks

## FRONTEND CONSTITUTION

**Technology Stack**:
- Next.js 16+ (App Router)
- TypeScript
- Tailwind CSS
- Better Auth (JWT enabled)

**Design System (LOCKED)**:

**Colors**:
- Primary: #4F46E5
- Secondary: #22C55E
- Danger: #EF4444
- Warning: #F59E0B
- Background: #F9FAFB
- Surface: #FFFFFF
- Text Primary: #111827
- Text Secondary: #6B7280
- Border: #E5E7EB

**Typography**:
- Inter (headings & body)
- JetBrains Mono (monospace)

**Border Radius**:
- Cards: 16px
- Buttons: 12px
- Inputs: 10px

**Mandatory UI Components**:
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

**UX Rules**:
- Mobile-first
- Keyboard accessible
- Optimistic UI updates
- Skeleton loaders (NO spinners)
- Inline validation
- No full page reloads

**State Management**:
- Server Components → server data
- Client Components → UI interactions
- URL params → search / filter / sort
- Redux is FORBIDDEN

**Performance Requirements**:
- Code splitting REQUIRED
- Dynamic imports for modals
- Memoized task lists
- Debounced search (300ms)
- Pagination or infinite scroll

**Prohibited Practices**:
- Inline styles
- Hardcoded colors
- UI decisions outside this file
- Auth logic outside Better Auth

## BACKEND CONSTITUTION

**Technology Stack**:
- Python 3.11+
- FastAPI
- SQLModel
- Neon Serverless PostgreSQL
- Async-first architecture

**Data Models**:

**Task Model**:
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

**API Rules**:
- JWT required for ALL endpoints
- user_id in path MUST match token
- 401 for auth errors
- 403 for ownership violations
- 404 for missing resources

**Required Middleware**:
- JWT verification
- Request timing
- Global error handler

**Business Logic Requirements**:
- Recurring tasks auto-reschedule on completion
- Soft deletes NOT allowed
- Completion is toggle-based
- Filtering & sorting server-side

**Database Rules**:
- Async sessions
- Connection pooling
- Indexes REQUIRED on:
  - user_id
  - due_date
  - priority
  - is_completed
- No raw SQL
- Migrations REQUIRED

**Performance Requirements**:
- Pagination mandatory
- Query limits enforced
- Max payload size enforced

**Prohibited Practices**:
- Trusting frontend user_id
- Storing auth sessions
- Cross-user queries
- Silent failures

## SPEC-DRIVEN DEVELOPMENT RULES

- No feature without spec
- No UI without component definition
- No API without request/response schema
- No styling without tokens
- No undocumented decisions

## QUALITY GATES

- All code must pass linting and type checking
- All APIs must be documented with OpenAPI
- All database migrations must be tested
- All auth flows must be verified end-to-end
- All UI components must be responsive
- All performance benchmarks must be met
- All security requirements must be validated

## IMPLEMENTATION CONTRACT

This constitution is the immutable source of truth. All development activities must strictly adhere to these specifications. No deviations are permitted without updating this document first.

## VERSION INFORMATION

**Version**: 1.0.0 | **Ratified**: 2026-01-08 | **Last Amended**: 2026-01-08
