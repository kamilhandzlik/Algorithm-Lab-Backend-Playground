"""
Builder Pattern

Description:
    The Builder Pattern is a creational design pattern that separates
    the construction of a complex object from its representation.

    Instead of creating an object using a large constructor with many
    parameters, the Builder Pattern creates the object step by step.

    Each configuration method returns the builder itself, allowing
    method chaining (also known as a fluent interface).

    This approach makes object creation easier to read, less error-prone
    and much more maintainable.

Purpose:
    - Simplify the creation of complex objects.
    - Avoid constructors with many parameters.
    - Support optional configuration.
    - Improve readability.
    - Build immutable objects.
    - Separate construction logic from business logic.

Problem it solves:
    Imagine creating an HTTP request object.

        request = HttpRequest(
            url,
            method,
            headers,
            body,
            timeout,
            retries,
            verify_ssl,
            follow_redirects,
            authentication,
            cookies,
            proxy
        )

    As the number of parameters grows, constructors become difficult
    to understand.

    It is easy to swap arguments accidentally or forget optional values.

    The Builder Pattern allows each property to be configured
    independently while keeping the code readable.

Structure:
    Product
        The complex object being created.

    Builder
        Declares methods for configuring the product.

    Concrete Builder
        Implements the construction process.

    Client
        Uses the builder to create the final object.

Workflow:
    Client
        ↓
    Builder
        ↓
    Configure URL
        ↓
    Configure Headers
        ↓
    Configure Timeout
        ↓
    Configure Authentication
        ↓
    Build Object

When to use:
    - Objects with many optional parameters.
    - Complex configuration.
    - Immutable objects.
    - Configuration APIs.
    - HTTP clients.
    - Database connections.
    - Query builders.

Advantages:
    - Eliminates long constructors.
    - Improves readability.
    - Supports method chaining.
    - Easier validation.
    - Easier maintenance.
    - Prevents partially initialized objects.

Disadvantages:
    - Requires additional classes.
    - Slightly increases project size.
    - May be unnecessary for simple objects.

Common backend usage:
    - SQL query builders.
    - HTTP request builders.
    - Docker configuration.
    - Kubernetes resources.
    - Email builders.
    - Database connection configuration.
    - Logging configuration.

Real-world frameworks:
    - SQLAlchemy
    - Spring Boot
    - ASP.NET Core
    - Django ORM
    - FastAPI
"""
from dataclasses import dataclass
import random
import string
import unittest


@dataclass
class HttpRequest:
    url: str
    method: str
    timeout: int
    headers: dict
    body: str | None


class HttpRequestBuilder:

    def __init__(self):
        self.url = ""
        self.method = "GET"
        self.timeout = 30
        self.headers = {}
        self.body = None

    def set_url(self, url: str):
        self.url = url
        return self

    def set_method(self, method: str):
        self.method = method
        return self

    def set_timeout(self, timeout: int):
        self.timeout = timeout
        return self

    def add_header(self, key: str, value: str):
        self.headers[key] = value
        return self

    def set_body(self, body: str):
        self.body = body
        return self

    def build(self):
        if not self.url:
            raise ValueError("URL is required")

        return HttpRequest(
            url=self.url,
            method=self.method,
            timeout=self.timeout,
            headers=self.headers,
            body=self.body
        )


class BuilderTests(unittest.TestCase):

    def test_default_values(self):
        request = (
            HttpRequestBuilder()
            .set_url("https://example.com")
            .build()
        )

        self.assertEqual(request.method, "GET")
        self.assertEqual(request.timeout, 30)

    def test_custom_values(self):
        request = (
            HttpRequestBuilder()
            .set_url("https://example.com")
            .set_method("POST")
            .set_timeout(60)
            .set_body("Hello")
            .build()
        )

        self.assertEqual(request.method, "POST")
        self.assertEqual(request.timeout, 60)
        self.assertEqual(request.body, "Hello")

    def test_headers(self):
        request = (
            HttpRequestBuilder()
            .set_url("https://example.com")
            .add_header("Authorization", "Bearer token")
            .add_header("Content-Type", "application/json")
            .build()
        )

        self.assertEqual(
            request.headers["Authorization"],
            "Bearer token"
        )

    def test_missing_url(self):
        with self.assertRaises(ValueError):
            HttpRequestBuilder().build()

    def test_builder_returns_self(self):
        builder = HttpRequestBuilder()

        self.assertIs(
            builder.set_timeout(10),
            builder
        )


class BuilderRandomTests(unittest.TestCase):

    def random_url(self):
        name = "".join(
            random.choice(string.ascii_lowercase)
            for _ in range(8)
        )

        return f"https://{name}.com"

    def test_random_requests(self):
        for _ in range(500):
            timeout = random.randint(1, 300)

            request = (
                HttpRequestBuilder()
                .set_url(self.random_url())
                .set_timeout(timeout)
                .build()
            )

            self.assertEqual(
                request.timeout,
                timeout
            )

    def test_random_headers(self):
        for _ in range(300):
            builder = (
                HttpRequestBuilder()
                .set_url(self.random_url())
            )

            count = random.randint(1, 15)

            for index in range(count):
                builder.add_header(
                    f"Header-{index}",
                    str(random.randint(1, 1000))
                )

            request = builder.build()

            self.assertEqual(
                len(request.headers),
                count
            )

    def test_random_methods(self):
        methods = [
            "GET",
            "POST",
            "PUT",
            "DELETE",
            "PATCH"
        ]

        for _ in range(300):
            method = random.choice(methods)

            request = (
                HttpRequestBuilder()
                .set_url(self.random_url())
                .set_method(method)
                .build()
            )

            self.assertEqual(
                request.method,
                method
            )


if __name__ == "__main__":
    unittest.main()
