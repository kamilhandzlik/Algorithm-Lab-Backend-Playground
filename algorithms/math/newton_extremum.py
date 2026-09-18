"""
Newton's Method for finding extrema of differentiable functions.

Newton's Method can also be used to find local extrema of a function.

An extremum occurs at a stationary point where:

    f'(x) = 0

Instead of directly solving f(x) = 0, we apply Newton's Method
to the derivative f'(x).

The iteration formula becomes:

    x(n+1) = x(n) - f'(x(n)) / f''(x(n))

where:

    f'(x)  -> first derivative
    f''(x) -> second derivative

After finding a stationary point, the second derivative can be
used to classify it:

    f''(x) > 0  -> local minimum
    f''(x) < 0  -> local maximum
    f''(x) = 0  -> inconclusive

The algorithm is iterative and therefore depends on the initial
approximation. A poor starting point can lead to convergence to
a different stationary point or cause the method to diverge.

The function returns the position of the extremum, its value,
and its classification.
"""

import math
import random
import unittest


def newton_extremum(
        function,
        first_derivative,
        second_derivative,
        initial_guess,
        tolerance=1e-10,
        max_iterations=100
):
    """
    Find a local extremum using Newton's Method.

    Args:
        function: Function f(x).
        first_derivative: First derivative f'(x).
        second_derivative: Second derivative f''(x).
        initial_guess: Starting approximation.
        tolerance: Required accuracy.
        max_iterations: Maximum number of iterations.

    Returns:
        Tuple:
            (x, function(x), classification)

        classification is one of:
            "minimum"
            "maximum"
            "inconclusive"

    Raises:
        ValueError: If parameters are invalid.
        ZeroDivisionError: If the second derivative is too close
            to zero.
        RuntimeError: If the method does not converge.
    """

    if tolerance <= 0:
        raise ValueError("Tolerance must be positive.")

    if max_iterations <= 0:
        raise ValueError("Maximum iterations must be positive.")

    x = initial_guess

    for _ in range(max_iterations):
        first = first_derivative(x)
        second = second_derivative(x)

        if abs(first) <= tolerance:
            break

        if math.isclose(second, 0.0, abs_tol=1e-15):
            raise ZeroDivisionError(
                "Second derivative is too close to zero."
            )

        next_x = x - first / second

        if abs(next_x - x) <= tolerance:
            x = next_x
            break

        x = next_x
    else:
        raise RuntimeError(
            "Newton's Method did not converge."
        )

    second = second_derivative(x)

    if second > tolerance:
        classification = "minimum"
    elif second < -tolerance:
        classification = "maximum"
    else:
        classification = "inconclusive"

    return x, function(x), classification


