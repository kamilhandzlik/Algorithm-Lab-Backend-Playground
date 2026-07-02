"""
Problem: HTTP Request Pipeline using Chain of Responsibility Pattern

Category:
- Design Patterns
- Chain of Responsibility
- Middleware
- HTTP Processing

Description:
This project implements a simple HTTP request pipeline
using the Chain of Responsibility design pattern.

The Chain of Responsibility Pattern allows multiple
handlers to process a request without the sender
knowing which handler will process it.

In this example:
- LoggingMiddleware logs incoming requests
- AuthenticationMiddleware validates users
- PermissionMiddleware checks permissions
- FinalHandler generates the response

Each middleware decides whether to continue processing
or stop the request.

This pattern is commonly used in:
- Django Middleware
- ASP.NET Middleware
- Express.js
- FastAPI
- HTTP servers

Features:
- request pipeline
- middleware chaining
- request interception
- flexible processing order

Time Complexity:
- Process request: O(n)

Space Complexity:
- O(1)
"""

import random
import unittest
from abc import ABC, abstractmethod


class Request:

    def __init__(self, authenticated, is_admin):
        self.authenticated = authenticated
        self.is_admin = is_admin


class Handler(ABC):

    def __init__(self):
        self.next_handler = None

    def set_next(self, handler):
        self.next_handler = handler
        return handler

    @abstractmethod
    def handle(self, request):
        pass


class LoggingMiddleware(Handler):

    def handle(self, request):

        if self.next_handler:
            return self.next_handler.handle(request)

        return "OK"


class AuthenticationMiddleware(Handler):

    def handle(self, request):

        if not request.authenticated:
            return "401 Unauthorized"

        if self.next_handler:
            return self.next_handler.handle(request)

        return "OK"


class PermissionMiddleware(Handler):

    def handle(self, request):

        if not request.is_admin:
            return "403 Forbidden"

        if self.next_handler:
            return self.next_handler.handle(request)

        return "OK"


class FinalHandler(Handler):

    def handle(self, request):
        return "200 OK"


class TestChainOfResponsibility(unittest.TestCase):

    def create_pipeline(self):

        logging = LoggingMiddleware()
        auth = AuthenticationMiddleware()
        permission = PermissionMiddleware()
        final = FinalHandler()

        logging.set_next(auth).set_next(permission).set_next(final)

        return logging

    def test_successful_request(self):

        pipeline = self.create_pipeline()

        request = Request(True, True)

        self.assertEqual(
            pipeline.handle(request),
            "200 OK"
        )

    def test_unauthorized_request(self):

        pipeline = self.create_pipeline()

        request = Request(False, True)

        self.assertEqual(
            pipeline.handle(request),
            "401 Unauthorized"
        )

    def test_forbidden_request(self):

        pipeline = self.create_pipeline()

        request = Request(True, False)

        self.assertEqual(
            pipeline.handle(request),
            "403 Forbidden"
        )

    def test_pipeline_exists(self):

        pipeline = self.create_pipeline()

        self.assertIsNotNone(pipeline.next_handler)


class TestRandom(unittest.TestCase):

    def create_pipeline(self):

        logging = LoggingMiddleware()
        auth = AuthenticationMiddleware()
        permission = PermissionMiddleware()
        final = FinalHandler()

        logging.set_next(auth).set_next(permission).set_next(final)

        return logging

    def test_random_requests(self):

        pipeline = self.create_pipeline()

        valid_responses = [
            "200 OK",
            "401 Unauthorized",
            "403 Forbidden"
        ]

        for _ in range(100):

            request = Request(
                authenticated=random.choice([True, False]),
                is_admin=random.choice([True, False])
            )

            response = pipeline.handle(request)

            self.assertIn(
                response,
                valid_responses
            )


if __name__ == "__main__":
    unittest.main()