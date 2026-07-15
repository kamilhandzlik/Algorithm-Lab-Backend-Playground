"""
Problem: Transaction Manager using Unit of Work Pattern

Category:
- Design Patterns
- Unit of Work Pattern
- Transactions
- Persistence

Description:
This project implements a simple transaction manager
using the Unit of Work Pattern.

The Unit of Work Pattern keeps track of changes made
to business objects during a transaction and commits
all changes as a single unit.

In this example:
- UserRepository stores users
- UnitOfWork tracks pending operations
- commit() applies all changes
- rollback() discards pending changes

This pattern is commonly used in:
- Entity Framework
- SQLAlchemy
- NHibernate
- Domain-Driven Design
- enterprise applications

Features:
- transaction management
- deferred persistence
- commit and rollback
- centralized change tracking

Time Complexity:
- Register operation: O(1)
- Commit: O(n)

Space Complexity:
- O(n)
"""

import random
import unittest


class User:

    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name


class UserRepository:

    def __init__(self):
        self.users = {}

    def add(self, user):
        self.users[user.user_id] = user

    def get(self, user_id):
        return self.users.get(user_id)

    def count(self):
        return len(self.users)


class UnitOfWork:

    def __init__(self, repository):
        self.repository = repository
        self.new_objects = []

    def register_new(self, user):
        self.new_objects.append(user)

    def commit(self):

        for user in self.new_objects:
            self.repository.add(user)

        self.new_objects.clear()

    def rollback(self):
        self.new_objects.clear()


class TestUnitOfWorkPattern(unittest.TestCase):

    def test_commit(self):

        repository = UserRepository()
        uow = UnitOfWork(repository)

        uow.register_new(User(1, "Alice"))
        uow.commit()

        self.assertEqual(repository.count(),1)

    def test_rollback(self):

        repository = UserRepository()
        uow = UnitOfWork(repository)

        uow.register_new(User(1, "Alice"))
        uow.rollback()

        self.assertEqual(repository.count(),0)

    def test_multiple_users(self):

        repository = UserRepository()
        uow = UnitOfWork(repository)

        uow.register_new(User(1, "Alice"))
        uow.register_new(User(2, "Bob"))
        uow.register_new(User(3, "Charlie"))

        uow.commit()

        self.assertEqual(repository.count(),3)

    def test_find_user(self):

        repository = UserRepository()
        uow = UnitOfWork(repository)

        uow.register_new(User(10, "David"))
        uow.commit()

        self.assertEqual( repository.get(10).name,"David")


class TestRandom(unittest.TestCase):

    def test_random_users(self):

        repository = UserRepository()
        uow = UnitOfWork(repository)

        total = random.randint(50, 150)

        for user_id in range(total):

            user = User( user_id,f"User{random.randint(1000, 9999)}")

            uow.register_new(user)

        uow.commit()

        self.assertEqual(repository.count(),total)


if __name__ == "__main__":
    unittest.main()