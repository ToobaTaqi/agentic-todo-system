"""Natural language task operations API for chatbot integration."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from models.models import Task
from database.db import get_db_session
from auth.auth import get_current_user, TokenData
from utils.task_resolver import get_task_by_name, get_task_by_partial_name

router = APIRouter(prefix="/natural")

@router.get("/tasks/by-name/{task_name}", response_model=Task)
async def get_task_by_name_endpoint(
    task_name: str,
    user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """Get a specific task by its name for the authenticated user"""
    print(f"Get task by name endpoint hit for user: {user.user_id}, task_name: {task_name}")
    
    # First try exact match
    task = await get_task_by_name(db, user.user_id, task_name)
    if not task:
        # Then try partial match
        task = await get_task_by_partial_name(db, user.user_id, task_name)
    
    if not task:
        print(f"Task with name '{task_name}' not found for user: {user.user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    print(f"Found task: {task.id} for user: {user.user_id}")
    return task

@router.put("/tasks/by-name/{task_name}")
async def update_task_by_name(
    task_name: str,
    task_update: Task,
    user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """Update a specific task by its name for the authenticated user"""
    print(f"Update task by name endpoint hit for user: {user.user_id}, task_name: {task_name}")
    
    # First try exact match
    db_task = await get_task_by_name(db, user.user_id, task_name)
    if not db_task:
        # Then try partial match
        db_task = await get_task_by_partial_name(db, user.user_id, task_name)
    
    if not db_task:
        print(f"Task with name '{task_name}' not found for user: {user.user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update task fields
    for field, value in task_update.dict(exclude_unset=True).items():
        if field != 'user_id' and field != 'id':  # Prevent changing user_id and id
            setattr(db_task, field, value)

    db_task.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(db_task)
    print(f"Updated task: {db_task.id} for user: {user.user_id}")
    return db_task

@router.delete("/tasks/by-name/{task_name}")
async def delete_task_by_name(
    task_name: str,
    user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """Delete a specific task by its name for the authenticated user"""
    print(f"Delete task by name endpoint hit for user: {user.user_id}, task_name: {task_name}")
    
    # First try exact match
    task = await get_task_by_name(db, user.user_id, task_name)
    if not task:
        # Then try partial match
        task = await get_task_by_partial_name(db, user.user_id, task_name)
    
    if not task:
        print(f"Task with name '{task_name}' not found for user: {user.user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    await db.delete(task)
    await db.commit()
    print(f"Deleted task: {task.id} for user: {user.user_id}")
    return {"message": "Task deleted successfully"}

@router.patch("/tasks/by-name/{task_name}/complete")
async def toggle_task_completion_by_name(
    task_name: str,
    user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """Toggle task completion status by task name"""
    print(f"Toggle task completion by name endpoint hit for user: {user.user_id}, task_name: {task_name}")
    
    # First try exact match
    task = await get_task_by_name(db, user.user_id, task_name)
    if not task:
        # Then try partial match
        task = await get_task_by_partial_name(db, user.user_id, task_name)
    
    if not task:
        print(f"Task with name '{task_name}' not found for user: {user.user_id}")
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