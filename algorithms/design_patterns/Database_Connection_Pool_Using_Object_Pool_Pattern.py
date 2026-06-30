"""
Problem: Database Connection Pool using Object Pool Pattern

Category:
- Design Patterns
- Object Pool Pattern
- Database
- Resource Management

Description:
This project implements a simple database connection pool
using the Object Pool design pattern.

The Object Pool Pattern manages a set of reusable objects,
avoiding the overhead of creating and destroying expensive
resources repeatedly.

In this example:
- DatabaseConnection represents a database connection
- ConnectionPool manages available connections
- connections are borrowed and returned to the pool

This pattern is commonly used in:
- database connection pools
- thread pools
- HTTP client pools
- socket management
- cloud resource management

Features:
- reusable resources
- limited pool size
- connection recycling
- efficient resource management

Time Complexity:
- Acquire connection: O(1)
- Release connection: O(1)

Space Complexity:
- O(n)
"""

import random
import unittest


class DatabaseConnection:

    def __init__(self, connection_id):
        self.connection_id = connection_id


class ConnectionPool:

    def __init__(self, size):
        self.available = [
            DatabaseConnection(i)
            for i in range(size)
        ]
        self.in_use = []

    def acquire(self):

        if not self.available:
            return None

        connection = self.available.pop()
        self.in_use.append(connection)

        return connection

    def release(self, connection):

        if connection in self.in_use:
            self.in_use.remove(connection)
            self.available.append(connection)

    def available_count(self):
        return len(self.available)

    def in_use_count(self):
        return len(self.in_use)


class TestObjectPoolPattern(unittest.TestCase):

    def test_acquire_connection(self):

        pool = ConnectionPool(3)

        connection = pool.acquire()

        self.assertIsNotNone(connection)
        self.assertEqual(pool.available_count(), 2)
        self.assertEqual(pool.in_use_count(), 1)

    def test_release_connection(self):

        pool = ConnectionPool(2)

        connection = pool.acquire()
        pool.release(connection)

        self.assertEqual(pool.available_count(), 2)
        self.assertEqual(pool.in_use_count(), 0)

    def test_pool_exhausted(self):

        pool = ConnectionPool(1)

        pool.acquire()

        self.assertIsNone(pool.acquire())

    def test_reuse_connection(self):

        pool = ConnectionPool(1)

        connection = pool.acquire()
        pool.release(connection)

        reused = pool.acquire()

        self.assertIs(connection, reused)


class TestRandom(unittest.TestCase):

    def test_random_operations(self):

        pool = ConnectionPool(10)

        borrowed = []

        for _ in range(100):

            if borrowed and random.choice([True, False]):

                connection = random.choice(borrowed)
                borrowed.remove(connection)
                pool.release(connection)

            else:

                connection = pool.acquire()

                if connection:
                    borrowed.append(connection)

        self.assertEqual(
            pool.available_count() + pool.in_use_count(),
            10
        )


if __name__ == "__main__":
    unittest.main()