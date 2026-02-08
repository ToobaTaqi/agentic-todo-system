"""MCP (Model Context Protocol) server for AI-powered task operations."""
import asyncio
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, ValidationError
from models.models import Task
from models.conversation_models import Conversation, Message
from database.db import get_db_session
from database.conversation_db import get_conversation_by_id
from auth.auth import get_current_user
from fastapi import HTTPException, status
from sqlmodel import select
from datetime import datetime, timedelta
import uuid
from utils.task_resolver import resolve_task_id_from_name, get_task_by_name
from websocket_manager import manager
import json


class ToolResult(BaseModel):
    """Result from an MCP tool execution."""
    success: bool
    data: Any = None
    error: Optional[str] = None


class AddTaskParams(BaseModel):
    """Parameters for add_task tool."""
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    tags: Optional[List[str]] = []
    due_date: Optional[str] = None
    is_recurring: Optional[bool] = False
    recurrence_pattern: Optional[str] = None

    def model_post_init(self, __context: Any) -> None:
        # Validate priority
        if self.priority and self.priority not in ["high", "medium", "low"]:
            raise ValueError("Priority must be one of: high, medium, low")

        # Validate recurrence pattern only if is_recurring is true
        if self.is_recurring and self.recurrence_pattern:
            if self.recurrence_pattern not in ["daily", "weekly", "monthly"]:
                raise ValueError("Recurrence pattern must be one of: daily, weekly, monthly when is_recurring is true")
        elif self.is_recurring and not self.recurrence_pattern:
            # If is_recurring is true but no pattern provided, set a default
            object.__setattr__(self, 'recurrence_pattern', 'daily')
        elif not self.is_recurring:
            # If not recurring, ensure recurrence_pattern is None
            object.__setattr__(self, 'recurrence_pattern', None)


class ListTasksParams(BaseModel):
    """Parameters for list_tasks tool."""
    status: Optional[str] = None
    priority: Optional[str] = None
    search: Optional[str] = None
    sort: Optional[str] = "due_date"
    order: Optional[str] = "asc"
    page: Optional[int] = 1
    limit: Optional[int] = 50

    def model_post_init(self, __context: Any) -> None:
        # Validate status
        if self.status and self.status not in ["completed", "incomplete"]:
            raise ValueError("Status must be one of: completed, incomplete")

        # Validate priority
        if self.priority and self.priority not in ["high", "medium", "low"]:
            raise ValueError("Priority must be one of: high, medium, low")

        # Validate sort
        if self.sort and self.sort not in ["due_date", "priority", "title", "created_at"]:
            raise ValueError("Sort must be one of: due_date, priority, title, created_at")

        # Validate order
        if self.order and self.order not in ["asc", "desc"]:
            raise ValueError("Order must be one of: asc, desc")


class CompleteTaskParams(BaseModel):
    """Parameters for complete_task tool."""
    task_id: Optional[str] = None  # Keep for backward compatibility
    task_name: Optional[str] = None  # New field for natural language task identification

    def model_post_init__(self, __context: Any) -> None:
        # Either task_id or task_name must be provided
        if not self.task_id and not self.task_name:
            raise ValueError("Either task_id or task_name must be provided")
        

class DeleteTaskParams(BaseModel):
    """Parameters for delete_task tool."""
    task_id: Optional[str] = None  # Keep for backward compatibility
    task_name: Optional[str] = None  # New field for natural language task identification

    def model_post_init__(self, __context: Any) -> None:
        # Either task_id or task_name must be provided
        if not self.task_id and not self.task_name:
            raise ValueError("Either task_id or task_name must be provided")


class UpdateTaskParams(BaseModel):
    """Parameters for update_task tool."""
    task_id: Optional[str] = None  # Keep for backward compatibility
    task_name: Optional[str] = None  # New field for natural language task identification
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    tags: Optional[List[str]] = None
    due_date: Optional[str] = None
    is_recurring: Optional[bool] = None
    recurrence_pattern: Optional[str] = None

    def model_post_init__(self, __context: Any) -> None:
        # Either task_id or task_name must be provided
        if not self.task_id and not self.task_name:
            raise ValueError("Either task_id or task_name must be provided")
        
        # Validate priority if provided
        if self.priority and self.priority not in ["high", "medium", "low"]:
            raise ValueError("Priority must be one of: high, medium, low")

        # Validate recurrence pattern only if is_recurring is true and pattern is provided
        if self.is_recurring is True and self.recurrence_pattern:
            if self.recurrence_pattern not in ["daily", "weekly", "monthly"]:
                raise ValueError("Recurrence pattern must be one of: daily, weekly, monthly when is_recurring is true")
        elif self.is_recurring is True and not self.recurrence_pattern:
            # If is_recurring is true but no pattern provided, set a default
            object.__setattr__(self, 'recurrence_pattern', 'daily')
        elif self.is_recurring is False:
            # If not recurring, ensure recurrence_pattern is None
            object.__setattr__(self, 'recurrence_pattern', None)


