"""
Problem: Document Processing System using Template Method Pattern

Category:
- Design Patterns
- Template Method Pattern
- Document Processing
- Workflow Management

Description:
This project implements a document processing system
using the Template Method design pattern.

The Template Method Pattern defines the skeleton of an
algorithm in a base class while allowing subclasses to
override specific steps without changing the overall process.

In this example:
- all documents follow the same processing workflow
- each document type implements its own validation
  and formatting logic
- the processing sequence remains unchanged

This pattern is commonly used in:
- file processing systems
- ETL pipelines
- report generation
- data import/export tools
- workflow automation

Features:
- reusable workflow definition
- customizable processing steps
- reduced code duplication
- consistent execution order

Time Complexity:
- Process document: O(n)

Space Complexity:
- O(n)
"""

import unittest
import random
import string
from abc import ABC, abstractmethod


class DocumentProcessor(ABC):

    def process(self, content):

        self.validate(content)

        formatted = self.format(content)

        return self.export(formatted)

    @abstractmethod
    def validate(self, content):
        pass

    @abstractmethod
    def format(self, content):
        pass

    def export(self, content):

        return f"EXPORTED: {content}"


class TextDocumentProcessor(DocumentProcessor):

    def validate(self, content):

        if not isinstance(content, str):
            raise ValueError(
                "Content must be string"
            )

    def format(self, content):

        return content.upper()


class JsonDocumentProcessor(DocumentProcessor):

    def validate(self, content):

        if not isinstance(content, dict):
            raise ValueError(
                "Content must be dictionary"
            )

    def format(self, content):

        return str(content)


class TestTemplateMethodPattern(unittest.TestCase):

    def test_text_document(self):

        processor = TextDocumentProcessor()

        result = processor.process(
            "hello world"
        )

        self.assertEqual(
            result,
            "EXPORTED: HELLO WORLD"
        )

    def test_json_document(self):

        processor = JsonDocumentProcessor()

        result = processor.process(
            {"name": "Kamil"}
        )

        self.assertEqual(
            result,
            "EXPORTED: {'name': 'Kamil'}"
        )

    def test_invalid_text_input(self):

        processor = TextDocumentProcessor()

        with self.assertRaises(
            ValueError
        ):

            processor.process(123)

    def test_invalid_json_input(self):

        processor = JsonDocumentProcessor()

        with self.assertRaises(
            ValueError
        ):

            processor.process("hello")


class TestRandom(unittest.TestCase):

    def random_string(self):

        length = random.randint(5, 15)

        return ''.join(
            random.choice(
                string.ascii_lowercase
            )
            for _ in range(length)
        )

    def test_random_text_documents(self):

        processor = TextDocumentProcessor()

        for _ in range(50):

            text = self.random_string()

            result = processor.process(
                text
            )

            self.assertEqual(
                result,
                f"EXPORTED: {text.upper()}"
            )


if __name__ == "__main__":

    unittest.main()