"""
Problem: Configuration System using Chain of Responsibility Pattern

Category:
- Design Patterns
- Chain of Responsibility
- Configuration Management
- Request Processing

Description:
This project implements a simple configuration validation
system using the Chain of Responsibility design pattern.

The Chain of Responsibility Pattern passes requests through
a chain of handlers. Each handler processes the request
or forwards it to the next handler in the chain.

In this example:
- each validator checks one configuration rule
- invalid configurations stop the chain
- valid configurations continue to the next validator

This pattern is commonly used in:
- middleware systems
- request validation
- authentication pipelines
- logging systems
- API processing

Features:
- chained validation logic
- modular request handlers
- flexible processing pipeline
- clean separation of responsibilities

Time Complexity:
- Validation process: O(n)

Space Complexity:
- O(n)
"""

import unittest
import random
import string


class Handler:

    def __init__(self):

        self.next_handler = None

    def set_next(self, handler):

        self.next_handler = handler

        return handler

    def handle(self, request):

        if self.next_handler:

            return self.next_handler.handle(
                request
            )

        return True


class HostValidator(Handler):

    def handle(self, request):

        if "host" not in request:

            return "Missing host"

        return super().handle(request)


class PortValidator(Handler):

    def handle(self, request):

        if "port" not in request:

            return "Missing port"

        return super().handle(request)


class ApiKeyValidator(Handler):

    def handle(self, request):

        if "api_key" not in request:

            return "Missing api_key"

        return super().handle(request)


class TestChainOfResponsibility(unittest.TestCase):

    def create_chain(self):

        host = HostValidator()
        port = PortValidator()
        api = ApiKeyValidator()

        host.set_next(port).set_next(api)

        return host

    def test_valid_config(self):

        chain = self.create_chain()

        config = {
            "host": "localhost",
            "port": 8000,
            "api_key": "SECRET"
        }

        self.assertTrue(
            chain.handle(config)
        )

    def test_missing_host(self):

        chain = self.create_chain()

        config = {
            "port": 8000,
            "api_key": "SECRET"
        }

        self.assertEqual(
            chain.handle(config),
            "Missing host"
        )

    def test_missing_port(self):

        chain = self.create_chain()

        config = {
            "host": "localhost",
            "api_key": "SECRET"
        }

        self.assertEqual(
            chain.handle(config),
            "Missing port"
        )

    def test_missing_api_key(self):

        chain = self.create_chain()

        config = {
            "host": "localhost",
            "port": 8000
        }

        self.assertEqual(
            chain.handle(config),
            "Missing api_key"
        )


class TestRandom(unittest.TestCase):

    def random_string(self):

        length = random.randint(5, 10)

        return ''.join(
            random.choice(
                string.ascii_letters
            )
            for _ in range(length)
        )

    def test_random_valid_configs(self):

        host = HostValidator()
        port = PortValidator()
        api = ApiKeyValidator()

        host.set_next(port).set_next(api)

        for _ in range(50):

            config = {
                "host": self.random_string(),
                "port": random.randint(
                    1000,
                    9999
                ),
                "api_key": self.random_string()
            }

            self.assertTrue(
                host.handle(config)
            )


if __name__ == "__main__":

    unittest.main()