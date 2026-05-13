"""
Problem: Logger Singleton
Category: Design Patterns / Singleton
"""
import unittest
import random
import string


class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            # inicjalizacja tylko raz
            cls._instance.logs = []

        return cls._instance

    def log(self, message):
        self.logs.append(message)

    def get_logs(self):
        return self.logs


class TestLoggerSingleton(unittest.TestCase):

    def test_single_instance(self):
        logger1 = Logger()
        logger2 = Logger()

        self.assertIs(logger1, logger2)

    def test_shared_logs(self):
        logger1 = Logger()
        logger2 = Logger()

        logger1.logs.clear()

        logger1.log("hello")
        logger2.log("world")

        self.assertEqual(
            logger1.get_logs(),
            ["hello", "world"]
        )

    def test_same_memory_reference(self):
        logger1 = Logger()
        logger2 = Logger()

        self.assertEqual(
            id(logger1),
            id(logger2)
        )


class TestRandomLogger(unittest.TestCase):

    def random_message(self):
        length = random.randint(3, 10)

        return ''.join(
            random.choice(string.ascii_letters)
            for _ in range(length)
        )

    def test_random_logs(self):
        logger = Logger()

        logger.logs.clear()

        generated = []

        for _ in range(100):
            message = self.random_message()

            generated.append(message)

            logger.log(message)

        self.assertEqual(
            logger.get_logs(),
            generated
        )
