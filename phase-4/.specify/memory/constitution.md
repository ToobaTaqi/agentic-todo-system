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
- AI Integration: OpenAI Agents SDK with MCP Protocol
- Containerization: Docker-based containerization
- Orchestration: Kubernetes (Minikube) for deployment
- Packaging: Helm charts for application packaging
- AI DevOps Tools: kubectl-ai, kagent for AI-assisted DevOps operations

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

## AI CONVERSATIONAL INTERFACE EXTENSIONS

**Conversational AI Architecture**:
- Natural language chatbot UI using OpenAI ChatKit
- Stateful conversation system with persistent history
- OpenAI Agents SDK integration with MCP protocol
- MCP server exposing task operations as standardized tools
- AI-powered task management via agent tools

**Agent & AI Architecture**:
- OpenAI Agents SDK integration
- Agent runner lifecycle management
- Agent-to-tool communication via MCP protocol
- Mandatory tool-based task operations through MCP
- Intent detection and tool selection logic
- Multi-tool chaining for complex operations
- Confirmation responses for destructive actions
- Graceful failure handling for tool operations

**MCP Server Integration**:
- Official MCP SDK implementation
- Dedicated MCP server exposing task operations as tools
- Stateless MCP tools with database-backed persistence
- Standardized tool schemas and validation
- MCP tool contracts with required parameters, return schemas, validation rules, and error contracts

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

**AI Security Extensions**:
- AI prompt injection protection for all natural language inputs
- Tool misuse prevention with parameter validation
- Conversation isolation ensuring user data separation
- Output sanitization for AI-generated responses
- Abuse detection for AI usage patterns
- Rate limiting for AI-powered endpoints

## API CONTRACT (IMMUTABLE)

**Existing Endpoints**:
- GET    `/api/{user_id}/tasks`
- POST   `/api/{user_id}/tasks`
- GET    `/api/{user_id}/tasks/{id}`
- PUT    `/api/{user_id}/tasks/{id}`
- DELETE `/api/{user_id}/tasks/{id}`
- PATCH  `/api/{user_id}/tasks/{id}/complete`

**New AI Endpoints**:
- POST   `/api/{user_id}/chat`

**Chat Endpoint Schema**:
- Request:
  - conversation_id (optional, string)
  - message (required, string)
- Response:
  - conversation_id (string)
  - response (string)
  - tool_calls (array of tool call objects)

**API Rules**:
- user_id in URL MUST match JWT user_id
- Backend MUST NOT trust frontend input
- ALL queries filtered by authenticated user_id
- JWT authentication required for ALL endpoints (including AI endpoints)
- user_id path validation enforced for all endpoints
- Ownership verification required for all operations
- Rate limiting applied to all endpoints including chat

## DATA OWNERSHIP RULES

- Every task belongs to exactly ONE user
- Cross-user access is impossible
- No admin bypass
- No shared tasks
- Conversation history is user-isolated and owned by the user who created it
- Messages in conversations are tied to the user and conversation ownership

## NEW DATABASE MODELS

**Conversation Model**:
- id (UUID, PK)
- user_id (UUID, indexed, FK to User)
- created_at (datetime)
- updated_at (datetime)

**Message Model**:
- id (UUID, PK)
- user_id (UUID, indexed, FK to User)
- conversation_id (UUID, indexed, FK to Conversation)
- role (string: "user" | "assistant")
- content (text)
- created_at (datetime)

## MCP TOOL SPECIFICATIONS

**Mandatory MCP Tools**:
- `add_task`: Create new tasks via natural language
- `list_tasks`: Retrieve user's tasks with optional filters
- `complete_task`: Mark tasks as complete/incomplete
- `delete_task`: Remove tasks from user's list
- `update_task`: Modify existing task properties

**Tool Contracts**:
- Required parameters for each tool with validation
- Return schemas specifying expected output formats
- Validation rules preventing invalid operations
- Error contracts defining error responses and codes

## STATELESS CONVERSATION LIFECYCLE

**Execution Flow**:
1. Receive message via POST `/api/{user_id}/chat`
2. Validate JWT and user ownership
3. Load conversation history from DB (if conversation_id provided)
4. Build agent context with user's task data
5. Persist user message to database
6. Execute agent with MCP tool access
7. Invoke MCP tools as needed for task operations
8. Persist assistant response to database
9. Return response, conversation_id, and tool_calls
10. Maintain no server-side conversation state between requests

## FRONTEND CONSTITUTION

**Technology Stack**:
- Next.js 16+ (App Router)
- TypeScript
- Tailwind CSS
- Better Auth (JWT enabled)
- OpenAI ChatKit for conversational UI

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
- ChatKit (AI conversational interface)
- ConversationSelector
- MessageTimeline
- TypingIndicator
- ToolExecutionFeedback

**UX Rules**:
- Mobile-first
- Keyboard accessible
- Optimistic UI updates
- Skeleton loaders (NO spinners)
- Inline validation
- No full page reloads
- AI conversation awareness with loading states for tool execution
- Clear feedback for AI tool operations

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
- Chat pagination for conversation history
- History window limits for performance
- Agent timeout enforcement
- Tool call quotas to prevent abuse

