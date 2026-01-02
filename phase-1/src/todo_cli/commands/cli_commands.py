import argparse
import sys
import os
from pathlib import Path
from typing import List

# Add the src directory to Python path for imports when running as module
if __name__ == "__main__" and __package__ is None:
    # Add the project root directory to sys.path
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from todo_cli.services.todo_service import TodoService
from todo_cli.models.todo import Todo


class CLICommands:
    def __init__(self, service: TodoService):
        self.service = service

    def add(self, description: str):
        todo = self.service.create_todo(description)
        print(f"Added todo: {todo.id} - {todo.description}")

    def list(self):
        todos = self.service.get_all_todos()
        if not todos:
            print("No todos found.")
        else:
            for todo in todos:
                status = "X" if todo.completed else "O"
                print(f"{todo.id} [{status}] {todo.description}")

    def update(self, todo_id: int, description: str):
        todo = self.service.update_todo(todo_id, description=description)
        if todo:
            print(f"Updated todo: {todo.id} - {todo.description}")
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
