"""
State Pattern

Description:
    The State Pattern is a behavioral design pattern that allows an
    object to change its behavior when its internal state changes.

    Instead of placing all state-dependent behavior inside one class
    using large if-elif-else statements, each state is represented by
    a separate class.

    The main object delegates operations to the current state object.

    This means that changing the state of an object effectively changes
    the behavior of that object without requiring large conditional
    statements.

Purpose:
    - Encapsulate state-specific behavior.
    - Remove large conditional statements.
    - Make state transitions explicit.
    - Separate business rules for different states.
    - Make complex workflows easier to maintain.
    - Prevent invalid operations.

Problem it solves:
    Imagine an e-commerce order with several possible states:

        CREATED
        PAID
        SHIPPED
        DELIVERED
        CANCELLED

    Different operations are allowed depending on the current state.

    For example:

        CREATED -> can be paid or cancelled.
        PAID -> can be shipped or cancelled.
        SHIPPED -> can be delivered.
        DELIVERED -> cannot be cancelled.
        CANCELLED -> cannot be modified.

    A naive implementation might contain many conditions:

        if status == "created":
            ...
        elif status == "paid":
            ...
        elif status == "shipped":
            ...

    As the number of states and operations grows, this code becomes
    difficult to understand and maintain.

    The State Pattern moves the behavior associated with each state
    into its own class.

Structure:
    Context
        Stores the current state and delegates operations to it.

    State
        Defines the common interface for states.

    Concrete States
        Implement behavior for individual states.

Workflow:
    Order
        ↓
    CreatedState
        ↓
    PaidState
        ↓
    ShippedState
        ↓
    DeliveredState

    A state can also transition to another state when an operation
    is successfully completed.

When to use:
    - Order processing.
    - Payment workflows.
    - Document approval.
    - User account lifecycle.
    - Shipment tracking.
    - Job processing.
    - Authentication sessions.
    - Workflow engines.

Advantages:
    - Eliminates large conditional statements.
    - Keeps state-specific logic separated.
    - Makes state transitions explicit.
    - Easier unit testing.
    - Easier to add new states.
    - Prevents invalid operations.
    - Improves readability.

Disadvantages:
    - Introduces additional classes.
    - Simple state machines may not require this pattern.
    - Large state machines can still become complex.

Common backend usage:
    - E-commerce orders.
    - Payment processing.
    - Background jobs.
    - Approval workflows.
    - Shipping systems.
    - User account management.
    - Reservation systems.

Real-world frameworks and technologies:
    - Django
    - FastAPI
    - Flask
    - Spring Boot
    - ASP.NET Core
    - Workflow engines
    - State machine libraries
"""
from abc import ABC, abstractmethod
import random
import unittest


class OrderState(ABC):

    @abstractmethod
    def pay(self, order):
        pass

    @abstractmethod
    def ship(self, order):
        pass

    @abstractmethod
    def deliver(self, order):
        pass

    @abstractmethod
    def cancel(self, order):
        pass


class CreatedState(OrderState):

    def pay(self, order):
        order.state = PaidState()

    def ship(self, order):
        raise ValueError("Order must be paid before shipping")

    def deliver(self, order):
        raise ValueError("Order must be shipped before delivery")

    def cancel(self, order):
        order.state = CancelledState()


class PaidState(OrderState):

    def pay(self, order):
        raise ValueError("Order is already paid")

    def ship(self, order):
        order.state = ShippedState()

    def deliver(self, order):
        raise ValueError("Order must be shipped before delivery")

    def cancel(self, order):
        order.state = CancelledState()


class ShippedState(OrderState):

    def pay(self, order):
        raise ValueError("Order is already paid")

    def ship(self, order):
        raise ValueError("Order is already shipped")

    def deliver(self, order):
        order.state = DeliveredState()

    def cancel(self, order):
        raise ValueError("Shipped order cannot be cancelled")


class DeliveredState(OrderState):

    def pay(self, order):
        raise ValueError("Order is already completed")

    def ship(self, order):
        raise ValueError("Order is already delivered")

    def deliver(self, order):
        raise ValueError("Order is already delivered")

    def cancel(self, order):
        raise ValueError("Delivered order cannot be cancelled")


