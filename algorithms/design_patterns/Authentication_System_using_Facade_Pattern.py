"""
Problem: Authentication System using Facade Pattern

Category:
- Design Patterns
- Facade Pattern
- Authentication
- System Simplification

Description:
This project implements a simple authentication system
using the Facade design pattern.

The Facade Pattern provides a simplified interface
to a complex subsystem.

In this example, the authentication process combines:
- user validation
- password verification
- token generation

Instead of interacting with multiple classes directly,
the client communicates only with the AuthenticationFacade.

This pattern is commonly used in:
- backend authentication systems
- API gateways
- payment systems
- microservices
- complex service orchestration

Features:
- simplified authentication workflow
- centralized access logic
- decoupled subsystems
- reusable authentication interface

Time Complexity:
- Login process: O(1)

Space Complexity:
- O(n)
"""

import unittest
import random
import string


class UserDatabase:

    def __init__(self):

        self.users = {
            "admin": "password123",
            "user": "secret"
        }

    def validate_user(
        self,
        username,
        password
    ):

        return (
            self.users.get(username)
            == password
        )


class TokenService:

    def generate_token(
        self,
        username
    ):

        return f"token_{username}"


class AuthenticationFacade:

    def __init__(self):

        self.database = UserDatabase()
        self.token_service = TokenService()

    def login(
        self,
        username,
        password
    ):

        if self.database.validate_user(
            username,
            password
        ):

            return self.token_service.generate_token(
                username
            )

        return None


class TestFacadePattern(unittest.TestCase):

    def test_valid_login(self):

        auth = AuthenticationFacade()

        token = auth.login(
            "admin",
            "password123"
        )

        self.assertEqual(
            token,
            "token_admin"
        )

    def test_invalid_login(self):

        auth = AuthenticationFacade()

        token = auth.login(
            "admin",
            "wrong_password"
        )

        self.assertIsNone(
            token
        )

    def test_unknown_user(self):

        auth = AuthenticationFacade()

        token = auth.login(
            "ghost",
            "123"
        )

        self.assertIsNone(
            token
        )


class TestRandom(unittest.TestCase):

    def random_string(self):

        length = random.randint(5, 10)

        return ''.join(
            random.choice(
                string.ascii_lowercase
            )
            for _ in range(length)
        )

    def test_random_invalid_logins(self):

        auth = AuthenticationFacade()

        for _ in range(50):

            username = self.random_string()
            password = self.random_string()

            token = auth.login(
                username,
                password
            )

            self.assertIsNone(
                token
            )


if __name__ == "__main__":

    unittest.main()