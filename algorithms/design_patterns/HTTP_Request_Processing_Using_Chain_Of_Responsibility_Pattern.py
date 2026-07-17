"""
Problem: HTTP Request Processing using Chain of Responsibility Pattern

Category:
- Design Patterns
- Chain of Responsibility
- Middleware
- HTTP Processing

Description:
This project implements an HTTP request processing
pipeline using the Chain of Responsibility Pattern.

The Chain of Responsibility Pattern allows multiple
handlers to process a request without the sender
knowing which handler will handle it.

Each middleware decides whether processing should
continue or stop.

In this example:
- AuthenticationMiddleware validates users
- LoggingMiddleware records requests
- RateLimitMiddleware limits request frequency
- RequestHandler executes the final action

This pattern is commonly used in:
- Django middleware
- FastAPI middleware
- Express.js
- ASP.NET Core
- Spring Security

Features:
- configurable middleware chain
- loose coupling
- reusable middleware
- easy extension

Time Complexity:
- Process request: O(n)

Space Complexity:
- O(n)
"""

import random
import unittest
from abc import ABC, abstractmethod


class Request:

    def __init__(self, authenticated, requests_count):
        self.authenticated = authenticated
        self.requests_count = requests_count
        self.logs = []


class Middleware(ABC):

    def __init__(self):
        self.next = None

    def set_next(self, middleware):
        self.next = middleware
        return middleware

    @abstractmethod
    def handle(self, request):
        pass

    def next_handler(self, request):
        if self.next:
            return self.next.handle(request)

        return "OK"


class LoggingMiddleware(Middleware):

    def handle(self, request):
        request.logs.append("Request logged")

        return self.next_handler(request)


class AuthenticationMiddleware(Middleware):

    def handle(self, request):
        if not request.authenticated:
            return "Unauthorized"

        return self.next_handler(request)


class RateLimitMiddleware(Middleware):

    def handle(self, request):
        if request.requests_count > 5:
            return "Too Many Requests"

        return self.next_handler(request)


class RequestHandler(Middleware):

    def handle(self, request):
        request.logs.append("Request processed")

        return "Success"


class TestChainPattern(unittest.TestCase):

    def build_chain(self):
        logging = LoggingMiddleware()
        auth = AuthenticationMiddleware()
        limit = RateLimitMiddleware()
        handler = RequestHandler()

        logging.set_next(auth).set_next(limit).set_next(handler)

        return logging

    def test_successful_request(self):
        chain = self.build_chain()

        request = Request(True, 2)

        self.assertEqual(chain.handle(request), "Success")

    def test_unauthorized(self):
        chain = self.build_chain()

        request = Request(False, 1)

        self.assertEqual(chain.handle(request), "Unauthorized")

    def test_rate_limit(self):
        chain = self.build_chain()

        request = Request(True, 10)

        self.assertEqual(chain.handle(request), "Too Many Requests")

    def test_logs(self):
        chain = self.build_chain()

        request = Request(True, 1)

        chain.handle(request)

        self.assertEqual(request.logs, ["Request logged", "Request processed"])


class TestRandom(unittest.TestCase):

    def build_chain(self):
        logging = LoggingMiddleware()
        auth = AuthenticationMiddleware()
        limit = RateLimitMiddleware()
        handler = RequestHandler()

        logging.set_next(auth).set_next(limit).set_next(handler)

        return logging

    def test_random_requests(self):
        chain = self.build_chain()

        for _ in range(100):
            request = Request(authenticated=random.choice([True, False]), requests_count=random.randint(0, 10))

            result = chain.handle(request)

            self.assertIn(result, ["Success", "Unauthorized", "Too Many Requests"])


if __name__ == "__main__":
    unittest.main()