class TestNewtonExtremum(unittest.TestCase):

    def test_quadratic_minimum(self):
        function = lambda x: (x - 3) ** 2
        first = lambda x: 2 * (x - 3)
        second = lambda x: 2

        x, value, classification = newton_extremum(
            function,
            first,
            second,
            0
        )

        self.assertAlmostEqual(x, 3.0, places=8)
        self.assertAlmostEqual(value, 0.0, places=8)
        self.assertEqual(classification, "minimum")

    def test_quadratic_maximum(self):
        function = lambda x: -(x - 4) ** 2 + 10
        first = lambda x: -2 * (x - 4)
        second = lambda x: -2

        x, value, classification = newton_extremum(
            function,
            first,
            second,
            10
        )

        self.assertAlmostEqual(x, 4.0, places=8)
        self.assertAlmostEqual(value, 10.0, places=8)
        self.assertEqual(classification, "maximum")

    def test_shifted_quadratic(self):
        function = lambda x: 5 * (x + 7) ** 2 - 12
        first = lambda x: 10 * (x + 7)
        second = lambda x: 10

        x, value, classification = newton_extremum(
            function,
            first,
            second,
            20
        )

        self.assertAlmostEqual(x, -7.0, places=8)
        self.assertAlmostEqual(value, -12.0, places=8)
        self.assertEqual(classification, "minimum")

    def test_cubic_function(self):
        function = lambda x: x ** 3 - 3 * x
        first = lambda x: 3 * x ** 2 - 3
        second = lambda x: 6 * x

        x, value, classification = newton_extremum(
            function,
            first,
            second,
            2
        )

        self.assertAlmostEqual(x, 1.0, places=8)
        self.assertAlmostEqual(value, -2.0, places=8)
        self.assertEqual(classification, "minimum")

    def test_cubic_other_extremum(self):
        function = lambda x: x ** 3 - 3 * x
        first = lambda x: 3 * x ** 2 - 3
        second = lambda x: 6 * x

        x, value, classification = newton_extremum(
            function,
            first,
            second,
            -2
        )

        self.assertAlmostEqual(x, -1.0, places=8)
        self.assertAlmostEqual(value, 2.0, places=8)
        self.assertEqual(classification, "maximum")

    def test_trigonometric_function(self):
        function = math.cos
        first = lambda x: -math.sin(x)
        second = lambda x: -math.cos(x)

        x, value, classification = newton_extremum(
            function,
            first,
            second,
            0.5
        )

        self.assertAlmostEqual(x, 0.0, places=8)
        self.assertAlmostEqual(value, 1.0, places=8)
        self.assertEqual(classification, "maximum")

    def test_already_at_extremum(self):
        function = lambda x: (x - 5) ** 2
        first = lambda x: 2 * (x - 5)
        second = lambda x: 2

        x, value, classification = newton_extremum(
            function,
            first,
            second,
            5
        )

        self.assertEqual(x, 5)
        self.assertEqual(value, 0)
        self.assertEqual(classification, "minimum")

    def test_invalid_tolerance(self):
        with self.assertRaises(ValueError):
            newton_extremum(
                lambda x: x ** 2,
                lambda x: 2 * x,
                lambda x: 2,
                1,
                tolerance=0
            )

    def test_invalid_iterations(self):
        with self.assertRaises(ValueError):
            newton_extremum(
                lambda x: x ** 2,
                lambda x: 2 * x,
                lambda x: 2,
                1,
                max_iterations=0
            )

    def test_inconclusive_classification(self):
        function = lambda x: x ** 4
        first = lambda x: 4 * x ** 3
        second = lambda x: 12 * x ** 2

        x, value, classification = newton_extremum(
            function,
            first,
            second,
            0
        )

        self.assertAlmostEqual(x, 0.0, places=8)
        self.assertAlmostEqual(value, 0.0, places=8)
        self.assertEqual(classification, "inconclusive")


class TestRandomFunctions(unittest.TestCase):

    def test_random_quadratic_minima(self):
        random.seed(42)

        for _ in range(100):
            minimum = random.uniform(-100, 100)
            coefficient = random.uniform(0.5, 10)

            function = (
                lambda x, m=minimum, a=coefficient:
                a * (x - m) ** 2
            )

            first = (
                lambda x, m=minimum, a=coefficient:
                2 * a * (x - m)
            )

            second = (
                lambda x, a=coefficient:
                2 * a
            )

            initial_guess = minimum + random.uniform(-50, 50)

            x, value, classification = newton_extremum(
                function,
                first,
                second,
                initial_guess
            )

            self.assertAlmostEqual(
                x,
                minimum,
                places=7
            )

            self.assertAlmostEqual(
                value,
                0.0,
                places=7
            )

            self.assertEqual(
                classification,
                "minimum"
            )

    def test_random_quadratic_maxima(self):
        random.seed(123)

        for _ in range(100):
            maximum = random.uniform(-100, 100)
            coefficient = random.uniform(0.5, 10)
            height = random.uniform(-100, 100)

            function = (
                lambda x, m=maximum, a=coefficient, h=height:
                -a * (x - m) ** 2 + h
            )

            first = (
                lambda x, m=maximum, a=coefficient:
                -2 * a * (x - m)
            )

            second = (
                lambda x, a=coefficient:
                -2 * a
            )

            initial_guess = maximum + random.uniform(-50, 50)

            x, value, classification = newton_extremum(
                function,
                first,
                second,
                initial_guess
            )

            self.assertAlmostEqual(
                x,
                maximum,
                places=7
            )

            self.assertAlmostEqual(
                value,
                height,
                places=7
            )

            self.assertEqual(
                classification,
                "maximum"
            )


if __name__ == "__main__":
    unittest.main()
