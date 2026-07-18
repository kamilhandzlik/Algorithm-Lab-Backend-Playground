"""
Problem: Task Queue using Command Pattern

Category:
- Design Patterns
- Command Pattern
- Task Queue
- Background Jobs

Description:
This project implements a simple task queue using
the Command Pattern.

The Command Pattern encapsulates a request as an object,
allowing requests to be queued, logged or executed later.

In this example:
- Command defines the command interface
- EmailCommand sends emails
- BackupCommand performs backups
- CleanupCommand removes temporary files
- TaskQueue stores and executes commands

This pattern is commonly used in:
- task schedulers
- background workers
- GUI applications
- undo/redo systems
- job queues

Features:
- queued commands
- delayed execution
- loose coupling
- easy extensibility

Time Complexity:
- Add command: O(1)
- Execute all commands: O(n)

Space Complexity:
- O(n)
"""

import random
import unittest
from abc import ABC, abstractmethod


class Command(ABC):

    @abstractmethod
    def execute(self):
        pass


class EmailCommand(Command):

    def execute(self):
        return "Email sent"


class BackupCommand(Command):

    def execute(self):
        return "Backup completed"


class CleanupCommand(Command):

    def execute(self):
        return "Temporary files removed"


class TaskQueue:

    def __init__(self):
        self.commands = []

    def add(self, command):
        self.commands.append(command)

    def execute_all(self):
        results = []

        for command in self.commands:
            results.append(command.execute())

        self.commands.clear()

        return results


class TestCommandPattern(unittest.TestCase):

    def test_single_command(self):
        queue = TaskQueue()

        queue.add(EmailCommand())

        self.assertEqual(queue.execute_all(), ["Email sent"])

    def test_multiple_commands(self):
        queue = TaskQueue()

        queue.add(EmailCommand())
        queue.add(BackupCommand())
        queue.add(CleanupCommand())

        self.assertEqual(queue.execute_all(), ["Email sent", "Backup completed", "Temporary files removed"])

    def test_queue_is_empty_after_execution(self):
        queue = TaskQueue()

        queue.add(BackupCommand())

        queue.execute_all()

        self.assertEqual(len(queue.commands), 0)

    def test_execute_empty_queue(self):
        queue = TaskQueue()

        self.assertEqual(queue.execute_all(), [])


class TestRandom(unittest.TestCase):

    def test_random_commands(self):
        queue = TaskQueue()

        command_types = [EmailCommand, BackupCommand, CleanupCommand]

        expected = 0

        for _ in range(100):
            command = random.choice(command_types)()

            queue.add(command)

            expected += 1

        results = queue.execute_all()

        self.assertEqual(len(results), expected)


if __name__ == "__main__":
    unittest.main()
