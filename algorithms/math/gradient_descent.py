"""
gradient_descent.py

Problem description:
---------------------
Implement numerical partial derivatives for multivariable functions and use
them to perform gradient descent optimization.

1. numerical_gradient(f, point, h=1e-6)
   Given f: R^n -> R and a point (a tuple/list of n coordinates), approximates
   the gradient vector (df/dx1, df/dx2, ..., df/dxn) using the central
   difference formula applied to each coordinate independently:
       df/dx_i ≈ (f(..., x_i + h, ...) - f(..., x_i - h, ...)) / (2h)

2. gradient_descent(f, start, learning_rate=0.1, tol=1e-8, max_iter=10000)
   Starting from `start`, repeatedly moves in the direction of steepest
   descent:
       point_{k+1} = point_k - learning_rate * numerical_gradient(f, point_k)
   until the gradient's magnitude drops below `tol` or max_iter is reached.
   Returns the final point (an approximate local minimum of f).

Correctness is verified against convex "bowl" functions with a known,
unique global minimum:
    f(x, y) = (x - a)^2 + (y - b)^2            -> minimum at (a, b)
    f(x, y) = 2*(x - a)^2 + 5*(y - b)^2 + c     -> minimum at (a, b), value c

Random tests generate random paraboloids f(x, y) = p*(x-a)^2 + q*(y-b)^2 with
random positive p, q and random centers (a, b), then check that gradient
descent converges to (a, b).
"""

import random
import unittest


def numerical_gradient(f, point, h=1e-6):
    """Approximate the gradient of f at `point` (a sequence of coordinates)."""
    point = list(point)
    grad = []
    for i in range(len(point)):
        forward = point[:]
        backward = point[:]
        forward[i] += h
        backward[i] -= h
        partial = (f(*forward) - f(*backward)) / (2 * h)
        grad.append(partial)
    return grad


def gradient_descent(f, start, learning_rate=0.1, tol=1e-8, max_iter=10000):
    """Find an approximate local minimum of f starting from `start`."""
    point = list(start)
    for _ in range(max_iter):
        grad = numerical_gradient(f, point)
        magnitude = sum(g**2 for g in grad) ** 0.5
        if magnitude < tol:
            break
        point = [p - learning_rate * g for p, g in zip(point, grad)]
    return point


class TestNumericalGradient(unittest.TestCase):
    def test_gradient_of_simple_paraboloid(self):
        # f(x, y) = x^2 + y^2, grad = (2x, 2y)
        f = lambda x, y: x**2 + y**2
        grad = numerical_gradient(f, (3.0, -2.0))
        self.assertAlmostEqual(grad[0], 6.0, places=4)
        self.assertAlmostEqual(grad[1], -4.0, places=4)

    def test_gradient_of_mixed_function(self):
        # f(x, y) = x^2 * y + y^3, df/dx = 2xy, df/dy = x^2 + 3y^2
        f = lambda x, y: x**2 * y + y**3
        grad = numerical_gradient(f, (2.0, 1.0))
        self.assertAlmostEqual(grad[0], 4.0, places=3)
        self.assertAlmostEqual(grad[1], 7.0, places=3)


class TestGradientDescent(unittest.TestCase):
    def test_simple_bowl_minimum(self):
        # f(x, y) = (x - 3)^2 + (y + 2)^2, minimum at (3, -2)
        f = lambda x, y: (x - 3) ** 2 + (y + 2) ** 2
        result = gradient_descent(f, start=(0.0, 0.0))
        self.assertAlmostEqual(result[0], 3.0, places=4)
        self.assertAlmostEqual(result[1], -2.0, places=4)

    def test_scaled_bowl_minimum(self):
        # f(x, y) = 2*(x - 1)^2 + 5*(y - 4)^2 + 10, minimum at (1, 4)
        f = lambda x, y: 2 * (x - 1) ** 2 + 5 * (y - 4) ** 2 + 10
        result = gradient_descent(f, start=(-5.0, -5.0), learning_rate=0.05)
        self.assertAlmostEqual(result[0], 1.0, places=3)
        self.assertAlmostEqual(result[1], 4.0, places=3)
        self.assertAlmostEqual(f(*result), 10.0, places=3)


class TestRandomizedAgainstKnownMinimum(unittest.TestCase):
    """Randomized tests: f(x, y) = p*(x-a)^2 + q*(y-b)^2 always has its
    unique global minimum at (a, b), regardless of p, q > 0."""

    def setUp(self):
        random.seed()  # non-deterministic seed each run

    def test_random_paraboloids(self):
        for _ in range(15):
            p = random.uniform(0.5, 3)
            q = random.uniform(0.5, 3)
            a = random.uniform(-5, 5)
            b = random.uniform(-5, 5)

            f = lambda x, y: p * (x - a) ** 2 + q * (y - b) ** 2

            start = (a + random.uniform(-3, 3), b + random.uniform(-3, 3))
            result = gradient_descent(f, start=start, learning_rate=0.05, max_iter=20000)

            self.assertAlmostEqual(result[0], a, places=2)
            self.assertAlmostEqual(result[1], b, places=2)


if __name__ == "__main__":
    unittest.main()