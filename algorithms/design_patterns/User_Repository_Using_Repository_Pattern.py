"""
Problem: User Repository using Repository Pattern

Category:
- Design Patterns
- Repository Pattern
- Data Access
- Backend Architecture

Description:
This project implements a simple User Repository
using the Repository Pattern.

The Repository Pattern abstracts the data access layer,
allowing business logic to work independently from the
underlying storage mechanism.

In this example:
- User represents a domain model
- UserRepository manages persistence
- UserService contains business logic

The storage is implemented using an in-memory dictionary,
but it could easily be replaced with a SQL database,
NoSQL database, REST API or another data source.

This pattern is commonly used in:
- Django applications
- ASP.NET Core
- Spring Boot
- Laravel
- Clean Architecture
- Domain-Driven Design (DDD)

Features:
- CRUD operations
- separation of concerns
- storage abstraction
- reusable repository layer

Time Complexity:
- Add user: O(1)
- Find user: O(1)
- Delete user: O(1)

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

    def delete(self, user_id):
        return self.users.pop(user_id, None)

    def count(self):
        return len(self.users)


class UserService:

    def __init__(self, repository):
        self.repository = repository

    def register(self, user_id, name):
        self.repository.add(User(user_id, name))

    def find(self, user_id):
        return self.repository.get(user_id)

    def remove(self, user_id):
        self.repository.delete(user_id)


class TestRepositoryPattern(unittest.TestCase):

    def test_register_user(self):

        repository = UserRepository()
        service = UserService(repository)

        service.register(1, "Alice")

        self.assertEqual(repository.count(),1)

    def test_find_user(self):

        repository = UserRepository()
        service = UserService(repository)

        service.register(2, "Bob")

        user = service.find(2)

        self.assertEqual(user.name,"Bob")

    def test_delete_user(self):

        repository = UserRepository()
        service = UserService(repository)

        service.register(3, "Charlie")
        service.remove(3)

        self.assertIsNone(service.find(3))

    def test_unknown_user(self):

        repository = UserRepository()
        service = UserService(repository)

        self.assertIsNone(service.find(999))


class TestRandom(unittest.TestCase):

    def test_random_users(self):

        repository = UserRepository()
        service = UserService(repository)

        expected = {}

        for user_id in range(100):

            name = f"User{random.randint(1, 10000)}"

            service.register(user_id, name)

            expected[user_id] = name

        self.assertEqual(repository.count(),100)

        for user_id, name in expected.items():

            self.assertEqual(service.find(user_id).name,name)


if __name__ == "__main__":
    unittest.main()