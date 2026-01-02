# Todo CLI Application

A command-line interface application for managing todos with full CRUD operations using in-memory storage.

## Features
- Add new todos
- List all todos
- Update existing todos
- Delete todos
- Mark todos as complete

## Usage
```bash
# Add a new todo
python -m src.todo_cli.main add "My new task"

# List all todos
python -m src.todo_cli.main list

# Update a todo
python -m src.todo_cli.main update 1 "Updated task description"

# Delete a todo
python -m src.todo_cli.main delete 1

# Mark a todo as complete
python -m src.todo_cli.main complete 1
```

## Development
Run tests with:
```bash
python -m unittest discover
```

## Architecture
- Models: Todo data structure
- Services: Business logic for CRUD operations
- Commands: CLI command handlers
- Utils: Helper functions
