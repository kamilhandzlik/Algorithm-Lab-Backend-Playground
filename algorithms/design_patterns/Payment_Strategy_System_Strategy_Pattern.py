"""
Problem: Payment Strategy System
Category: Design Patterns / Strategy
"""

from abc import ABC, abstractmethod
import random
import unittest


class PaymentStrategy(ABC):

    @abstractmethod
    def pay(self, amount):
        pass


class CreditCardPayment(PaymentStrategy):

    def pay(self, amount):
        return f"Paid {amount}$ using Credit Card"


class PayPalPayment(PaymentStrategy):

    def pay(self, amount):
        return f"Paid {amount}$ using PayPal"


class BlikPayment(PaymentStrategy):

    def pay(self, amount):
        return f"Paid {amount}$ using BLIK"


class PaymentProcessor:

    def __init__(self, strategy):

        self.strategy = strategy

    def process_payment(self, amount):

        return self.strategy.pay(amount)




class TestPaymentStrategy(unittest.TestCase):

    def test_credit_card_payment(self):

        processor = PaymentProcessor(
            CreditCardPayment()
        )

        self.assertEqual(
            processor.process_payment(100),
            "Paid 100$ using Credit Card"
        )

    def test_paypal_payment(self):

        processor = PaymentProcessor(
            PayPalPayment()
        )

        self.assertEqual(
            processor.process_payment(50),
            "Paid 50$ using PayPal"
        )

    def test_blik_payment(self):

        processor = PaymentProcessor(
            BlikPayment()
        )

        self.assertEqual(
            processor.process_payment(20),
            "Paid 20$ using BLIK"
        )




class TestRandomPayments(unittest.TestCase):

    def test_random_payment_methods(self):

        strategies = [
            CreditCardPayment,
            PayPalPayment,
            BlikPayment
        ]

        for _ in range(100):

            amount = random.randint(1, 1000)

            strategy_class = random.choice(strategies)

            processor = PaymentProcessor(
                strategy_class()
            )

            result = processor.process_payment(amount)

            self.assertIn(
                str(amount),
                result
            )