async def add_task_tool(params: dict, user_id: str) -> ToolResult:
    """MCP tool to add a new task."""
    try:
        validated_params = AddTaskParams(**params)

        # Validate title length
        if len(validated_params.title) > 255:
            return ToolResult(success=False, error="Title must be less than 255 characters")

        # Validate description length if provided
        if validated_params.description and len(validated_params.description) > 1000:
            return ToolResult(success=False, error="Description must be less than 1000 characters")

        # Validate tags length
        if len(validated_params.tags) > 10:
            return ToolResult(success=False, error="Maximum 10 tags allowed")

        # Parse due date if provided
        due_date_value = None
        if validated_params.due_date:
            try:
                due_date_value = datetime.fromisoformat(validated_params.due_date.replace('Z', '+00:00'))
                # Convert to timezone-naive to match database expectations
                if due_date_value.tzinfo is not None:
                    due_date_value = due_date_value.replace(tzinfo=None)
            except ValueError:
                return ToolResult(success=False, error="Invalid due date format")

        # Import here to avoid circular imports
        from database.db import engine
        from sqlalchemy.ext.asyncio import AsyncSession
        
        # Create task
        async with AsyncSession(engine) as db:
            new_task = Task(
                user_id=uuid.UUID(user_id),
                title=validated_params.title,
                description=validated_params.description,
                priority=validated_params.priority,
                tags=validated_params.tags,
                due_date=due_date_value,
                is_completed=False,  # New tasks are not completed by default
                is_recurring=validated_params.is_recurring,
                recurrence_pattern=validated_params.recurrence_pattern
            )

            db.add(new_task)
            await db.commit()
            await db.refresh(new_task)

            # Send real-time update to the frontend
            try:
                await manager.broadcast_to_user({
                    "type": "task_created",
                    "task": new_task.dict(),
                    "timestamp": datetime.utcnow().isoformat()
                }, user_id)
            except Exception as e:
                # Log the error but don't fail the operation
                print(f"Error broadcasting task creation: {str(e)}")

            return ToolResult(success=True, data=new_task.dict())

    except ValidationError as ve:
        return ToolResult(success=False, error=f"Validation error: {str(ve)}")
    except Exception as e:
        return ToolResult(success=False, error=f"Error creating task: {str(e)}")


async def list_tasks_tool(params: dict, user_id: str) -> ToolResult:
    """MCP tool to list tasks with optional filtering."""
    try:
        validated_params = ListTasksParams(**params)

        # Import here to avoid circular imports
        from database.db import engine
        from sqlalchemy.ext.asyncio import AsyncSession

        async with AsyncSession(engine) as db:
            statement = select(Task).where(Task.user_id == uuid.UUID(user_id))

            # Apply filters
            if validated_params.status:
                is_completed = validated_params.status == "completed"
                statement = statement.where(Task.is_completed == is_completed)

            if validated_params.priority:
                statement = statement.where(Task.priority == validated_params.priority)

            if validated_params.search:
                search_term = f"%{validated_params.search}%"
                statement = statement.where(
                    Task.title.ilike(search_term) |
                    Task.description.ilike(search_term)
                )

            # Apply sorting
            if validated_params.sort == "due_date":
                order_clause = Task.due_date.asc() if validated_params.order == "asc" else Task.due_date.desc()
            elif validated_params.sort == "priority":
                order_clause = Task.priority.asc() if validated_params.order == "asc" else Task.priority.desc()
            elif validated_params.sort == "title":
                order_clause = Task.title.asc() if validated_params.order == "asc" else Task.title.desc()
            else:  # created_at
                order_clause = Task.created_at.asc() if validated_params.order == "asc" else Task.created_at.desc()

            statement = statement.order_by(order_clause)

            # Apply pagination
            offset = (validated_params.page - 1) * validated_params.limit
            statement = statement.offset(offset).limit(validated_params.limit)

            result = await db.execute(statement)
            tasks = result.scalars().all()

            task_dicts = [task.dict() for task in tasks]

            return ToolResult(success=True, data={
                "tasks": task_dicts,
                "pagination": {
                    "page": validated_params.page,
                    "limit": validated_params.limit,
                    "total": len(task_dicts)  # Note: This is not the total count, just the returned count
                }
            })

    except ValidationError as ve:
        return ToolResult(success=False, error=f"Validation error: {str(ve)}")
    except Exception as e:
        return ToolResult(success=False, error=f"Error listing tasks: {str(e)}")


