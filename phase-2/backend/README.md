# AI-Ready Todo App - Backend

This is the backend of the AI-Ready Full-Stack Todo App, built with FastAPI, SQLModel, and PostgreSQL.

## Tech Stack

- **Framework**: FastAPI (Python 3.11+)
- **Database**: Neon Serverless PostgreSQL
- **ORM**: SQLModel
- **Authentication**: JWT-based with Better Auth compatibility
- **Async**: Built with async-first architecture

## Features

- RESTful API with JWT authentication
- User management (registration, login, session management)
- Task CRUD operations with user ownership
- Priority levels (High/Medium/Low)
- Tagging system with JSON storage
- Due dates and recurring tasks
- Search, filter, and sort functionality
- Secure user isolation (no cross-user access)

## Prerequisites

- Python 3.11+
- PostgreSQL (or Neon Serverless Database)
- pip package manager

## Installation & Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd agentic-todo-system/phase-2/backend
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
# If requirements.txt doesn't exist, install the necessary packages:
pip install fastapi uvicorn sqlmodel python-jose[cryptography] passlib[bcrypt] python-dotenv psycopg2-binary
```

### 4. Environment Configuration

Create a `.env` file in the backend root directory with the following content:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
BETTER_AUTH_SECRET=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 7 days (as per constitution)
```

**Note**: The `BETTER_AUTH_SECRET` should match the one used in the frontend for JWT validation.

### 5. Database Setup

Ensure PostgreSQL is running and create the database tables:

```bash
# Run the application to initialize the database
python main.py
```

Or manually run database initialization if needed.

### 6. Run the development server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at [http://localhost:8000](http://localhost:8000)

