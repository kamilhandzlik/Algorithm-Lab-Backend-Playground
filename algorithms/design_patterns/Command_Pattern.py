"""
Command Pattern

Description:
    The Command Pattern is a behavioral design pattern that converts
    a request into an object. Instead of calling methods directly,
    every operation is represented by a command object that contains
    all information required to execute the action.

    A command object typically contains:
        - The receiver (the object performing the work)
        - The action to execute
        - Any parameters required for execution

    The sender of a command does not need to know how the work is
    performed. It only knows that it can execute a command.

Purpose:
    - Encapsulate requests into standalone objects.
    - Decouple the sender from the receiver.
    - Queue operations for later execution.
    - Support logging and history of executed operations.
    - Enable undo/redo functionality.
    - Improve extensibility.

Problem it solves:
    Imagine an application where users can perform many different
    operations such as:

        - Create an account
        - Send an email
        - Generate a report
        - Export data
        - Process a payment

    A naive implementation often results in one large controller
    containing many if-elif statements.

    As the application grows, the controller becomes difficult
    to maintain.

    The Command Pattern moves every action into its own class.
    New operations can be added without modifying existing code.

Structure:
    Command
        Declares the execute() interface.

    Concrete Command
        Implements a specific operation.

    Receiver
        Performs the actual work.

    Invoker
        Stores commands and executes them.

When to use:
    - Building task queues.
    - Scheduling jobs.
    - Background processing.
    - Undo/Redo systems.
    - Event-driven applications.
    - Macro recording.
    - CQRS architectures.

Advantages:
    - Strong separation of responsibilities.
    - Very easy to extend.
    - Supports asynchronous execution.
    - Commands can be queued.
    - Commands can be logged.
    - Easy to unit test.
    - Encourages loose coupling.
    - Follows SOLID principles.

Disadvantages:
    - Introduces many small classes.
    - Slightly increases project complexity.
    - Can be overkill for simple applications.

Common backend usage:
    - Celery tasks
    - RabbitMQ consumers
    - Kafka message handlers
    - Email sending
    - File processing
    - Payment processing
    - Report generation
    - Notification systems
    - CQRS Command Handlers

Real-world frameworks:
    - Django
    - FastAPI
    - Flask
    - Spring Boot
    - ASP.NET Core
"""
from abc import ABC, abstractmethod
import random
import string
import unittest


class Command(ABC):

    @abstractmethod
    def execute(self):
        pass


class EmailService:

    def __init__(self):
        self.sent_emails = []

    def send_email(self, recipient: str, message: str):
        self.sent_emails.append((recipient, message))


class SendEmailCommand(Command):

    def __init__(self, service: EmailService, recipient: str, message: str):
        self.service = service
        self.recipient = recipient
        self.message = message

    def execute(self):
        self.service.send_email(self.recipient, self.message)


class CommandInvoker:

    def __init__(self):
        self.history = []

    def execute(self, command: Command):
        command.execute()
        self.history.append(command)


class CommandTests(unittest.TestCase):

    def setUp(self):
        self.service = EmailService()
        self.invoker = CommandInvoker()

    def test_send_single_email(self):
        command = SendEmailCommand(
            self.service,
            "john@example.com",
            "Hello"
        )

        self.invoker.execute(command)

        self.assertEqual(len(self.service.sent_emails), 1)
        self.assertEqual(
            self.service.sent_emails[0],
            ("john@example.com", "Hello")
        )

    def test_command_history(self):
        command = SendEmailCommand(
            self.service,
            "alice@example.com",
            "Welcome"
        )

        self.invoker.execute(command)

        self.assertEqual(len(self.invoker.history), 1)
        self.assertIs(self.invoker.history[0], command)

    def test_multiple_commands(self):
        for i in range(5):
            command = SendEmailCommand(
                self.service,
                f"user{i}@mail.com",
                "Test"
            )

            self.invoker.execute(command)

        self.assertEqual(len(self.service.sent_emails), 5)

    def test_empty_history(self):
        self.assertEqual(len(self.invoker.history), 0)


class CommandRandomTests(unittest.TestCase):

    def random_email(self):
        username = "".join(random.choice(string.ascii_lowercase) for _ in range(8))
        return f"{username}@example.com"

    def random_message(self):
        length = random.randint(10, 50)
        return "".join(random.choice(string.ascii_letters) for _ in range(length))

    def test_random_email_sending(self):
        service = EmailService()
        invoker = CommandInvoker()

        count = random.randint(100, 500)

        for _ in range(count):
            command = SendEmailCommand(
                service,
                self.random_email(),
                self.random_message()
            )

            invoker.execute(command)

        self.assertEqual(len(service.sent_emails), count)
        self.assertEqual(len(invoker.history), count)

    def test_random_command_execution(self):
        service = EmailService()
        invoker = CommandInvoker()

        for _ in range(300):
            recipient = self.random_email()
            message = self.random_message()

            command = SendEmailCommand(
                service,
                recipient,
                message
            )

            invoker.execute(command)

            self.assertEqual(
                service.sent_emails[-1],
                (recipient, message)
            )

    def test_random_history_integrity(self):
        service = EmailService()
        invoker = CommandInvoker()

        commands = []

        for _ in range(200):
            command = SendEmailCommand(
                service,
                self.random_email(),
                self.random_message()
            )

            commands.append(command)
            invoker.execute(command)

        self.assertEqual(len(invoker.history), len(commands))

        for expected, actual in zip(commands, invoker.history):
            self.assertIs(expected, actual)


if __name__ == "__main__":
    unittest.main()