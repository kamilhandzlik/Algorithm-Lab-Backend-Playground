"""
ode_numerical.py

Problem description:
---------------------
Implement two numerical methods for solving first-order ordinary differential
equations of the form:
        dy/dx = f(x, y),    y(x0) = y0

1. euler_method(f, x0, y0, x_end, n=1000)
   Approximates y(x_end) using the (simple, first-order accurate) Euler method:
       y_{i+1} = y_i + h * f(x_i, y_i)
   where h = (x_end - x0) / n.

2. rk4_method(f, x0, y0, x_end, n=1000)
   Approximates y(x_end) using the classical fourth-order Runge-Kutta method:
       k1 = f(x_i, y_i)
       k2 = f(x_i + h/2, y_i + h/2 * k1)
       k3 = f(x_i + h/2, y_i + h/2 * k2)
       k4 = f(x_i + h,   y_i + h * k3)
       y_{i+1} = y_i + (h/6) * (k1 + 2*k2 + 2*k3 + k4)

Both methods are verified against ODEs with known closed-form (analytical)
solutions:
    dy/dx = y            ->  y(x) = y0 * e^(x - x0)
    dy/dx = k*y          ->  y(x) = y0 * e^(k*(x - x0))   (linear growth/decay)
    dy/dx = cos(x)       ->  y(x) = y0 + sin(x) - sin(x0)

Random tests generate random growth/decay constants k and random intervals,
and compare both numerical methods to the exact exponential solution.
"""

import math
import random
import unittest


def euler_method(f, x0, y0, x_end, n=1000):
    """Approximate y(x_end) for dy/dx = f(x, y), y(x0) = y0, via Euler's method."""
    h = (x_end - x0) / n
    x, y = x0, y0
    for _ in range(n):
        y = y + h * f(x, y)
        x = x + h
    return y


def rk4_method(f, x0, y0, x_end, n=1000):
    """Approximate y(x_end) for dy/dx = f(x, y), y(x0) = y0, via classical RK4."""
    h = (x_end - x0) / n
    x, y = x0, y0
    for _ in range(n):
        k1 = f(x, y)
        k2 = f(x + h / 2, y + h / 2 * k1)
        k3 = f(x + h / 2, y + h / 2 * k2)
        k4 = f(x + h, y + h * k3)
        y = y + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
        x = x + h
    return y


class TestEulerMethod(unittest.TestCase):
    def test_exponential_growth(self):
        # dy/dx = y, y(0) = 1  ->  y(1) = e
        result = euler_method(lambda x, y: y, 0, 1, 1, n=5000)
        self.assertAlmostEqual(result, math.e, places=2)

    def test_exponential_decay(self):
        # dy/dx = -2y, y(0) = 5  ->  y(1) = 5 * e^-2
        result = euler_method(lambda x, y: -2 * y, 0, 5, 1, n=5000)
        self.assertAlmostEqual(result, 5 * math.exp(-2), places=2)

    def test_cosine_antiderivative(self):
        # dy/dx = cos(x), y(0) = 0  ->  y(pi/2) = sin(pi/2) = 1
        result = euler_method(lambda x, y: math.cos(x), 0, 0, math.pi / 2, n=5000)
        self.assertAlmostEqual(result, 1.0, places=2)


class TestRK4Method(unittest.TestCase):
    def test_exponential_growth(self):
        # RK4 should be far more accurate than Euler for the same n
        result = rk4_method(lambda x, y: y, 0, 1, 1, n=100)
        self.assertAlmostEqual(result, math.e, places=6)

    def test_exponential_decay(self):
        result = rk4_method(lambda x, y: -2 * y, 0, 5, 1, n=100)
        self.assertAlmostEqual(result, 5 * math.exp(-2), places=6)

    def test_cosine_antiderivative(self):
        result = rk4_method(lambda x, y: math.cos(x), 0, 0, math.pi / 2, n=100)
        self.assertAlmostEqual(result, 1.0, places=6)


class TestRandomizedAgainstAnalytical(unittest.TestCase):
    """Randomized tests: dy/dx = k*y has the exact solution y0 * e^(k*(x-x0))."""

    def setUp(self):
        random.seed()  # non-deterministic seed each run

    def test_random_linear_growth_rk4(self):
        for _ in range(20):
            k = random.uniform(-3, 3)
            x0 = random.uniform(-2, 2)
            y0 = random.uniform(0.1, 5)
            x_end = x0 + random.uniform(0.1, 2)

            expected = y0 * math.exp(k * (x_end - x0))
            actual = rk4_method(lambda x, y: k * y, x0, y0, x_end, n=500)

            self.assertAlmostEqual(actual, expected, places=4)

    def test_random_linear_growth_euler_converges(self):
        # Euler is less accurate, so we just check it stays reasonably close
        # when using a fine enough step count.
        for _ in range(20):
            k = random.uniform(-2, 2)
            x0 = random.uniform(-1, 1)
            y0 = random.uniform(0.1, 5)
            x_end = x0 + random.uniform(0.1, 1)

            expected = y0 * math.exp(k * (x_end - x0))
            actual = euler_method(lambda x, y: k * y, x0, y0, x_end, n=5000)

            # Euler's method has first-order global error, so we allow a small
            # relative tolerance instead of a fixed number of decimal places.
            self.assertAlmostEqual(actual, expected, delta=max(0.01, abs(expected) * 0.01))


if __name__ == "__main__":
    unittest.main()