API documentation will be available at:
- [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI)
- [http://localhost:8000/redoc](http://localhost:8000/redoc) (ReDoc)

### 7. Alternative: Run with Gunicorn (production-like)

```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## API Endpoints

### Authentication Endpoints

- `POST /api/v1/register` - Register a new user
- `POST /api/v1/login` - Authenticate user and return JWT token
- `POST /api/v1/logout` - Logout user
- `GET /api/v1/session` - Verify current session
- `POST /api/v1/refresh` - Refresh JWT token

### Task Endpoints (Constitution Compliant)

- `GET /api/{user_id}/tasks` - Get all tasks for a specific user
- `POST /api/{user_id}/tasks` - Create a new task for a specific user
- `GET /api/{user_id}/tasks/{id}` - Get a specific task for a user
- `PUT /api/{user_id}/tasks/{id}` - Update a specific task for a user
- `DELETE /api/{user_id}/tasks/{id}` - Delete a specific task for a user
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion status

### Legacy Endpoints (for backward compatibility)

- `GET /api/v1/tasks` - Get tasks for authenticated user
- `POST /api/v1/tasks` - Create a task for authenticated user
- `GET /api/v1/tasks/{task_id}` - Get a specific task
- `PUT /api/v1/tasks/{task_id}` - Update a specific task
- `DELETE /api/v1/tasks/{task_id}` - Delete a specific task
- `PATCH /api/v1/tasks/{task_id}/complete` - Toggle task completion

## Project Structure

```
backend/
├── main.py               # FastAPI app entry point
├── models/              # SQLModel database models
│   └── models.py        # User and Task models
├── routes/              # API route handlers
│   ├── auth/           # Authentication routes
│   ├── tasks/          # Task-related routes (including constitution-compliant ones)
│   └── users/          # User-related routes
├── auth/                # Authentication utilities
│   └── auth.py          # JWT handling and user authentication
├── database/            # Database connection utilities
│   └── db.py            # Database session management
├── schemas/             # Pydantic request/response schemas
│   └── auth_schemas.py  # Authentication-related schemas
├── middleware/          # Request processing middleware
├── tests/               # Unit and integration tests
├── utils/               # Helper functions and utilities
└── requirements.txt     # Python dependencies
```

## Authentication & Security

The backend implements JWT-based authentication with the following characteristics:

- JWT tokens contain: user_id, email, issued_at, expiry (max 7 days as per constitution)
- All endpoints require valid JWT tokens
- User ID in URL path is validated against authenticated user ID
- No cross-user access is possible
- Tokens are validated using the shared BETTER_AUTH_SECRET

## Database Models

### User Model
- `id`: UUID (Primary Key)
- `email`: String (Unique, Indexed)
- `password_hash`: String
- `first_name`: String (Optional)
- `last_name`: String (Optional)
- `is_active`: Boolean (Default: True)
- `is_verified`: Boolean (Default: False)
- `created_at`: DateTime

### Task Model
- `id`: UUID (Primary Key)
- `user_id`: UUID (Indexed, Foreign Key to User)
- `title`: String (Required, max 255 chars)
- `description`: String (Optional)
- `priority`: String (Default: "medium", Values: "high", "medium", "low")
- `tags`: List (Stored as JSON)
- `due_date`: DateTime (Optional)
- `is_completed`: Boolean (Default: False)
- `is_recurring`: Boolean (Default: False)
- `recurrence_pattern`: String (Optional, Values: "daily", "weekly", "monthly")
- `created_at`: DateTime
- `updated_at`: DateTime

## Error Handling

- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: Access denied (user_id mismatch)
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource already exists (e.g., duplicate email)
- `500 Internal Server Error`: Unexpected server error

## Testing

To run tests:

```bash
pytest
```

Or for more verbose output:

```bash
pytest -v
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| DATABASE_URL | PostgreSQL connection string | Yes |
| BETTER_AUTH_SECRET | Secret key for JWT signing/validation | Yes |
| JWT_ALGORITHM | Algorithm for JWT (default: HS256) | No |
| ACCESS_TOKEN_EXPIRE_MINUTES | Token expiration in minutes (default: 10080 for 7 days) | No |
| SENDER_EMAIL | Email address for sending verification emails | For email verification |
| GMAIL_APP_PASSWORD | App password for Gmail SMTP authentication | For email verification |

## Deployment

For production deployment:

1. Use environment variables for configuration
2. Set up a reverse proxy (nginx, Apache)
3. Use a WSGI server like Gunicorn
4. Configure SSL certificates
5. Set up proper logging and monitoring

## Email Verification Setup

To enable email verification functionality:

1. **Configure Gmail SMTP**:
   - Enable 2-factor authentication on your Gmail account
   - Go to Google Account settings > Security > App passwords
   - Generate an app password for "Mail" and your device
   - Update your `.env` file with:
     ```env
     SENDER_EMAIL=toobtq@gmail.com
     GMAIL_APP_PASSWORD=your_16_char_app_password_here
     ```

2. **Environment Variables**:
   - `SENDER_EMAIL`: The Gmail address to send verification emails from
   - `GMAIL_APP_PASSWORD`: The 16-character app password (NOT your regular Gmail password)

3. **Important Notes**:
   - Do NOT use your regular Gmail password
   - App passwords are 16 characters long and contain spaces when displayed, but enter without spaces
   - The email verification system sends a verification link to new users upon registration
   - Users must verify their email within 30 minutes of registration

## Troubleshooting

- If you get database connection errors, verify your `DATABASE_URL` is correct
- For authentication issues, ensure the `BETTER_AUTH_SECRET` matches between frontend and backend
- If endpoints return 403 errors, check that the user_id in the URL matches the authenticated user
- For token expiration issues, verify that the clock on your server is synchronized
- For email verification issues, ensure `GMAIL_APP_PASSWORD` is correctly set to a valid app password
- If users don't receive verification emails, check that the email configuration is correct and that emails are not going to spam/junk folders

## API Documentation

The API is self-documenting with automatic OpenAPI/Swagger documentation available at `/docs` endpoint.