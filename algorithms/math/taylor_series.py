"""
taylor_series.py

Problem description:
---------------------
Implement a numerical n-th derivative estimator and use it to build a Taylor
series approximation of a function around a point x0, without relying on any
symbolic/analytical derivative formulas supplied by the caller.

1. nth_derivative(f, x, n, h=1e-3)
   Approximates the n-th derivative of f at x using a straightforward
   iterated central-difference scheme:
       f^(0)(x) = f(x)
       f^(n)(x) ≈ (f^(n-1)(x + h) - f^(n-1)(x - h)) / (2h)
   (Each derivative order is obtained by numerically differentiating the
   previous derivative "function".)

2. taylor_approximation(f, x0, x, n_terms, h=1e-3)
   Builds the degree-(n_terms - 1) Taylor polynomial of f around x0 and
   evaluates it at x:
       f(x) ≈ sum_{k=0}^{n_terms-1} [ f^(k)(x0) / k! ] * (x - x0)^k

Correctness is checked against functions with well-known Taylor series
around x0 = 0:
    e^x  = 1 + x + x^2/2! + x^3/3! + ...
    sin(x) = x - x^3/3! + x^5/5! - ...
    cos(x) = 1 - x^2/2! + x^4/4! - ...

Random tests pick random small x values (inside the region where a modest
number of Taylor terms already gives a good approximation) and compare the
Taylor approximation of e^x against math.exp(x).
"""

import math
import random
import unittest


def nth_derivative(f, x, n, h=1e-3):
    """Approximate the n-th derivative of f at x via iterated central differences."""
    if n == 0:
        return f(x)

    def prev(y):
        return nth_derivative(f, y, n - 1, h)

    return (prev(x + h) - prev(x - h)) / (2 * h)


def taylor_approximation(f, x0, x, n_terms, h=1e-3):
    """Evaluate the degree-(n_terms - 1) Taylor polynomial of f around x0 at point x."""
    total = 0.0
    for k in range(n_terms):
        coefficient = nth_derivative(f, x0, k, h) / math.factorial(k)
        total += coefficient * (x - x0) ** k
    return total


class TestNthDerivative(unittest.TestCase):
    def test_zeroth_derivative_is_function_value(self):
        result = nth_derivative(math.sin, 1.0, 0)
        self.assertAlmostEqual(result, math.sin(1.0), places=8)

    def test_second_derivative_of_square(self):
        # f(x) = x^2, f''(x) = 2 for all x
        result = nth_derivative(lambda x: x ** 2, 5.0, 2, h=1e-2)
        self.assertAlmostEqual(result, 2.0, places=2)

    def test_third_derivative_of_cube(self):
        # f(x) = x^3, f'''(x) = 6 for all x
        result = nth_derivative(lambda x: x ** 3, 2.0, 3, h=1e-1)
        self.assertAlmostEqual(result, 6.0, places=1)


class TestTaylorApproximation(unittest.TestCase):
    def test_exp_at_zero(self):
        # e^x around x0 = 0, evaluated at x = 1, using 10 terms
        result = taylor_approximation(math.exp, x0=0, x=1, n_terms=10, h=1e-2)
        self.assertAlmostEqual(result, math.e, places=2)

    def test_sin_at_zero(self):
        # sin(x) around x0 = 0, evaluated at x = 0.5, using 8 terms
        result = taylor_approximation(math.sin, x0=0, x=0.5, n_terms=8, h=1e-2)
        self.assertAlmostEqual(result, math.sin(0.5), places=2)

    def test_cos_at_zero(self):
        # cos(x) around x0 = 0, evaluated at x = 0.3, using 8 terms
        result = taylor_approximation(math.cos, x0=0, x=0.3, n_terms=8, h=1e-2)
        self.assertAlmostEqual(result, math.cos(0.3), places=2)


class TestRandomizedAgainstMathExp(unittest.TestCase):
    """Randomized tests comparing the Taylor approximation of e^x against
    Python's built-in math.exp for random small x values."""

    def setUp(self):
        random.seed()  # non-deterministic seed each run

    def test_random_small_x_values(self):
        for _ in range(15):
            x = random.uniform(-1.5, 1.5)
            expected = math.exp(x)
            # n_terms=10 keeps truncation error tiny for |x| <= 1.5, and a
            # slightly larger step h=3e-2 keeps the recursive finite-difference
            # derivative estimates numerically stable at higher orders.
            actual = taylor_approximation(math.exp, x0=0, x=x, n_terms=10, h=3e-2)
            self.assertAlmostEqual(actual, expected, places=2)


if __name__ == "__main__":
    unittest.main()
