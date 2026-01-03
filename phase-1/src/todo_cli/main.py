import argparse
import sys
import os
from pathlib import Path

# Add the src directory to Python path for imports when running as module
if __name__ == "__main__" and __package__ is None:
    # Add the project root directory to sys.path
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from todo_cli.commands.cli_commands import CLICommands
from todo_cli.services.todo_service import TodoService


def main():
    service = TodoService()
    commands = CLICommands(service)

    parser = argparse.ArgumentParser(description="Todo CLI Application")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new todo")
    add_parser.add_argument("description", help="Description of the todo")
    add_parser.add_argument("--priority", "-p", choices=["high", "medium", "low"], default="medium", help="Priority level (high/medium/low)")
    add_parser.add_argument("--tag", "-t", action="append", dest="tags", help="Tags for categorization (can be used multiple times)")
    add_parser.add_argument("--due-date", help="Due date in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)")
    add_parser.add_argument("--recurrence", choices=["none", "daily", "weekly", "monthly", "yearly"], default="none", help="Recurrence pattern (none/daily/weekly/monthly/yearly)")
    add_parser.add_argument("--recurrence-end", help="End date for recurrence in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)")
    add_parser.add_argument("--reminder", help="Reminder time in ISO format (YYYY-MM-DDTHH:MM:SS)")

    # List command
    list_parser = subparsers.add_parser("list", help="List all todos")
    list_parser.add_argument("--status", choices=["completed", "pending"], help="Filter by completion status")
    list_parser.add_argument("--priority", choices=["high", "medium", "low"], help="Filter by priority")
    list_parser.add_argument("--tag", help="Filter by tag")
    list_parser.add_argument("--sort", default="id", choices=["id", "priority", "due_date", "description"], help="Sort by field")
    list_parser.add_argument("--order", default="asc", choices=["asc", "desc"], help="Sort order (asc/desc)")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update a todo")
    update_parser.add_argument("id", type=int, help="ID of the todo to update")
    update_parser.add_argument("description", nargs="?", help="New description of the todo")
    update_parser.add_argument("--priority", "-p", choices=["high", "medium", "low"], help="New priority level")
    update_parser.add_argument("--tag", "-t", action="append", dest="tags", help="New tags (replaces existing tags)")
    update_parser.add_argument("--due-date", help="New due date in ISO format")
    update_parser.add_argument("--recurrence", choices=["none", "daily", "weekly", "monthly", "yearly"], help="New recurrence pattern")
    update_parser.add_argument("--recurrence-end", help="New end date for recurrence in ISO format")
    update_parser.add_argument("--reminder", help="New reminder time in ISO format")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a todo")
    delete_parser.add_argument("id", type=int, help="ID of the todo to delete")

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark a todo as complete")
    complete_parser.add_argument("id", type=int, help="ID of the todo to mark complete")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search todos by keyword")
    search_parser.add_argument("keyword", help="Keyword to search for in description and tags")

    # Filter command
    filter_parser = subparsers.add_parser("filter", help="Filter todos by criteria")
    filter_parser.add_argument("--status", choices=["completed", "pending"], help="Filter by completion status")
    filter_parser.add_argument("--priority", choices=["high", "medium", "low"], help="Filter by priority")
    filter_parser.add_argument("--due-date", help="Filter by due date")
    filter_parser.add_argument("--tag", help="Filter by tag")

    # Sort command
    sort_parser = subparsers.add_parser("sort", help="Sort todos by criteria")
    sort_parser.add_argument("--by", default="id", choices=["id", "priority", "due_date", "description"], help="Sort by field")
    sort_parser.add_argument("--order", default="asc", choices=["asc", "desc"], help="Sort order (asc/desc)")

    # Add tag command
    add_tag_parser = subparsers.add_parser("add-tag", help="Add a tag to a todo")
    add_tag_parser.add_argument("id", type=int, help="ID of the todo")
    add_tag_parser.add_argument("tag", help="Tag to add")

    # Remove tag command
    remove_tag_parser = subparsers.add_parser("remove-tag", help="Remove a tag from a todo")
    remove_tag_parser.add_argument("id", type=int, help="ID of the todo")
    remove_tag_parser.add_argument("tag", help="Tag to remove")

    # Set priority command
    priority_parser = subparsers.add_parser("priority", help="Set priority of a todo")
    priority_parser.add_argument("id", type=int, help="ID of the todo")
    priority_parser.add_argument("priority", choices=["high", "medium", "low"], help="Priority level to set")

    # Recurring task command
    recurring_parser = subparsers.add_parser("recurring", help="Create a recurring task")
    recurring_parser.add_argument("description", help="Description of the recurring task")
    recurring_parser.add_argument("--priority", "-p", choices=["high", "medium", "low"], default="medium", help="Priority level (high/medium/low)")
    recurring_parser.add_argument("--tag", "-t", action="append", dest="tags", help="Tags for categorization (can be used multiple times)")
    recurring_parser.add_argument("--due-date", help="Due date in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)")
    recurring_parser.add_argument("--pattern", choices=["daily", "weekly", "monthly", "yearly"], default="daily", help="Recurrence pattern (daily/weekly/monthly/yearly)")
    recurring_parser.add_argument("--end-date", help="End date for recurrence in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)")

    # Cancel recurring task command
    cancel_recurring_parser = subparsers.add_parser("cancel-recurring", help="Cancel a recurring task")
    cancel_recurring_parser.add_argument("id", type=int, help="ID of the recurring task to cancel")

    # Reminder command
    reminder_parser = subparsers.add_parser("reminder", help="Set a reminder for a todo")
    reminder_parser.add_argument("id", type=int, help="ID of the todo")
    reminder_parser.add_argument("time", help="Reminder time in ISO format (YYYY-MM-DDTHH:MM:SS)")

    # Snooze reminder command
    snooze_parser = subparsers.add_parser("snooze", help="Snooze a reminder")
    snooze_parser.add_argument("id", type=int, help="ID of the todo with the reminder")
    snooze_parser.add_argument("--minutes", type=int, default=5, help="Number of minutes to snooze (default: 5)")

    # Schedule command
    schedule_parser = subparsers.add_parser("schedule", help="View scheduled tasks and reminders")

    args = parser.parse_args()

    if args.command == "add":
        commands.add(args.description, args.priority, args.tags, args.due_date,
                     args.recurrence, args.recurrence_end, args.reminder)
    elif args.command == "list":
        commands.list(args.status, args.priority, args.tag, args.sort, args.order)
    elif args.command == "update":
        commands.update(args.id, args.description, args.priority, args.tags, args.due_date,
                        args.recurrence, args.recurrence_end, args.reminder)
    elif args.command == "delete":
        commands.delete(args.id)
    elif args.command == "complete":
        commands.complete(args.id)
    elif args.command == "search":
        commands.search(args.keyword)
    elif args.command == "filter":
        commands.filter(args.status, args.priority, args.due_date, args.tag)
    elif args.command == "sort":
        commands.sort(args.by, args.order)
    elif args.command == "add-tag":
        commands.add_tag(args.id, args.tag)
    elif args.command == "remove-tag":
        commands.remove_tag(args.id, args.tag)
    elif args.command == "priority":
        commands.set_priority(args.id, args.priority)
    elif args.command == "recurring":
        commands.recurring(args.description, args.priority, args.tags, args.due_date,
                           args.pattern, args.end_date)
    elif args.command == "cancel-recurring":
        commands.cancel_recurring(args.id)
    elif args.command == "reminder":
        commands.reminder(args.id, args.time)
    elif args.command == "snooze":
        commands.snooze_reminder(args.id, args.minutes)
    elif args.command == "schedule":
        commands.schedule()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
