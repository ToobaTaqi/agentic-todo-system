#!/usr/bin/env python3
"""
Todo CLI Application - Main Entry Point
"""
import argparse
import sys
import os
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from src.todo_cli.commands.cli_commands import CLICommands
from src.todo_cli.services.todo_service import TodoService


def main():
    service = TodoService()
    commands = CLICommands(service)

    parser = argparse.ArgumentParser(description="Todo CLI Application")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new todo")
    add_parser.add_argument("description", help="Description of the todo")

    # List command
    list_parser = subparsers.add_parser("list", help="List all todos")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update a todo")
    update_parser.add_argument("id", type=int, help="ID of the todo to update")
    update_parser.add_argument("description", help="New description of the todo")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a todo")
    delete_parser.add_argument("id", type=int, help="ID of the todo to delete")

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark a todo as complete")
    complete_parser.add_argument("id", type=int, help="ID of the todo to mark complete")

    args = parser.parse_args()

    if args.command == "add":
        commands.add(args.description)
    elif args.command == "list":
        commands.list()
    elif args.command == "update":
        commands.update(args.id, args.description)
    elif args.command == "delete":
        commands.delete(args.id)
    elif args.command == "complete":
        commands.complete(args.id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()