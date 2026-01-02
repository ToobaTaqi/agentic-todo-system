import json
import os
from typing import List, Optional
from todo_cli.models.todo import Todo


class TodoService:
    def __init__(self, storage_file="todos.json"):
        self.storage_file = storage_file
        self.todos: List[Todo] = []
        self.next_id = 1
        self.load_from_file()

    def create_todo(self, description: str) -> Todo:
        todo = Todo(id=self.next_id, description=description)
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

    def update_todo(self, todo_id: int, description: str = None, completed: bool = None) -> Optional[Todo]:
        todo = self.get_todo_by_id(todo_id)
        if todo:
            if description is not None:
                todo.description = description
            if completed is not None:
                todo.completed = completed
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
                'created_at': todo.created_at.isoformat() if todo.created_at else None
            })

        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump(todos_data, f, indent=2)

    def load_from_file(self):
        """Load todos from the storage file."""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    todos_data = json.load(f)

                from datetime import datetime
                self.todos = []
                max_id = 0

                for todo_data in todos_data:
                    created_at = datetime.fromisoformat(todo_data['created_at']) if todo_data['created_at'] else None
                    todo = Todo(
                        id=todo_data['id'],
                        description=todo_data['description'],
                        completed=todo_data['completed'],
                        created_at=created_at
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
