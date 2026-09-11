"""
newton_method.py

Problem description:
---------------------
Implement the Newton-Raphson method for finding roots of a differentiable
function f(x), i.e. solving f(x) = 0.

newton_raphson(f, f_prime, x0, tol=1e-10, max_iter=100)
    Starting from an initial guess x0, repeatedly applies the update rule
    (derived directly from the first-order Taylor expansion of f around x_i):
        x_{i+1} = x_i - f(x_i) / f_prime(x_i)
    until |f(x_i)| < tol or max_iter iterations have been performed.

Correctness is checked against problems with known exact roots:
    - sqrt(a):  root of f(x) = x^2 - a
    - cbrt(a):  root of f(x) = x^3 - a
    - a root of f(x) = cos(x) - x  (the Dottie number, ~0.739085...)

Random tests generate random quadratic equations a*x^2 + b*x + c = 0 with
real roots (guaranteed via a positive discriminant), and compare the root
found by Newton's method against the exact root from the quadratic formula.
"""

import math
import random
import unittest


def newton_raphson(f, f_prime, x0, tol=1e-10, max_iter=100):
    """Find a root of f near x0 using the Newton-Raphson method."""
    x = x0
    for _ in range(max_iter):
        fx = f(x)
        if abs(fx) < tol:
            return x
        fpx = f_prime(x)
        if fpx == 0:
            raise ZeroDivisionError("Derivative is zero; Newton's method failed.")
        x = x - fx / fpx
    return x


class TestNewtonRaphsonKnownRoots(unittest.TestCase):
    def test_square_root(self):
        # f(x) = x^2 - 16, root = 4
        f = lambda x: x**2 - 16
        f_prime = lambda x: 2 * x
        result = newton_raphson(f, f_prime, x0=1.0)
        self.assertAlmostEqual(result, 4.0, places=8)

    def test_cube_root(self):
        # f(x) = x^3 - 27, root = 3
        f = lambda x: x**3 - 27
        f_prime = lambda x: 3 * x**2
        result = newton_raphson(f, f_prime, x0=1.0)
        self.assertAlmostEqual(result, 3.0, places=8)

    def test_dottie_number(self):
        # f(x) = cos(x) - x, root ~ 0.7390851332151607 (the Dottie number)
        f = lambda x: math.cos(x) - x
        f_prime = lambda x: -math.sin(x) - 1
        result = newton_raphson(f, f_prime, x0=0.5)
        self.assertAlmostEqual(result, 0.7390851332151607, places=8)

    def test_negative_root(self):
        # f(x) = x^2 - 9, starting near -1 should converge to -3
        f = lambda x: x**2 - 9
        f_prime = lambda x: 2 * x
        result = newton_raphson(f, f_prime, x0=-1.0)
        self.assertAlmostEqual(result, -3.0, places=8)


class TestRandomizedAgainstQuadraticFormula(unittest.TestCase):
    """Randomized tests comparing Newton's method to the exact quadratic formula
    for a*x^2 + b*x + c = 0."""

    def setUp(self):
        random.seed()  # non-deterministic seed each run

    def test_random_quadratics(self):
        for _ in range(20):
            a = random.uniform(0.5, 5)
            # Choose roots directly, then derive b, c, to guarantee real roots
            r1 = random.uniform(-10, 10)
            r2 = random.uniform(-10, 10)
            b = -a * (r1 + r2)
            c = a * r1 * r2

            f = lambda x: a * x**2 + b * x + c
            f_prime = lambda x: 2 * a * x + b

            # Start Newton's method slightly offset from one of the roots.
            x0 = r1 + 0.5

            result = newton_raphson(f, f_prime, x0)

            # Genuine correctness check: f(result) must be (numerically) zero...
            self.assertAlmostEqual(f(result), 0.0, places=6)
            # ...and the result must actually coincide with one of the two
            # exact roots computed independently of Newton's method.
            min_distance = min(abs(result - r1), abs(result - r2))
            self.assertLess(min_distance, 1e-5)


if __name__ == "__main__":
    unittest.main()