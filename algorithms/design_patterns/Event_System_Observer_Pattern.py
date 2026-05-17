"""
Problem: Event System
Category: Design Patterns / Observer
"""

from abc import ABC, abstractmethod
import unittest
import random
import string


class Observer(ABC):

    @abstractmethod
    def update(self, message):
        pass


class UserObserver(Observer):

    def __init__(self, name):

        self.name = name
        self.notifications = []

    def update(self, message):

        self.notifications.append(
            f"{self.name} received: {message}"
        )


class EventManager:

    def __init__(self):

        self.observers = []

    def subscribe(self, observer):

        self.observers.append(observer)

    def unsubscribe(self, observer):

        self.observers.remove(observer)

    def notify(self, message):

        for observer in self.observers:
            observer.update(message)




class TestObserverPattern(unittest.TestCase):

    def test_single_observer(self):

        manager = EventManager()

        user = UserObserver("Kamil")

        manager.subscribe(user)

        manager.notify("New event!")

        self.assertEqual(
            user.notifications,
            ["Kamil received: New event!"]
        )

    def test_multiple_observers(self):

        manager = EventManager()

        user1 = UserObserver("Alice")
        user2 = UserObserver("Bob")

        manager.subscribe(user1)
        manager.subscribe(user2)

        manager.notify("System update")

        self.assertEqual(
            user1.notifications,
            ["Alice received: System update"]
        )

        self.assertEqual(
            user2.notifications,
            ["Bob received: System update"]
        )

    def test_unsubscribe(self):

        manager = EventManager()

        user = UserObserver("Mike")

        manager.subscribe(user)
        manager.unsubscribe(user)

        manager.notify("Hidden event")

        self.assertEqual(
            user.notifications,
            []
        )





class TestRandomObserver(unittest.TestCase):

    def random_name(self):

        length = random.randint(3, 8)

        return ''.join(
            random.choice(string.ascii_letters)
            for _ in range(length)
        )

    def random_message(self):

        length = random.randint(5, 15)

        return ''.join(
            random.choice(string.ascii_letters)
            for _ in range(length)
        )

    def test_random_notifications(self):

        manager = EventManager()

        users = []

        for _ in range(10):

            user = UserObserver(
                self.random_name()
            )

            users.append(user)

            manager.subscribe(user)

        message = self.random_message()

        manager.notify(message)

        for user in users:

            self.assertEqual(
                len(user.notifications),
                1
            )

            self.assertIn(
                message,
                user.notifications[0]
            )