from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import WebSocket, WebSocketDisconnect
from dotenv import load_dotenv
import os
import asyncio

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="AI-Ready Todo API",
    description="API for the AI-Ready Full-Stack Todo App",
    version="1.0.0"
)

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
from models.conversation_models import Conversation, Message  # Import conversation models to register with SQLModel

# Ensure all models are registered with SQLModel metadata
from sqlmodel import SQLModel

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
from routes.tasks.natural_language_tasks import router as natural_tasks
from routes.auth.auth import router as auth
from routes.users.users import router as users
from routes.chat.chat_api import router as chat
app.include_router(tasks_legacy, prefix="/api/v1")  # Legacy routes
app.include_router(tasks, prefix="/api")  # Constitution-compliant routes
app.include_router(natural_tasks, prefix="/api/v1")  # Natural language task operations
app.include_router(auth, prefix="/api/v1")
app.include_router(users, prefix="/api/v1")
app.include_router(chat, prefix="/api")  # AI chat endpoint

@app.get("/")
async def root():
    return {"message": "AI-Ready Todo API"}

@app.websocket("/ws/tasks/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """WebSocket endpoint for real-time task updates."""
    await manager.connect(websocket, user_id)
    try:
        # Keep the connection alive - we only send updates from backend
        # Just wait for disconnect without expecting any messages from frontend
        while True:
            # Sleep indefinitely until disconnect occurs
            await asyncio.sleep(3600)  # Sleep for 1 hour, will be interrupted on disconnect
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
    except Exception:
        # Handle any other exceptions
        manager.disconnect(websocket, user_id)


@app.get("/health")
async def health_check():
    return {"status": "ok"}