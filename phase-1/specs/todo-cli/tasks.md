# Todo CLI Development Tasks

## Phase 1: Enhanced Model
- [ ] Update Todo model with priority field (high/medium/low) (DONE)
- [ ] Add tags field to Todo model (List[str]) (DONE)
- [ ] Add due_date field to Todo model (datetime) (DONE)
- [ ] Add validation for priority values (DONE)
- [ ] Update Todo model initialization with new fields (DONE)
- [ ] Write unit tests for enhanced Todo model (DONE)
- [ ] Add recurrence_pattern field to Todo model (none, daily, weekly, monthly, yearly)
- [ ] Add recurrence_end_date field to Todo model (datetime)
- [ ] Add reminder_time field to Todo model (datetime)
- [ ] Add reminder_snoozed_until field to Todo model (datetime)
- [ ] Add parent_task_id field to Todo model (int)
- [ ] Update Todo model validation for new recurrence and reminder fields
- [ ] Write unit tests for recurrence and reminder functionality

## Phase 2: Enhanced Service Layer
- [ ] Update TodoService to handle new fields in save/load (DONE)
- [ ] Implement search_todos method (keyword search) (DONE)
- [ ] Implement filter_todos method (by status, priority, date) (DONE)
- [ ] Implement sort_todos method (by due date, priority, alpha) (DONE)
- [ ] Implement add_tag_to_todo method (DONE)
- [ ] Implement remove_tag_from_todo method (DONE)
- [ ] Implement update_priority method (DONE)
- [ ] Write unit tests for new service methods (DONE)
- [ ] Implement create_recurring_task method
- [ ] Implement process_recurring_tasks method
- [ ] Implement schedule_reminders method
- [ ] Implement send_reminders method
- [ ] Implement snooze_reminder method
- [ ] Implement cancel_recurring_task method
- [ ] Update save_to_file and load_from_file for new fields
- [ ] Write unit tests for new recurrence and reminder methods

## Phase 3: Background Scheduler
- [ ] Create scheduler module for recurring tasks
- [ ] Create scheduler module for reminders
- [ ] Implement background task processor
- [ ] Add scheduler startup/shutdown functionality
- [ ] Test scheduler reliability and persistence

## Phase 4: New CLI Commands
- [ ] Create search command handler (DONE)
- [ ] Create filter command handler (DONE)
- [ ] Create sort command handler (DONE)
- [ ] Create tag command handler (DONE)
- [ ] Create priority command handler (DONE)
- [ ] Update existing commands to handle new fields (DONE)
- [ ] Add help documentation for new commands (DONE)
- [ ] Create recurring command handler
- [ ] Create reminder command handler
- [ ] Create schedule command handler
- [ ] Add argument parsing for recurrence patterns
- [ ] Add argument parsing for reminder settings

## Phase 5: Integration and Testing
- [ ] Write integration tests for new CLI commands (DONE)
- [ ] Update existing integration tests to handle new features (DONE)
- [ ] Test data persistence with new fields (DONE)
- [ ] Verify backward compatibility with existing todos (DONE)
- [ ] Run all tests and fix any issues (DONE)
- [ ] Test recurring task functionality
- [ ] Test reminder functionality
- [ ] Test scheduler integration

## Phase 6: Finalization
- [ ] Update main.py with new command parsers (DONE)
- [ ] Add error handling for new features (DONE)
- [ ] Update help documentation (DONE)
- [ ] Create/update examples and usage documentation (DONE)
- [ ] Run full test suite (DONE)
- [ ] Update USAGE.md with new features
- [ ] Document scheduler setup and requirements
