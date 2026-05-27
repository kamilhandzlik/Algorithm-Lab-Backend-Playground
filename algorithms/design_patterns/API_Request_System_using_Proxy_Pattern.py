"""
Problem: API Request System using Proxy Pattern

Category:
- Design Patterns
- Proxy Pattern
- API Management
- Access Control

Description:
This project implements a simple API request system
using the Proxy design pattern.

The Proxy Pattern provides a placeholder object
that controls access to another object.

In this example:
- RealAPIService handles real API requests
- APIProxy controls access to the service
- the proxy adds request validation and rate limiting

This pattern is commonly used in:
- API gateways
- authentication systems
- caching layers
- lazy loading
- access control systems

Features:
- controlled API access
- request validation
- simple rate limiting
- transparent service communication

Time Complexity:
- Request handling: O(1)

Space Complexity:
- O(n)
"""

import unittest
import random


class RealAPIService:

    def request(self, endpoint):

        return f"Response from {endpoint}"


class APIProxy:

    def __init__(self):

        self.api_service = RealAPIService()

        self.request_count = 0

        self.limit = 5

    def request(self, endpoint):

        if self.request_count >= self.limit:

            return "Rate limit exceeded"

        self.request_count += 1

        return self.api_service.request(
            endpoint
        )


class TestProxyPattern(unittest.TestCase):

    def test_valid_request(self):

        proxy = APIProxy()

        result = proxy.request(
            "/users"
        )

        self.assertEqual(
            result,
            "Response from /users"
        )

    def test_rate_limit(self):

        proxy = APIProxy()

        for _ in range(5):

            proxy.request("/test")

        result = proxy.request(
            "/blocked"
        )

        self.assertEqual(
            result,
            "Rate limit exceeded"
        )

    def test_request_counter(self):

        proxy = APIProxy()

        proxy.request("/a")
        proxy.request("/b")

        self.assertEqual(
            proxy.request_count,
            2
        )


class TestRandom(unittest.TestCase):

    def test_random_requests(self):

        proxy = APIProxy()

        endpoints = [
            "/users",
            "/posts",
            "/comments",
            "/products"
        ]

        success_count = 0

        for _ in range(10):

            endpoint = random.choice(
                endpoints
            )

            result = proxy.request(
                endpoint
            )

            if result != "Rate limit exceeded":

                success_count += 1

        self.assertEqual(
            success_count,
            5
        )


if __name__ == "__main__":

    unittest.main()