"""
Problem: Database Connection Manager using Singleton Pattern

Category:
- Design Patterns
- Singleton Pattern
- Database Management

Description:
This project implements a simple database connection manager
using the Singleton design pattern.

The goal is to ensure that the application uses only one
shared database connection instance during runtime.

Singleton is commonly used for:
- database connections
- configuration managers
- logging systems
- cache systems

Features:
- single shared instance
- centralized connection management
- shared application state
- memory optimization

Time Complexity:
- Instance access: O(1)

Space Complexity:
- O(1)
"""

import unittest
import random


class DatabaseConnection:

    _instance = None

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

            cls._instance.connected = False
            cls._instance.connection_id = random.randint(
                1000,
                9999
            )

        return cls._instance

    def connect(self):

        self.connected = True

        return (
            f"Connected to database "
            f"(id={self.connection_id})"
        )

    def disconnect(self):

        self.connected = False

        return "Disconnected"

    def status(self):

        return self.connected


class TestDatabaseConnection(unittest.TestCase):

    def test_singleton_instance(self):

        db1 = DatabaseConnection()
        db2 = DatabaseConnection()

        self.assertIs(db1, db2)

    def test_connection_status(self):

        db = DatabaseConnection()

        db.connect()

        self.assertTrue(
            db.status()
        )

    def test_disconnect(self):

        db = DatabaseConnection()

        db.connect()
        db.disconnect()

        self.assertFalse(
            db.status()
        )

    def test_same_connection_id(self):

        db1 = DatabaseConnection()
        db2 = DatabaseConnection()

        self.assertEqual(
            db1.connection_id,
            db2.connection_id
        )


class TestRandom(unittest.TestCase):

    def test_random_connections(self):

        ids = set()

        for _ in range(100):

            db = DatabaseConnection()

            ids.add(
                db.connection_id
            )

        self.assertEqual(
            len(ids),
            1
        )


if __name__ == "__main__":

    unittest.main()