import argparse
import sys
import os
from pathlib import Path
from typing import List
from datetime import datetime

# Add the src directory to Python path for imports when running as module
if __name__ == "__main__" and __package__ is None:
    # Add the project root directory to sys.path
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from todo_cli.services.todo_service import TodoService
from todo_cli.models.todo import Todo


class CLICommands:
    def __init__(self, service: TodoService):
        self.service = service

    def add(self, description: str, priority: str = "medium", tags: List[str] = None, due_date: str = None,
            recurrence_pattern: str = "none", recurrence_end_date: str = None, reminder_time: str = None):
        # Parse due_date if provided
        due_date_obj = None
        if due_date:
            try:
                due_date_obj = datetime.fromisoformat(due_date)
            except ValueError:
                print(f"Warning: Invalid date format for due date: {due_date}. Expected ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS).")
                return

        # Parse recurrence_end_date if provided
        recurrence_end_date_obj = None
        if recurrence_end_date:
            try:
                recurrence_end_date_obj = datetime.fromisoformat(recurrence_end_date)
            except ValueError:
                print(f"Warning: Invalid date format for recurrence end date: {recurrence_end_date}. Expected ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS).")
                return

        # Parse reminder_time if provided
        reminder_time_obj = None
        if reminder_time:
            try:
                reminder_time_obj = datetime.fromisoformat(reminder_time)
            except ValueError:
                print(f"Warning: Invalid date format for reminder time: {reminder_time}. Expected ISO format (YYYY-MM-DDTHH:MM:SS).")
                return

        todo = self.service.create_todo(
            description, priority, tags or [], due_date_obj,
            recurrence_pattern, recurrence_end_date_obj, reminder_time_obj
        )
        print(f"Added todo: {todo.id} - {todo.description} [Priority: {todo.priority}]")
        if todo.tags:
            print(f"  Tags: {', '.join(todo.tags)}")
        if todo.due_date:
            print(f"  Due: {todo.due_date.strftime('%Y-%m-%d %H:%M:%S')}")
        if todo.recurrence_pattern != "none":
            print(f"  Recurrence: {todo.recurrence_pattern}")
            if todo.recurrence_end_date:
                print(f"  Recurrence ends: {todo.recurrence_end_date.strftime('%Y-%m-%d %H:%M:%S')}")
        if todo.reminder_time:
            print(f"  Reminder: {todo.reminder_time.strftime('%Y-%m-%d %H:%M:%S')}")

    def list(self, status: str = None, priority: str = None, tag: str = None, sort_by: str = "id", order: str = "asc"):
        # Get all todos first
        todos = self.service.get_all_todos()

        # Apply filters if specified
        if status or priority or tag:
            todos = self.service.filter_todos(status=status, priority=priority, tag=tag)

        # Apply sorting
        todos = self.service.sort_todos(sort_by=sort_by, order=order)

        if not todos:
            print("No todos found.")
        else:
            print(f"{'ID':<4} {'Status':<8} {'Priority':<10} {'Due Date':<12} {'Recurrence':<12} {'Reminder':<12} {'Tags':<15} {'Description'}")
            print("-" * 100)
            for todo in todos:
                status = "X" if todo.completed else "O"
                due_str = todo.due_date.strftime('%Y-%m-%d') if todo.due_date else "None"
                recurrence_str = todo.recurrence_pattern if todo.recurrence_pattern != "none" else "None"
                reminder_str = todo.reminder_time.strftime('%Y-%m-%d %H:%M') if todo.reminder_time else "None"
                tags_str = ",".join(todo.tags) if todo.tags else ""
                # Truncate tags if too long
                if len(tags_str) > 15:
                    tags_str = tags_str[:12] + "..."
                print(f"{todo.id:<4} [{status}{'':<6} {todo.priority:<10} {due_str:<12} {recurrence_str:<12} {reminder_str:<12} {tags_str:<15} {todo.description}")

    def update(self, todo_id: int, description: str = None, priority: str = None, tags: List[str] = None, due_date: str = None,
               recurrence_pattern: str = None, recurrence_end_date: str = None, reminder_time: str = None):
        # Parse due_date if provided
        due_date_obj = None
        if due_date:
            try:
                due_date_obj = datetime.fromisoformat(due_date)
            except ValueError:
                print(f"Warning: Invalid date format for due date: {due_date}. Expected ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS).")
                return

        # Parse recurrence_end_date if provided
        recurrence_end_date_obj = None
        if recurrence_end_date:
            try:
                recurrence_end_date_obj = datetime.fromisoformat(recurrence_end_date)
            except ValueError:
                print(f"Warning: Invalid date format for recurrence end date: {recurrence_end_date}. Expected ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS).")
                return

        # Parse reminder_time if provided
        reminder_time_obj = None
        if reminder_time:
            try:
                reminder_time_obj = datetime.fromisoformat(reminder_time)
            except ValueError:
                print(f"Warning: Invalid date format for reminder time: {reminder_time}. Expected ISO format (YYYY-MM-DDTHH:MM:SS).")
                return

        todo = self.service.update_todo(
            todo_id, description=description, priority=priority, tags=tags, due_date=due_date_obj,
            recurrence_pattern=recurrence_pattern, recurrence_end_date=recurrence_end_date_obj,
            reminder_time=reminder_time_obj
        )
        if todo:
            print(f"Updated todo: {todo.id} - {todo.description} [Priority: {todo.priority}]")
            if todo.tags:
                print(f"  Tags: {', '.join(todo.tags)}")
            if todo.due_date:
                print(f"  Due: {todo.due_date.strftime('%Y-%m-%d %H:%M:%S')}")
            if todo.recurrence_pattern != "none":
                print(f"  Recurrence: {todo.recurrence_pattern}")
                if todo.recurrence_end_date:
                    print(f"  Recurrence ends: {todo.recurrence_end_date.strftime('%Y-%m-%d %H:%M:%S')}")
            if todo.reminder_time:
                print(f"  Reminder: {todo.reminder_time.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"Todo with id {todo_id} not found.")

    def delete(self, todo_id: int):
        success = self.service.delete_todo(todo_id)
        if success:
            print(f"Deleted todo with id {todo_id}")
        else:
            print(f"Todo with id {todo_id} not found.")

    def complete(self, todo_id: int):
        todo = self.service.mark_complete(todo_id)
        if todo:
            print(f"Marked todo as complete: {todo.id} - {todo.description}")
        else:
            print(f"Todo with id {todo_id} not found.")

    def search(self, keyword: str):
        todos = self.service.search_todos(keyword)
        if not todos:
            print(f"No todos found matching '{keyword}'.")
        else:
            print(f"Search results for '{keyword}':")
            print(f"{'ID':<4} {'Status':<8} {'Priority':<10} {'Due Date':<12} {'Recurrence':<12} {'Reminder':<12} {'Tags':<15} {'Description'}")
            print("-" * 100)
            for todo in todos:
                status = "X" if todo.completed else "O"
                due_str = todo.due_date.strftime('%Y-%m-%d') if todo.due_date else "None"
                recurrence_str = todo.recurrence_pattern if todo.recurrence_pattern != "none" else "None"
                reminder_str = todo.reminder_time.strftime('%Y-%m-%d %H:%M') if todo.reminder_time else "None"
                tags_str = ",".join(todo.tags) if todo.tags else ""
                # Truncate tags if too long
                if len(tags_str) > 15:
                    tags_str = tags_str[:12] + "..."
                print(f"{todo.id:<4} [{status}{'':<6} {todo.priority:<10} {due_str:<12} {recurrence_str:<12} {reminder_str:<12} {tags_str:<15} {todo.description}")

    def filter(self, status: str = None, priority: str = None, due_date: str = None, tag: str = None):
        todos = self.service.filter_todos(status=status, priority=priority, due_date=due_date, tag=tag)
        if not todos:
            print("No todos found matching the filter criteria.")
        else:
            print("Filtered todos:")
            print(f"{'ID':<4} {'Status':<8} {'Priority':<10} {'Due Date':<12} {'Recurrence':<12} {'Reminder':<12} {'Tags':<15} {'Description'}")
            print("-" * 100)
            for todo in todos:
                status = "X" if todo.completed else "O"
                due_str = todo.due_date.strftime('%Y-%m-%d') if todo.due_date else "None"
                recurrence_str = todo.recurrence_pattern if todo.recurrence_pattern != "none" else "None"
                reminder_str = todo.reminder_time.strftime('%Y-%m-%d %H:%M') if todo.reminder_time else "None"
                tags_str = ",".join(todo.tags) if todo.tags else ""
                # Truncate tags if too long
                if len(tags_str) > 15:
                    tags_str = tags_str[:12] + "..."
                print(f"{todo.id:<4} [{status}{'':<6} {todo.priority:<10} {due_str:<12} {recurrence_str:<12} {reminder_str:<12} {tags_str:<15} {todo.description}")

    def sort(self, sort_by: str = "id", order: str = "asc"):
        todos = self.service.sort_todos(sort_by=sort_by, order=order)
        if not todos:
            print("No todos to sort.")
        else:
            print(f"Todos sorted by {sort_by} ({order}):")
            print(f"{'ID':<4} {'Status':<8} {'Priority':<10} {'Due Date':<12} {'Recurrence':<12} {'Reminder':<12} {'Tags':<15} {'Description'}")
            print("-" * 100)
            for todo in todos:
                status = "X" if todo.completed else "O"
                due_str = todo.due_date.strftime('%Y-%m-%d') if todo.due_date else "None"
                recurrence_str = todo.recurrence_pattern if todo.recurrence_pattern != "none" else "None"
                reminder_str = todo.reminder_time.strftime('%Y-%m-%d %H:%M') if todo.reminder_time else "None"
                tags_str = ",".join(todo.tags) if todo.tags else ""
                # Truncate tags if too long
                if len(tags_str) > 15:
                    tags_str = tags_str[:12] + "..."
                print(f"{todo.id:<4} [{status}{'':<6} {todo.priority:<10} {due_str:<12} {recurrence_str:<12} {reminder_str:<12} {tags_str:<15} {todo.description}")

    def add_tag(self, todo_id: int, tag: str):
        success = self.service.add_tag_to_todo(todo_id, tag)
        if success:
            print(f"Added tag '{tag}' to todo {todo_id}")
        else:
            print(f"Failed to add tag '{tag}' to todo {todo_id} (todo not found or tag already exists)")

    def remove_tag(self, todo_id: int, tag: str):
        success = self.service.remove_tag_from_todo(todo_id, tag)
        if success:
            print(f"Removed tag '{tag}' from todo {todo_id}")
        else:
            print(f"Failed to remove tag '{tag}' from todo {todo_id} (todo not found or tag doesn't exist)")

    def set_priority(self, todo_id: int, priority: str):
        todo = self.service.update_priority(todo_id, priority)
        if todo:
            print(f"Updated priority of todo {todo.id} to {todo.priority}")
        else:
            print(f"Failed to update priority. Priority must be one of: high, medium, low")

    def recurring(self, description: str, priority: str = "medium", tags: List[str] = None, due_date: str = None,
                  recurrence_pattern: str = "daily", recurrence_end_date: str = None):
        """Create a recurring task."""
        # Parse due_date if provided
        due_date_obj = None
        if due_date:
            try:
                due_date_obj = datetime.fromisoformat(due_date)
            except ValueError:
                print(f"Warning: Invalid date format for due date: {due_date}. Expected ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS).")
                return

        # Parse recurrence_end_date if provided
        recurrence_end_date_obj = None
        if recurrence_end_date:
            try:
                recurrence_end_date_obj = datetime.fromisoformat(recurrence_end_date)
            except ValueError:
                print(f"Warning: Invalid date format for recurrence end date: {recurrence_end_date}. Expected ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS).")
                return

        todo = self.service.create_recurring_task(
            description, priority, tags or [], due_date_obj, recurrence_pattern, recurrence_end_date_obj
        )
        print(f"Created recurring task: {todo.id} - {todo.description}")
        print(f"  Pattern: {recurrence_pattern}")
        if todo.due_date:
            print(f"  Due: {todo.due_date.strftime('%Y-%m-%d %H:%M:%S')}")
        if todo.recurrence_end_date:
            print(f"  Ends: {todo.recurrence_end_date.strftime('%Y-%m-%d %H:%M:%S')}")
        if todo.tags:
            print(f"  Tags: {', '.join(todo.tags)}")

    def cancel_recurring(self, todo_id: int):
        """Cancel a recurring task."""
        success = self.service.cancel_recurring_task(todo_id)
        if success:
            print(f"Cancelled recurring task {todo_id}")
        else:
            print(f"Failed to cancel recurring task {todo_id} (not found or not a recurring task)")

    def reminder(self, todo_id: int, reminder_time: str):
        """Set a reminder for a todo."""
        # Parse reminder_time
        try:
            reminder_time_obj = datetime.fromisoformat(reminder_time)
        except ValueError:
            print(f"Warning: Invalid date format for reminder time: {reminder_time}. Expected ISO format (YYYY-MM-DDTHH:MM:SS).")
            return

        todo = self.service.update_todo(todo_id, reminder_time=reminder_time_obj)
        if todo:
            print(f"Set reminder for todo {todo.id} - {todo.description}")
            print(f"  Reminder: {todo.reminder_time.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"Todo with id {todo_id} not found.")

    def snooze_reminder(self, todo_id: int, minutes: int = 5):
        """Snooze a reminder."""
        success = self.service.snooze_reminder(todo_id, minutes)
        if success:
            print(f"Snoozed reminder for todo {todo_id} for {minutes} minutes")
        else:
            print(f"Failed to snooze reminder for todo {todo_id} (not found or no reminder set)")

    def schedule(self):
        """View scheduled tasks and reminders."""
        todos = self.service.get_all_todos()
        recurring_todos = [t for t in todos if t.recurrence_pattern != "none" and not t.completed]
        reminder_todos = [t for t in todos if t.reminder_time and not t.completed]

        print("Scheduled recurring tasks:")
        if recurring_todos:
            for todo in recurring_todos:
                print(f"  {todo.id} - {todo.description} ({todo.recurrence_pattern} until {todo.recurrence_end_date.strftime('%Y-%m-%d') if todo.recurrence_end_date else 'forever'})")
        else:
            print("  None")

        print("\nScheduled reminders:")
        if reminder_todos:
            for todo in reminder_todos:
                print(f"  {todo.id} - {todo.description} (at {todo.reminder_time.strftime('%Y-%m-%d %H:%M:%S')})")
        else:
            print("  None")
