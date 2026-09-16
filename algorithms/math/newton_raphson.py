"""
Newton-Raphson Method for finding roots of nonlinear equations.

The Newton-Raphson Method is an iterative numerical algorithm used
to approximate a root of an equation:

    f(x) = 0

Starting from an initial approximation x0, the next approximation
is calculated using:

    x(n+1) = x(n) - f(x(n)) / f'(x(n))

The method uses the derivative of the function to determine the
slope of the tangent line at the current approximation.

When the initial approximation is sufficiently close to a simple
root, Newton's Method usually converges very quickly.

Advantages:
- Very fast convergence near a simple root.
- Often requires relatively few iterations.
- Can provide highly accurate results.

Disadvantages:
- Requires the derivative of the function.
- Can fail when the derivative is zero or very small.
- A poor initial approximation can cause divergence.

This implementation accepts both the function and its derivative
and stops when either the function value or the change between
successive approximations becomes smaller than the tolerance.
"""

import math
import random
import unittest


def newton_raphson(function, derivative, initial_guess,
                   tolerance=1e-10, max_iterations=100):
    """
    Find a root of a function using Newton-Raphson Method.

    Args:
        function: Function f(x).
        derivative: Derivative f'(x).
        initial_guess: Starting approximation.
        tolerance: Required numerical accuracy.
        max_iterations: Maximum number of iterations.

    Returns:
        Approximation of the root.

    Raises:
        ValueError: If tolerance or max_iterations is invalid.
        ZeroDivisionError: If the derivative is too close to zero.
        RuntimeError: If the method does not converge.
    """

    if tolerance <= 0:
        raise ValueError("Tolerance must be positive.")

    if max_iterations <= 0:
        raise ValueError("Maximum iterations must be positive.")

    x = initial_guess

    for _ in range(max_iterations):
        fx = function(x)

        if abs(fx) <= tolerance:
            return x

        derivative_x = derivative(x)

        if math.isclose(derivative_x, 0.0, abs_tol=1e-15):
            raise ZeroDivisionError(
                "Derivative is too close to zero."
            )

        next_x = x - fx / derivative_x

        if abs(next_x - x) <= tolerance:
            return next_x

        x = next_x

    raise RuntimeError("Newton-Raphson Method did not converge.")


class TestNewtonRaphson(unittest.TestCase):

    def test_linear_function(self):
        function = lambda x: 3 * x - 12
        derivative = lambda x: 3

        root = newton_raphson(function, derivative, 0)

        self.assertAlmostEqual(root, 4.0, places=8)

    def test_quadratic_function(self):
        function = lambda x: x ** 2 - 9
        derivative = lambda x: 2 * x

        root = newton_raphson(function, derivative, 5)

        self.assertAlmostEqual(root, 3.0, places=8)

    def test_negative_root(self):
        function = lambda x: x ** 2 - 16
        derivative = lambda x: 2 * x

        root = newton_raphson(function, derivative, -5)

        self.assertAlmostEqual(root, -4.0, places=8)

    def test_cubic_function(self):
        function = lambda x: x ** 3 - 27
        derivative = lambda x: 3 * x ** 2

        root = newton_raphson(function, derivative, 2)

        self.assertAlmostEqual(root, 3.0, places=8)

    def test_square_root(self):
        function = lambda x: x ** 2 - 2
        derivative = lambda x: 2 * x

        root = newton_raphson(function, derivative, 1)

        self.assertAlmostEqual(root, math.sqrt(2), places=8)

    def test_trigonometric_function(self):
        function = math.sin
        derivative = math.cos

        root = newton_raphson(function, derivative, 3)

        self.assertAlmostEqual(root, math.pi, places=8)

    def test_exponential_function(self):
        function = lambda x: math.exp(x) - 7
        derivative = math.exp

        root = newton_raphson(function, derivative, 2)

        self.assertAlmostEqual(root, math.log(7), places=8)

    def test_immediate_root(self):
        function = lambda x: x ** 2 - 25
        derivative = lambda x: 2 * x

        root = newton_raphson(function, derivative, 5)

        self.assertEqual(root, 5)

    def test_invalid_tolerance(self):
        with self.assertRaises(ValueError):
            newton_raphson(
                lambda x: x - 1,
                lambda x: 1,
                0,
                tolerance=0
            )

    def test_invalid_iterations(self):
        with self.assertRaises(ValueError):
            newton_raphson(
                lambda x: x - 1,
                lambda x: 1,
                0,
                max_iterations=0
            )



class TestRandomFunctions(unittest.TestCase):

    def test_random_linear_equations(self):
        random.seed(42)

        for _ in range(100):
            root = random.uniform(-100, 100)
            coefficient = random.uniform(0.1, 20)

            function = (
                lambda x, r=root, a=coefficient:
                a * (x - r)
            )

            derivative = (
                lambda x, a=coefficient:
                a
            )

            initial_guess = root + random.uniform(-10, 10)

            result = newton_raphson(
                function,
                derivative,
                initial_guess
            )

            self.assertAlmostEqual(result, root, places=7)

    def test_random_quadratic_equations(self):
        random.seed(42)

        for _ in range(100):
            root = random.uniform(-50, 50)

            if abs(root) < 1:
                root += 2

            function = (
                lambda x, r=root:
                x ** 2 - r ** 2
            )

            derivative = lambda x: 2 * x

            initial_guess = root * 1.5

            result = newton_raphson(
                function,
                derivative,
                initial_guess
            )

            self.assertAlmostEqual(
                function(result),
                0.0,
                places=7
            )


if __name__ == "__main__":
    unittest.main()
