"""
Problem: Payment Service using Circuit Breaker Pattern

Category:
- Design Patterns
- Circuit Breaker Pattern
- Fault Tolerance
- Distributed Systems

Description:
This project implements a simple Circuit Breaker
using the Circuit Breaker design pattern.

The Circuit Breaker Pattern prevents repeated calls
to a failing service. Once a predefined failure limit
is reached, the circuit opens and immediately rejects
new requests until the service is considered healthy
again.

In this example:
- PaymentService simulates an external API
- CircuitBreaker protects the service
- failures are counted automatically
- successful calls reset the failure counter

This pattern is commonly used in:
- microservices
- REST APIs
- cloud services
- payment gateways
- distributed systems

Features:
- automatic failure detection
- circuit opening
- failure counter reset
- service protection

Time Complexity:
- Call service: O(1)

Space Complexity:
- O(1)
"""

import random
import unittest


class PaymentService:

    def __init__(self):
        self.available = True

    def process_payment(self):
        if not self.available:
            raise ConnectionError("Payment service unavailable")

        return "Payment completed"


class CircuitBreaker:

    def __init__(self, service, failure_limit):

        self.service = service
        self.failure_limit = failure_limit
        self.failures = 0
        self.open = False

    def call(self):

        if self.open:
            return "Circuit Open"

        try:

            result = self.service.process_payment()

            self.failures = 0

            return result

        except ConnectionError:

            self.failures += 1

            if self.failures >= self.failure_limit:
                self.open = True

            return "Service Failed"

    def reset(self):

        self.failures = 0
        self.open = False


class TestCircuitBreaker(unittest.TestCase):

    def test_successful_call(self):
        breaker = CircuitBreaker(PaymentService(), failure_limit=3)

        self.assertEqual(breaker.call(), "Payment completed")

    def test_open_circuit(self):
        service = PaymentService()
        service.available = False

        breaker = CircuitBreaker(service, failure_limit=2)

        breaker.call()
        breaker.call()

        self.assertTrue(breaker.open)

    def test_reject_when_open(self):
        service = PaymentService()
        service.available = False

        breaker = CircuitBreaker(service, failure_limit=1)

        breaker.call()

        self.assertEqual(breaker.call(), "Circuit Open")

    def test_reset(self):
        service = PaymentService()
        service.available = False

        breaker = CircuitBreaker(service, failure_limit=1)

        breaker.call()

        breaker.reset()

        service.available = True

        self.assertEqual(breaker.call(), "Payment completed")


class TestRandom(unittest.TestCase):

    def test_random_calls(self):

        service = PaymentService()

        breaker = CircuitBreaker(service, failure_limit=3)

        for _ in range(100):

            service.available = random.choice([True, False])

            result = breaker.call()

            self.assertIn(result, ["Payment completed", "Service Failed", "Circuit Open"])

            if breaker.open:
                breaker.reset()


if __name__ == "__main__":
    unittest.main()
