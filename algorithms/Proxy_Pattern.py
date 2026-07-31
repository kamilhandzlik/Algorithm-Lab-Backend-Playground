"""
Proxy Pattern

Description:
    The Proxy Pattern is a structural design pattern that provides
    a placeholder or surrogate object that controls access to another
    object.

    Instead of communicating with the real object directly, clients
    interact with the proxy. The proxy decides whether the request
    should be forwarded, delayed, cached, logged or rejected.

    From the client's perspective, the proxy behaves exactly like
    the original object because both expose the same interface.

Purpose:
    - Control access to objects.
    - Delay expensive object creation.
    - Cache frequently requested data.
    - Add logging without modifying business logic.
    - Perform authorization checks.
    - Hide remote communication.
    - Improve performance.

Problem it solves:
    Imagine an application that retrieves user profiles from an
    external REST API.

    Every request takes several hundred milliseconds because it
    requires a network call.

    If the same profile is requested repeatedly, the application
    performs unnecessary HTTP requests.

    A proxy can cache previously retrieved objects and return
    cached results instead of calling the remote service every time.

    The business logic remains completely unaware that caching
    even exists.

Structure:
    Subject
        Declares the common interface shared by the real object
        and the proxy.

    Real Subject
        Performs the actual work.

    Proxy
        Stores a reference to the real subject and controls access
        to it.

    Client
        Works only with the Subject interface.

Types of Proxy:
    - Virtual Proxy
        Delays object creation until necessary.

    - Protection Proxy
        Performs authorization before forwarding requests.

    - Remote Proxy
        Represents an object located on another machine.

    - Caching Proxy
        Stores results of expensive operations.

    - Logging Proxy
        Records every request.

When to use:
    - Expensive database queries.
    - REST API communication.
    - File systems.
    - Authentication.
    - Authorization.
    - Lazy loading.
    - Distributed systems.
    - Caching.

Advantages:
    - Improves performance.
    - Adds new behavior transparently.
    - Separates infrastructure from business logic.
    - Reduces duplicated code.
    - Supports the Open/Closed Principle.
    - Simplifies monitoring.

Disadvantages:
    - Adds another abstraction layer.
    - Can make debugging slightly harder.
    - Poorly designed proxies may hide performance problems.

Common backend usage:
    - ORM lazy loading.
    - Redis caching.
    - HTTP client wrappers.
    - Authentication middleware.
    - Reverse proxies.
    - API Gateways.
    - CDN services.

Real-world frameworks:
    - Django
    - FastAPI
    - Flask
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


class CachedUserService(UserService):

    def __init__(self, service: UserService):
        self.service = service
        self.cache = {}

    def get_user(self, user_id: int):
        if user_id not in self.cache:
            self.cache[user_id] = self.service.get_user(user_id)

        return self.cache[user_id]


class UserController:

    def __init__(self, service: UserService):
        self.service = service

    def get_profile(self, user_id: int):
        return self.service.get_user(user_id)


class ProxyTests(unittest.TestCase):

    def setUp(self):
        database = DatabaseUserService()
        cache = CachedUserService(database)

        self.controller = UserController(cache)

    def test_get_existing_user(self):
        user = self.controller.get_profile(10)

        self.assertEqual(user["id"], 10)
        self.assertEqual(user["name"], "User 10")

    def test_cache_returns_same_object(self):
        user1 = self.controller.get_profile(5)
        user2 = self.controller.get_profile(5)

        self.assertIs(user1, user2)

    def test_different_users(self):
        user1 = self.controller.get_profile(1)
        user2 = self.controller.get_profile(2)

        self.assertNotEqual(user1, user2)

    def test_cache_size(self):
        self.controller.get_profile(1)
        self.controller.get_profile(2)
        self.controller.get_profile(1)

        cache = self.controller.service.cache

        self.assertEqual(len(cache), 2)

    def test_service_type(self):
        self.assertIsInstance(
            self.controller.service,
            UserService
        )


class ProxyRandomTests(unittest.TestCase):

    def test_random_requests(self):
        database = DatabaseUserService()
        cache = CachedUserService(database)

        ids = [
            random.randint(1, 50)
            for _ in range(1000)
        ]

        for user_id in ids:
            user = cache.get_user(user_id)

            self.assertEqual(user["id"], user_id)

        self.assertLessEqual(
            len(cache.cache),
            50
        )

    def test_random_cache_integrity(self):
        database = DatabaseUserService()
        cache = CachedUserService(database)

        for _ in range(500):
            user_id = random.randint(1, 100)

            user1 = cache.get_user(user_id)
            user2 = cache.get_user(user_id)

            self.assertIs(user1, user2)

    def test_random_unique_users(self):
        database = DatabaseUserService()
        cache = CachedUserService(database)

        unique_ids = set()

        for _ in range(500):
            user_id = random.randint(1, 200)

            unique_ids.add(user_id)

            cache.get_user(user_id)

        self.assertEqual(
            len(cache.cache),
            len(unique_ids)
        )


if __name__ == "__main__":
    unittest.main()
