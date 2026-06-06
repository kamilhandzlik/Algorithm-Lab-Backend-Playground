"""
Problem: Order Processing System using Mediator Pattern

Category:
- Design Patterns
- Mediator Pattern
- Order Management
- Communication Coordination

Description:
This project implements a simple order processing system
using the Mediator design pattern.

The Mediator Pattern centralizes communication between
multiple objects, reducing direct dependencies between them.

In this example:
- CustomerService receives orders
- InventoryService checks product availability
- PaymentService processes payments
- OrderMediator coordinates communication

Instead of services communicating directly with each other,
all interactions go through the mediator.

This pattern is commonly used in:
- order management systems
- chat applications
- workflow engines
- GUI frameworks
- microservice orchestration

Features:
- centralized communication
- reduced coupling
- simplified coordination
- scalable architecture

Time Complexity:
- Process order: O(1)

Space Complexity:
- O(1)
"""

import unittest
import random


class InventoryService:

    def check_stock(self, quantity):

        return quantity <= 10


class PaymentService:

    def process_payment(self, amount):

        return amount > 0


class CustomerService:

    def notify(self, message):

        return f"Customer notified: {message}"


class OrderMediator:

    def __init__(self):

        self.inventory = InventoryService()
        self.payment = PaymentService()
        self.customer = CustomerService()

    def place_order(
        self,
        quantity,
        amount
    ):

        if not self.inventory.check_stock(
            quantity
        ):

            return (
                "Order failed: "
                "insufficient stock"
            )

        if not self.payment.process_payment(
            amount
        ):

            return (
                "Order failed: "
                "payment rejected"
            )

        return self.customer.notify(
            "order completed"
        )


class TestMediatorPattern(
    unittest.TestCase
):

    def test_successful_order(self):

        mediator = OrderMediator()

        result = mediator.place_order(
            5,
            100
        )

        self.assertEqual(
            result,
            "Customer notified: order completed"
        )

    def test_stock_failure(self):

        mediator = OrderMediator()

        result = mediator.place_order(
            20,
            100
        )

        self.assertEqual(
            result,
            "Order failed: insufficient stock"
        )

    def test_payment_failure(self):

        mediator = OrderMediator()

        result = mediator.place_order(
            5,
            0
        )

        self.assertEqual(
            result,
            "Order failed: payment rejected"
        )

    def test_multiple_orders(self):

        mediator = OrderMediator()

        self.assertEqual(
            mediator.place_order(1, 50),
            "Customer notified: order completed"
        )

        self.assertEqual(
            mediator.place_order(15, 50),
            "Order failed: insufficient stock"
        )


class TestRandom(unittest.TestCase):

    def test_random_orders(self):

        mediator = OrderMediator()

        for _ in range(100):

            quantity = random.randint(
                1,
                20
            )

            amount = random.randint(
                -10,
                1000
            )

            result = mediator.place_order(
                quantity,
                amount
            )

            if quantity > 10:

                self.assertEqual(
                    result,
                    "Order failed: insufficient stock"
                )

            elif amount <= 0:

                self.assertEqual(
                    result,
                    "Order failed: payment rejected"
                )

            else:

                self.assertEqual(
                    result,
                    "Customer notified: order completed"
                )


if __name__ == "__main__":

    unittest.main()