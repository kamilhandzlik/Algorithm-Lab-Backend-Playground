"""
Secant Method for finding roots of nonlinear equations.

The Secant Method is a numerical root-finding algorithm used to
approximate a solution of the equation:

    f(x) = 0

Instead of calculating the derivative of the function, the method
uses two previous approximations to construct a secant line.

Given two starting points x0 and x1, the next approximation is:

    x2 = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))

The process is repeated until the function value is sufficiently
close to zero or the maximum number of iterations is reached.

Unlike the Bisection Method, the Secant Method does not require
the initial points to form a bracket containing a root.

Advantages:
- Does not require calculating a derivative.
- Usually converges faster than the Bisection Method.
- Works well for many nonlinear functions.

Disadvantages:
- It does not always converge.
- It can become unstable when f(x1) and f(x0) are very close.
- A poor choice of starting points can lead to divergence.

The implementation below returns an approximation of the root
and raises exceptions when the method cannot continue safely.
"""

import math
import random
import unittest


def secant_method(function, x0, x1, tolerance=1e-10, max_iterations=100):
    """
    Find a root of a function using the Secant Method.

    Args:
        function: Function for which f(x) = 0 is solved.
        x0: First starting point.
        x1: Second starting point.
        tolerance: Required accuracy.
        max_iterations: Maximum number of iterations.

    Returns:
        An approximation of the root.

    Raises:
        ValueError: If the parameters are invalid.
        ZeroDivisionError: If the method cannot continue because
            two function values are equal.
        RuntimeError: If the method does not converge.
    """

    if tolerance <= 0:
        raise ValueError("Tolerance must be positive.")

    if max_iterations <= 0:
        raise ValueError("Maximum iterations must be positive.")

    f0 = function(x0)
    f1 = function(x1)

    if abs(f0) <= tolerance:
        return x0

    if abs(f1) <= tolerance:
        return x1

    for _ in range(max_iterations):
        denominator = f1 - f0

        if math.isclose(denominator, 0.0, abs_tol=1e-15):
            raise ZeroDivisionError(
                "Secant method cannot continue because "
                "the function values are too close."
            )

        x2 = x1 - f1 * (x1 - x0) / denominator
        f2 = function(x2)

        if abs(f2) <= tolerance:
            return x2

        x0, x1 = x1, x2
        f0, f1 = f1, f2

    raise RuntimeError("The Secant Method did not converge.")


class TestSecantMethod(unittest.TestCase):

    def test_linear_function(self):
        root = secant_method(lambda x: 2 * x - 10, 0, 10)

        self.assertAlmostEqual(root, 5.0, places=8)

    def test_quadratic_function(self):
        root = secant_method(lambda x: x ** 2 - 4, 1, 3)

        self.assertAlmostEqual(root, 2.0, places=8)

    def test_cubic_function(self):
        root = secant_method(lambda x: x ** 3 - 8, 1, 3)

        self.assertAlmostEqual(root, 2.0, places=8)

    def test_trigonometric_function(self):
        root = secant_method(math.sin, 3, 4)

        self.assertAlmostEqual(root, math.pi, places=8)

    def test_exponential_function(self):
        root = secant_method(lambda x: math.exp(x) - 5, 0, 2)

        self.assertAlmostEqual(root, math.log(5), places=8)

    def test_function_with_negative_root(self):
        root = secant_method(lambda x: x ** 2 - 9, -4, -2)

        self.assertAlmostEqual(root, -3.0, places=8)

    def test_root_is_returned_immediately(self):
        root = secant_method(lambda x: x ** 2 - 9, 3, 10)

        self.assertEqual(root, 3)

    def test_invalid_tolerance(self):
        with self.assertRaises(ValueError):
            secant_method(lambda x: x - 1, 0, 2, tolerance=0)

    def test_invalid_iterations(self):
        with self.assertRaises(ValueError):
            secant_method(lambda x: x - 1, 0, 2, max_iterations=0)

    def test_zero_denominator(self):
        with self.assertRaises(ZeroDivisionError):
            secant_method(lambda x: x ** 2 + 1, 0, 0)

    def test_no_convergence(self):
        with self.assertRaises(RuntimeError):
            secant_method(
                lambda x: math.exp(x),
                -10,
                10,
                max_iterations=1
            )


class TestRandomFunctions(unittest.TestCase):

    def test_random_linear_equations(self):
        random.seed(42)

        for _ in range(100):
            root = random.uniform(-100, 100)
            coefficient = random.uniform(0.1, 10)

            function = lambda x, r=root, a=coefficient: a * (x - r)

            result = secant_method(
                function,
                root - 1,
                root + 1
            )

            self.assertAlmostEqual(result, root, places=7)

    def test_random_quadratic_roots(self):
        random.seed(42)

        for _ in range(100):
            root = random.uniform(-50, 50)
            other_root = random.uniform(-50, 50)

            function = (
                lambda x, r=root, o=other_root:
                (x - r) * (x - o)
            )

            if abs(root - other_root) < 0.1:
                continue

            x0 = root + 0.5
            x1 = root + 1.0

            try:
                result = secant_method(function, x0, x1)

                self.assertAlmostEqual(
                    function(result),
                    0.0,
                    places=7
                )
            except (ZeroDivisionError, RuntimeError):
                pass


if __name__ == "__main__":
    unittest.main()