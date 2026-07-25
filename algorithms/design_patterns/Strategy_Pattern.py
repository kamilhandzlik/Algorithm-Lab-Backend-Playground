"""
Strategy Pattern

Description:
    The Strategy Pattern is a behavioral design pattern that defines
    a family of interchangeable algorithms, encapsulates each one
    into a separate class, and allows them to be selected at runtime.

    Instead of using long if-elif-else statements or switch cases,
    the application delegates a task to a strategy object that
    implements a common interface.

Purpose:
    - Encapsulate algorithms into separate classes.
    - Eliminate complex conditional statements.
    - Allow changing an algorithm at runtime.
    - Follow the Open/Closed Principle by allowing new behaviors
      without modifying existing code.

Problem it solves:
    Imagine an application responsible for calculating shipping costs.

    A beginner implementation may look like this:

        if shipping == "standard":
            ...
        elif shipping == "express":
            ...
        elif shipping == "priority":
            ...

    Every time a new shipping method is added, this function
    becomes larger and harder to maintain.

    The Strategy Pattern solves this by moving every algorithm
    into its own class.

Structure:
    Strategy
        Defines the common interface.

    Concrete Strategies
        Implement different algorithms.

    Context
        Stores a reference to a strategy object and delegates
        work to it.

When to use:
    - Multiple algorithms solve the same problem.
    - Different business rules should be selected dynamically.
    - Large conditional statements become difficult to maintain.
    - New behaviors are expected to be added frequently.
    - Runtime configuration determines application behavior.

Advantages:
    - Better separation of responsibilities.
    - Easier unit testing.
    - Removes duplicated conditional logic.
    - New strategies can be added without changing existing code.
    - Improves readability.
    - Encourages composition over inheritance.
    - Supports dependency injection.
    - Complies with SOLID principles.

Disadvantages:
    - Introduces additional classes.
    - Slightly increases project complexity.
    - Can be excessive for very small projects.

Common backend usage:
    - Payment providers (Stripe, PayPal, BLIK).
    - Authentication mechanisms (JWT, OAuth, API Keys).
    - Shipping cost calculation.
    - Tax calculation.
    - Discount systems.
    - File compression.
    - Serialization formats (JSON, XML, YAML).
    - Search algorithms.
    - Data validation.
    - Recommendation engines.

Real-world frameworks:
    - Django
    - Flask
    - FastAPI
    - Spring Boot
    - ASP.NET Core
    - Laravel
"""
from abc import ABC, abstractmethod
import unittest
import random


class DiscountStrategy(ABC):

    @abstractmethod
    def calculate(self, price: float) -> float:
        pass


class NoDiscountStrategy(DiscountStrategy):

    def calculate(self, price: float) -> float:
        return price


class PercentageDiscountStrategy(DiscountStrategy):

    def __init__(self, percent: float):
        self.percent = percent

    def calculate(self, price: float) -> float:
        return price * (1 - self.percent / 100)


class FixedDiscountStrategy(DiscountStrategy):

    def __init__(self, amount: float):
        self.amount = amount

    def calculate(self, price: float) -> float:
        return max(0, price - self.amount)


class ShoppingCart:

    def __init__(self, strategy: DiscountStrategy):
        self.strategy = strategy

    def checkout(self, price: float) -> float:
        return round(self.strategy.calculate(price), 2)




class StrategyTests(unittest.TestCase):

    def test_no_discount(self):
        cart = ShoppingCart(NoDiscountStrategy())

        self.assertEqual(cart.checkout(100), 100)

    def test_percentage_discount(self):
        cart = ShoppingCart(PercentageDiscountStrategy(20))

        self.assertEqual(cart.checkout(100), 80)

    def test_fixed_discount(self):
        cart = ShoppingCart(FixedDiscountStrategy(30))

        self.assertEqual(cart.checkout(100), 70)

    def test_discount_cannot_be_negative(self):
        cart = ShoppingCart(FixedDiscountStrategy(500))

        self.assertEqual(cart.checkout(100), 0)

    def test_strategy_can_be_changed(self):
        cart = ShoppingCart(NoDiscountStrategy())

        self.assertEqual(cart.checkout(100), 100)

        cart.strategy = PercentageDiscountStrategy(50)

        self.assertEqual(cart.checkout(100), 50)




class StrategyRandomTests(unittest.TestCase):

    def test_random_percentage_discounts(self):
        for _ in range(500):
            price = random.uniform(1, 10000)
            discount = random.uniform(0, 90)

            cart = ShoppingCart(PercentageDiscountStrategy(discount))

            expected = round(price * (1 - discount / 100), 2)

            self.assertEqual(cart.checkout(price), expected)

    def test_random_fixed_discounts(self):
        for _ in range(500):
            price = random.uniform(1, 5000)
            discount = random.uniform(0, 6000)

            cart = ShoppingCart(FixedDiscountStrategy(discount))

            expected = round(max(0, price - discount), 2)

            self.assertEqual(cart.checkout(price), expected)

    def test_random_strategy_selection(self):
        strategies = [
            NoDiscountStrategy(),
            PercentageDiscountStrategy(10),
            PercentageDiscountStrategy(25),
            PercentageDiscountStrategy(50),
            FixedDiscountStrategy(20),
            FixedDiscountStrategy(100)
        ]

        for _ in range(500):
            strategy = random.choice(strategies)
            cart = ShoppingCart(strategy)

            price = random.uniform(10, 5000)

            result = cart.checkout(price)

            self.assertGreaterEqual(result, 0)
            self.assertLessEqual(result, round(price, 2))

if __name__ == "__main__":
    unittest.main()