import unittest
from io import StringIO
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from src.todo_cli.commands.cli_commands import CLICommands
from src.todo_cli.services.todo_service import TodoService


class TestCLICommands(unittest.TestCase):
    def setUp(self):
        self.service = TodoService()
        self.commands = CLICommands(self.service)

    def test_add_command(self):
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        self.commands.add("Test todo")
        
        # Reset redirect
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue().strip()
        self.assertIn("Added todo", output)

    def test_list_command(self):
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        self.service.create_todo("Test todo")
        self.commands.list()
        
        # Reset redirect
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue().strip()
        self.assertIn("Test todo", output)
