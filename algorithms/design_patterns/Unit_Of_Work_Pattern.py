"""
Unit of Work Pattern

Description:
    The Unit of Work Pattern is a behavioral design pattern that
    coordinates a group of database operations as a single transaction.

    Instead of committing every operation independently, the Unit of
    Work collects changes and commits them together.

    If every operation succeeds, the Unit of Work commits the transaction.

    If any operation fails, the Unit of Work rolls back the entire
    transaction so that the database is not left in a partially modified
    state.

    The pattern is especially useful when one business operation requires
    changes to multiple repositories or database tables.

Purpose:
    - Group multiple database operations into one transaction.
    - Maintain data consistency.
    - Provide atomic business operations.
    - Centralize commit and rollback logic.
    - Keep transaction management outside business logic.
    - Coordinate multiple repositories.

Problem it solves:
    Imagine an e-commerce application processing an order.

    Creating an order may require:

        - Creating an Order record.
        - Reducing product inventory.
        - Creating a Payment record.
        - Creating an Invoice record.

    If the application saves the order first and then the inventory
    update fails, the database may contain an order that cannot actually
    be fulfilled.

    A Unit of Work treats all these operations as one transaction.

        BEGIN TRANSACTION

        Create Order
        Update Inventory
        Create Payment
        Create Invoice

        COMMIT

    If something fails:

        ROLLBACK

    This guarantees that the database either contains all changes or
    none of them.

Structure:
    Unit of Work
        Controls the transaction lifecycle.

    Repositories
        Perform operations on individual types of data.

    Service
        Contains business logic and coordinates the operation.

    Database
        Commits or rolls back the transaction.

Typical workflow:
    Service
        ↓
    Unit of Work
        ↓
    Order Repository
        ↓
    Inventory Repository
        ↓
    Payment Repository
        ↓
    Commit

    If an error occurs:
        ↓
    Rollback

When to use:
    - Multiple database changes must be atomic.
    - One business operation modifies multiple repositories.
    - Transactions span multiple tables.
    - Complex business workflows require consistency.
    - Database operations should be committed explicitly.

Advantages:
    - Protects database consistency.
    - Centralizes transaction management.
    - Makes business operations atomic.
    - Simplifies rollback.
    - Works well with Repository Pattern.
    - Makes transaction boundaries explicit.
    - Improves testability.

Disadvantages:
    - Adds an additional abstraction layer.
    - Requires careful transaction management.
    - Can become complicated when transactions are very large.
    - Not every operation requires a Unit of Work.

Common backend usage:
    - E-commerce order processing.
    - Banking transactions.
    - Inventory management.
    - Booking systems.
    - Financial systems.
    - Account creation.
    - Multi-table database operations.

Real-world technologies:
    - SQLAlchemy
    - Django ORM
    - PostgreSQL
    - Entity Framework
    - Hibernate
    - Spring Data

Important concept:
    The Unit of Work is responsible for the transaction boundary,
    while repositories are responsible for data access.

    Repository answers:
        "How do I access this data?"

    Unit of Work answers:
        "Which operations belong to the same transaction?"
"""
from abc import ABC, abstractmethod
import unittest
import random


class Database:

    def __init__(self):
        self.orders = []
        self.inventory = {}
        self._backup = None

    def begin(self):
        self._backup = (self.orders.copy(), self.inventory.copy())

    def commit(self):
        self._backup = None

    def rollback(self):
        self.orders = self._backup[0]
        self.inventory = self._backup[1]
        self._backup = None


class OrderRepository:
    def __init__(self, database: Database):
        self.database = database

    def add(self, order):
        self.database.orders.append(order)


class InventoryRepository:
    def __init__(self, database: Database):
        self.database = database

    def add_product(self, product_id: int, quantity: int):
        self.database.inventory[product_id] = quantity

    def remove_stock(self, product_id: int, quantity: int):
        if product_id not in self.database.inventory:
            raise ValueError("Product does not exist")

        if self.database.inventory[product_id] < quantity:
            raise ValueError("Not enough stock")

        self.database.inventory[product_id] -= quantity


class UnitOfWork(ABC):

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_value, traceback):
        pass


