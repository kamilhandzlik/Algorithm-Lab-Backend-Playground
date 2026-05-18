"""
Problem: Cache System using Decorator Pattern

Category:
- Design Patterns
- Decorator Pattern
- Caching / Memoization

Description:
This project implements a simple cache system using the
Decorator design pattern.

The decorator stores previously computed function results.
If the function is called again with the same arguments,
the cached value is returned instantly instead of executing
the function again.

This technique is commonly used to improve performance in:
- backend applications
- API systems
- database queries
- recursive algorithms

Features:
- automatic caching
- reusable decorator
- faster repeated calls
- transparent function wrapping

Time Complexity:
- First call: depends on function
- Cached call: O(1)

Space Complexity:
- O(n)
"""

import unittest
import random


def cache(func):

    cached_results = {}

    def wrapper(*args):

        if args in cached_results:
            return cached_results[args]

        result = func(*args)

        cached_results[args] = result

        return result

    return wrapper


@cache
def fibonacci(n):

    if n <= 1:
        return n

    return fibonacci(n - 1) + fibonacci(n - 2)


class TestCacheDecorator(unittest.TestCase):

    def test_fibonacci(self):

        self.assertEqual(fibonacci(10), 55)

    def test_small_numbers(self):

        self.assertEqual(fibonacci(1), 1)
        self.assertEqual(fibonacci(2), 1)
        self.assertEqual(fibonacci(5), 5)

    def test_zero(self):

        self.assertEqual(fibonacci(0), 0)


class TestRandom(unittest.TestCase):

    def fibonacci_brute(self, n):

        if n <= 1:
            return n

        return (
            self.fibonacci_brute(n - 1)
            + self.fibonacci_brute(n - 2)
        )

    def test_random_values(self):

        for _ in range(20):

            n = random.randint(0, 15)

            self.assertEqual(
                fibonacci(n),
                self.fibonacci_brute(n)
            )


if __name__ == "__main__":

    unittest.main()