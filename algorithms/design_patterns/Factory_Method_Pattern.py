"""
Factory Method Pattern

Description:
    The Factory Method Pattern is a creational design pattern that
    defines an interface for creating objects while allowing subclasses
    or dedicated factory classes to decide which concrete object should
    be instantiated.

    Instead of creating objects directly using constructors throughout
    the codebase, object creation is delegated to a factory.

    This makes the application less dependent on concrete classes and
    easier to extend as new object types are introduced.

Purpose:
    - Encapsulate object creation.
    - Reduce coupling between classes.
    - Centralize initialization logic.
    - Hide implementation details.
    - Support dependency injection.
    - Simplify future extensions.

Problem it solves:
    Imagine a notification service supporting multiple providers.

        if provider == "email":
            service = EmailNotification()

        elif provider == "sms":
            service = SmsNotification()

        elif provider == "push":
            service = PushNotification()

    As more providers are added, the conditional statements grow larger
    and appear in many different places.

    The Factory Method Pattern moves object creation into one dedicated
    location. The rest of the application only asks the factory for an
    object and does not care which implementation is returned.

Structure:
    Product
        Defines the common interface.

    Concrete Products
        Different implementations of the interface.

    Factory
        Responsible for creating concrete objects.

Client
    Uses the factory instead of directly instantiating classes.

When to use:
    - Multiple implementations share one interface.
    - Object creation is complex.
    - Initialization depends on configuration.
    - Different environments require different implementations.
    - Future object types are expected.

Advantages:
    - Reduces code duplication.
    - Centralizes creation logic.
    - Easier maintenance.
    - Easier unit testing.
    - Supports Open/Closed Principle.
    - Simplifies dependency injection.

Disadvantages:
    - Introduces additional classes.
    - Can be unnecessary for very small applications.

Common backend usage:
    - Database connection factories.
    - Payment gateway selection.
    - Notification services.
    - Authentication providers.
    - Storage providers.
    - Logging implementations.
    - Cache providers.

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


class NotificationService(ABC):

    @abstractmethod
    def send(self, recipient: str, message: str):
        pass


class EmailNotification(NotificationService):

    def send(self, recipient: str, message: str):
        return f"Email sent to {recipient}: {message}"


class SmsNotification(NotificationService):

    def send(self, recipient: str, message: str):
        return f"SMS sent to {recipient}: {message}"


class PushNotification(NotificationService):

    def send(self, recipient: str, message: str):
        return f"Push notification sent to {recipient}: {message}"


class NotificationFactory:

    @staticmethod
    def create(provider: str) -> NotificationService:
        providers = {
            "email": EmailNotification,
            "sms": SmsNotification,
            "push": PushNotification
        }

        if provider not in providers:
            raise ValueError(f"Unknown provider: {provider}")

        return providers[provider]()


class FactoryMethodTests(unittest.TestCase):

    def test_create_email_notification(self):
        service = NotificationFactory.create("email")

        self.assertIsInstance(service, EmailNotification)

    def test_create_sms_notification(self):
        service = NotificationFactory.create("sms")

        self.assertIsInstance(service, SmsNotification)

    def test_create_push_notification(self):
        service = NotificationFactory.create("push")

        self.assertIsInstance(service, PushNotification)

    def test_send_email(self):
        service = NotificationFactory.create("email")

        result = service.send(
            "john@example.com",
            "Hello!"
        )

        self.assertEqual(
            result,
            "Email sent to john@example.com: Hello!"
        )

    def test_unknown_provider(self):
        with self.assertRaises(ValueError):
            NotificationFactory.create("discord")


class FactoryMethodRandomTests(unittest.TestCase):

    def random_provider(self):
        return random.choice([
            "email",
            "sms",
            "push"
        ])

    def random_recipient(self):
        username = "".join(
            random.choice(string.ascii_lowercase)
            for _ in range(8)
        )

        return f"{username}@example.com"

    def random_message(self):
        length = random.randint(5, 30)

        return "".join(
            random.choice(string.ascii_letters)
            for _ in range(length)
        )

    def test_random_factory_creation(self):
        for _ in range(500):
            provider = self.random_provider()

            service = NotificationFactory.create(provider)

            self.assertIsInstance(
                service,
                NotificationService
            )

    def test_random_notifications(self):
        for _ in range(500):
            provider = self.random_provider()

            service = NotificationFactory.create(provider)

            result = service.send(
                self.random_recipient(),
                self.random_message()
            )

            self.assertIsInstance(result, str)
            self.assertGreater(len(result), 0)

    def test_random_invalid_provider(self):
        invalid = [
            "ftp",
            "discord",
            "telegram",
            "carrier_pigeon",
            "unknown"
        ]

        for provider in invalid:
            with self.assertRaises(ValueError):
                NotificationFactory.create(provider)


if __name__ == "__main__":
    unittest.main()