**Container & Deployment Rules**:
- Dockerfile for containerization with multi-stage builds
- Environment variable configuration for different deployment environments
- Health check endpoints for container orchestration readiness
- Resource limits and requests defined in deployment configurations
- Security scanning integrated into CI/CD pipeline
- Image tagging strategy following semantic versioning
- Container registry integration for image distribution
- CDN configuration for static asset delivery
- SSL/TLS termination configuration for secure communication

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
- OpenAI Agents SDK
- MCP Protocol Implementation

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

**Conversation Model**:
- id (UUID, PK)
- user_id (UUID, indexed, FK to User)
- created_at
- updated_at

**Message Model**:
- id (UUID, PK)
- user_id (UUID, indexed, FK to User)
- conversation_id (UUID, indexed, FK to Conversation)
- role (user | assistant)
- content
- created_at

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
- AI usage monitoring and rate limiting

**Business Logic Requirements**:
- Recurring tasks auto-reschedule on completion
- Soft deletes NOT allowed
- Completion is toggle-based
- Filtering & sorting server-side
- MCP tool execution follows same business rules as traditional API
- AI agents operate within same security and ownership constraints

**Database Rules**:
- Async sessions
- Connection pooling
- Indexes REQUIRED on:
  - user_id
  - due_date
  - priority
  - is_completed
  - conversation.user_id
  - message.conversation_id
  - message.user_id
- No raw SQL
- Migrations REQUIRED

**Performance Requirements**:
- Pagination mandatory
- Query limits enforced
- Max payload size enforced
- Chat pagination for conversation history
- History window limits for performance
- Agent timeout enforcement (max 30 seconds)
- Tool call quotas to prevent abuse
- Cost monitoring for AI usage

**Kubernetes Execution Rules**:
- Pod specifications with resource limits and requests
- Service definitions for internal communication
- ConfigMaps and Secrets for configuration management
- Health checks (liveness and readiness probes)
- Horizontal Pod Autoscaler configurations
- Persistent volume claims for stateful components
- Network policies for service isolation
- Security contexts for container security
- Init containers for pre-startup tasks
- Sidecar containers for logging and monitoring
- Database connection pooling in containerized environments
- Circuit breaker patterns for resilient service communication

**Prohibited Practices**:
- Trusting frontend user_id
- Storing auth sessions
- Cross-user queries
- Silent failures
- Direct database access bypassing ORM
- AI operations without proper authentication

## SPEC-DRIVEN DEVELOPMENT RULES

- No feature without spec
- No UI without component definition
- No API without request/response schema
- No styling without tokens
- No undocumented decisions
- No AI features without /specs/agents documentation
- No MCP tools without /specs/mcp-tools documentation
- No chat API without OpenAPI documentation
- No AI workflows without reproducible test cases
- No infrastructure changes without /specs/infrastructure documentation
- No Kubernetes manifests without /specs/k8s documentation
- No Helm charts without /specs/helm documentation
- No container images without /specs/container documentation
- No deployment configurations without infrastructure specs
- Infrastructure specifications must be version-controlled alongside application specs
- Kubernetes manifest specifications must follow established patterns
- Helm chart specifications must include parameter validation
- Container image build specifications must define security requirements
- Network policy definitions must be documented in specs
- Monitoring and logging configuration specs must be maintained
- Security policy specifications for containers must be defined
- Resource allocation and scaling specifications must be documented

## QUALITY GATES

- All code must pass linting and type checking
- All APIs must be documented with OpenAPI
- All database migrations must be tested
- All auth flows must be verified end-to-end
- All UI components must be responsive
- All performance benchmarks must be met
- All security requirements must be validated
- All AI workflows must have end-to-end tests
- All MCP tools must have unit and integration tests
- All AI security measures must be validated
- Pre-deployment health checks for all services
- Configuration validation against security policies
- Resource availability verification before deployment
- Network connectivity testing between services
- Service discovery validation for inter-service communication
- Kubernetes cluster health checks before deployment
- Resource quota compliance verification
- Security policy enforcement validation
- Backup and recovery validation for stateful components
- Monitoring and alerting verification for deployed services

## IMPLEMENTATION CONTRACT

This constitution is the immutable source of truth. All development activities must strictly adhere to these specifications. No deviations are permitted without updating this document first.

## VERSION INFORMATION

**Version**: 2.0.0 | **Ratified**: 2026-01-08 | **Last Amended**: 2026-02-08

**Phase Evolution**:
- **Phase I**: Basic Todo CRUD functionality
- **Phase II**: Authentication and authorization
- **Phase III**: AI integration and real-time updates
- **Phase IV**: Cloud-native deployment and Kubernetes orchestration

## CLOUD-NATIVE & DEPLOYMENT CONSTITUTION (PHASE IV)

### Project Architecture Extension
The existing architecture is extended to include:

