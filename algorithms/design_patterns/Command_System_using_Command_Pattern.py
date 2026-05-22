"""
Problem: Command System using Command Pattern

Category:
- Design Patterns
- Command Pattern
- Task Execution
- Decoupled Architecture

Description:
This project implements a simple command execution system
using the Command design pattern.

The Command Pattern encapsulates actions as objects,
allowing commands to be executed dynamically and independently
from the objects that invoke them.

This pattern is commonly used in:
- task schedulers
- GUI applications
- undo/redo systems
- job queues
- automation systems

Features:
- command abstraction
- decoupled execution logic
- dynamic command execution
- reusable command objects

Time Complexity:
- Execute command: O(1)

Space Complexity:
- O(n)
"""

import unittest
import random
from abc import ABC, abstractmethod


class Command(ABC):

    @abstractmethod
    def execute(self):
        pass


class StartServerCommand(Command):

    def execute(self):

        return "Server started"


class StopServerCommand(Command):

    def execute(self):

        return "Server stopped"


class RestartServerCommand(Command):

    def execute(self):

        return "Server restarted"


class CommandExecutor:

    def __init__(self):

        self.history = []

    def run(self, command):

        result = command.execute()

        self.history.append(result)

        return result


class TestCommandPattern(unittest.TestCase):

    def test_start_command(self):

        executor = CommandExecutor()

        result = executor.run(
            StartServerCommand()
        )

        self.assertEqual(
            result,
            "Server started"
        )

    def test_stop_command(self):

        executor = CommandExecutor()

        result = executor.run(
            StopServerCommand()
        )

        self.assertEqual(
            result,
            "Server stopped"
        )

    def test_restart_command(self):

        executor = CommandExecutor()

        result = executor.run(
            RestartServerCommand()
        )

        self.assertEqual(
            result,
            "Server restarted"
        )

    def test_history(self):

        executor = CommandExecutor()

        executor.run(StartServerCommand())
        executor.run(StopServerCommand())

        self.assertEqual(
            executor.history,
            [
                "Server started",
                "Server stopped"
            ]
        )


class TestRandom(unittest.TestCase):

    def test_random_commands(self):

        executor = CommandExecutor()

        commands = [
            StartServerCommand,
            StopServerCommand,
            RestartServerCommand
        ]

        expected = []

        for _ in range(50):

            command_class = random.choice(commands)

            result = executor.run(
                command_class()
            )

            expected.append(result)

        self.assertEqual(
            executor.history,
            expected
        )


if __name__ == "__main__":

    unittest.main()