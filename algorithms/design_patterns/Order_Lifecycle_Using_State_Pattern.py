"""
Problem: Order Lifecycle using State Pattern

Category:
- Design Patterns
- State Pattern
- Order Management
- Workflow

Description:
This project implements an order lifecycle using
the State design pattern.

The State Pattern allows an object to change its
behavior when its internal state changes.

In this example:
- NewState represents a newly created order
- PaidState represents a paid order
- ShippedState represents a shipped order
- DeliveredState represents a completed order

Each state controls which transitions are allowed.

This pattern is commonly used in:
- order processing systems
- workflow engines
- vending machines
- game AI
- traffic lights

Features:
- encapsulated state transitions
- simplified business logic
- flexible workflow
- easy to extend

Time Complexity:
- State transition: O(1)

Space Complexity:
- O(1)
"""

import random
import unittest
from abc import ABC, abstractmethod


class OrderState(ABC):

    @abstractmethod
    def next(self, order):
        pass

    @abstractmethod
    def name(self):
        pass


class NewState(OrderState):

    def next(self, order):
        order.state = PaidState()

    def name(self):
        return "NEW"


class PaidState(OrderState):

    def next(self, order):
        order.state = ShippedState()

    def name(self):
        return "PAID"


class ShippedState(OrderState):

    def next(self, order):
        order.state = DeliveredState()

    def name(self):
        return "SHIPPED"


class DeliveredState(OrderState):

    def next(self, order):
        pass

    def name(self):
        return "DELIVERED"


class Order:

    def __init__(self):
        self.state = NewState()

    def next_state(self):
        self.state.next(self)

    def current_state(self):
        return self.state.name()


class TestStatePattern(unittest.TestCase):

    def test_initial_state(self):
        order = Order()

        self.assertEqual(order.current_state(), "NEW")

    def test_paid_state(self):
        order = Order()

        order.next_state()

        self.assertEqual(order.current_state(), "PAID")

    def test_shipped_state(self):
        order = Order()

        order.next_state()
        order.next_state()

        self.assertEqual(order.current_state(), "SHIPPED")

    def test_delivered_state(self):
        order = Order()

        order.next_state()
        order.next_state()
        order.next_state()

        self.assertEqual(order.current_state(), "DELIVERED")

    def test_delivered_is_final(self):
        order = Order()

        for _ in range(5):
            order.next_state()

        self.assertEqual(order.current_state(), "DELIVERED")


class TestRandom(unittest.TestCase):

    def test_random_transitions(self):

        for _ in range(100):

            order = Order()

            transitions = random.randint(0, 10)

            for _ in range(transitions):
                order.next_state()

            self.assertIn(order.current_state(), ["NEW", "PAID", "SHIPPED", "DELIVERED"])


if __name__ == "__main__":
    unittest.main()
