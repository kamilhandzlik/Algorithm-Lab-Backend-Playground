"""
Problem: Notification Pipeline using State Pattern

Category:
- Design Patterns
- State Pattern
- Workflow Management
- Notification Processing

Description:
This project implements a notification processing system
using the State design pattern.

The State Pattern allows an object to change its behavior
when its internal state changes.

In this example:
- a notification moves through different states
- each state defines what actions are allowed
- state transitions are controlled by the workflow

States:
- Pending
- Sent
- Delivered

This pattern is commonly used in:
- order management systems
- ticketing systems
- payment processing
- workflow engines
- delivery tracking

Features:
- controlled state transitions
- encapsulated state logic
- flexible workflow management
- clean separation of responsibilities

Time Complexity:
- State transition: O(1)

Space Complexity:
- O(1)
"""

import unittest
import random
from abc import ABC, abstractmethod


class NotificationState(ABC):

    @abstractmethod
    def next_state(self):
        pass

    @abstractmethod
    def name(self):
        pass


class PendingState(NotificationState):

    def next_state(self):

        return SentState()

    def name(self):

        return "PENDING"


class SentState(NotificationState):

    def next_state(self):

        return DeliveredState()

    def name(self):

        return "SENT"


class DeliveredState(NotificationState):

    def next_state(self):

        return self

    def name(self):

        return "DELIVERED"


class Notification:

    def __init__(self):

        self.state = PendingState()

    def advance(self):

        self.state = self.state.next_state()

    def current_state(self):

        return self.state.name()


class TestStatePattern(unittest.TestCase):

    def test_initial_state(self):

        notification = Notification()

        self.assertEqual(
            notification.current_state(),
            "PENDING"
        )

    def test_state_transition(self):

        notification = Notification()

        notification.advance()

        self.assertEqual(
            notification.current_state(),
            "SENT"
        )

    def test_final_state(self):

        notification = Notification()

        notification.advance()
        notification.advance()

        self.assertEqual(
            notification.current_state(),
            "DELIVERED"
        )

    def test_delivered_stays_delivered(self):

        notification = Notification()

        notification.advance()
        notification.advance()
        notification.advance()

        self.assertEqual(
            notification.current_state(),
            "DELIVERED"
        )


class TestRandom(unittest.TestCase):

    def test_random_transitions(self):

        for _ in range(50):

            notification = Notification()

            transitions = random.randint(
                0,
                10
            )

            for _ in range(transitions):

                notification.advance()

            self.assertIn(
                notification.current_state(),
                [
                    "PENDING",
                    "SENT",
                    "DELIVERED"
                ]
            )


if __name__ == "__main__":

    unittest.main()