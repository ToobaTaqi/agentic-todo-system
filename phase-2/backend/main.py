from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="AI-Ready Todo API",
    description="API for the AI-Ready Full-Stack Todo App",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://agentic-todo-system-phase2.vercel.app"],  # Allow frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import models to register them with SQLModel before creating tables
from models.models import User, Task  # This will also import VerificationToken
from models.verification_models import VerificationToken

# Initialize database tables on startup
@app.on_event("startup")
async def startup_event():
    import asyncio
    from sqlalchemy import create_engine
    from sqlmodel import SQLModel

    # Get database URL from environment
    DATABASE_URL = os.getenv("DATABASE_URL")
    if DATABASE_URL:
        # Convert async URL to sync URL for table creation
        sync_database_url = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")

        # Create sync engine and tables
        sync_engine = create_engine(sync_database_url)
        SQLModel.metadata.create_all(sync_engine)

# Include routes
from routes.tasks.tasks import router as tasks_legacy
from routes.tasks.tasks_constitution import router as tasks
from routes.auth.auth import router as auth
from routes.users.users import router as users
app.include_router(tasks_legacy, prefix="/api/v1")  # Legacy routes
app.include_router(tasks, prefix="/api")  # Constitution-compliant routes
app.include_router(auth, prefix="/api/v1")
app.include_router(users, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "AI-Ready Todo API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}