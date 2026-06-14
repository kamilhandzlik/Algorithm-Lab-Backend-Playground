"""
Problem: Feature Toggle System using Command Pattern

Category:
- Design Patterns
- Command Pattern
- Feature Flags
- Configuration Management

Description:
This project implements a simple feature toggle system
using the Command design pattern.

The Command Pattern encapsulates actions as objects,
allowing operations to be executed, stored, and tracked
independently from the client code.

In this example:
- EnableFeatureCommand enables a feature
- DisableFeatureCommand disables a feature
- FeatureManager stores feature states
- CommandInvoker executes commands

This pattern is commonly used in:
- feature flag systems
- deployment pipelines
- CI/CD tools
- administration panels
- configuration management

Features:
- enable and disable features
- command execution history
- decoupled architecture
- centralized feature management

Time Complexity:
- Execute command: O(1)

Space Complexity:
- O(n)
"""

import unittest
import random
from abc import ABC, abstractmethod


class FeatureManager:

    def __init__(self):

        self.features = {}

    def enable(self, feature):

        self.features[feature] = True

    def disable(self, feature):

        self.features[feature] = False

    def is_enabled(self, feature):

        return self.features.get(
            feature,
            False
        )


class Command(ABC):

    @abstractmethod
    def execute(self):
        pass


class EnableFeatureCommand(Command):

    def __init__(
        self,
        manager,
        feature
    ):

        self.manager = manager
        self.feature = feature

    def execute(self):

        self.manager.enable(
            self.feature
        )


class DisableFeatureCommand(Command):

    def __init__(
        self,
        manager,
        feature
    ):

        self.manager = manager
        self.feature = feature

    def execute(self):

        self.manager.disable(
            self.feature
        )


class CommandInvoker:

    def __init__(self):

        self.history = []

    def execute(self, command):

        command.execute()

        self.history.append(
            command.__class__.__name__
        )


class TestCommandPattern(unittest.TestCase):

    def test_enable_feature(self):

        manager = FeatureManager()

        command = EnableFeatureCommand(
            manager,
            "chat"
        )

        CommandInvoker().execute(
            command
        )

        self.assertTrue(
            manager.is_enabled(
                "chat"
            )
        )

    def test_disable_feature(self):

        manager = FeatureManager()

        manager.enable("chat")

        command = DisableFeatureCommand(
            manager,
            "chat"
        )

        CommandInvoker().execute(
            command
        )

        self.assertFalse(
            manager.is_enabled(
                "chat"
            )
        )

    def test_command_history(self):

        manager = FeatureManager()

        invoker = CommandInvoker()

        invoker.execute(
            EnableFeatureCommand(
                manager,
                "payments"
            )
        )

        self.assertEqual(
            invoker.history,
            [
                "EnableFeatureCommand"
            ]
        )

    def test_multiple_commands(self):

        manager = FeatureManager()

        invoker = CommandInvoker()

        invoker.execute(
            EnableFeatureCommand(
                manager,
                "api"
            )
        )

        invoker.execute(
            DisableFeatureCommand(
                manager,
                "api"
            )
        )

        self.assertFalse(
            manager.is_enabled(
                "api"
            )
        )


class TestRandom(unittest.TestCase):

    def test_random_feature_toggles(self):

        manager = FeatureManager()

        invoker = CommandInvoker()

        features = [
            "chat",
            "payments",
            "analytics",
            "reports",
            "notifications"
        ]

        for _ in range(100):

            feature = random.choice(
                features
            )

            command = random.choice(
                [
                    EnableFeatureCommand,
                    DisableFeatureCommand
                ]
            )(
                manager,
                feature
            )

            invoker.execute(
                command
            )

        self.assertEqual(
            len(invoker.history),
            100
        )


if __name__ == "__main__":

    unittest.main()