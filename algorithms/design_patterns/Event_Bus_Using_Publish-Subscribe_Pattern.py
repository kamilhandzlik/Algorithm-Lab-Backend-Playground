"""
Problem: Event Bus using Publish-Subscribe Pattern

Category:
- Design Patterns
- Publish-Subscribe
- Event Bus
- Event-Driven Architecture

Description:
This project implements a simple Event Bus using
the Publish-Subscribe design pattern.

The Publish-Subscribe Pattern allows publishers to
broadcast events without knowing who receives them.

Subscribers register interest in specific event types
and are notified whenever those events occur.

In this example:
- EventBus manages subscriptions
- Logger listens for all events
- EmailNotifier sends notifications
- AnalyticsService collects statistics

This pattern is commonly used in:
- microservices
- monitoring systems
- logging frameworks
- CQRS
- event-driven applications

Features:
- loose coupling
- multiple subscribers
- event broadcasting
- dynamic subscription management

Time Complexity:
- Publish event: O(n)

Space Complexity:
- O(n)
"""
import random
import unittest
from abc import ABC, abstractmethod


class Subscriber(ABC):
    @abstractmethod
    def notify(self, event):
        pass


class EventBus:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_name, subscriber):
        self.subscribers.setdefault(event_name, []).append(subscriber)

    def publish(self, event_name, payload):
        event = {"name": event_name, "payload": payload}

        for subscriber in self.subscribers.get(event_name, []):
            subscriber.notify(event)


class Logger(Subscriber):
    def __init__(self):
        self.logs = []

    def notify(self, event):
        self.logs.append(event)


class EmailNotifier(Subscriber):
    def __init__(self):
        self.sent = 0

    def notify(self, event):
        self.sent += 1


class AnalyticsService(Subscriber):
    def __init__(self):
        self.events = []

    def notify(self, event):
        self.events.append(event)


class TestEventBus(unittest.TestCase):
    def test_single_subscriber(self):
        bus = EventBus()
        logger = Logger()

        bus.subscribe("user_created", logger)
        bus.publish("user_created", {"id": 1})

        self.assertEqual(len(logger.logs), 1)

    def test_multiple_subscribers(self):
        bus = EventBus()

        logger = Logger()
        analytics = AnalyticsService()

        bus.subscribe("login", logger)
        bus.subscribe("login", analytics)

        bus.publish("login", {"user": "john"})

        self.assertEqual(len(logger.logs), 1)
        self.assertEqual(len(analytics.events), 1)

    def test_different_events(self):
        bus = EventBus()

        logger = Logger()

        bus.subscribe("payment", logger)

        bus.publish("order", {})
        bus.publish("payment", {})

        self.assertEqual(len(logger.logs), 1)

    def test_email_notifier(self):
        bus = EventBus()

        email = EmailNotifier()

        bus.subscribe("register", email)

        bus.publish("register", {})
        bus.publish("register", {})

        self.assertEqual(email.sent, 2)


class TestRandom(unittest.TestCase):

    def test_random_events(self):

        bus = EventBus()

        logger = Logger()

        events = ["login", "logout", "payment", "register", "delete_account"]

        for event in events:
            bus.subscribe(event, logger)

        count = 0

        for _ in range(100):
            event = random.choice(events)

            bus.publish(event, {})

            count += 1

        self.assertEqual(len(logger.logs), count)


if __name__ == "__main__":
    unittest.main()
