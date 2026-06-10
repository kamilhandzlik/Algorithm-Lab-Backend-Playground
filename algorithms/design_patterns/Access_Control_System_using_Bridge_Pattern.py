"""
Problem: Access Control System using Bridge Pattern

Category:
- Design Patterns
- Bridge Pattern
- Access Control
- Authorization

Description:
This project implements an access control system using
the Bridge design pattern.

The Bridge Pattern separates an abstraction from its
implementation, allowing both to evolve independently.

In this example:
- AccessRole represents the abstraction
- AccessProvider represents the implementation
- different roles can work with different providers

This pattern is commonly used in:
- authorization systems
- cloud platforms
- payment providers
- messaging services
- device drivers

Features:
- separation of abstraction and implementation
- flexible role-provider combinations
- reduced class explosion
- scalable architecture

Time Complexity:
- Check access: O(1)

Space Complexity:
- O(1)
"""

import unittest
import random
from abc import ABC, abstractmethod


class AccessProvider(ABC):

    @abstractmethod
    def has_access(self):
        pass


class LocalProvider(AccessProvider):

    def has_access(self):

        return True


class ExternalProvider(AccessProvider):

    def has_access(self):

        return False


class AccessRole(ABC):

    def __init__(self, provider):

        self.provider = provider

    @abstractmethod
    def check_access(self):
        pass


class AdminRole(AccessRole):

    def check_access(self):

        if self.provider.has_access():

            return "Admin access granted"

        return "Admin access denied"


class UserRole(AccessRole):

    def check_access(self):

        if self.provider.has_access():

            return "User access granted"

        return "User access denied"


class TestBridgePattern(unittest.TestCase):

    def test_admin_local_provider(self):

        role = AdminRole(
            LocalProvider()
        )

        self.assertEqual(
            role.check_access(),
            "Admin access granted"
        )

    def test_admin_external_provider(self):

        role = AdminRole(
            ExternalProvider()
        )

        self.assertEqual(
            role.check_access(),
            "Admin access denied"
        )

    def test_user_local_provider(self):

        role = UserRole(
            LocalProvider()
        )

        self.assertEqual(
            role.check_access(),
            "User access granted"
        )

    def test_user_external_provider(self):

        role = UserRole(
            ExternalProvider()
        )

        self.assertEqual(
            role.check_access(),
            "User access denied"
        )


class TestRandom(unittest.TestCase):

    def test_random_access_checks(self):

        roles = [
            AdminRole,
            UserRole
        ]

        providers = [
            LocalProvider,
            ExternalProvider
        ]

        for _ in range(100):

            role_class = random.choice(
                roles
            )

            provider_class = random.choice(
                providers
            )

            role = role_class(
                provider_class()
            )

            result = role.check_access()

            self.assertIn(
                result,
                [
                    "Admin access granted",
                    "Admin access denied",
                    "User access granted",
                    "User access denied"
                ]
            )


if __name__ == "__main__":

    unittest.main()