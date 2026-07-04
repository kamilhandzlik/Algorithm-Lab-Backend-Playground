"""
Problem: File Storage Service using Adapter Pattern

Category:
- Design Patterns
- Adapter Pattern
- File Storage
- Cloud Services

Description:
This project implements a file storage service using
the Adapter design pattern.

The Adapter Pattern allows incompatible interfaces to
work together without modifying their original code.

In this example:
- LocalStorage stores files locally
- CloudStorage uses a different interface
- CloudStorageAdapter adapts the cloud interface
  to match the storage interface expected by clients

This pattern is commonly used in:
- cloud storage integrations
- payment gateways
- third-party APIs
- legacy system integration
- external libraries

Features:
- unified storage interface
- support for multiple providers
- easy provider replacement
- loose coupling

Time Complexity:
- Upload file: O(1)

Space Complexity:
- O(1)
"""

import random
import string
import unittest
from abc import ABC, abstractmethod


class Storage(ABC):

    @abstractmethod
    def upload(self, filename):
        pass


class LocalStorage(Storage):

    def upload(self, filename):
        return f"Stored {filename} locally"


class CloudStorage:

    def send_file(self, filename):
        return f"Uploaded {filename} to cloud"


class CloudStorageAdapter(Storage):

    def __init__(self, cloud_storage):
        self.cloud_storage = cloud_storage

    def upload(self, filename):
        return self.cloud_storage.send_file(filename)


class FileService:

    def __init__(self, storage):
        self.storage = storage

    def save(self, filename):
        return self.storage.upload(filename)


class TestAdapterPattern(unittest.TestCase):

    def test_local_storage(self):

        service = FileService(LocalStorage())

        result = service.save("photo.png")

        self.assertEqual(
            result,
            "Stored photo.png locally"
        )

    def test_cloud_storage(self):

        adapter = CloudStorageAdapter(
            CloudStorage()
        )

        service = FileService(adapter)

        result = service.save("photo.png")

        self.assertEqual(
            result,
            "Uploaded photo.png to cloud"
        )

    def test_multiple_uploads(self):

        service = FileService(LocalStorage())

        self.assertEqual(
            service.save("a.txt"),
            "Stored a.txt locally"
        )

        self.assertEqual(
            service.save("b.txt"),
            "Stored b.txt locally"
        )

    def test_adapter_type(self):

        adapter = CloudStorageAdapter(
            CloudStorage()
        )

        self.assertIsInstance(
            adapter,
            Storage
        )


class TestRandom(unittest.TestCase):

    def random_filename(self):

        name = "".join(
            random.choice(string.ascii_lowercase)
            for _ in range(8)
        )

        extension = random.choice(
            [
                ".txt",
                ".png",
                ".pdf",
                ".jpg"
            ]
        )

        return name + extension

    def test_random_uploads(self):

        services = [
            FileService(LocalStorage()),
            FileService(
                CloudStorageAdapter(
                    CloudStorage()
                )
            )
        ]

        for _ in range(100):

            filename = self.random_filename()

            service = random.choice(services)

            result = service.save(filename)

            self.assertIn(
                filename,
                result
            )


if __name__ == "__main__":
    unittest.main()