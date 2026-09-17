"""
Gradient Descent for finding a local minimum of a mathematical function.

Gradient Descent is an iterative numerical optimization algorithm.
Instead of searching for a root of:

    f(x) = 0

we try to find a point where the function reaches a local minimum.

For a function f(x), the algorithm uses its derivative:

    f'(x)

The next approximation is calculated as:

    x(n+1) = x(n) - learning_rate * f'(x(n))

The derivative tells us the direction in which the function
increases. Therefore, moving in the opposite direction allows
the algorithm to descend toward a local minimum.

The learning rate determines the size of each step.

If the learning rate is too small, convergence can be very slow.
If it is too large, the algorithm can overshoot the minimum and
even diverge.

For a differentiable function, a local minimum occurs at a point
where:

    f'(x) = 0

However, not every point where the derivative is zero is a minimum.
It can also be a maximum or a saddle point.

This implementation works with one-dimensional functions and
returns an approximation of a local minimum.
"""

import math
import random
import unittest


def gradient_descent(
    function,
    derivative,
    initial_guess,
    learning_rate=0.01,
    tolerance=1e-10,
    max_iterations=10000
):
    """
    Find a local minimum of a function using Gradient Descent.

    Args:
        function: Function f(x) to minimize.
        derivative: Derivative f'(x).
        initial_guess: Starting point.
        learning_rate: Size of every optimization step.
        tolerance: Required accuracy.
        max_iterations: Maximum number of iterations.

    Returns:
        A tuple containing:

            (minimum_x, minimum_value)

    Raises:
        ValueError: If parameters are invalid.
        RuntimeError: If the algorithm does not converge.
    """

    if learning_rate <= 0:
        raise ValueError("Learning rate must be positive.")

    if tolerance <= 0:
        raise ValueError("Tolerance must be positive.")

    if max_iterations <= 0:
        raise ValueError("Maximum iterations must be positive.")

    x = initial_guess

    for _ in range(max_iterations):
        gradient = derivative(x)

        if abs(gradient) <= tolerance:
            return x, function(x)

        next_x = x - learning_rate * gradient

        if abs(next_x - x) <= tolerance:
            return next_x, function(next_x)

        x = next_x

    raise RuntimeError("Gradient Descent did not converge.")


class TestGradientDescent(unittest.TestCase):

    def test_simple_quadratic(self):
        function = lambda x: (x - 3) ** 2
        derivative = lambda x: 2 * (x - 3)

        x, value = gradient_descent(
            function,
            derivative,
            initial_guess=0,
            learning_rate=0.1
        )

        self.assertAlmostEqual(x, 3.0, places=7)
        self.assertAlmostEqual(value, 0.0, places=10)

    def test_shifted_quadratic(self):
        function = lambda x: (x + 5) ** 2
        derivative = lambda x: 2 * (x + 5)

        x, value = gradient_descent(
            function,
            derivative,
            initial_guess=10,
            learning_rate=0.1
        )

        self.assertAlmostEqual(x, -5.0, places=7)
        self.assertAlmostEqual(value, 0.0, places=10)

    def test_quadratic_with_minimum_value(self):
        function = lambda x: (x - 4) ** 2 + 7
        derivative = lambda x: 2 * (x - 4)

        x, value = gradient_descent(
            function,
            derivative,
            initial_guess=-10,
            learning_rate=0.1
        )

        self.assertAlmostEqual(x, 4.0, places=7)
        self.assertAlmostEqual(value, 7.0, places=7)

    def test_cubic_like_convex_function(self):
        function = lambda x: x ** 4 + x ** 2
        derivative = lambda x: 4 * x ** 3 + 2 * x

        x, value = gradient_descent(
            function,
            derivative,
            initial_guess=2,
            learning_rate=0.01
        )

        self.assertAlmostEqual(x, 0.0, places=6)
        self.assertAlmostEqual(value, 0.0, places=8)

    def test_exponential_quadratic(self):
        function = lambda x: math.exp(x) - x
        derivative = lambda x: math.exp(x) - 1

        x, value = gradient_descent(
            function,
            derivative,
            initial_guess=2,
            learning_rate=0.1
        )

        self.assertAlmostEqual(x, 0.0, places=6)
        self.assertAlmostEqual(value, 1.0, places=6)

    def test_already_at_minimum(self):
        function = lambda x: (x - 10) ** 2
        derivative = lambda x: 2 * (x - 10)

        x, value = gradient_descent(
            function,
            derivative,
            initial_guess=10
        )

        self.assertEqual(x, 10)
        self.assertEqual(value, 0)

    def test_invalid_learning_rate(self):
        with self.assertRaises(ValueError):
            gradient_descent(
                lambda x: x ** 2,
                lambda x: 2 * x,
                1,
                learning_rate=0
            )

    def test_invalid_tolerance(self):
        with self.assertRaises(ValueError):
            gradient_descent(
                lambda x: x ** 2,
                lambda x: 2 * x,
                1,
                tolerance=0
            )

    def test_invalid_iterations(self):
        with self.assertRaises(ValueError):
            gradient_descent(
                lambda x: x ** 2,
                lambda x: 2 * x,
                1,
                max_iterations=0
            )

    def test_non_convergence(self):
        function = lambda x: (x - 3) ** 2
        derivative = lambda x: 2 * (x - 3)

        with self.assertRaises(RuntimeError):
            gradient_descent(
                function,
                derivative,
                initial_guess=0,
                learning_rate=0.1,
                max_iterations=1
            )


class TestRandomFunctions(unittest.TestCase):

    def test_random_quadratic_minima(self):
        random.seed(42)

        for _ in range(100):
            minimum = random.uniform(-50, 50)
            coefficient = random.uniform(0.5, 5.0)

            function = (
                lambda x, m=minimum, a=coefficient:
                a * (x - m) ** 2
            )

            derivative = (
                lambda x, m=minimum, a=coefficient:
                2 * a * (x - m)
            )

            initial_guess = minimum + random.uniform(-20, 20)

            x, value = gradient_descent(
                function,
                derivative,
                initial_guess,
                learning_rate=0.05
            )

            self.assertAlmostEqual(x, minimum, places=6)
            self.assertAlmostEqual(value, 0.0, places=8)

    def test_random_shifted_quadratics(self):
        random.seed(123)

        for _ in range(100):
            minimum = random.uniform(-20, 20)
            vertical_shift = random.uniform(-10, 10)

            function = (
                lambda x, m=minimum, c=vertical_shift:
                (x - m) ** 2 + c
            )

            derivative = (
                lambda x, m=minimum:
                2 * (x - m)
            )

            initial_guess = random.uniform(-50, 50)

            x, value = gradient_descent(
                function,
                derivative,
                initial_guess,
                learning_rate=0.1
            )

            self.assertAlmostEqual(x, minimum, places=7)
            self.assertAlmostEqual(value, vertical_shift, places=7)


if __name__ == "__main__":
    unittest.main()

