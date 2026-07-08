"""
Problem: Retry Service using Strategy Pattern

Category:
- Design Patterns
- Strategy Pattern
- Retry Logic
- Fault Tolerance

Description:
This project implements a retry service using the
Strategy design pattern.

The Strategy Pattern defines a family of algorithms,
encapsulates each one, and makes them interchangeable.

In this example:
- RetryStrategy defines the retry interface
- FixedRetry always uses the same delay
- ExponentialRetry doubles the delay after each attempt
- RetryExecutor executes operations using the selected strategy

This pattern is commonly used in:
- HTTP clients
- database connections
- cloud SDKs
- distributed systems
- message brokers

Features:
- interchangeable retry strategies
- reusable retry executor
- fault tolerance
- clean separation of concerns

Time Complexity:
- Execute operation: O(n)

Space Complexity:
- O(1)
"""
import random
import unittest
from abc import ABC, abstractmethod


class RetryStrategy(ABC):
    @abstractmethod
    def delays(self, attempts):
        pass


class FixedRetry(RetryStrategy):
    def delays(self, attempts):
        return [1] * attempts


class ExponentialRetry(RetryStrategy):
    def delays(self, attempts):
        delays = []
        delay = 1

        for _ in range(attempts):
            delays.append(delay)
            delay *= 2

        return delays


class RetryExecutor:
    def __init__(self, strategy):
        self.strategy = strategy

    def execute(self, operation, attempts):
        for delay in self.strategy.delays(attempts):

            if operation():
                return True

        return False


class TestStrategyPattern(unittest.TestCase):
    def test_fixed_retry_success(self):
        executor = RetryExecutor(FixedRetry())
        attempts = {"count": 0}

        def operation():
            attempts["count"] += 1

            return attempts["count"] == 3

        self.assertTrue(executor.execute(operation, 5))

    def test_fixed_retry_failure(self):
        executor = RetryExecutor(FixedRetry())
        self.assertFalse(executor.execute(lambda: False, 4))

    def test_exponential_retry(self):
        strategy = ExponentialRetry()
        self.assertEqual(strategy.delays(5), [1, 2, 4, 8, 16])

    def test_fixed_retry(self):
        strategy = FixedRetry()

        self.assertEqual(strategy.delays(4), [1, 1, 1, 1])


class TestRandom(unittest.TestCase):
    def test_random_retry(self):
        strategies = [FixedRetry(), ExponentialRetry()]

        for _ in range(100):
            strategy = random.choice(strategies)
            executor = RetryExecutor(strategy)
            success_after = random.randint(1, 5)
            counter = {"value": 0}

            def operation():
                counter["value"] += 1

                return counter["value"] >= success_after

            result = executor.execute(operation, 5)

            self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
