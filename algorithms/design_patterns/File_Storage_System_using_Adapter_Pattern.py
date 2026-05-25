"""
Problem: File Storage System using Adapter Pattern

Category:
- Design Patterns
- Adapter Pattern
- File Management
- System Integration

Description:
This project implements a simple file storage system
using the Adapter design pattern.

The Adapter Pattern allows incompatible interfaces
to work together by wrapping existing classes with
a unified interface.

In this example:
- LocalStorage and CloudStorage have different APIs
- StorageAdapter provides a common interface
- the application can interact with both systems
  in the same way

This pattern is commonly used in:
- API integrations
- legacy system support
- third-party services
- payment gateways
- cloud providers

Features:
- unified storage interface
- integration of incompatible systems
- reusable adapter layer
- simplified storage handling

Time Complexity:
- Upload file: O(1)

Space Complexity:
- O(n)
"""

import unittest
import random
import string


class LocalStorage:

    def save_file(self, filename):

        return f"Saved {filename} locally"


class CloudStorage:

    def upload(self, filename):

        return f"Uploaded {filename} to cloud"


class StorageAdapter:

    def __init__(self, storage):

        self.storage = storage

    def store(self, filename):

        if isinstance(
            self.storage,
            LocalStorage
        ):

            return self.storage.save_file(
                filename
            )

        elif isinstance(
            self.storage,
            CloudStorage
        ):

            return self.storage.upload(
                filename
            )

        else:
            raise ValueError(
                "Unsupported storage type"
            )


class TestAdapterPattern(unittest.TestCase):

    def test_local_storage(self):

        storage = StorageAdapter(
            LocalStorage()
        )

        result = storage.store(
            "file.txt"
        )

        self.assertEqual(
            result,
            "Saved file.txt locally"
        )

    def test_cloud_storage(self):

        storage = StorageAdapter(
            CloudStorage()
        )

        result = storage.store(
            "image.png"
        )

        self.assertEqual(
            result,
            "Uploaded image.png to cloud"
        )

    def test_invalid_storage(self):

        class UnknownStorage:
            pass

        storage = StorageAdapter(
            UnknownStorage()
        )

        with self.assertRaises(
            ValueError
        ):

            storage.store("test.txt")


class TestRandom(unittest.TestCase):

    def random_filename(self):

        length = random.randint(5, 10)

        name = ''.join(
            random.choice(
                string.ascii_lowercase
            )
            for _ in range(length)
        )

        return f"{name}.txt"

    def test_random_files(self):

        storages = [
            LocalStorage(),
            CloudStorage()
        ]

        for _ in range(50):

            filename = self.random_filename()

            storage = StorageAdapter(
                random.choice(storages)
            )

            result = storage.store(
                filename
            )

            self.assertIn(
                filename,
                result
            )


if __name__ == "__main__":

    unittest.main()