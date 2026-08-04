"""
Decorator Pattern

Description:
    The Decorator Pattern is a structural design pattern that allows
    new behavior to be added to individual objects dynamically without
    modifying their original implementation.

    Instead of changing an existing class or creating numerous subclasses,
    a decorator wraps an object and forwards requests to it while adding
    additional functionality before or after the original operation.

    Multiple decorators can be stacked together, allowing behavior to be
    composed dynamically at runtime.

    Unlike inheritance, decorators provide flexibility by combining
    behaviors without creating complex class hierarchies.

Purpose:
    - Extend object behavior dynamically.
    - Avoid excessive inheritance.
    - Add cross-cutting concerns.
    - Improve code reuse.
    - Keep business logic isolated.
    - Compose behaviors at runtime.

Problem it solves:
    Imagine a service responsible for retrieving user information.

        user = service.get_user(user_id)

    Later the application requires:

        - Logging
        - Caching
        - Authorization
        - Performance monitoring
        - Metrics collection

    A common beginner solution is to place all these responsibilities
    inside the service itself.

    As more features are added, the service becomes larger and violates
    the Single Responsibility Principle.

    The Decorator Pattern solves this problem by wrapping the service
    with independent decorators.

    Every decorator adds exactly one responsibility while exposing
    the same interface as the wrapped object.

Structure:
    Component
        Defines the common interface.

    Concrete Component
        Implements the original behavior.

    Decorator
        Stores a reference to another component.

    Concrete Decorators
        Add additional responsibilities.

Workflow:
    Client
        ↓
    LoggingDecorator
        ↓
    CacheDecorator
        ↓
    AuthorizationDecorator
        ↓
    UserService

When to use:
    - Logging.
    - Caching.
    - Authentication.
    - Authorization.
    - Monitoring.
    - Metrics collection.
    - Retry policies.
    - Compression.
    - Encryption.

Advantages:
    - Adds functionality without modifying existing classes.
    - Eliminates large inheritance hierarchies.
    - Supports composition.
    - Easy to extend.
    - Follows the Open/Closed Principle.
    - Promotes the Single Responsibility Principle.

Disadvantages:
    - Many decorators may complicate debugging.
    - Execution flow becomes less obvious.
    - Too many layers may slightly affect performance.

Common backend usage:
    - Redis caching.
    - Logging.
    - Performance measurement.
    - Retry mechanisms.
    - HTTP client wrappers.
    - Security layers.
    - Compression.
    - Encryption.

Real-world frameworks:
    - Django
    - Flask
    - FastAPI
    - Spring Boot
    - ASP.NET Core
"""
from abc import ABC, abstractmethod
import random
import unittest


class UserService(ABC):

    @abstractmethod
    def get_user(self, user_id: int):
        pass


class DatabaseUserService(UserService):

    def get_user(self, user_id: int):
        return {
            "id": user_id,
            "name": f"User {user_id}"
        }


class UserServiceDecorator(UserService):

    def __init__(self, service: UserService):
        self.service = service

    def get_user(self, user_id: int):
        return self.service.get_user(user_id)


class LoggingDecorator(UserServiceDecorator):

    def __init__(self, service: UserService):
        super().__init__(service)
        self.logs = []

    def get_user(self, user_id: int):
        self.logs.append(f"User {user_id} requested")

        return super().get_user(user_id)


class CacheDecorator(UserServiceDecorator):

    def __init__(self, service: UserService):
        super().__init__(service)
        self.cache = {}

    def get_user(self, user_id: int):
        if user_id not in self.cache:
            self.cache[user_id] = super().get_user(user_id)

        return self.cache[user_id]


class DecoratorTests(unittest.TestCase):

    def test_database_service(self):
        service = DatabaseUserService()

        result = service.get_user(5)

        self.assertEqual(result["id"], 5)

    def test_logging_decorator(self):
        service = LoggingDecorator(
            DatabaseUserService()
        )

        service.get_user(10)

        self.assertEqual(
            len(service.logs),
            1
        )

    def test_cache_decorator(self):
        service = CacheDecorator(
            DatabaseUserService()
        )

        user1 = service.get_user(15)
        user2 = service.get_user(15)

        self.assertIs(
            user1,
            user2
        )

    def test_multiple_decorators(self):
        service = LoggingDecorator(
            CacheDecorator(
                DatabaseUserService()
            )
        )

        service.get_user(20)

        self.assertEqual(
            len(service.logs),
            1
        )

    def test_cache_size(self):
        service = CacheDecorator(
            DatabaseUserService()
        )

        service.get_user(1)
        service.get_user(2)
        service.get_user(1)

        self.assertEqual(
            len(service.cache),
            2
        )


class DecoratorRandomTests(unittest.TestCase):

    def test_random_cache(self):
        service = CacheDecorator(
            DatabaseUserService()
        )

        ids = [
            random.randint(1, 50)
            for _ in range(1000)
        ]

        for user_id in ids:
            service.get_user(user_id)

        self.assertLessEqual(
            len(service.cache),
            50
        )

    def test_random_logging(self):
        service = LoggingDecorator(
            DatabaseUserService()
        )

        count = random.randint(100, 500)

        for _ in range(count):
            service.get_user(
                random.randint(1, 100)
            )

        self.assertEqual(
            len(service.logs),
            count
        )

    def test_random_stacked_decorators(self):
        service = LoggingDecorator(
            CacheDecorator(
                DatabaseUserService()
            )
        )

        for _ in range(500):
            service.get_user(
                random.randint(1, 30)
            )

        self.assertGreaterEqual(
            len(service.logs),
            500
        )

        self.assertLessEqual(
            len(service.service.cache),
            30
        )


if __name__ == "__main__":
    unittest.main()