async def complete_task_tool(params: dict, user_id: str) -> ToolResult:
    """MCP tool to toggle task completion status."""
    try:
        validated_params = CompleteTaskParams(**params)

        # Import here to avoid circular imports
        from database.db import engine
        from sqlalchemy.ext.asyncio import AsyncSession
        
        # Create a session directly using the engine
        async with AsyncSession(engine) as db:
            task = None
            
            # Determine the task based on either task_id or task_name
            if validated_params.task_id:
                # Validate UUID format
                try:
                    task_uuid = uuid.UUID(validated_params.task_id)
                    # Get the task by ID and verify ownership
                    statement = select(Task).where(
                        Task.id == task_uuid,
                        Task.user_id == uuid.UUID(user_id)
                    )
                    result = await db.execute(statement)
                    task = result.scalar_one_or_none()
                except ValueError:
                    return ToolResult(success=False, error="Invalid task ID format")
            elif validated_params.task_name:
                # Get the task by name
                task = await get_task_by_name(db, user_id, validated_params.task_name)
            
            if not task:
                return ToolResult(success=False, error="Task not found or not authorized")

            # Toggle completion status
            task.is_completed = not task.is_completed

            # Handle recurring tasks - if marking as complete, auto-schedule next occurrence
            if task.is_completed and task.recurrence_pattern:
                # For recurring tasks, we would typically create a new instance for the next occurrence
                # For simplicity in this implementation, we'll just update the due date
                if task.recurrence_pattern == "daily":
                    task.due_date = datetime(task.due_date.year, task.due_date.month, task.due_date.day) + timedelta(days=1) if task.due_date else None
                elif task.recurrence_pattern == "weekly":
                    task.due_date = datetime(task.due_date.year, task.due_date.month, task.due_date.day) + timedelta(weeks=1) if task.due_date else None
                elif task.recurrence_pattern == "monthly":
                    # Simple month addition - in production, would need to handle month boundaries properly
                    next_month = task.due_date.month + 1 if task.due_date else None
                    if next_month > 12:
                        next_month = 1
                        year = task.due_date.year + 1 if task.due_date else None
                    else:
                        year = task.due_date.year if task.due_date else None
                    if task.due_date:
                        task.due_date = datetime(year, next_month, task.due_date.day)

            task.updated_at = datetime.utcnow()
            await db.commit()
            await db.refresh(task)

            # Send real-time update to the frontend
            try:
                await manager.broadcast_to_user({
                    "type": "task_updated",  # Completion is a form of update
                    "task": task.dict(),
                    "timestamp": datetime.utcnow().isoformat()
                }, user_id)
            except Exception as e:
                # Log the error but don't fail the operation
                print(f"Error broadcasting task completion: {str(e)}")

            return ToolResult(success=True, data=task.dict())

    except ValidationError as ve:
        return ToolResult(success=False, error=f"Validation error: {str(ve)}")
    except Exception as e:
        return ToolResult(success=False, error=f"Error completing task: {str(e)}")


async def delete_task_tool(params: dict, user_id: str) -> ToolResult:
    """MCP tool to delete a task."""
    try:
        validated_params = DeleteTaskParams(**params)

        # Import here to avoid circular imports
        from database.db import engine
        from sqlalchemy.ext.asyncio import AsyncSession
        
        # Create a session directly using the engine
        async with AsyncSession(engine) as db:
            task = None
            
            # Determine the task based on either task_id or task_name
            if validated_params.task_id:
                # Validate UUID format
                try:
                    task_uuid = uuid.UUID(validated_params.task_id)
                    # Get the task by ID and verify ownership
                    statement = select(Task).where(
                        Task.id == task_uuid,
                        Task.user_id == uuid.UUID(user_id)
                    )
                    result = await db.execute(statement)
                    task = result.scalar_one_or_none()
                except ValueError:
                    return ToolResult(success=False, error="Invalid task ID format")
            elif validated_params.task_name:
                # Get the task by name
                task = await get_task_by_name(db, user_id, validated_params.task_name)
            
            if not task:
                return ToolResult(success=False, error="Task not found or not authorized")

            # Get the task data before deletion to send in the update
            task_data = task.dict()
            
            await db.delete(task)
            await db.commit()

            # Send real-time update to the frontend
            try:
                await manager.broadcast_to_user({
                    "type": "task_deleted",
                    "task_id": str(task_data['id']),
                    "task_title": task_data['title'],
                    "timestamp": datetime.utcnow().isoformat()
                }, user_id)
            except Exception as e:
                # Log the error but don't fail the operation
                print(f"Error broadcasting task deletion: {str(e)}")

            return ToolResult(success=True, data={"message": "Task deleted successfully"})

    except ValidationError as ve:
        return ToolResult(success=False, error=f"Validation error: {str(ve)}")
    except Exception as e:
        return ToolResult(success=False, error=f"Error deleting task: {str(e)}")


