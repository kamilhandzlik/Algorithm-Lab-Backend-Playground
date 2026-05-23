"""
Problem: Event System using Observer Pattern

Category:
- Design Patterns
- Observer Pattern
- Event-Driven Architecture
- Decoupled Communication

Description:
This project implements a simple event notification system
using the Observer design pattern.

The Observer Pattern defines a one-to-many dependency between
objects so that when one object (the subject) changes state,
all its dependents (observers) are notified automatically.

This pattern is commonly used in:
- event-driven systems
- GUI frameworks
- pub/sub messaging
- model-view architectures
- real-time dashboards

Features:
- observer abstraction
- dynamic subscribe/unsubscribe
- decoupled notification logic
- multiple independent observers

Time Complexity:
- Notify all observers: O(n)

Space Complexity:
- O(n)
"""

import unittest
import random
from abc import ABC, abstractmethod


class Observer(ABC):

    @abstractmethod
    def update(self, event: str):
        pass


class LoggerObserver(Observer):

    def __init__(self):

        self.logs = []

    def update(self, event: str):

        message = f"LOG: {event}"

        self.logs.append(message)

        return message


class AlertObserver(Observer):

    def __init__(self):

        self.alerts = []

    def update(self, event: str):

        message = f"ALERT: {event}"

        self.alerts.append(message)

        return message


class MetricsObserver(Observer):

    def __init__(self):

        self.count = 0

    def update(self, event: str):

        self.count += 1

        return f"METRIC: event #{self.count} — {event}"


class EventBus:

    def __init__(self):

        self._observers: list[Observer] = []

    def subscribe(self, observer: Observer):

        self._observers.append(observer)

    def unsubscribe(self, observer: Observer):

        self._observers.remove(observer)

    def publish(self, event: str):

        results = []

        for observer in self._observers:

            result = observer.update(event)

            results.append(result)

        return results


class TestObserverPattern(unittest.TestCase):

    def test_logger_receives_event(self):

        bus = EventBus()

        logger = LoggerObserver()

        bus.subscribe(logger)

        bus.publish("user_signup")

        self.assertEqual(
            logger.logs,
            ["LOG: user_signup"]
        )

    def test_alert_receives_event(self):

        bus = EventBus()

        alert = AlertObserver()

        bus.subscribe(alert)

        bus.publish("payment_failed")

        self.assertEqual(
            alert.alerts,
            ["ALERT: payment_failed"]
        )

    def test_metrics_counts_events(self):

        bus = EventBus()

        metrics = MetricsObserver()

        bus.subscribe(metrics)

        bus.publish("page_view")
        bus.publish("page_view")
        bus.publish("page_view")

        self.assertEqual(
            metrics.count,
            3
        )

    def test_multiple_observers_notified(self):

        bus = EventBus()

        logger = LoggerObserver()
        alert = AlertObserver()

        bus.subscribe(logger)
        bus.subscribe(alert)

        results = bus.publish("server_down")

        self.assertIn(
            "LOG: server_down",
            results
        )

        self.assertIn(
            "ALERT: server_down",
            results
        )

    def test_unsubscribe_stops_notifications(self):

        bus = EventBus()

        logger = LoggerObserver()

        bus.subscribe(logger)

        bus.publish("first_event")

        bus.unsubscribe(logger)

        bus.publish("second_event")

        self.assertEqual(
            logger.logs,
            ["LOG: first_event"]
        )

    def test_no_observers_returns_empty(self):

        bus = EventBus()

        results = bus.publish("ghost_event")

        self.assertEqual(
            results,
            []
        )


class TestRandom(unittest.TestCase):

    def test_random_events(self):

        bus = EventBus()

        logger = LoggerObserver()

        bus.subscribe(logger)

        events = [
            "user_login",
            "user_logout",
            "payment_success",
            "payment_failed",
            "server_down",
        ]

        expected = []

        for _ in range(50):

            event = random.choice(events)

            bus.publish(event)

            expected.append(f"LOG: {event}")

        self.assertEqual(
            logger.logs,
            expected
        )


if __name__ == "__main__":

    unittest.main()