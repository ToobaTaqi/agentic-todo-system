"""Utility functions for resolving task names to IDs and vice versa."""
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import Task
import uuid
from typing import Optional, List


async def get_task_by_name(db: AsyncSession, user_id: str, task_name: str) -> Optional[Task]:
    """
    Find a task by its name for a specific user.
    
    Args:
        db: Async database session
        user_id: User's UUID as string
        task_name: Name/title of the task
    
    Returns:
        Task object if found, None otherwise
    """
    try:
        user_uuid = uuid.UUID(user_id)
        
        # Query for tasks with the exact title for the user
        statement = select(Task).where(
            Task.user_id == user_uuid,
            Task.title == task_name
        )
        
        result = await db.execute(statement)
        task = result.scalar_one_or_none()
        
        return task
    except Exception:
        # Return None if there's any error (e.g., invalid UUID)
        return None


async def get_task_by_partial_name(db: AsyncSession, user_id: str, task_name: str) -> Optional[Task]:
    """
    Find a task by partial name matching for a specific user.
    
    Args:
        db: Async database session
        user_id: User's UUID as string
        task_name: Partial name/title of the task
    
    Returns:
        Task object if found, None otherwise
    """
    try:
        user_uuid = uuid.UUID(user_id)
        
        # Query for tasks with partial title matching for the user
        statement = select(Task).where(
            Task.user_id == user_uuid,
            Task.title.ilike(f"%{task_name}%")
        ).order_by(Task.created_at.desc())  # Get most recent if multiple matches
        
        result = await db.execute(statement)
        task = result.scalar_one_or_none()
        
        return task
    except Exception:
        # Return None if there's any error (e.g., invalid UUID)
        return None


async def get_all_tasks_by_user(db: AsyncSession, user_id: str) -> List[Task]:
    """
    Get all tasks for a specific user.
    
    Args:
        db: Async database session
        user_id: User's UUID as string
    
    Returns:
        List of Task objects
    """
    try:
        user_uuid = uuid.UUID(user_id)
        
        statement = select(Task).where(Task.user_id == user_uuid)
        result = await db.execute(statement)
        tasks = result.scalars().all()
        
        return tasks
    except Exception:
        # Return empty list if there's any error
        return []


async def resolve_task_id_from_name(db: AsyncSession, user_id: str, task_identifier: str) -> Optional[str]:
    """
    Resolve a task identifier (name) to a task ID.
    
    Args:
        db: Async database session
        user_id: User's UUID as string
        task_identifier: Task name or identifier
    
    Returns:
        Task ID as string if found, None otherwise
    """
    # First try exact match
    task = await get_task_by_name(db, user_id, task_identifier)
    if task:
        return str(task.id)
    
    # Then try partial match
    task = await get_task_by_partial_name(db, user_id, task_identifier)
    if task:
        return str(task.id)
    
    return None