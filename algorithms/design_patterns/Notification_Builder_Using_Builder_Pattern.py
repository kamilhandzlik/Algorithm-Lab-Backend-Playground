"""
Problem: Notification Builder using Builder Pattern

Category:
- Design Patterns
- Builder Pattern
- Notifications
- Object Construction

Description:
This project implements a notification builder using
the Builder design pattern.

The Builder Pattern separates the construction of
a complex object from its representation, allowing
different configurations using the same construction
process.

In this example:
- Notification represents the final object
- NotificationBuilder builds notifications
- clients configure only the fields they need

This pattern is commonly used in:
- HTTP request builders
- SQL query builders
- configuration objects
- email generation
- test data creation

Features:
- fluent interface
- optional fields
- readable object creation
- immutable final object

Time Complexity:
- Build object: O(1)

Space Complexity:
- O(1)
"""

import random
import string
import unittest


class Notification:

    def __init__(self, title, message, recipient, priority):

        self.title = title
        self.message = message
        self.recipient = recipient
        self.priority = priority


class NotificationBuilder:

    def __init__(self):

        self.title = ""
        self.message = ""
        self.recipient = ""
        self.priority = "NORMAL"

    def set_title(self, title):
        self.title = title
        return self

    def set_message(self, message):
        self.message = message
        return self

    def set_recipient(self, recipient):
        self.recipient = recipient
        return self

    def set_priority(self, priority):
        self.priority = priority
        return self

    def build(self):

        return Notification(
            self.title,
            self.message,
            self.recipient,
            self.priority
        )


class TestBuilderPattern(unittest.TestCase):

    def test_build_notification(self):

        notification = (
            NotificationBuilder()
            .set_title("Server")
            .set_message("Server restarted")
            .set_recipient("admin")
            .build()
        )

        self.assertEqual(
            notification.title,
            "Server"
        )

        self.assertEqual(
            notification.priority,
            "NORMAL"
        )

    def test_custom_priority(self):

        notification = (
            NotificationBuilder()
            .set_priority("HIGH")
            .build()
        )

        self.assertEqual(
            notification.priority,
            "HIGH"
        )

    def test_builder_chaining(self):

        notification = (
            NotificationBuilder()
            .set_title("Backup")
            .set_message("Completed")
            .set_priority("LOW")
            .build()
        )

        self.assertEqual(
            notification.message,
            "Completed"
        )

    def test_default_values(self):

        notification = NotificationBuilder().build()

        self.assertEqual(
            notification.priority,
            "NORMAL"
        )


class TestRandom(unittest.TestCase):

    def random_text(self):

        return "".join(
            random.choice(string.ascii_letters)
            for _ in range(10)
        )

    def test_random_notifications(self):

        priorities = [
            "LOW",
            "NORMAL",
            "HIGH"
        ]

        for _ in range(100):

            notification = (
                NotificationBuilder()
                .set_title(self.random_text())
                .set_message(self.random_text())
                .set_recipient(self.random_text())
                .set_priority(random.choice(priorities))
                .build()
            )

            self.assertIn(
                notification.priority,
                priorities
            )


if __name__ == "__main__":
    unittest.main()