async def update_task_tool(params: dict, user_id: str) -> ToolResult:
    """MCP tool to update task properties."""
    try:
        validated_params = UpdateTaskParams(**params)

        # Validate title length if provided
        if validated_params.title and len(validated_params.title) > 255:
            return ToolResult(success=False, error="Title must be less than 255 characters")

        # Validate description length if provided
        if validated_params.description and len(validated_params.description) > 1000:
            return ToolResult(success=False, error="Description must be less than 1000 characters")

        # Validate tags length if provided
        if validated_params.tags and len(validated_params.tags) > 10:
            return ToolResult(success=False, error="Maximum 10 tags allowed")

        # Parse due date if provided
        due_date_value = None
        if validated_params.due_date:
            try:
                due_date_value = datetime.fromisoformat(validated_params.due_date.replace('Z', '+00:00'))
                # Convert to timezone-naive to match database expectations
                if due_date_value.tzinfo is not None:
                    due_date_value = due_date_value.replace(tzinfo=None)
            except ValueError:
                return ToolResult(success=False, error="Invalid due date format")

        # Import here to avoid circular imports
        from database.db import engine
        from sqlalchemy.ext.asyncio import AsyncSession
        
        # Create a session directly using the engine
        async with AsyncSession(engine) as db:
            task = None
            
            # Determine the task based on either task_id or task_name
            if validated_params.task_id:
                # Validate UUID format
                try:
                    task_uuid = uuid.UUID(validated_params.task_id)
                    # Get the task by ID and verify ownership
                    statement = select(Task).where(
                        Task.id == task_uuid,
                        Task.user_id == uuid.UUID(user_id)
                    )
                    result = await db.execute(statement)
                    task = result.scalar_one_or_none()
                except ValueError:
                    return ToolResult(success=False, error="Invalid task ID format")
            elif validated_params.task_name:
                # Get the task by name
                task = await get_task_by_name(db, user_id, validated_params.task_name)
            
            if not task:
                return ToolResult(success=False, error="Task not found or not authorized")

            # Update fields that were provided (excluding task_id and task_name)
            update_fields = validated_params.dict(exclude_unset=True)
            for field, value in update_fields.items():
                if field not in ['task_id', 'task_name']:  # Don't update these fields
                    if field == 'due_date':
                        setattr(task, field, due_date_value)
                    elif field == 'is_recurring':
                        # Update is_recurring and handle recurrence_pattern accordingly
                        setattr(task, field, value)
                        # If is_recurring is False, set recurrence_pattern to None
                        if value is False:
                            setattr(task, 'recurrence_pattern', None)
                    else:
                        setattr(task, field, value)

            task.updated_at = datetime.utcnow()
            await db.commit()
            await db.refresh(task)

            # Send real-time update to the frontend
            try:
                await manager.broadcast_to_user({
                    "type": "task_updated",
                    "task": task.dict(),
                    "timestamp": datetime.utcnow().isoformat()
                }, user_id)
            except Exception as e:
                # Log the error but don't fail the operation
                print(f"Error broadcasting task update: {str(e)}")

            return ToolResult(success=True, data=task.dict())

    except ValidationError as ve:
        return ToolResult(success=False, error=f"Validation error: {str(ve)}")
    except Exception as e:
        return ToolResult(success=False, error=f"Error updating task: {str(e)}")


# Dictionary mapping tool names to their functions
MCP_TOOLS = {
    "add_task": add_task_tool,
    "list_tasks": list_tasks_tool,
    "complete_task": complete_task_tool,
    "delete_task": delete_task_tool,
    "update_task": update_task_tool
}


async def execute_mcp_tool(tool_name: str, params: dict, user_id: str) -> ToolResult:
    """Execute an MCP tool with the given parameters."""
    if tool_name not in MCP_TOOLS:
        return ToolResult(success=False, error=f"Unknown tool: {tool_name}")

    tool_func = MCP_TOOLS[tool_name]
    return await tool_func(params, user_id)