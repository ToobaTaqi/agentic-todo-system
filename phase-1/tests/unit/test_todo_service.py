import unittest
import sys
import os
import tempfile
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from src.todo_cli.services.todo_service import TodoService


class TestTodoService(unittest.TestCase):
    def setUp(self):
        # Use a temporary file for tests to avoid conflicts
        self.test_storage_file = "test_todos.json"
        # Clear the test file before each test
        if os.path.exists(self.test_storage_file):
            os.remove(self.test_storage_file)
        self.service = TodoService(storage_file=self.test_storage_file)

    def test_create_todo(self):
        todo = self.service.create_todo("Test description")
        self.assertEqual(todo.description, "Test description")
        self.assertEqual(todo.id, 1)

    def test_get_all_todos(self):
        self.service.create_todo("First todo")
        self.service.create_todo("Second todo")
        todos = self.service.get_all_todos()
        self.assertEqual(len(todos), 2)

    def test_get_todo_by_id(self):
        created_todo = self.service.create_todo("Test todo")
        retrieved_todo = self.service.get_todo_by_id(created_todo.id)
        self.assertEqual(retrieved_todo.id, created_todo.id)
        self.assertEqual(retrieved_todo.description, created_todo.description)

    def test_update_todo(self):
        todo = self.service.create_todo("Original description")
        updated_todo = self.service.update_todo(todo.id, description="Updated description")
        self.assertEqual(updated_todo.description, "Updated description")

    def test_delete_todo(self):
        todo = self.service.create_todo("Test todo")
        result = self.service.delete_todo(todo.id)
        self.assertTrue(result)
        self.assertIsNone(self.service.get_todo_by_id(todo.id))