class DatabaseUnitOfWork(UnitOfWork):
    def __init__(self, database: Database):
        self.database = database
        self.orders = OrderRepository(database)
        self.inventory = InventoryRepository(database)

    def __enter__(self):
        self.database.begin()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.database.commit()
        else:
            self.database.rollback()

        return False


class OrderService:

    def __init__(self, unit_of_work: DatabaseUnitOfWork):
        self.unit_of_work = unit_of_work

    def create_order(self, order_id: int, product_id: int, quantity: int):
        with self.unit_of_work as uow:
            uow.orders.add({"id": order_id, "product_id": product_id, "quantity": quantity})

            uow.inventory.remove_stock(product_id, quantity)


class UnitOfWorkTests(unittest.TestCase):

    def setUp(self):
        self.database = Database()

        self.database.inventory = {1: 100, 2: 50}

        self.unit_of_work = DatabaseUnitOfWork(self.database)

        self.service = OrderService(self.unit_of_work)

    def test_successful_transaction(self):
        self.service.create_order(order_id=1, product_id=1, quantity=10)

        self.assertEqual(len(self.database.orders), 1)

        self.assertEqual(self.database.inventory[1], 90)

    def test_transaction_rolls_back(self):
        with self.assertRaises(ValueError):
            self.service.create_order(order_id=1, product_id=1, quantity=200)

        self.assertEqual(len(self.database.orders), 0)

        self.assertEqual(self.database.inventory[1], 100)

    def test_missing_product_rolls_back(self):
        with self.assertRaises(ValueError):
            self.service.create_order(order_id=1, product_id=999, quantity=10)

        self.assertEqual(
            len(self.database.orders), 0)

    def test_multiple_successful_transactions(self):
        self.service.create_order(order_id=1, product_id=1, quantity=20)

        self.service.create_order(order_id=2, product_id=2, quantity=10)

        self.assertEqual(len(self.database.orders), 2)

        self.assertEqual(self.database.inventory[1], 80)

        self.assertEqual(self.database.inventory[2], 40)

    def test_context_manager(self):
        with self.unit_of_work as uow:
            uow.orders.add({"id": 10, "product_id": 1, "quantity": 5})

        self.assertEqual(len(self.database.orders), 1)


class UnitOfWorkRandomTests(unittest.TestCase):

    def create_database(self):
        database = Database()

        database.inventory = {product_id: random.randint(50, 500) for product_id in range(1, 21)}

        return database

    def test_random_successful_transactions(self):
        database = self.create_database()

        unit_of_work = DatabaseUnitOfWork(database)

        service = OrderService(unit_of_work)

        successful_orders = 0

        for order_id in range(1, 501):
            product_id = random.randint(1, 20)
            available = database.inventory[product_id]

            if available == 0:
                continue

            quantity = random.randint(1, min(10, available))

            service.create_order(order_id, product_id, quantity)

            successful_orders += 1

        self.assertEqual(len(database.orders), successful_orders)

    def test_random_failed_transactions(self):
        database = self.create_database()

        unit_of_work = DatabaseUnitOfWork(database)

        service = OrderService(unit_of_work)

        for order_id in range(1, 200):
            product_id = random.randint(1, 20)
            initial_stock = database.inventory[product_id]

            with self.assertRaises(ValueError):
                service.create_order(order_id, product_id, initial_stock + 1)

            self.assertEqual(database.inventory[product_id], initial_stock)

            self.assertEqual(len(database.orders), 0)

    def test_random_transaction_integrity(self):
        database = self.create_database()

        unit_of_work = DatabaseUnitOfWork(database)

        service = OrderService(unit_of_work)

        initial_inventory = database.inventory.copy()

        for order_id in range(1, 300):
            product_id = random.randint(1, 20)
            quantity = random.randint(1, 1000)

            try:
                service.create_order(order_id, product_id, quantity)
            except ValueError:
                self.assertEqual(
                    database.inventory,
                    {key: value for key, value in database.inventory.items()})

        for product_id, quantity in database.inventory.items():
            self.assertLessEqual(quantity, initial_inventory[product_id])

            self.assertGreaterEqual(quantity, 0)


if __name__ == "__main__":
    unittest.main()