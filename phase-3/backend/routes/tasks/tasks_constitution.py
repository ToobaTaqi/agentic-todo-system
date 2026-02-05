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

@router.get("/{user_id}/tasks", response_model=List[Task])
async def get_user_tasks(
    user_id: str,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """Get all tasks for a specific user - follows constitution API contract"""
    print(f"Get user tasks endpoint hit for user: {user_id}")
    # Verify that the user_id in the URL matches the authenticated user's ID
    if current_user.user_id != user_id:
        print(f"Access denied: user_id {user_id} does not match authenticated user {current_user.user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user_id does not match authenticated user"
        )

    # Use SQLModel's exec method for better async session handling
    statement = select(Task).where(Task.user_id == UUID(user_id))
    result = await db.exec(statement)
    tasks = result.all()
    print(f"Found {len(tasks)} tasks for user: {user_id}")
    return tasks

@router.post("/{user_id}/tasks", response_model=Task)
async def create_user_task(
    user_id: str,
    task: Task,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """Create a new task for a specific user - follows constitution API contract"""
    print(f"Create user task endpoint hit for user: {user_id}")
    # Verify that the user_id in the URL matches the authenticated user's ID
    if current_user.user_id != user_id:
        print(f"Access denied: user_id {user_id} does not match authenticated user {current_user.user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user_id does not match authenticated user"
        )

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
    new_task.user_id = UUID(user_id)

    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    print(f"Created task with ID: {new_task.id} for user: {user_id}")
    return new_task

@router.get("/{user_id}/tasks/{id}", response_model=Task)
async def get_user_task(
    user_id: str,
    id: str,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """Get a specific task for a specific user - follows constitution API contract"""
    print(f"Get specific user task endpoint hit for user: {user_id}, task id: {id}")
    # Verify that the user_id in the URL matches the authenticated user's ID
    if current_user.user_id != user_id:
        print(f"Access denied: user_id {user_id} does not match authenticated user {current_user.user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user_id does not match authenticated user"
        )

    task_id = UUID(id)
    # Use SQLModel's exec method for better async session handling
    statement = select(Task).where(Task.id == task_id).where(Task.user_id == UUID(user_id))
    result = await db.exec(statement)
    task = result.first()

    if not task:
        print(f"Task {id} not found for user: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    print(f"Found task: {task.id} for user: {user_id}")
    return task

@router.put("/{user_id}/tasks/{id}", response_model=Task)
async def update_user_task(
    user_id: str,
    id: str,
    task_update: Task,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """Update a specific task for a specific user - follows constitution API contract"""
    print(f"Update user task endpoint hit for user: {user_id}, task id: {id}")
    # Verify that the user_id in the URL matches the authenticated user's ID
    if current_user.user_id != user_id:
        print(f"Access denied: user_id {user_id} does not match authenticated user {current_user.user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user_id does not match authenticated user"
        )

    task_id = UUID(id)
    # Use SQLModel's exec method for better async session handling
    statement = select(Task).where(Task.id == task_id).where(Task.user_id == UUID(user_id))
    result = await db.exec(statement)
    db_task = result.first()

    if not db_task:
        print(f"Task {id} not found for user: {user_id}")
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
    print(f"Updated task: {db_task.id} for user: {user_id}")
    return db_task

@router.delete("/{user_id}/tasks/{id}")
async def delete_user_task(
    user_id: str,
    id: str,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """Delete a specific task for a specific user - follows constitution API contract"""
    print(f"Delete user task endpoint hit for user: {user_id}, task id: {id}")
    # Verify that the user_id in the URL matches the authenticated user's ID
    if current_user.user_id != user_id:
        print(f"Access denied: user_id {user_id} does not match authenticated user {current_user.user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user_id does not match authenticated user"
        )

    task_id = UUID(id)
    # Use SQLModel's exec method for better async session handling
    statement = select(Task).where(Task.id == task_id).where(Task.user_id == UUID(user_id))
    result = await db.exec(statement)
    task = result.first()

    if not task:
        print(f"Task {id} not found for user: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    await db.delete(task)
    await db.commit()
    print(f"Deleted task: {task.id} for user: {user_id}")
    return {"message": "Task deleted successfully"}

@router.patch("/{user_id}/tasks/{id}/complete")
async def toggle_user_task_completion(
    user_id: str,
    id: str,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """Toggle task completion status for a specific user - follows constitution API contract"""
    print(f"Toggle task completion endpoint hit for user: {user_id}, task id: {id}")
    # Verify that the user_id in the URL matches the authenticated user's ID
    if current_user.user_id != user_id:
        print(f"Access denied: user_id {user_id} does not match authenticated user {current_user.user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user_id does not match authenticated user"
        )

    task_id = UUID(id)
    # Use SQLModel's exec method for better async session handling
    statement = select(Task).where(Task.id == task_id).where(Task.user_id == UUID(user_id))
    result = await db.exec(statement)
    task = result.first()

    if not task:
        print(f"Task {id} not found for user: {user_id}")
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