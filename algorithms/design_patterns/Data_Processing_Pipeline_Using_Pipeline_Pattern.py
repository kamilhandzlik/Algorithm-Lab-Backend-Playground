"""
Problem: Data Processing Pipeline using Pipeline Pattern

Category:
- Design Patterns
- Pipeline Pattern
- Data Processing
- ETL

Description:
This project implements a simple data processing pipeline
using the Pipeline Pattern.

The Pipeline Pattern breaks processing into multiple,
independent stages. Each stage receives data,
transforms it and passes the result to the next stage.

In this example:
- RemoveSpacesStage removes whitespace
- LowercaseStage converts text to lowercase
- ReverseStage reverses the string
- Pipeline executes all stages sequentially

This pattern is commonly used in:
- ETL systems
- CI/CD pipelines
- middleware chains
- image processing
- machine learning preprocessing

Features:
- reusable processing stages
- configurable execution order
- clean separation of responsibilities
- extensible architecture

Time Complexity:
- Execute pipeline: O(n)

Space Complexity:
- O(n)
"""

import random
import string
import unittest
from abc import ABC, abstractmethod


class Stage(ABC):

    @abstractmethod
    def process(self, data):
        pass


class RemoveSpacesStage(Stage):

    def process(self, data):
        return data.replace(" ", "")


class LowercaseStage(Stage):

    def process(self, data):
        return data.lower()


class ReverseStage(Stage):

    def process(self, data):
        return data[::-1]


class Pipeline:

    def __init__(self):
        self.stages = []

    def add_stage(self, stage):
        self.stages.append(stage)

    def execute(self, data):
        for stage in self.stages:
            data = stage.process(data)

        return data


class TestPipelinePattern(unittest.TestCase):

    def test_remove_spaces(self):
        pipeline = Pipeline()
        pipeline.add_stage(RemoveSpacesStage())

        result = pipeline.execute("Hello World")

        self.assertEqual(result, "HelloWorld")

    def test_lowercase(self):
        pipeline = Pipeline()
        pipeline.add_stage(LowercaseStage())

        result = pipeline.execute("HELLO")

        self.assertEqual(
            result, "hello")

    def test_reverse(self):
        pipeline = Pipeline()
        pipeline.add_stage(ReverseStage())

        result = pipeline.execute("abc")

        self.assertEqual(result, "cba")

    def test_complete_pipeline(self):
        pipeline = Pipeline()

        pipeline.add_stage(RemoveSpacesStage())
        pipeline.add_stage(LowercaseStage())
        pipeline.add_stage(ReverseStage())

        result = pipeline.execute("Hello World")

        self.assertEqual(result, "dlrowolleh")


class TestRandom(unittest.TestCase):

    def random_text(self):
        length = random.randint(5, 20)

        characters = string.ascii_letters + " "

        return "".join(random.choice(characters) for _ in range(length))

    def test_random_pipeline(self):
        pipeline = Pipeline()

        pipeline.add_stage(RemoveSpacesStage())
        pipeline.add_stage(LowercaseStage())

        for _ in range(100):
            text = self.random_text()

            result = pipeline.execute(text)

            self.assertEqual(result, text.replace(" ", "").lower())


if __name__ == "__main__":
    unittest.main()
