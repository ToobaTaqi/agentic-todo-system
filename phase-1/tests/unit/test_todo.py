import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from src.todo_cli.models.todo import Todo


class TestTodoModel(unittest.TestCase):
    def test_todo_creation(self):
        todo = Todo(id=1, description="Test todo")
        self.assertEqual(todo.id, 1)
        self.assertEqual(todo.description, "Test todo")
        self.assertFalse(todo.completed)

    def test_todo_completion(self):
        todo = Todo(id=1, description="Test todo", completed=True)
        self.assertTrue(todo.completed)
