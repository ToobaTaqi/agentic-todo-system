# Todo CLI Application - User Guide

## Overview
A command-line interface application for managing todos with full CRUD operations using persistent file-based storage. The application includes advanced features like priorities, tags, search, filter, and sort capabilities.

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

### Adding a Todo with Priority, Tags, Due Date, Recurrence, and Reminders
```bash
todo add "Your todo description" --priority high --tag work --due-date 2026-12-31 --recurrence daily --reminder 2026-12-31T09:00:00
```
Example:
```bash
todo add "Complete project proposal" --priority high --tag work --due-date 2026-12-15 --recurrence weekly
```

Available recurrence patterns: `none`, `daily`, `weekly`, `monthly`, `yearly`
Example with end date for recurrence:
```bash
todo add "Daily exercise" --priority high --due-date 2026-12-31 --recurrence daily --recurrence-end 2026-12-31
```

### Listing Todos
```bash
todo list
```
This will show all todos with their status:
- `[O]` indicates an open (incomplete) todo
- `[X]` indicates a completed todo

### Listing Todos with Filters and Sorting
```bash
todo list --status pending --priority high --sort priority --order desc
```

### Updating a Todo
```bash
todo update <todo_id> "Your updated description here"
```
Example:
```bash
todo update 1 "Updated grocery list"
```

### Updating a Todo with Priority, Tags, Due Date, Recurrence, and Reminders
```bash
todo update <todo_id> --priority low --tag personal --due-date 2023-12-20 --recurrence weekly --reminder 2023-12-20T10:00:00
```
Example:
```bash
todo update 1 --priority medium --due-date 2023-12-25 --recurrence daily
```

You can also update recurrence end date:
```bash
todo update 1 --recurrence-end 2024-01-01
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

## Advanced Features

### Search Todos
Search for todos by keyword in description or tags:
```bash
todo search "keyword"
```
Example:
```bash
todo search "grocery"
```

### Filter Todos
Filter todos by various criteria:
```bash
todo filter --status completed --priority high
```
Example:
```bash
todo filter --tag work --priority medium
```

### Sort Todos
Sort todos by different criteria:
```bash
todo sort --by priority --order desc
```
Available sort options: `id`, `priority`, `due_date`, `description`
Available order options: `asc`, `desc`

### Manage Tags
Add a tag to a todo:
```bash
todo add-tag <todo_id> <tag_name>
```
Example:
```bash
todo add-tag 1 work
```

Remove a tag from a todo:
```bash
todo remove-tag <todo_id> <tag_name>
```
Example:
```bash
todo remove-tag 1 work
```

### Set Priority
Update the priority of a todo:
```bash
todo priority <todo_id> <priority_level>
```
Priority levels: `high`, `medium`, `low`
Example:
```bash
todo priority 1 high
```

### Create Recurring Tasks
Create a recurring task that repeats based on a pattern:
```bash
todo recurring "Your recurring task description" --pattern daily --priority high --tag work
```
Available recurrence patterns: `daily`, `weekly`, `monthly`, `yearly`
Example:
```bash
todo recurring "Weekly team meeting" --pattern weekly --priority medium --tag work
```

You can also specify an end date for the recurrence:
```bash
todo recurring "Daily workout" --pattern daily --end-date 2026-12-31 --priority high
```

### Cancel Recurring Tasks
Cancel a recurring task to stop it from repeating:
```bash
todo cancel-recurring <todo_id>
```
Example:
```bash
todo cancel-recurring 5
```

### Set Reminders
Set a reminder for a specific todo:
```bash
todo reminder <todo_id> <iso_datetime>
```
Example:
```bash
todo reminder 1 2026-12-15T09:00:00
```

### Snooze Reminders
Snooze a reminder for a specific number of minutes:
```bash
todo snooze <todo_id> --minutes 10
```
Default snooze time is 5 minutes if not specified:
```bash
todo snooze 1
```

### View Schedule
View all scheduled recurring tasks and reminders:
```bash
todo schedule
```
This will show:
- All recurring tasks that are active
- All scheduled reminders

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
- ✅ Priorities (high/medium/low)
- ✅ Tags for categorization
- ✅ Search functionality
- ✅ Filter functionality
- ✅ Sort functionality
- ✅ Due dates for todos
- ✅ Recurring tasks (daily, weekly, monthly, yearly)
- ✅ Reminder system with notifications
- ✅ Snooze reminders functionality
- ✅ Schedule view for recurring tasks and reminders
- ✅ Cancel recurring tasks

## History and Development Artifacts
- Specifications: `specs/todo-cli/spec.md`
- Implementation Plan: `specs/todo-cli/plan.md`
- Development Tasks: `specs/todo-cli/tasks.md`
- Architecture Decisions: `history/adr/`
- Prompt History Records: `history/prompts/`