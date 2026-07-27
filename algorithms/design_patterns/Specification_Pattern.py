"""
Specification Pattern

Description:
    The Specification Pattern is a behavioral design pattern used to
    encapsulate business rules into reusable specification objects.

    Instead of scattering validation rules and filtering logic across
    multiple methods, each rule is represented by a separate class.

    Specifications can also be combined using logical operations
    such as AND, OR and NOT, making complex business rules easy to
    build and understand.

Purpose:
    - Encapsulate business rules.
    - Create reusable filtering logic.
    - Avoid duplicated validation code.
    - Build complex queries from smaller rules.
    - Improve readability and maintainability.

Problem it solves:
    Imagine an e-commerce application where customers can be filtered
    according to many different rules.

        if customer.age >= 18 and customer.is_active and customer.points > 1000:
            ...

        if customer.age >= 18 and customer.country == "USA":
            ...

        if customer.is_active and customer.points > 500:
            ...

    As the application grows, similar conditions begin appearing
    throughout the project.

    The Specification Pattern extracts every rule into its own object.
    These rules can later be combined without duplicating logic.

Structure:
    Specification
        Declares the is_satisfied_by() interface.

    Concrete Specification
        Implements one business rule.

    Composite Specification
        Combines multiple specifications using logical operators.

When to use:
    - Complex filtering.
    - Business rule validation.
    - Search systems.
    - Product filtering.
    - Permission checking.
    - User eligibility validation.
    - Domain-Driven Design.

Advantages:
    - Reusable business rules.
    - Easy unit testing.
    - Eliminates duplicated conditions.
    - Easy to extend.
    - Improves readability.
    - Supports composition of rules.
    - Follows the Open/Closed Principle.

Disadvantages:
    - Requires additional classes.
    - May be excessive for very small projects.

Common backend usage:
    - Product search.
    - User filtering.
    - Permission systems.
    - Discount eligibility.
    - Order validation.
    - Loan approval systems.

Real-world frameworks:
    - Spring Boot
    - ASP.NET Core
    - Django
    - FastAPI
    - Flask
"""
from abc import ABC, abstractmethod
import random
import unittest


class Customer:

    def __init__(self, age: int, points: int, active: bool):
        self.age = age
        self.points = points
        self.active = active


class Specification(ABC):

    @abstractmethod
    def is_satisfied_by(self, item):
        pass


class AdultSpecification(Specification):

    def is_satisfied_by(self, customer: Customer):
        return customer.age >= 18


class ActiveSpecification(Specification):

    def is_satisfied_by(self, customer: Customer):
        return customer.active


class PremiumSpecification(Specification):

    def is_satisfied_by(self, customer: Customer):
        return customer.points >= 1000


class AndSpecification(Specification):

    def __init__(self, left: Specification, right: Specification):
        self.left = left
        self.right = right

    def is_satisfied_by(self, customer: Customer):
        return (
                self.left.is_satisfied_by(customer)
                and self.right.is_satisfied_by(customer)
        )


class CustomerFilter:

    def filter(self, customers, specification):
        return [
            customer
            for customer in customers
            if specification.is_satisfied_by(customer)
        ]


class SpecificationTests(unittest.TestCase):

    def setUp(self):
        self.customers = [
            Customer(25, 1500, True),
            Customer(17, 2000, True),
            Customer(35, 500, True),
            Customer(40, 1800, False)
        ]

        self.filter = CustomerFilter()

    def test_adult_specification(self):
        spec = AdultSpecification()

        result = self.filter.filter(self.customers, spec)

        self.assertEqual(len(result), 3)

    def test_active_specification(self):
        spec = ActiveSpecification()

        result = self.filter.filter(self.customers, spec)

        self.assertEqual(len(result), 3)

    def test_premium_specification(self):
        spec = PremiumSpecification()

        result = self.filter.filter(self.customers, spec)

        self.assertEqual(len(result), 3)

    def test_and_specification(self):
        spec = AndSpecification(
            AdultSpecification(),
            PremiumSpecification()
        )

        result = self.filter.filter(self.customers, spec)

        self.assertEqual(len(result), 2)

    def test_adult_and_active(self):
        spec = AndSpecification(
            AdultSpecification(),
            ActiveSpecification()
        )

        result = self.filter.filter(self.customers, spec)

        self.assertEqual(len(result), 2)


class SpecificationRandomTests(unittest.TestCase):

    def random_customer(self):
        return Customer(
            age=random.randint(10, 80),
            points=random.randint(0, 3000),
            active=random.choice([True, False])
        )

    def test_random_adult_filter(self):
        customers = [
            self.random_customer()
            for _ in range(500)
        ]

        spec = AdultSpecification()
        customer_filter = CustomerFilter()

        result = customer_filter.filter(customers, spec)

        for customer in result:
            self.assertGreaterEqual(customer.age, 18)

    def test_random_premium_filter(self):
        customers = [
            self.random_customer()
            for _ in range(500)
        ]

        spec = PremiumSpecification()
        customer_filter = CustomerFilter()

        result = customer_filter.filter(customers, spec)

        for customer in result:
            self.assertGreaterEqual(customer.points, 1000)

    def test_random_and_specification(self):
        customers = [
            self.random_customer()
            for _ in range(1000)
        ]

        spec = AndSpecification(
            AdultSpecification(),
            ActiveSpecification()
        )

        customer_filter = CustomerFilter()

        result = customer_filter.filter(customers, spec)

        for customer in result:
            self.assertGreaterEqual(customer.age, 18)
            self.assertTrue(customer.active)

    def test_random_combined_specifications(self):
        customers = [
            self.random_customer()
            for _ in range(1000)
        ]

        spec = AndSpecification(
            AndSpecification(
                AdultSpecification(),
                ActiveSpecification()
            ),
            PremiumSpecification()
        )

        customer_filter = CustomerFilter()

        result = customer_filter.filter(customers, spec)

        for customer in result:
            self.assertGreaterEqual(customer.age, 18)
            self.assertTrue(customer.active)
            self.assertGreaterEqual(customer.points, 1000)


if __name__ == "__main__":
    unittest.main()
