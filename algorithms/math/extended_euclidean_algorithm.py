"""
Greatest Common Divisor and Extended Euclidean Algorithm

The Greatest Common Divisor (GCD) of two integers a and b is the largest
positive integer that divides both numbers without leaving a remainder.

For example:

    gcd(48, 18) = 6

because 6 is the largest integer that divides both 48 and 18.

A naive solution would try every integer from 1 up to min(a, b), but this
approach becomes inefficient for large numbers.

We can solve the problem efficiently using the Euclidean algorithm.

The key observation is:

    gcd(a, b) = gcd(b, a % b)

This allows us to repeatedly replace the larger problem with a smaller one
until the second number becomes zero.

For example:

    gcd(48, 18)
    gcd(18, 12)
    gcd(12, 6)
    gcd(6, 0)

Therefore:

    gcd(48, 18) = 6

The Euclidean algorithm runs in O(log(min(a, b))) time.

We can extend this algorithm to calculate coefficients x and y such that:

    ax + by = gcd(a, b)

This is known as the Extended Euclidean Algorithm.

It is useful in many programming and mathematical problems, including:

- solving linear Diophantine equations,
- calculating modular inverses,
- working with modular arithmetic,
- cryptography,
- number theory algorithms.

The implementation below supports negative integers as well as positive
integers. The returned GCD is always non-negative.
"""

import random
import unittest


def gcd(a: int, b: int) -> int:
    """
    Calculate the greatest common divisor of two integers.

    Time complexity:
        O(log(min(|a|, |b|)))

    Space complexity:
        O(1)
    """
    a = abs(a)
    b = abs(b)

    while b:
        a, b = b, a % b

    return a


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """
    Calculate gcd(a, b) and coefficients x and y satisfying:

        ax + by = gcd(a, b)

    Returns:
        (g, x, y)

    where:
        g = gcd(a, b)
        ax + by = g
    """
    original_a = a
    original_b = b

    old_r, r = abs(a), abs(b)
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r:
        quotient = old_r // r

        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    g = old_r

    x = old_s if original_a >= 0 else -old_s
    y = old_t if original_b >= 0 else -old_t

    return g, x, y


class TestGCD(unittest.TestCase):

    def test_positive_numbers(self):
        self.assertEqual(gcd(48, 18), 6)
        self.assertEqual(gcd(100, 25), 25)
        self.assertEqual(gcd(17, 13), 1)

    def test_zero(self):
        self.assertEqual(gcd(0, 10), 10)
        self.assertEqual(gcd(10, 0), 10)
        self.assertEqual(gcd(0, 0), 0)

    def test_negative_numbers(self):
        self.assertEqual(gcd(-48, 18), 6)
        self.assertEqual(gcd(48, -18), 6)
        self.assertEqual(gcd(-48, -18), 6)

    def test_same_numbers(self):
        self.assertEqual(gcd(42, 42), 42)
        self.assertEqual(gcd(-42, -42), 42)

    def test_coprime_numbers(self):
        self.assertEqual(gcd(17, 4), 1)
        self.assertEqual(gcd(101, 37), 1)

    def test_extended_gcd(self):
        g, x, y = extended_gcd(48, 18)

        self.assertEqual(g, 6)
        self.assertEqual(48 * x + 18 * y, g)

    def test_extended_gcd_negative_numbers(self):
        test_cases = [
            (-48, 18),
            (48, -18),
            (-48, -18),
            (-100, 25),
            (17, -13),
        ]

        for a, b in test_cases:
            with self.subTest(a=a, b=b):
                g, x, y = extended_gcd(a, b)

                self.assertEqual(g, gcd(a, b))
                self.assertEqual(a * x + b * y, g)

    def test_extended_gcd_zero(self):
        test_cases = [
            (0, 10),
            (10, 0),
            (0, 0),
        ]

        for a, b in test_cases:
            with self.subTest(a=a, b=b):
                g, x, y = extended_gcd(a, b)

                self.assertEqual(g, gcd(a, b))
                self.assertEqual(a * x + b * y, g)


class TestRandomGCD(unittest.TestCase):

    def test_random_gcd(self):
        """
        Test the implementation against a simple reference implementation.

        The reference implementation uses Python's modulo operation in the
        same mathematical way, but keeps the algorithm intentionally simple.
        """

        for _ in range(1000):
            a = random.randint(-1_000_000, 1_000_000)
            b = random.randint(-1_000_000, 1_000_000)

            expected = self.reference_gcd(a, b)
            result = gcd(a, b)

            self.assertEqual(result, expected)

    @staticmethod
    def reference_gcd(a: int, b: int) -> int:
        """
        Simple reference implementation used only for testing.
        """
        a = abs(a)
        b = abs(b)

        if a == 0:
            return b

        if b == 0:
            return a

        while a != b:
            if a > b:
                a -= b
            else:
                b -= a

        return a

    def test_random_extended_gcd(self):
        """
        Verify the Bézout identity for randomly generated integers.

        For every pair (a, b), the algorithm must return x and y such that:

            ax + by = gcd(a, b)
        """

        for _ in range(1000):
            a = random.randint(-100_000, 100_000)
            b = random.randint(-100_000, 100_000)

            g, x, y = extended_gcd(a, b)

            self.assertEqual(g, gcd(a, b))
            self.assertEqual(a * x + b * y, g)


if __name__ == "__main__":
    unittest.main()