- **Containerization**: Docker-based containerization for both frontend and backend services
- **Orchestration**: Kubernetes (Minikube) for container orchestration and management
- **Packaging**: Helm charts for application packaging and deployment
- **AI DevOps Tools**: kubectl-ai, kagent for AI-assisted DevOps operations
- **Infrastructure as Code**: Declarative infrastructure management

### Deployment Principles
- Immutable infrastructure approach for consistent deployments
- Declarative configuration management using Kubernetes manifests
- Self-healing system capabilities with automatic recovery
- Blue-green deployment strategies for zero-downtime updates
- GitOps workflow implementation for infrastructure changes
- Reproducible deployments across different environments

### Container Rules (Frontend & Backend)
- Minimal base images for enhanced security posture
- Multi-stage builds to minimize attack surface
- Non-root user execution within containers
- Read-only root filesystem where possible for security
- Resource limits enforcement to prevent resource exhaustion
- Health check endpoint implementation for container orchestration
- Proper signal handling for graceful shutdown procedures
- Security scanning integration in the build pipeline

### Kubernetes Architecture
- Namespaced resource organization for multi-tenancy
- Pod Disruption Budgets to ensure availability during maintenance
- Resource quotas and limits for fair resource allocation
- Network policies for service isolation and security
- Service mesh implementation for advanced traffic management
- Ingress controllers for external access and load balancing
- Certificate management for TLS termination and encryption
- Cluster autoscaling configuration for dynamic resource management

### Helm Governance
- Parameterized chart templates for environment-specific configurations
- Version-controlled chart releases with semantic versioning
- Chart dependency management with proper version pinning
- Release lifecycle management with rollback capabilities
- Rollback and rollback validation procedures for failed deployments
- Chart testing with ct (Chart Testing) tool for quality assurance
- Chart security scanning for vulnerability detection
- Multi-environment configuration management through values files

### AI DevOps Policy
- AI-assisted Kubernetes resource management using kubectl-ai
- Intelligent deployment recommendations based on historical data
- Automated scaling decisions based on usage patterns and metrics
- Predictive failure detection and prevention mechanisms
- AI-powered log analysis and anomaly detection systems
- Automated incident response workflows for common issues
- Continuous optimization suggestions for resource efficiency
- AI-assisted security policy enforcement and compliance checking

### Configuration Management
- Centralized configuration with ConfigMaps and Secrets for sensitive data
- External configuration providers (HashiCorp Vault, Consul) for advanced use cases
- Dynamic configuration reloading without service restarts
- Configuration validation pipelines to prevent invalid configurations
- Environment-specific overrides through values files in Helm
- Secure secret rotation procedures with automated renewal
- Configuration drift detection to ensure compliance
- Immutable configuration principles to prevent runtime modifications

### Security in Containerized Environments
- Image vulnerability scanning at build and runtime
- Runtime security monitoring for anomalous behavior
- Network segmentation and encryption for inter-service communication
- RBAC policy enforcement for granular access control
- Pod security standards compliance for baseline security
- Admission controller policies for enforcement of security practices
- Secret encryption at rest using Kubernetes encryption providers
- Compliance auditing for containerized workloads and configurations

### Extended Frontend Constitution with Container & Deployment Rules
- Dockerfile for containerization with multi-stage builds
- Environment variable configuration for different deployment environments
- Health check endpoints for container orchestration readiness
- Resource limits and requests defined in deployment configurations
- Security scanning integrated into CI/CD pipeline
- Image tagging strategy following semantic versioning
- Container registry integration for image distribution
- CDN configuration for static asset delivery
- SSL/TLS termination configuration for secure communication

### Extended Backend Constitution with Kubernetes Execution Rules
- Pod specifications with resource limits and requests
- Service definitions for internal communication
- ConfigMaps and Secrets for configuration management
- Health checks (liveness and readiness probes)
- Horizontal Pod Autoscaler configurations
- Persistent volume claims for stateful components
- Network policies for service isolation
- Security contexts for container security
- Init containers for pre-startup tasks
- Sidecar containers for logging and monitoring
- Database connection pooling in containerized environments
- Circuit breaker patterns for resilient service communication

### Extended Spec-Driven Development Rules to Include Infrastructure Specs
- Infrastructure specifications must be version-controlled alongside application specs
- Kubernetes manifest specifications must follow established patterns
- Helm chart specifications must include parameter validation
- Container image build specifications must define security requirements
- Network policy definitions must be documented in specs
- Monitoring and logging configuration specs must be maintained
- Security policy specifications for containers must be defined
- Resource allocation and scaling specifications must be documented

### Extended Quality Gates with Deployment Validation Requirements
- Pre-deployment health checks for all services
- Configuration validation against security policies
- Resource availability verification before deployment
- Network connectivity testing between services
- Service discovery validation for inter-service communication
- Kubernetes cluster health checks before deployment
- Resource quota compliance verification
- Security policy enforcement validation
- Backup and recovery validation for stateful components
- Monitoring and alerting verification for deployed services
