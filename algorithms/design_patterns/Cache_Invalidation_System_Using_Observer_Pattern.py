"""
Problem: Cache Invalidation System using Observer Pattern

Category:
- Design Patterns
- Observer Pattern
- Cache Management
- Event-Driven Architecture

Description:
This project implements a cache invalidation system
using the Observer design pattern.

The Observer Pattern defines a one-to-many relationship
between objects so that when one object changes state,
all dependent objects are notified automatically.

In this example:
- DataSource acts as the publisher
- Cache instances act as observers
- updating data automatically invalidates caches

This pattern is commonly used in:
- Redis cache invalidation
- event-driven systems
- message brokers
- real-time applications
- distributed architectures

Features:
- automatic cache invalidation
- event notification system
- loose coupling
- scalable architecture

Time Complexity:
- Notify observers: O(n)

Space Complexity:
- O(n)
"""
import unittest
import random
import string
from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def update(self):
        pass


class Cache(Observer):
    def __init__(self, name):
        self.name = name
        self.valid = True

    def update(self):
        self.valid = False

    def is_valid(self):
        return self.valid


class DataSource:
    def __init__(self):
        self.observers = []

    def subscribe(self, observer):
        self.observers.append(observer)

    def unsubscribe(self, observer):
        self.observers.remove(observer)

    def update_data(self):
        for observer in self.observers:
            observer.update()


class TestObserverPattern(unittest.TestCase):

    def test_single_cache(self):
        source = DataSource()

        cache = Cache("users")

        source.subscribe(cache)

        source.update_data()

        self.assertFalse(cache.is_valid())

    def test_multiple_caches(self):
        source = DataSource()

        cache1 = Cache("users")
        cache2 = Cache("products")

        source.subscribe(cache1)
        source.subscribe(cache2)

        source.update_data()

        self.assertFalse(cache1.is_valid())

        self.assertFalse(cache2.is_valid())

    def test_unsubscribe(self):
        source = DataSource()

        cache = Cache("orders")

        source.subscribe(cache)

        source.unsubscribe(cache)

        source.update_data()

        self.assertTrue(cache.is_valid())

    def test_no_observers(self):
        source = DataSource()

        source.update_data()

        self.assertEqual(len(source.observers), 0)


class TestRandom(unittest.TestCase):

    def random_name(self):
        length = random.randint(5, 10)

        return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

    def test_random_caches(self):
        source = DataSource()

        caches = []

        for _ in range(100):
            cache = Cache(self.random_name())

            caches.append(cache)

            source.subscribe(cache)

        source.update_data()

        self.assertTrue(all(not cache.is_valid() for cache in caches))


if __name__ == "__main__":
    unittest.main()
