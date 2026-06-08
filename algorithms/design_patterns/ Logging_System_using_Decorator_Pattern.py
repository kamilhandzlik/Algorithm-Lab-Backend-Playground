"""
Problem: Logging System using Decorator Pattern

Category:
- Design Patterns
- Decorator Pattern
- Logging
- Monitoring

Description:
This project implements a simple logging system using
the Decorator design pattern.

The Decorator Pattern allows behavior to be added to
objects dynamically without modifying their original code.

In this example:
- a logger decorator wraps service methods
- every method call is automatically logged
- business logic remains unchanged

This pattern is commonly used in:
- API request logging
- monitoring systems
- auditing
- performance tracking
- middleware frameworks

Features:
- automatic logging
- non-intrusive implementation
- reusable decorators
- execution monitoring

Time Complexity:
- Method call: O(1)

Space Complexity:
- O(n)
"""

import unittest
import random
import functools


def logger(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        wrapper.logs.append(
            f"Called: {func.__name__}"
        )

        return func(*args, **kwargs)

    wrapper.logs = []

    return wrapper


class UserService:

    @logger
    def create_user(self, username):

        return f"User {username} created"

    @logger
    def delete_user(self, username):

        return f"User {username} deleted"


class TestDecoratorPattern(unittest.TestCase):

    def test_create_user(self):

        service = UserService()

        result = service.create_user(
            "Kamil"
        )

        self.assertEqual(
            result,
            "User Kamil created"
        )

    def test_delete_user(self):

        service = UserService()

        result = service.delete_user(
            "John"
        )

        self.assertEqual(
            result,
            "User John deleted"
        )

    def test_create_user_log(self):

        service = UserService()

        service.create_user(
            "Alice"
        )

        self.assertIn(
            "Called: create_user",
            service.create_user.logs
        )

    def test_delete_user_log(self):

        service = UserService()

        service.delete_user(
            "Bob"
        )

        self.assertIn(
            "Called: delete_user",
            service.delete_user.logs
        )


class TestRandom(unittest.TestCase):

    def test_random_users(self):

        service = UserService()

        usernames = []

        for i in range(50):

            username = (
                f"user_"
                f"{random.randint(1, 10000)}"
            )

            usernames.append(
                username
            )

            result = service.create_user(
                username
            )

            self.assertEqual(
                result,
                f"User {username} created"
            )

        self.assertGreaterEqual(
            len(service.create_user.logs),
            50
        )


if __name__ == "__main__":

    unittest.main()