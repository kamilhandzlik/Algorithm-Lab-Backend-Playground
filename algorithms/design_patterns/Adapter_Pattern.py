"""
Adapter Pattern

Description:
    The Adapter Pattern is a structural design pattern that allows
    incompatible interfaces to work together.

    It acts as a bridge between two classes whose interfaces differ,
    converting one interface into another expected by the client.

    The adapter wraps an existing object and translates method calls
    into a format understood by that object.

    Instead of modifying third-party code or changing the client,
    an adapter provides a compatible interface.

Purpose:
    - Connect incompatible interfaces.
    - Reuse existing code.
    - Simplify third-party integrations.
    - Isolate external libraries from business logic.
    - Improve maintainability.
    - Reduce coupling.

Problem it solves:
    Imagine an application that sends notifications.

    Initially, only one provider exists.

        notification.send(message)

    Later, another provider is introduced.

        external_api.publish(
            body=message,
            destination=user
        )

    The new provider uses a completely different API.

    Changing the existing application to support every provider
    would spread conditional logic across the codebase.

    Instead, an adapter converts the new provider into the interface
    already expected by the application.

Structure:
    Target
        Defines the interface expected by the client.

    Adaptee
        Existing class with an incompatible interface.

    Adapter
        Converts the adaptee interface into the target interface.

    Client
        Uses only the target interface.

When to use:
    - Integrating external APIs.
    - Wrapping legacy code.
    - Replacing one library with another.
    - Supporting multiple vendors.
    - Migrating between services.
    - Standardizing interfaces.

Advantages:
    - Reuses existing implementations.
    - Keeps business logic clean.
    - Makes external libraries replaceable.
    - Reduces dependencies.
    - Easier testing.
    - Easier maintenance.
    - Supports the Open/Closed Principle.

Disadvantages:
    - Adds another abstraction layer.
    - May increase the number of classes.
    - Poor adapters can hide design problems.

Common backend usage:
    - Payment gateways.
    - Cloud storage providers.
    - SMS providers.
    - Email providers.
    - External REST APIs.
    - GraphQL wrappers.
    - Legacy system integration.
    - Database migration tools.

Real-world frameworks:
    - Django
    - Flask
    - FastAPI
    - Spring Boot
    - ASP.NET Core
"""
from abc import ABC, abstractmethod
import random
import string
import unittest


class NotificationService(ABC):

    @abstractmethod
    def send(self, recipient: str, message: str):
        pass


class LegacyEmailProvider:

    def deliver(self, email: str, content: str):
        return f"Legacy email sent to {email}: {content}"


class EmailAdapter(NotificationService):

    def __init__(self, provider: LegacyEmailProvider):
        self.provider = provider

    def send(self, recipient: str, message: str):
        return self.provider.deliver(recipient, message)


class NotificationManager:

    def __init__(self, service: NotificationService):
        self.service = service

    def notify(self, recipient: str, message: str):
        return self.service.send(recipient, message)


class AdapterTests(unittest.TestCase):

    def setUp(self):
        provider = LegacyEmailProvider()
        adapter = EmailAdapter(provider)

        self.manager = NotificationManager(adapter)

    def test_send_notification(self):
        result = self.manager.notify(
            "john@example.com",
            "Hello"
        )

        self.assertEqual(
            result,
            "Legacy email sent to john@example.com: Hello"
        )

    def test_multiple_notifications(self):
        for i in range(10):
            result = self.manager.notify(
                f"user{i}@example.com",
                "Test"
            )

            self.assertIn("Legacy email sent", result)

    def test_adapter_type(self):
        provider = LegacyEmailProvider()
        adapter = EmailAdapter(provider)

        self.assertIsInstance(
            adapter,
            NotificationService
        )

    def test_provider_is_stored(self):
        provider = LegacyEmailProvider()
        adapter = EmailAdapter(provider)

        self.assertIs(adapter.provider, provider)


class AdapterRandomTests(unittest.TestCase):

    def random_email(self):
        username = "".join(
            random.choice(string.ascii_lowercase)
            for _ in range(10)
        )

        return f"{username}@example.com"

    def random_message(self):
        length = random.randint(10, 40)

        return "".join(
            random.choice(string.ascii_letters)
            for _ in range(length)
        )

    def test_random_notifications(self):
        provider = LegacyEmailProvider()
        adapter = EmailAdapter(provider)
        manager = NotificationManager(adapter)

        for _ in range(500):
            result = manager.notify(
                self.random_email(),
                self.random_message()
            )

            self.assertTrue(
                result.startswith("Legacy email sent")
            )

    def test_random_adapter_calls(self):
        provider = LegacyEmailProvider()
        adapter = EmailAdapter(provider)

        for _ in range(300):
            recipient = self.random_email()
            message = self.random_message()

            result = adapter.send(
                recipient,
                message
            )

            self.assertIn(recipient, result)
            self.assertIn(message, result)

    def test_random_provider_instances(self):
        for _ in range(100):
            provider = LegacyEmailProvider()
            adapter = EmailAdapter(provider)

            self.assertIs(adapter.provider, provider)


if __name__ == "__main__":
    unittest.main()
