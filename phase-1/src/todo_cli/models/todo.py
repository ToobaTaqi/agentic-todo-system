from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Todo:
    id: int
    description: str
    completed: bool = False
    created_at: datetime = None
    priority: str = "medium"  # high, medium, low
    tags: List[str] = None   # List of tags for categorization
    due_date: datetime = None  # Optional due date
    recurrence_pattern: str = "none"  # none, daily, weekly, monthly, yearly
    recurrence_end_date: datetime = None  # Optional end date for recurrence
    reminder_time: datetime = None  # Time to send reminder
    reminder_snoozed_until: datetime = None  # Time when snoozed reminder should fire
    parent_task_id: int = None  # For recurring tasks - links to parent recurring task

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.tags is None:
            self.tags = []
        if self.priority not in ["high", "medium", "low"]:
            self.priority = "medium"  # Default to medium if invalid priority
        if self.recurrence_pattern not in ["none", "daily", "weekly", "monthly", "yearly"]:
            self.recurrence_pattern = "none"  # Default to none if invalid pattern
