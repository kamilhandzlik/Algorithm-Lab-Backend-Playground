"""
Template Method Pattern

Description:
    The Template Method Pattern is a behavioral design pattern that
    defines the skeleton of an algorithm in a base class while allowing
    subclasses to override specific steps without changing the overall
    algorithm.

    The parent class controls the order of execution, while subclasses
    customize individual operations.

    This ensures that every implementation follows the same workflow
    while still allowing flexibility where needed.

Purpose:
    - Define a fixed workflow.
    - Allow subclasses to customize individual steps.
    - Eliminate duplicated algorithm structure.
    - Promote code reuse.
    - Standardize business processes.

Problem it solves:
    Imagine a system that imports different file formats.

    Every import follows the same sequence:

        Read file
        Validate data
        Transform records
        Save data
        Generate report

    However, each file format requires different parsing and
    transformation logic.

    Without the Template Method Pattern, every importer would
    duplicate the same workflow.

    The Template Method Pattern places the common algorithm in one
    base class while subclasses implement only the steps that differ.

Structure:
    Abstract Class
        Defines the template method containing the algorithm.

    Primitive Operations
        Abstract methods implemented by subclasses.

    Concrete Classes
        Provide specific implementations for each step.

Workflow:
    Template Method
        ↓
    Read
        ↓
    Validate
        ↓
    Process
        ↓
    Save
        ↓
    Finish

When to use:
    - File import/export.
    - Authentication workflows.
    - Data processing pipelines.
    - ETL systems.
    - Report generation.
    - Payment processing.
    - Order processing.
    - Backup systems.

Advantages:
    - Eliminates duplicated workflow logic.
    - Encourages code reuse.
    - Standardizes business processes.
    - Easy to extend.
    - Supports the Open/Closed Principle.
    - Makes testing individual steps easier.

Disadvantages:
    - Requires inheritance.
    - Deep inheritance hierarchies may become difficult to maintain.
    - Less flexible than composition-based patterns.

Common backend usage:
    - CSV importers.
    - JSON/XML parsers.
    - Authentication providers.
    - Invoice generation.
    - ETL pipelines.
    - Report generators.
    - Deployment pipelines.

Real-world frameworks:
    - Django
    - FastAPI
    - Flask
    - Spring Boot
    - ASP.NET Core
"""
from abc import ABC, abstractmethod
import random
import string
import unittest


class DataImporter(ABC):

    def import_data(self, data):
        parsed = self.parse(data)
        self.validate(parsed)
        result = self.process(parsed)
        self.save(result)

        return result

    @abstractmethod
    def parse(self, data):
        pass

    @abstractmethod
    def validate(self, data):
        pass

    @abstractmethod
    def process(self, data):
        pass

    @abstractmethod
    def save(self, data):
        pass


class CsvImporter(DataImporter):

    def __init__(self):
        self.saved_data = []

    def parse(self, data):
        return data.split(",")

    def validate(self, data):
        if not data:
            raise ValueError("Empty data")

    def process(self, data):
        return [item.strip().upper() for item in data]

    def save(self, data):
        self.saved_data.extend(data)


class TemplateMethodTests(unittest.TestCase):

    def setUp(self):
        self.importer = CsvImporter()

    def test_import_data(self):
        result = self.importer.import_data(
            "apple, banana, orange"
        )

        self.assertEqual(
            result,
            ["APPLE", "BANANA", "ORANGE"]
        )

    def test_saved_data(self):
        self.importer.import_data(
            "cat,dog"
        )

        self.assertEqual(
            self.importer.saved_data,
            ["CAT", "DOG"]
        )

    def test_empty_string(self):
        result = self.importer.import_data("")

        self.assertEqual(
            result,
            [""]
        )

    def test_multiple_imports(self):
        self.importer.import_data("a,b")
        self.importer.import_data("c,d")

        self.assertEqual(
            self.importer.saved_data,
            ["A", "B", "C", "D"]
        )

    def test_process_removes_spaces(self):
        result = self.importer.import_data(
            " one , two , three "
        )

        self.assertEqual(
            result,
            ["ONE", "TWO", "THREE"]
        )


class TemplateMethodRandomTests(unittest.TestCase):

    def random_word(self):
        length = random.randint(3, 12)

        return "".join(
            random.choice(string.ascii_letters)
            for _ in range(length)
        )

    def test_random_imports(self):
        importer = CsvImporter()

        for _ in range(300):
            words = [
                self.random_word()
                for _ in range(random.randint(2, 10))
            ]

            csv = ",".join(words)

            result = importer.import_data(csv)

            expected = [
                word.upper()
                for word in words
            ]

            self.assertEqual(result, expected)

    def test_random_saved_records(self):
        importer = CsvImporter()

        expected_count = 0

        for _ in range(200):
            words = [
                self.random_word()
                for _ in range(random.randint(1, 8))
            ]

            expected_count += len(words)

            importer.import_data(",".join(words))

        self.assertEqual(
            len(importer.saved_data),
            expected_count
        )

    def test_random_uppercase_conversion(self):
        importer = CsvImporter()

        for _ in range(500):
            word = self.random_word()

            result = importer.import_data(word)

            self.assertEqual(
                result[0],
                word.upper()
            )


if __name__ == "__main__":
    unittest.main()
