"""
   Repository Pattern

   Purpose:
       The Repository Pattern provides an abstraction layer between
       the business logic and the data source.

   When to use:
       - Working with databases.
       - Decoupling business logic from persistence.
       - Making unit testing easier by replacing real repositories
         with in-memory implementations or mocks.

   Advantages:
       - Improves maintainability.
       - Easier testing.
       - Allows changing the storage implementation without
         affecting business logic.

   Common backend usage:
       Django, FastAPI, Flask, Spring Boot, ASP.NET Core.
   """

from abc import ABC, abstractmethod
import unittest
import random
import string


class User:
    def __init__(self, user_id: int, name: str):
        self.id = user_id
        self.name = name

    def __eq__(self, other):
        return isinstance(other, User) and self.id == other.id and self.name == other.name

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}')"


class UserRepository(ABC):
    @abstractmethod
    def add(self, user: User):
        pass

    @abstractmethod
    def get(self, user_id: int):
        pass

    @abstractmethod
    def remove(self, user_id: int):
        pass

    @abstractmethod
    def list_all(self):
        pass


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self._users = {}

    def add(self, user: User):
        self._users[user.id] = user

    def get(self, user_id: int):
        return self._users.get(user_id)

    def remove(self, user_id: int):
        return self._users.pop(user_id, None)

    def list_all(self):
        return list(self._users.values())


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register_user(self, user_id: int, name: str):
        if self.repository.get(user_id):
            raise ValueError("User already exists")

        user = User(user_id, name)
        self.repository.add(user)
        return user

    def delete_user(self, user_id: int):
        if not self.repository.get(user_id):
            raise ValueError("User does not exist")

        self.repository.remove(user_id)

    def get_user(self, user_id: int):
        return self.repository.get(user_id)





class RepositoryTests(unittest.TestCase):

    def setUp(self):
        self.repo = InMemoryUserRepository()
        self.service = UserService(self.repo)

    def test_register_user(self):
        user = self.service.register_user(1, "John")

        self.assertEqual(user.id, 1)
        self.assertEqual(user.name, "John")
        self.assertEqual(self.service.get_user(1), user)

    def test_duplicate_user(self):
        self.service.register_user(1, "John")

        with self.assertRaises(ValueError):
            self.service.register_user(1, "Alice")

    def test_delete_user(self):
        self.service.register_user(10, "Kate")

        self.service.delete_user(10)

        self.assertIsNone(self.service.get_user(10))

    def test_delete_missing_user(self):
        with self.assertRaises(ValueError):
            self.service.delete_user(999)

    def test_list_all(self):
        self.service.register_user(1, "John")
        self.service.register_user(2, "Kate")
        self.service.register_user(3, "Mike")

        users = self.repo.list_all()

        self.assertEqual(len(users), 3)

class RepositoryRandomTests(unittest.TestCase):

    def random_name(self):
        length = random.randint(3, 12)
        return "".join(random.choice(string.ascii_letters) for _ in range(length))

    def test_random_insertions(self):
        repo = InMemoryUserRepository()
        service = UserService(repo)

        ids = random.sample(range(1, 100000), 500)

        for user_id in ids:
            service.register_user(user_id, self.random_name())

        self.assertEqual(len(repo.list_all()), 500)

        for user_id in ids:
            self.assertIsNotNone(service.get_user(user_id))

    def test_random_insert_delete(self):
        repo = InMemoryUserRepository()
        service = UserService(repo)

        ids = random.sample(range(1, 100000), 300)

        for user_id in ids:
            service.register_user(user_id, self.random_name())

        removed = random.sample(ids, 120)

        for user_id in removed:
            service.delete_user(user_id)

        expected = len(ids) - len(removed)

        self.assertEqual(len(repo.list_all()), expected)

        for user_id in removed:
            self.assertIsNone(service.get_user(user_id))

    def test_random_duplicate_insertions(self):
        repo = InMemoryUserRepository()
        service = UserService(repo)

        for _ in range(100):
            user_id = random.randint(1, 20)

            if service.get_user(user_id) is None:
                service.register_user(user_id, self.random_name())
            else:
                with self.assertRaises(ValueError):
                    service.register_user(user_id, self.random_name())


if __name__ == "__main__":
    unittest.main()