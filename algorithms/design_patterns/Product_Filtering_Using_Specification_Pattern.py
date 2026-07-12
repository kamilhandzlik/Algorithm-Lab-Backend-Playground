"""
Problem: Product Filtering using Specification Pattern

Category:
- Design Patterns
- Specification Pattern
- Business Rules
- Product Filtering

Description:
This project implements a product filtering system
using the Specification Pattern.

The Specification Pattern encapsulates business rules
into reusable objects that can be combined to create
complex filtering logic.

In this example:
- Product represents a store item
- Specification defines filtering criteria
- ColorSpecification filters by color
- PriceSpecification filters by maximum price
- AndSpecification combines multiple specifications

This pattern is commonly used in:
- e-commerce applications
- search engines
- rule engines
- inventory systems
- Domain-Driven Design (DDD)

Features:
- reusable business rules
- composable specifications
- flexible filtering
- clean separation of concerns

Time Complexity:
- Filter products: O(n)

Space Complexity:
- O(n)
"""

import random
import unittest
from abc import ABC, abstractmethod


class Product:

    def __init__(self, name, color, price):
        self.name = name
        self.color = color
        self.price = price


class Specification(ABC):

    @abstractmethod
    def is_satisfied(self, product):
        pass


class ColorSpecification(Specification):

    def __init__(self, color):
        self.color = color

    def is_satisfied(self, product):
        return product.color == self.color


class PriceSpecification(Specification):

    def __init__(self, max_price):
        self.max_price = max_price

    def is_satisfied(self, product):
        return product.price <= self.max_price


class AndSpecification(Specification):

    def __init__(self, first, second):
        self.first = first
        self.second = second

    def is_satisfied(self, product):
        return (self.first.is_satisfied(product) and self.second.is_satisfied(product))


class ProductFilter:

    def filter(self, products, specification):
        return [product for product in products if specification.is_satisfied(product)]


class TestSpecificationPattern(unittest.TestCase):

    def setUp(self):
        self.products = [
            Product("Laptop", "black", 5000),
            Product("Mouse", "black", 120),
            Product("Keyboard", "white", 250),
            Product("Monitor", "black", 1800)
        ]

        self.filter = ProductFilter()

    def test_color_filter(self):
        specification = ColorSpecification("black")

        result = self.filter.filter(self.products, specification)

        self.assertEqual(len(result), 3)

    def test_price_filter(self):
        specification = PriceSpecification(500)

        result = self.filter.filter(self.products, specification)

        self.assertEqual(len(result), 2)

    def test_combined_filter(self):
        specification = AndSpecification(ColorSpecification("black"), PriceSpecification(2000))

        result = self.filter.filter(self.products, specification)

        self.assertEqual(len(result), 2)

    def test_empty_result(self):
        specification = AndSpecification(ColorSpecification("red"), PriceSpecification(100))

        result = self.filter.filter(self.products, specification)

        self.assertEqual(len(result), 0)


class TestRandom(unittest.TestCase):

    def test_random_products(self):

        colors = ["black", "white", "red", "blue"]

        products = []

        for i in range(100):
            products.append(Product(f"Product{i}",random.choice(colors), random.randint(50, 5000)))

        specification = AndSpecification(ColorSpecification("black"), PriceSpecification(1000))

        result = ProductFilter().filter(products, specification)

        for product in result:
            self.assertEqual(product.color, "black")

            self.assertLessEqual(product.price, 1000)


if __name__ == "__main__":
    unittest.main()
