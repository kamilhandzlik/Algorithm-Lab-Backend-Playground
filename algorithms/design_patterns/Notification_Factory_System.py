"""
Problem: Notification Factory
Category: Design Patterns / Factory Method
"""

from abc import ABC, abstractmethod
import unittest
import random


class Notification(ABC):

    @abstractmethod
    def send(self, message):
        pass


class EmailNotification(Notification):

    def send(self, message):
        return f"EMAIL: {message}"


class SMSNotification(Notification):

    def send(self, message):
        return f"SMS: {message}"


class PushNotification(Notification):

    def send(self, message):
        return f"PUSH: {message}"


class NotificationFactory:

    @staticmethod
    def create(notification_type):

        notification_type = notification_type.lower()

        if notification_type == "email":
            return EmailNotification()

        elif notification_type == "sms":
            return SMSNotification()

        elif notification_type == "push":
            return PushNotification()

        else:
            raise ValueError(
                f"Unknown notification type: {notification_type}"
            )


class TestNotificationFactory(unittest.TestCase):

    def test_email_notification(self):
        notification = NotificationFactory.create("email")

        self.assertEqual(
            notification.send("hello"),
            "EMAIL: hello"
        )

    def test_sms_notification(self):
        notification = NotificationFactory.create("sms")

        self.assertEqual(
            notification.send("test"),
            "SMS: test"
        )

    def test_push_notification(self):
        notification = NotificationFactory.create("push")

        self.assertEqual(
            notification.send("ping"),
            "PUSH: ping"
        )

    def test_invalid_type(self):
        with self.assertRaises(ValueError):
            NotificationFactory.create("fax")


class TestRandomNotifications(unittest.TestCase):

    def test_random_types(self):
        valid_types = ["email", "sms", "push"]

        for _ in range(100):
            notification_type = random.choice(valid_types)

            notification = NotificationFactory.create(
                notification_type
            )

            result = notification.send("message")

            self.assertTrue(
                result.startswith(
                    notification_type.upper()
                )
            )
