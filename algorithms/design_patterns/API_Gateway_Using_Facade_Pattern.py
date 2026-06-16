"""
Problem: API Gateway using Facade Pattern

Category:
- Design Patterns
- Facade Pattern
- API Gateway
- Service Orchestration

Description:
This project implements a simple API Gateway using
the Facade design pattern.

The Facade Pattern provides a unified interface to
a set of interfaces in a subsystem, making the system
easier to use.

In this example:
- UserService handles user information
- OrderService handles order data
- PaymentService handles payment status
- APIGateway provides a single entry point

Instead of communicating with multiple services,
clients interact only with the gateway.

This pattern is commonly used in:
- microservices architectures
- backend-for-frontend systems
- API gateways
- service orchestration
- enterprise applications

Features:
- centralized access point
- simplified client interaction
- service orchestration
- reduced coupling

Time Complexity:
- Fetch dashboard data: O(1)

Space Complexity:
- O(1)
"""
import unittest
import random


class UserService:
    def get_user(self, user_id):
        return {"id": user_id, "name": f"User{user_id}"}


class OrderService:
    def get_orders(self, user_id):
        return [f"order_{user_id}_1", f"order_{user_id}_2"]


class PaymentService:
    def get_payment_status(self, user_id):
        return "PAID"


class APIGateway:
    def __init__(self):
        self.user_service = UserService()
        self.order_service = OrderService()
        self.payment_service = PaymentService()

    def get_dashboard_data(self, user_id):
        return {"user": self.user_service.get_user(user_id),
                "orders": self.order_service.get_orders(user_id),
                "payment": self.payment_service.get_payment_status(user_id)}


class TestFacadePattern(unittest.TestCase):

    def test_user_data(self):
        gateway = APIGateway()
        result = gateway.get_dashboard_data(1)

        self.assertEqual(result["user"]["id"], 1)

    def test_orders_exist(self):
        gateway = APIGateway()

        result = gateway.get_dashboard_data(5)

        self.assertEqual(len(result["orders"]), 2)

    def test_payment_status(self):
        gateway = APIGateway()

        result = gateway.get_dashboard_data(10)

        self.assertEqual(result["payment"], "PAID")

    def test_dashboard_structure(self):
        gateway = APIGateway()

        result = gateway.get_dashboard_data(3)

        self.assertIn("user", result)

        self.assertIn("orders", result)

        self.assertIn("payment", result)


class TestRandom(unittest.TestCase):

    def test_random_users(self):
        gateway = APIGateway()

        for _ in range(100):
            user_id = random.randint(1, 10000)

            result = gateway.get_dashboard_data(user_id)

            self.assertEqual(result["user"]["id"], user_id)

            self.assertEqual(result["payment"], "PAID")

            self.assertEqual(len(result["orders"]), 2)


if __name__ == "__main__":
    unittest.main()
