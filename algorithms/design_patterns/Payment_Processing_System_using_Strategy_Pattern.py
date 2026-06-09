"""
Problem: Payment Processing System using Strategy Pattern

Category:
- Design Patterns
- Strategy Pattern
- Payment Processing
- Business Logic

Description:
This project implements a payment processing system
using the Strategy design pattern.

The Strategy Pattern allows different algorithms
to be selected at runtime without changing the
client code.

In this example:
- CreditCardPayment handles card payments
- PayPalPayment handles PayPal transactions
- CryptoPayment handles cryptocurrency payments
- PaymentProcessor delegates payment execution
  to the selected strategy

This pattern is commonly used in:
- payment gateways
- sorting algorithms
- authentication providers
- shipping calculators
- discount systems

Features:
- interchangeable payment methods
- runtime strategy selection
- clean separation of business logic
- extensible architecture

Time Complexity:
- Process payment: O(1)

Space Complexity:
- O(1)
"""

import unittest
import random
from abc import ABC, abstractmethod


class PaymentStrategy(ABC):

    @abstractmethod
    def pay(self, amount):
        pass


class CreditCardPayment(PaymentStrategy):

    def pay(self, amount):

        return (
            f"Paid {amount}$ "
            f"using Credit Card"
        )


class PayPalPayment(PaymentStrategy):

    def pay(self, amount):

        return (
            f"Paid {amount}$ "
            f"using PayPal"
        )


class CryptoPayment(PaymentStrategy):

    def pay(self, amount):

        return (
            f"Paid {amount}$ "
            f"using Cryptocurrency"
        )


class PaymentProcessor:

    def __init__(self, strategy):

        self.strategy = strategy

    def process_payment(self, amount):

        return self.strategy.pay(amount)


class TestStrategyPattern(unittest.TestCase):

    def test_credit_card_payment(self):

        processor = PaymentProcessor(
            CreditCardPayment()
        )

        result = processor.process_payment(
            100
        )

        self.assertEqual(
            result,
            "Paid 100$ using Credit Card"
        )

    def test_paypal_payment(self):

        processor = PaymentProcessor(
            PayPalPayment()
        )

        result = processor.process_payment(
            250
        )

        self.assertEqual(
            result,
            "Paid 250$ using PayPal"
        )

    def test_crypto_payment(self):

        processor = PaymentProcessor(
            CryptoPayment()
        )

        result = processor.process_payment(
            500
        )

        self.assertEqual(
            result,
            "Paid 500$ using Cryptocurrency"
        )

    def test_change_strategy(self):

        processor = PaymentProcessor(
            CreditCardPayment()
        )

        processor.strategy = PayPalPayment()

        result = processor.process_payment(
            50
        )

        self.assertEqual(
            result,
            "Paid 50$ using PayPal"
        )


class TestRandom(unittest.TestCase):

    def test_random_payments(self):

        strategies = [
            CreditCardPayment,
            PayPalPayment,
            CryptoPayment
        ]

        for _ in range(100):

            amount = random.randint(
                1,
                10000
            )

            strategy = random.choice(
                strategies
            )()

            processor = PaymentProcessor(
                strategy
            )

            result = processor.process_payment(
                amount
            )

            self.assertIn(
                str(amount),
                result
            )


if __name__ == "__main__":

    unittest.main()