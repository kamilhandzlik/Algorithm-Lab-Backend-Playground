"""
Problem: Search Engine using Specification Pattern

Category:
- Design Patterns
- Specification Pattern
- Filtering
- Query Systems

Description:
This project implements a simple search engine using
the Specification design pattern.

The Specification Pattern allows business rules and
filter conditions to be encapsulated into reusable
objects that can be combined together.

In this example:
- products can be filtered by category
- products can be filtered by price
- specifications can be combined using AND logic

This pattern is commonly used in:
- e-commerce platforms
- search engines
- database query builders
- ORM frameworks
- business rule systems

Features:
- reusable filtering rules
- composable specifications
- clean query logic
- extensible search system

Time Complexity:
- Search: O(n)

Space Complexity:
- O(n)
"""

import unittest
import random
from abc import ABC, abstractmethod


class Product:

    def __init__(
        self,
        name,
        category,
        price
    ):

        self.name = name
        self.category = category
        self.price = price


class Specification(ABC):

    @abstractmethod
    def is_satisfied_by(
        self,
        item
    ):
        pass

    def __and__(
        self,
        other
    ):

        return AndSpecification(
            self,
            other
        )


class CategorySpecification(
    Specification
):

    def __init__(
        self,
        category
    ):

        self.category = category

    def is_satisfied_by(
        self,
        item
    ):

        return (
            item.category
            == self.category
        )


class PriceSpecification(
    Specification
):

    def __init__(
        self,
        max_price
    ):

        self.max_price = max_price

    def is_satisfied_by(
        self,
        item
    ):

        return (
            item.price
            <= self.max_price
        )


class AndSpecification(
    Specification
):

    def __init__(
        self,
        left,
        right
    ):

        self.left = left
        self.right = right

    def is_satisfied_by(
        self,
        item
    ):

        return (
            self.left.is_satisfied_by(item)
            and
            self.right.is_satisfied_by(item)
        )


class ProductFilter:

    def filter(
        self,
        products,
        specification
    ):

        return [
            product
            for product in products
            if specification.is_satisfied_by(
                product
            )
        ]


class TestSpecificationPattern(
    unittest.TestCase
):

    def setUp(self):

        self.products = [

            Product(
                "Laptop",
                "Electronics",
                3000
            ),

            Product(
                "Mouse",
                "Electronics",
                100
            ),

            Product(
                "Book",
                "Education",
                50
            )
        ]

    def test_category_filter(self):

        spec = CategorySpecification(
            "Electronics"
        )

        result = ProductFilter().filter(
            self.products,
            spec
        )

        self.assertEqual(
            len(result),
            2
        )

    def test_price_filter(self):

        spec = PriceSpecification(
            100
        )

        result = ProductFilter().filter(
            self.products,
            spec
        )

        self.assertEqual(
            len(result),
            2
        )

    def test_combined_filter(self):

        spec = (
            CategorySpecification(
                "Electronics"
            )
            &
            PriceSpecification(
                500
            )
        )

        result = ProductFilter().filter(
            self.products,
            spec
        )

        self.assertEqual(
            len(result),
            1
        )

        self.assertEqual(
            result[0].name,
            "Mouse"
        )


class TestRandom(unittest.TestCase):

    def test_random_products(self):

        categories = [
            "Electronics",
            "Books",
            "Games"
        ]

        products = []

        for i in range(100):

            products.append(

                Product(
                    f"Product{i}",
                    random.choice(
                        categories
                    ),
                    random.randint(
                        10,
                        1000
                    )
                )
            )

        spec = PriceSpecification(
            500
        )

        result = ProductFilter().filter(
            products,
            spec
        )

        self.assertTrue(

            all(
                product.price <= 500
                for product in result
            )
        )


if __name__ == "__main__":

    unittest.main()