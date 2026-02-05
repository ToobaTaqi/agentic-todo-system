from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from datetime import datetime, timezone
from dateutil import parser
from models.models import Task
from database.db import get_db_session
from auth.auth import get_current_user, TokenData

router = APIRouter()

@router.get("/", response_model=List[Task])
async def get_tasks(
    user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """Get all tasks for the authenticated user"""
    print(f"Get tasks endpoint hit for user: {user.user_id}")
    statement = select(Task).where(Task.user_id == UUID(user.user_id))
    result = await db.execute(statement)
    tasks = result.scalars().all()
    print(f"Found {len(tasks)} tasks for user: {user.user_id}")
    return tasks

@router.post("/", response_model=Task)
async def create_task(
    task: Task,
    user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """Create a new task for the authenticated user"""
    print(f"Create task endpoint hit for user: {user.user_id}")
    # Create a new task instance to avoid potential conflicts with existing data
    # Handle datetime conversion for due_date if it's a string
    due_date_value = task.due_date
    if isinstance(due_date_value, str):
        try:
            # Try parsing the datetime string in ISO format
            due_date_value = parser.parse(due_date_value)
        except (ValueError, TypeError):
            # If parsing fails, set to None
            due_date_value = None

    new_task = Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        tags=task.tags,
        due_date=due_date_value,
        is_completed=task.is_completed or False,
        is_recurring=task.is_recurring or False,
        recurrence_pattern=task.recurrence_pattern
    )
    new_task.user_id = UUID(user.user_id)

    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    print(f"Created task with ID: {new_task.id} for user: {user.user_id}")
    return new_task

@router.get("/{task_id}", response_model=Task)
async def get_task(
    task_id: UUID,
    user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """Get a specific task for the authenticated user"""
    print(f"Get task endpoint hit for user: {user.user_id}, task_id: {task_id}")
    statement = select(Task).where(Task.id == task_id).where(Task.user_id == UUID(user.user_id))
    result = await db.execute(statement)
    task = result.scalar_one_or_none()

    if not task:
        print(f"Task {task_id} not found for user: {user.user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    print(f"Found task: {task.id} for user: {user.user_id}")
    return task

@router.put("/{task_id}", response_model=Task)
async def update_task(
    task_id: UUID,
    task_update: Task,
    user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """Update a specific task for the authenticated user"""
    print(f"Update task endpoint hit for user: {user.user_id}, task_id: {task_id}")
    statement = select(Task).where(Task.id == task_id).where(Task.user_id == UUID(user.user_id))
    result = await db.execute(statement)
    db_task = result.scalar_one_or_none()

    if not db_task:
        print(f"Task {task_id} not found for user: {user.user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update task fields with proper datetime handling
    for field, value in task_update.dict(exclude_unset=True).items():
        if field != 'user_id':  # Prevent changing user_id
            # Handle datetime conversion for due_date if it's a string
            if field == 'due_date' and isinstance(value, str):
                try:
                    parsed_value = parser.parse(value)
                    # Ensure the datetime is timezone-naive to match database expectations
                    if parsed_value.tzinfo is not None:
                        # Convert to UTC and remove timezone info to make it naive
                        parsed_value = parsed_value.astimezone(timezone.utc).replace(tzinfo=None)
                    setattr(db_task, field, parsed_value)
                except (ValueError, TypeError):
                    # If parsing fails, set to None
                    setattr(db_task, field, None)
            else:
                setattr(db_task, field, value)

    await db.commit()
    await db.refresh(db_task)
    print(f"Updated task: {db_task.id} for user: {user.user_id}")
    return db_task

@router.delete("/{task_id}")
async def delete_task(
    task_id: UUID,
    user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """Delete a specific task for the authenticated user"""
    print(f"Delete task endpoint hit for user: {user.user_id}, task_id: {task_id}")
    statement = select(Task).where(Task.id == task_id).where(Task.user_id == UUID(user.user_id))
    result = await db.execute(statement)
    task = result.scalar_one_or_none()

    if not task:
        print(f"Task {task_id} not found for user: {user.user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    await db.delete(task)
    await db.commit()
    print(f"Deleted task: {task.id} for user: {user.user_id}")
    return {"message": "Task deleted successfully"}

@router.patch("/{task_id}/complete")
async def toggle_task_completion(
    task_id: UUID,
    user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """Toggle task completion status"""
    print(f"Toggle task completion endpoint hit for user: {user.user_id}, task_id: {task_id}")
    statement = select(Task).where(Task.id == task_id).where(Task.user_id == UUID(user.user_id))
    result = await db.execute(statement)
    task = result.scalar_one_or_none()

    if not task:
        print(f"Task {task_id} not found for user: {user.user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    task.is_completed = not task.is_completed
    task.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(task)
    print(f"Toggled completion status for task: {task.id}, now completed: {task.is_completed}")
    return task