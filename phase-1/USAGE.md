# Todo CLI Application - User Guide

## Overview
A command-line interface application for managing todos with full CRUD operations using persistent file-based storage.

## Installation
First, install the application in development mode to make the `todo` command available system-wide:

```bash
pip install -e .
```

## Basic Usage

### Adding a Todo
```bash
todo add "Your todo description here"
```
Example:
```bash
todo add "Buy groceries"
```

### Listing Todos
```bash
todo list
```
This will show all todos with their status:
- `[O]` indicates an open (incomplete) todo
- `[X]` indicates a completed todo

### Updating a Todo
```bash
todo update <todo_id> "Your updated description here"
```
Example:
```bash
todo update 1 "Updated grocery list"
```

### Marking a Todo as Complete
```bash
todo complete <todo_id>
```
Example:
```bash
todo complete 1
```

### Deleting a Todo
```bash
todo delete <todo_id>
```
Example:
```bash
todo delete 1
```

### Getting Help
```bash
todo --help
```

## Data Storage
Todos are stored in a `todos.json` file in your current working directory. This file is created automatically when you add your first todo and persists between sessions.

## Project Structure
The application follows a spec-driven development approach with the following structure:
- `specs/todo-cli/` - Feature specifications, plans, and tasks
- `src/todo_cli/` - Source code (models, services, commands)
- `tests/` - Unit and integration tests
- `.specify/` - Spec-driven development artifacts

## Development
If you want to run tests or develop the application:
```bash
# Run all tests
python -m unittest discover -s tests -p "test_*.py"

# Run specific test
python -m unittest tests.unit.test_todo -v
```

## Troubleshooting
- If you get a "command not found" error, make sure you ran `pip install -e .`
- If todos aren't persisting, check if the `todos.json` file has the correct permissions
- To reset all todos, simply delete the `todos.json` file

## Features
- ✅ Add new todos
- ✅ List all todos with completion status
- ✅ Update existing todos
- ✅ Delete todos
- ✅ Mark todos as complete
- ✅ Persistent storage using JSON file
- ✅ Command-line interface with intuitive commands
- ✅ Comprehensive test suite

## History and Development Artifacts
- Specifications: `specs/todo-cli/spec.md`
- Implementation Plan: `specs/todo-cli/plan.md`
- Development Tasks: `specs/todo-cli/tasks.md`
- Architecture Decisions: `history/adr/`
- Prompt History Records: `history/prompts/`