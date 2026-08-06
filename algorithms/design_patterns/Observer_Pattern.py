"""
Observer Pattern

Description:
    The Observer Pattern is a behavioral design pattern that defines
    a one-to-many dependency between objects.

    When the state of one object changes, all registered observers
    are automatically notified.

    The subject does not need to know anything about the observers
    except that they implement a common interface.

    This loose coupling allows new observers to be added or removed
    without changing the subject itself.

Purpose:
    - Notify multiple objects about state changes.
    - Decouple event producers from event consumers.
    - Support event-driven architectures.
    - Improve extensibility.
    - Enable asynchronous processing.
    - Promote loose coupling.

Problem it solves:
    Imagine an e-commerce application.

    After an order is placed, several independent actions must occur:

        - Send a confirmation email.
        - Update inventory.
        - Generate an invoice.
        - Notify the warehouse.
        - Publish analytics events.
        - Send a webhook.

    A beginner implementation often places all these actions inside
    one method.

    As new requirements appear, that method grows larger and becomes
    difficult to maintain.

    The Observer Pattern allows every action to become an independent
    observer.

    The order service simply announces that an order has been created.
    Each observer reacts independently.

Structure:
    Subject
        Stores registered observers.

    Observer
        Declares the update() interface.

    Concrete Observer
        Implements reaction to an event.

    Client
        Registers observers.

Workflow:
    Subject
        ↓
    notify()
        ↓
    EmailObserver
        ↓
    InventoryObserver
        ↓
    AnalyticsObserver
        ↓
    WebhookObserver

When to use:
    - Notifications.
    - Event systems.
    - Webhooks.
    - Background jobs.
    - Logging.
    - Analytics.
    - Cache invalidation.
    - GUI events.

Advantages:
    - Loose coupling.
    - Easy to extend.
    - Multiple listeners.
    - Independent event handlers.
    - Supports asynchronous architectures.
    - Encourages the Open/Closed Principle.

Disadvantages:
    - Many observers may make debugging difficult.
    - Notification order is not always guaranteed.
    - Event chains may become difficult to trace.

Common backend usage:
    - Django Signals.
    - Domain Events.
    - Event Bus.
    - Kafka consumers.
    - RabbitMQ subscribers.
    - Webhooks.
    - Notification systems.
    - Audit logging.

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


class Observer(ABC):

    @abstractmethod
    def update(self, order_id: int):
        pass


class EmailObserver(Observer):

    def __init__(self):
        self.sent = []

    def update(self, order_id: int):
        self.sent.append(order_id)


class InventoryObserver(Observer):

    def __init__(self):
        self.updated = []

    def update(self, order_id: int):
        self.updated.append(order_id)


class OrderService:

    def __init__(self):
        self.observers = []

    def subscribe(self, observer: Observer):
        self.observers.append(observer)

    def unsubscribe(self, observer: Observer):
        self.observers.remove(observer)

    def create_order(self, order_id: int):
        for observer in self.observers:
            observer.update(order_id)


class ObserverTests(unittest.TestCase):

    def setUp(self):
        self.service = OrderService()
        self.email = EmailObserver()
        self.inventory = InventoryObserver()

        self.service.subscribe(self.email)
        self.service.subscribe(self.inventory)

    def test_single_order(self):
        self.service.create_order(100)

        self.assertEqual(self.email.sent, [100])
        self.assertEqual(self.inventory.updated, [100])

    def test_multiple_orders(self):
        for order_id in [1, 2, 3]:
            self.service.create_order(order_id)

        self.assertEqual(self.email.sent, [1, 2, 3])
        self.assertEqual(self.inventory.updated, [1, 2, 3])

    def test_unsubscribe(self):
        self.service.unsubscribe(self.email)

        self.service.create_order(50)

        self.assertEqual(self.email.sent, [])
        self.assertEqual(self.inventory.updated, [50])

    def test_multiple_observers(self):
        self.assertEqual(len(self.service.observers), 2)

    def test_observer_type(self):
        self.assertIsInstance(self.email, Observer)


class ObserverRandomTests(unittest.TestCase):

    def test_random_orders(self):
        service = OrderService()
        email = EmailObserver()
        inventory = InventoryObserver()

        service.subscribe(email)
        service.subscribe(inventory)

        count = random.randint(100, 500)

        for _ in range(count):
            order_id = random.randint(1, 100000)

            service.create_order(order_id)

        self.assertEqual(len(email.sent), count)
        self.assertEqual(len(inventory.updated), count)

    def test_random_subscribe_unsubscribe(self):
        service = OrderService()

        observers = [
            EmailObserver()
            for _ in range(20)
        ]

        for observer in observers:
            service.subscribe(observer)

        random.shuffle(observers)

        for observer in observers[:10]:
            service.unsubscribe(observer)

        self.assertEqual(
            len(service.observers),
            10
        )

    def test_random_notifications(self):
        service = OrderService()

        observers = [
            EmailObserver()
            for _ in range(5)
        ]

        for observer in observers:
            service.subscribe(observer)

        for _ in range(300):
            order_id = random.randint(1, 10000)

            service.create_order(order_id)

        for observer in observers:
            self.assertEqual(
                len(observer.sent),
                300
            )


if __name__ == "__main__":
    unittest.main()
