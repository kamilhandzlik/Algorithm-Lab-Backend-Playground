"""
Chain of Responsibility Pattern

Description:
    The Chain of Responsibility Pattern is a behavioral design pattern
    that allows a request to pass through a chain of handlers.

    Each handler decides whether it can process the request.
    If it cannot, it forwards the request to the next handler
    in the chain.

    This eliminates the need for large conditional statements
    and allows processing logic to be divided into small,
    reusable components.

    Every handler follows the same interface, making the chain
    easy to extend or reorder.

Purpose:
    - Decouple request senders from request handlers.
    - Divide complex processing into independent steps.
    - Allow multiple handlers to process a request.
    - Build configurable processing pipelines.
    - Improve extensibility and maintainability.

Problem it solves:
    Imagine a REST API receiving user requests.

    Before a request reaches the business logic, several checks
    must be performed:

        - Authentication
        - Authorization
        - Input validation
        - Logging
        - Rate limiting
        - Audit logging

    A naive implementation often places all of these checks inside
    one controller method.

    As the application grows, controllers become difficult to read,
    maintain and test.

    The Chain of Responsibility Pattern moves every responsibility
    into its own handler.

    Each handler performs one task and either passes the request
    to the next handler or stops further processing.

Structure:
    Handler
        Declares the interface for handling requests.

    Base Handler
        Implements common chain logic.

    Concrete Handlers
        Perform individual processing steps.

    Client
        Builds the chain and sends requests.

Workflow:
    Client
        ↓
    AuthenticationHandler
        ↓
    AuthorizationHandler
        ↓
    ValidationHandler
        ↓
    LoggingHandler
        ↓
    Business Logic

When to use:
    - HTTP middleware.
    - Authentication.
    - Authorization.
    - Request validation.
    - Logging.
    - Rate limiting.
    - Event processing.
    - Data processing pipelines.

Advantages:
    - Removes large if-elif statements.
    - Promotes single responsibility.
    - Easy to extend.
    - Handlers can be reordered.
    - Supports dependency injection.
    - Simplifies testing.
    - Encourages reusable components.

Disadvantages:
    - Debugging long chains may be harder.
    - Incorrect handler order may produce bugs.
    - Too many handlers may impact readability.

Common backend usage:
    - Django Middleware.
    - ASP.NET Middleware.
    - Spring Security Filters.
    - Express.js Middleware.
    - FastAPI Dependencies.
    - API Gateways.
    - Request Pipelines.

Real-world frameworks:
    - Django
    - Flask
    - FastAPI
    - Spring Boot
    - ASP.NET Core
"""
from abc import ABC, abstractmethod
import random
import unittest


class Request:

    def __init__(self, authenticated: bool, admin: bool, valid: bool):
        self.authenticated = authenticated
        self.admin = admin
        self.valid = valid


class Handler(ABC):

    def __init__(self):
        self.next_handler = None

    def set_next(self, handler):
        self.next_handler = handler
        return handler

    @abstractmethod
    def handle(self, request: Request):
        pass


class AuthenticationHandler(Handler):

    def handle(self, request: Request):
        if not request.authenticated:
            return "Authentication failed"

        if self.next_handler:
            return self.next_handler.handle(request)

        return "Success"


class AuthorizationHandler(Handler):

    def handle(self, request: Request):
        if not request.admin:
            return "Authorization failed"

        if self.next_handler:
            return self.next_handler.handle(request)

        return "Success"


class ValidationHandler(Handler):

    def handle(self, request: Request):
        if not request.valid:
            return "Validation failed"

        if self.next_handler:
            return self.next_handler.handle(request)

        return "Success"


class ChainTests(unittest.TestCase):

    def setUp(self):
        self.auth = AuthenticationHandler()
        self.authorization = AuthorizationHandler()
        self.validation = ValidationHandler()

        self.auth.set_next(self.authorization).set_next(self.validation)

    def test_successful_request(self):
        request = Request(True, True, True)

        result = self.auth.handle(request)

        self.assertEqual(result, "Success")

    def test_authentication_failure(self):
        request = Request(False, True, True)

        result = self.auth.handle(request)

        self.assertEqual(result, "Authentication failed")

    def test_authorization_failure(self):
        request = Request(True, False, True)

        result = self.auth.handle(request)

        self.assertEqual(result, "Authorization failed")

    def test_validation_failure(self):
        request = Request(True, True, False)

        result = self.auth.handle(request)

        self.assertEqual(result, "Validation failed")

    def test_chain_configuration(self):
        self.assertIs(
            self.auth.next_handler,
            self.authorization
        )

        self.assertIs(
            self.authorization.next_handler,
            self.validation
        )


class ChainRandomTests(unittest.TestCase):

    def setUp(self):
        self.auth = AuthenticationHandler()
        self.authorization = AuthorizationHandler()
        self.validation = ValidationHandler()

        self.auth.set_next(self.authorization).set_next(self.validation)

    def test_random_requests(self):
        for _ in range(1000):
            authenticated = random.choice([True, False])
            admin = random.choice([True, False])
            valid = random.choice([True, False])

            request = Request(
                authenticated,
                admin,
                valid
            )

            result = self.auth.handle(request)

            if not authenticated:
                self.assertEqual(
                    result,
                    "Authentication failed"
                )

            elif not admin:
                self.assertEqual(
                    result,
                    "Authorization failed"
                )

            elif not valid:
                self.assertEqual(
                    result,
                    "Validation failed"
                )

            else:
                self.assertEqual(
                    result,
                    "Success"
                )

    def test_random_chain_order(self):
        handlers = [
            AuthenticationHandler(),
            AuthorizationHandler(),
            ValidationHandler()
        ]

        random.shuffle(handlers)

        for index in range(len(handlers) - 1):
            handlers[index].set_next(handlers[index + 1])

        self.assertEqual(
            len(handlers),
            3
        )

    def test_random_request_generation(self):
        for _ in range(500):
            request = Request(
                random.choice([True, False]),
                random.choice([True, False]),
                random.choice([True, False])
            )

            self.assertIsInstance(
                request,
                Request
            )


if __name__ == "__main__":
    unittest.main()