class CancelledState(OrderState):

    def pay(self, order):
        raise ValueError("Cancelled order cannot be paid")

    def ship(self, order):
        raise ValueError("Cancelled order cannot be shipped")

    def deliver(self, order):
        raise ValueError("Cancelled order cannot be delivered")

    def cancel(self, order):
        raise ValueError("Order is already cancelled")


class Order:

    def __init__(self):
        self.state = CreatedState()

    def pay(self):
        self.state.pay(self)

    def ship(self):
        self.state.ship(self)

    def deliver(self):
        self.state.deliver(self)

    def cancel(self):
        self.state.cancel(self)

    def get_status(self):
        return self.state.__class__.__name__.replace("State", "")


class StateTests(unittest.TestCase):

    def setUp(self):
        self.order = Order()

    def test_initial_state(self):
        self.assertEqual(self.order.get_status(), "Created")

    def test_pay_order(self):
        self.order.pay()

        self.assertEqual(self.order.get_status(), "Paid")

    def test_ship_order(self):
        self.order.pay()
        self.order.ship()

        self.assertEqual(self.order.get_status(), "Shipped")

    def test_deliver_order(self):
        self.order.pay()
        self.order.ship()
        self.order.deliver()

        self.assertEqual(self.order.get_status(), "Delivered")

    def test_cancel_created_order(self):
        self.order.cancel()

        self.assertEqual(self.order.get_status(), "Cancelled")

    def test_cancel_paid_order(self):
        self.order.pay()
        self.order.cancel()

        self.assertEqual(self.order.get_status(), "Cancelled")

    def test_cannot_ship_unpaid_order(self):
        with self.assertRaises(ValueError):
            self.order.ship()

    def test_cannot_deliver_unshipped_order(self):
        with self.assertRaises(ValueError):
            self.order.deliver()

    def test_cannot_cancel_shipped_order(self):
        self.order.pay()
        self.order.ship()

        with self.assertRaises(ValueError):
            self.order.cancel()

    def test_cannot_modify_delivered_order(self):
        self.order.pay()
        self.order.ship()
        self.order.deliver()

        with self.assertRaises(ValueError):
            self.order.cancel()


class StateRandomTests(unittest.TestCase):

    def random_operation(self):
        return random.choice([
            "pay",
            "ship",
            "deliver",
            "cancel"
        ])

    def test_random_operations(self):
        for _ in range(500):
            order = Order()

            for _ in range(20):
                operation = self.random_operation()

                try:
                    getattr(order, operation)()
                except ValueError:
                    pass

            self.assertIn(
                order.get_status(),
                ["Created", "Paid", "Shipped", "Delivered", "Cancelled"]
            )

    def test_random_valid_workflow(self):
        for _ in range(500):
            order = Order()

            order.pay()
            self.assertEqual(order.get_status(), "Paid")

            order.ship()
            self.assertEqual(order.get_status(), "Shipped")

            order.deliver()
            self.assertEqual(order.get_status(), "Delivered")

    def test_random_cancellation(self):
        for _ in range(500):
            order = Order()

            if random.choice([True, False]):
                order.pay()

            if order.get_status() in ["Created", "Paid"]:
                order.cancel()

                self.assertEqual(
                    order.get_status(),
                    "Cancelled"
                )

    def test_random_invalid_operations(self):
        invalid_operations = {
            "Created": ["ship", "deliver"],
            "Paid": ["deliver"],
            "Shipped": ["cancel"],
            "Delivered": ["pay", "ship", "deliver", "cancel"],
            "Cancelled": ["pay", "ship", "deliver", "cancel"]
        }

        for _ in range(500):
            order = Order()

            operations = [
                ("Created", "ship"),
                ("Created", "deliver")
            ]

            status, operation = random.choice(operations)

            with self.assertRaises(ValueError):
                getattr(order, operation)()


if __name__ == "__main__":
    unittest.main()
