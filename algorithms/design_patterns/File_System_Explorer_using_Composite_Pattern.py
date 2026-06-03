"""
Problem: File System Explorer using Composite Pattern

Category:
- Design Patterns
- Composite Pattern
- File Systems
- Tree Structures

Description:
This project implements a simple file system explorer
using the Composite design pattern.

The Composite Pattern allows individual objects and
groups of objects to be treated uniformly.

In this example:
- File represents a leaf node
- Directory represents a composite node
- both share a common interface

This pattern is commonly used in:
- file systems
- GUI component trees
- organization hierarchies
- menu systems
- document structures

Features:
- hierarchical object structure
- recursive traversal
- unified interface
- tree-based navigation

Time Complexity:
- Traverse structure: O(n)

Space Complexity:
- O(n)
"""

import unittest
import random
import string
from abc import ABC, abstractmethod


class FileSystemNode(ABC):

    @abstractmethod
    def get_size(self):
        pass


class File(FileSystemNode):

    def __init__(self, name, size):

        self.name = name
        self.size = size

    def get_size(self):

        return self.size


class Directory(FileSystemNode):

    def __init__(self, name):

        self.name = name
        self.children = []

    def add(self, node):

        self.children.append(node)

    def get_size(self):

        return sum(
            child.get_size()
            for child in self.children
        )


class TestCompositePattern(unittest.TestCase):

    def test_single_file(self):

        file = File(
            "document.txt",
            100
        )

        self.assertEqual(
            file.get_size(),
            100
        )

    def test_directory_size(self):

        directory = Directory(
            "root"
        )

        directory.add(
            File("a.txt", 100)
        )

        directory.add(
            File("b.txt", 200)
        )

        self.assertEqual(
            directory.get_size(),
            300
        )

    def test_nested_directories(self):

        root = Directory("root")

        images = Directory("images")

        images.add(
            File("cat.png", 150)
        )

        images.add(
            File("dog.png", 250)
        )

        root.add(images)

        self.assertEqual(
            root.get_size(),
            400
        )

    def test_empty_directory(self):

        directory = Directory(
            "empty"
        )

        self.assertEqual(
            directory.get_size(),
            0
        )


class TestRandom(unittest.TestCase):

    def random_name(self):

        length = random.randint(5, 10)

        return ''.join(
            random.choice(
                string.ascii_lowercase
            )
            for _ in range(length)
        )

    def test_random_files(self):

        directory = Directory(
            "root"
        )

        expected_size = 0

        for _ in range(50):

            size = random.randint(
                1,
                1000
            )

            expected_size += size

            directory.add(
                File(
                    self.random_name(),
                    size
                )
            )

        self.assertEqual(
            directory.get_size(),
            expected_size
        )


if __name__ == "__main__":

    unittest.main()