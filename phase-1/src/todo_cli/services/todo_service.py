import json
import os
from typing import List, Optional
from todo_cli.models.todo import Todo
from datetime import datetime, timedelta
import threading
import time


class TodoService:
    def __init__(self, storage_file="todos.json"):
        self.storage_file = storage_file
        self.todos: List[Todo] = []
        self.next_id = 1
        self.load_from_file()
        # Start background scheduler thread
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.scheduler_thread.start()

    def create_todo(self, description: str, priority: str = "medium", tags: List[str] = None, due_date: datetime = None,
                    recurrence_pattern: str = "none", recurrence_end_date: datetime = None,
                    reminder_time: datetime = None) -> Todo:
        if tags is None:
            tags = []
        todo = Todo(
            id=self.next_id,
            description=description,
            priority=priority,
            tags=tags,
            due_date=due_date,
            recurrence_pattern=recurrence_pattern,
            recurrence_end_date=recurrence_end_date,
            reminder_time=reminder_time
        )
        self.todos.append(todo)
        self.next_id += 1
        self.save_to_file()
        return todo

    def get_all_todos(self) -> List[Todo]:
        return self.todos

    def get_todo_by_id(self, todo_id: int) -> Optional[Todo]:
        for todo in self.todos:
            if todo.id == todo_id:
                return todo
        return None

    def update_todo(self, todo_id: int, description: str = None, completed: bool = None, priority: str = None,
                    tags: List[str] = None, due_date: datetime = None, recurrence_pattern: str = None,
                    recurrence_end_date: datetime = None, reminder_time: datetime = None,
                    reminder_snoozed_until: datetime = None, parent_task_id: int = None) -> Optional[Todo]:
        todo = self.get_todo_by_id(todo_id)
        if todo:
            if description is not None:
                todo.description = description
            if completed is not None:
                todo.completed = completed
            if priority is not None:
                todo.priority = priority
            if tags is not None:
                todo.tags = tags
            if due_date is not None:
                todo.due_date = due_date
            if recurrence_pattern is not None:
                todo.recurrence_pattern = recurrence_pattern
            if recurrence_end_date is not None:
                todo.recurrence_end_date = recurrence_end_date
            if reminder_time is not None:
                todo.reminder_time = reminder_time
            if reminder_snoozed_until is not None:
                todo.reminder_snoozed_until = reminder_snoozed_until
            if parent_task_id is not None:
                todo.parent_task_id = parent_task_id
            self.save_to_file()
            return todo
        return None

    def delete_todo(self, todo_id: int) -> bool:
        todo = self.get_todo_by_id(todo_id)
        if todo:
            self.todos.remove(todo)
            self.save_to_file()
            return True
        return False

    def mark_complete(self, todo_id: int) -> Optional[Todo]:
        return self.update_todo(todo_id, completed=True)

    def search_todos(self, keyword: str) -> List[Todo]:
        """Search todos by keyword in description and tags."""
        keyword_lower = keyword.lower()
        matching_todos = []

        for todo in self.todos:
            # Search in description
            if keyword_lower in todo.description.lower():
                matching_todos.append(todo)
            # Search in tags
            elif any(keyword_lower in tag.lower() for tag in todo.tags):
                matching_todos.append(todo)

        return matching_todos

    def filter_todos(self, status: str = None, priority: str = None, due_date: str = None, tag: str = None) -> List[Todo]:
        """Filter todos by status, priority, due date, or tag."""
        filtered_todos = self.todos

        if status is not None:
            if status.lower() == "completed":
                filtered_todos = [todo for todo in filtered_todos if todo.completed]
            elif status.lower() == "pending":
                filtered_todos = [todo for todo in filtered_todos if not todo.completed]

        if priority is not None:
            filtered_todos = [todo for todo in filtered_todos if todo.priority.lower() == priority.lower()]

        if due_date is not None:
            # Parse due_date string to date object for comparison
            try:
                date_obj = datetime.fromisoformat(due_date.replace("Z", "+00:00")) if due_date.endswith("Z") else datetime.fromisoformat(due_date)
                filtered_todos = [todo for todo in filtered_todos if todo.due_date and todo.due_date.date() == date_obj.date()]
            except ValueError:
                # If date format is invalid, continue without date filtering
                pass

        if tag is not None:
            filtered_todos = [todo for todo in filtered_todos if tag.lower() in [t.lower() for t in todo.tags]]

        return filtered_todos

    def sort_todos(self, sort_by: str = "id", order: str = "asc") -> List[Todo]:
        """Sort todos by id, priority, due_date, or alphabetically by description."""
        reverse = order.lower() == "desc"

        if sort_by.lower() == "priority":
            # Define priority order: high > medium > low
            priority_order = {"high": 3, "medium": 2, "low": 1}
            sorted_todos = sorted(self.todos, key=lambda t: priority_order.get(t.priority, 0), reverse=reverse)
        elif sort_by.lower() == "due_date":
            sorted_todos = sorted(self.todos, key=lambda t: t.due_date or datetime.min, reverse=reverse)
        elif sort_by.lower() == "description":
            sorted_todos = sorted(self.todos, key=lambda t: t.description.lower(), reverse=reverse)
        else:  # Default sort by id
            sorted_todos = sorted(self.todos, key=lambda t: t.id, reverse=reverse)

        return sorted_todos

    def add_tag_to_todo(self, todo_id: int, tag: str) -> bool:
        """Add a tag to a specific todo."""
        todo = self.get_todo_by_id(todo_id)
        if todo and tag.lower() not in [t.lower() for t in todo.tags]:
            todo.tags.append(tag)
            self.save_to_file()
            return True
        return False

    def remove_tag_from_todo(self, todo_id: int, tag: str) -> bool:
        """Remove a tag from a specific todo."""
        todo = self.get_todo_by_id(todo_id)
        if todo:
            # Find and remove the tag (case-insensitive)
            tag_index = -1
            for i, t in enumerate(todo.tags):
                if t.lower() == tag.lower():
                    tag_index = i
                    break
            if tag_index != -1:
                todo.tags.pop(tag_index)
                self.save_to_file()
                return True
        return False

    def update_priority(self, todo_id: int, priority: str) -> Optional[Todo]:
        """Update priority of a specific todo."""
        if priority.lower() not in ["high", "medium", "low"]:
            return None
        return self.update_todo(todo_id, priority=priority)

    def create_recurring_task(self, description: str, priority: str = "medium", tags: List[str] = None,
                              due_date: datetime = None, recurrence_pattern: str = "daily",
                              recurrence_end_date: datetime = None) -> Todo:
        """Create a recurring task with specified pattern."""
        if recurrence_pattern not in ["daily", "weekly", "monthly", "yearly"]:
            raise ValueError("Invalid recurrence pattern. Must be daily, weekly, monthly, or yearly.")

        # Create the parent recurring task
        parent_todo = self.create_todo(
            description=description,
            priority=priority,
            tags=tags,
            due_date=due_date,
            recurrence_pattern=recurrence_pattern,
            recurrence_end_date=recurrence_end_date
        )
        # Mark this as a parent task by setting parent_task_id to None (it's already done by default)

        return parent_todo

    def process_recurring_tasks(self):
        """Process and generate new instances of recurring tasks."""
        current_time = datetime.now()
        new_todos = []

        for todo in self.todos:
            if todo.recurrence_pattern != "none" and not todo.completed:
                # Check if this is a parent task (not an instance of a recurring task)
                if todo.parent_task_id is None:
                    # Determine the next occurrence based on the pattern
                    should_create_new = False
                    next_occurrence = None

                    # Find the most recent occurrence of this recurring task
                    related_todos = [t for t in self.todos if t.parent_task_id == todo.id]
                    if related_todos:
                        # Get the most recent occurrence
                        latest_occurrence = max(related_todos, key=lambda t: t.created_at if t.created_at else datetime.min)
                        last_occurrence_time = latest_occurrence.due_date or latest_occurrence.created_at
                    else:
                        # If no related todos, use the parent's creation time or due date
                        last_occurrence_time = todo.due_date or todo.created_at

                    # Calculate next occurrence based on pattern
                    if todo.recurrence_pattern == "daily":
                        next_occurrence = last_occurrence_time + timedelta(days=1)
                    elif todo.recurrence_pattern == "weekly":
                        next_occurrence = last_occurrence_time + timedelta(weeks=1)
                    elif todo.recurrence_pattern == "monthly":
                        # Simple approach: add ~30 days, but for a more robust solution,
                        # we'd want to handle months with different numbers of days
                        next_occurrence = last_occurrence_time + timedelta(days=30)
                    elif todo.recurrence_pattern == "yearly":
                        next_occurrence = last_occurrence_time + timedelta(days=365)

                    # Check if we should create a new occurrence
                    if next_occurrence and next_occurrence <= current_time:
                        if todo.recurrence_end_date is None or next_occurrence <= todo.recurrence_end_date:
                            should_create_new = True

                    if should_create_new:
                        # Create a new instance of the recurring task
                        new_todo = Todo(
                            id=self.next_id,
                            description=todo.description,
                            priority=todo.priority,
                            tags=todo.tags.copy(),
                            due_date=next_occurrence if todo.due_date else None,
                            recurrence_pattern="none",  # New instance doesn't recur itself
                            parent_task_id=todo.id
                        )
                        new_todos.append(new_todo)
                        self.next_id += 1

        # Add all new recurring task instances to the list
        for new_todo in new_todos:
            self.todos.append(new_todo)

        # Save if we added new todos
        if new_todos:
            self.save_to_file()

        return len(new_todos)

    def schedule_reminders(self):
        """Schedule due date reminders for todos."""
        # This method is for manual triggering of reminder scheduling if needed
        pass

    def send_reminders(self):
        """Send notifications for due date reminders."""
        import platform
        import subprocess
        current_time = datetime.now()
        reminders_sent = []

        for todo in self.todos:
            # Check if reminder should be sent
            if (todo.reminder_time and
                not todo.completed and
                todo.reminder_time <= current_time and
                (not todo.reminder_snoozed_until or todo.reminder_snoozed_until <= current_time)):

                # Create notification message
                message = f"Reminder: '{todo.description}'"
                if todo.due_date:
                    message += f" (Due: {todo.due_date.strftime('%Y-%m-%d %H:%M')})"

                # Try to send notification based on the platform
                try:
                    if platform.system() == "Windows":
                        # For Windows, we can use PowerShell to show a notification
                        script = f'''
                        [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
                        [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null

                        $template = @"
                        <toast>
                            <visual>
                                <binding template="ToastText01">
                                    <text id="1">{message}</text>
                                </binding>
                            </visual>
                        </toast>
                        "@

                        $xml = New-Object Windows.Data.Xml.Dom.XmlDocument
                        $xml.LoadXml($template)
                        $toast = New-Object Windows.UI.Notifications.ToastNotification $xml
                        [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("TodoApp").Show($toast)
                        '''
                        subprocess.run(["powershell", "-Command", script], capture_output=True)
                    elif platform.system() == "Darwin":  # macOS
                        subprocess.run(["osascript", "-e", f'display notification "{message}" with title "Todo Reminder"'])
                    else:  # Linux and others
                        subprocess.run(["notify-send", "Todo Reminder", message])
                except Exception as e:
                    print(f"Could not send notification: {e}")

                reminders_sent.append(todo.id)

        return reminders_sent

    def snooze_reminder(self, todo_id: int, snooze_minutes: int = 5) -> bool:
        """Snooze a reminder for a specified time period."""
        todo = self.get_todo_by_id(todo_id)
        if todo and todo.reminder_time:
            snooze_time = datetime.now() + timedelta(minutes=snooze_minutes)
            todo.reminder_snoozed_until = snooze_time
            self.save_to_file()
            return True
        return False

    def cancel_recurring_task(self, todo_id: int) -> bool:
        """Cancel a recurring task pattern (stops future occurrences)."""
        todo = self.get_todo_by_id(todo_id)
        if todo and todo.recurrence_pattern != "none":
            # Simply change the recurrence pattern to "none" to stop future occurrences
            todo.recurrence_pattern = "none"
            self.save_to_file()
            return True
        return False

    def _scheduler_loop(self):
        """Background thread loop that handles recurring tasks and reminders."""
        while True:
            try:
                # Process recurring tasks
                self.process_recurring_tasks()

                # Send reminders
                self.send_reminders()

                # Sleep for a minute before the next check
                time.sleep(60)
            except Exception as e:
                print(f"Error in scheduler: {e}")
                time.sleep(60)  # Wait a minute before trying again

    def save_to_file(self):
        """Save todos to the storage file."""
        # Convert todos to a serializable format
        todos_data = []
        for todo in self.todos:
            # Convert datetime to ISO format string for JSON serialization
            todos_data.append({
                'id': todo.id,
                'description': todo.description,
                'completed': todo.completed,
                'created_at': todo.created_at.isoformat() if todo.created_at else None,
                'priority': todo.priority,
                'tags': todo.tags,
                'due_date': todo.due_date.isoformat() if todo.due_date else None,
                'recurrence_pattern': todo.recurrence_pattern,
                'recurrence_end_date': todo.recurrence_end_date.isoformat() if todo.recurrence_end_date else None,
                'reminder_time': todo.reminder_time.isoformat() if todo.reminder_time else None,
                'reminder_snoozed_until': todo.reminder_snoozed_until.isoformat() if todo.reminder_snoozed_until else None,
                'parent_task_id': todo.parent_task_id
            })

        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump(todos_data, f, indent=2)

    def load_from_file(self):
        """Load todos from the storage file."""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    todos_data = json.load(f)

                self.todos = []
                max_id = 0

                for todo_data in todos_data:
                    created_at = datetime.fromisoformat(todo_data['created_at']) if todo_data['created_at'] else None
                    due_date = datetime.fromisoformat(todo_data['due_date']) if todo_data.get('due_date') else None
                    recurrence_end_date = datetime.fromisoformat(todo_data['recurrence_end_date']) if todo_data.get('recurrence_end_date') else None
                    reminder_time = datetime.fromisoformat(todo_data['reminder_time']) if todo_data.get('reminder_time') else None
                    reminder_snoozed_until = datetime.fromisoformat(todo_data['reminder_snoozed_until']) if todo_data.get('reminder_snoozed_until') else None
                    tags = todo_data.get('tags', [])
                    priority = todo_data.get('priority', 'medium')
                    recurrence_pattern = todo_data.get('recurrence_pattern', 'none')
                    parent_task_id = todo_data.get('parent_task_id')

                    todo = Todo(
                        id=todo_data['id'],
                        description=todo_data['description'],
                        completed=todo_data['completed'],
                        created_at=created_at,
                        priority=priority,
                        tags=tags,
                        due_date=due_date,
                        recurrence_pattern=recurrence_pattern,
                        recurrence_end_date=recurrence_end_date,
                        reminder_time=reminder_time,
                        reminder_snoozed_until=reminder_snoozed_until,
                        parent_task_id=parent_task_id
                    )
                    self.todos.append(todo)
                    if todo.id > max_id:
                        max_id = todo.id

                self.next_id = max_id + 1
            except (json.JSONDecodeError, KeyError, ValueError):
                # If there's an error loading the file, start with empty list
                self.todos = []
                self.next_id = 1
        else:
            # If file doesn't exist, start with empty list
            self.todos = []
            self.next_id = 1
