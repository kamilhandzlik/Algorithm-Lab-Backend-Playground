"""
Problem: Notification Delivery System using Visitor Pattern

Category:
- Design Patterns
- Visitor Pattern
- Notifications
- Extensible Operations

Description:
This project implements a notification delivery system
using the Visitor design pattern.

The Visitor Pattern allows new operations to be added
to existing object structures without modifying the
objects themselves.

In this example:
- EmailNotification
- SMSNotification
- PushNotification

all accept visitors that perform operations on them.

This pattern is commonly used in:
- compilers and AST processing
- report generators
- notification systems
- document processing
- code analysis tools

Features:
- separation of operations from objects
- easy extensibility
- clean architecture
- support for multiple operations

Time Complexity:
- Visit operation: O(1)

Space Complexity:
- O(1)
"""

import unittest
import random
from abc import ABC, abstractmethod


class Notification(ABC):

    @abstractmethod
    def accept(self, visitor):
        pass


class EmailNotification(Notification):

    def accept(self, visitor):

        return visitor.visit_email(self)


class SMSNotification(Notification):

    def accept(self, visitor):

        return visitor.visit_sms(self)


class PushNotification(Notification):

    def accept(self, visitor):

        return visitor.visit_push(self)


class NotificationVisitor(ABC):

    @abstractmethod
    def visit_email(self, notification):
        pass

    @abstractmethod
    def visit_sms(self, notification):
        pass

    @abstractmethod
    def visit_push(self, notification):
        pass


class DeliveryVisitor(NotificationVisitor):

    def visit_email(self, notification):

        return "Email delivered"

    def visit_sms(self, notification):

        return "SMS delivered"

    def visit_push(self, notification):

        return "Push notification delivered"


class TestVisitorPattern(unittest.TestCase):

    def setUp(self):

        self.visitor = DeliveryVisitor()

    def test_email_delivery(self):

        notification = EmailNotification()

        self.assertEqual(
            notification.accept(
                self.visitor
            ),
            "Email delivered"
        )

    def test_sms_delivery(self):

        notification = SMSNotification()

        self.assertEqual(
            notification.accept(
                self.visitor
            ),
            "SMS delivered"
        )

    def test_push_delivery(self):

        notification = PushNotification()

        self.assertEqual(
            notification.accept(
                self.visitor
            ),
            "Push notification delivered"
        )

    def test_multiple_notifications(self):

        notifications = [
            EmailNotification(),
            SMSNotification(),
            PushNotification()
        ]

        results = [

            notification.accept(
                self.visitor
            )

            for notification in notifications
        ]

        self.assertEqual(
            len(results),
            3
        )


class TestRandom(unittest.TestCase):

    def test_random_notifications(self):

        visitor = DeliveryVisitor()

        notification_types = [

            EmailNotification,
            SMSNotification,
            PushNotification
        ]

        valid_results = [

            "Email delivered",
            "SMS delivered",
            "Push notification delivered"
        ]

        for _ in range(100):

            notification = random.choice(
                notification_types
            )()

            result = notification.accept(
                visitor
            )

            self.assertIn(
                result,
                valid_results
            )


if __name__ == "__main__":

    unittest.main()