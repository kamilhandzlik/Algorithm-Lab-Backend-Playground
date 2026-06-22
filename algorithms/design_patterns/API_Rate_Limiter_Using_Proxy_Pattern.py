"""
Problem: API Rate Limiter using Proxy Pattern

Category:
- Design Patterns
- Proxy Pattern
- Rate Limiting
- API Protection

Description:
This project implements a simple API Rate Limiter
using the Proxy design pattern.

The Proxy Pattern provides a placeholder or surrogate
for another object to control access to it.

In this example:
- ApiService contains the real business logic
- RateLimitProxy controls access to the service
- users can make only a limited number of requests

This pattern is commonly used in:
- API gateways
- rate limiting
- authentication systems
- caching layers
- reverse proxies

Features:
- request limiting
- access control
- transparent service usage
- separation of concerns

Time Complexity:
- Request: O(1)

Space Complexity:
- O(n)
"""
import random
import unittest

class ApiService:
    def get_data(self):
        return  "API response"

class RateLimitProxy:
    def __init__(self, service, limit):
        self.service = service
        self.limit = limit
        self.requests = {}

    def get_data(self, user_id):
        count = self.requests.get(user_id, 0)

        if count >= self.limit:
            return "Rate limit exceeded"

        self.requests[user_id] = count + 1

        return  self.service.get_data()

class TestProxyPattern(unittest.TestCase):

    def test_request_allowed(self):

        proxy = RateLimitProxy(ApiService(), limit=3)

        result = proxy.get_data("user1")

        self.assertEqual(result,"API response")

    def test_limit_exceeded(self):

        proxy = RateLimitProxy(ApiService(),limit=2)

        proxy.get_data("user1")
        proxy.get_data("user1")

        result = proxy.get_data("user1")

        self.assertEqual(result,"Rate limit exceeded")

    def test_different_users(self):

        proxy = RateLimitProxy(ApiService(),limit=1)

        self.assertEqual(proxy.get_data("user1"),"API response")

        self.assertEqual(proxy.get_data("user2"),"API response")

    def test_request_counter(self):

        proxy = RateLimitProxy(ApiService(),limit=5)

        proxy.get_data("user1")
        proxy.get_data("user1")

        self.assertEqual(proxy.requests["user1"],2)


class TestRandom(unittest.TestCase):

    def test_random_requests(self):

        proxy = RateLimitProxy(
            ApiService(),
            limit=5
        )

        users = ["user1","user2","user3","user4"]

        for _ in range(100):

            user = random.choice(users)

            result = proxy.get_data(user)

            self.assertIn(result,["API response","Rate limit exceeded"])


if __name__ == "__main__":
    unittest.main()