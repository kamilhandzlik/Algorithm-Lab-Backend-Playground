"""
Simpson's Rule for numerical integration.

Numerical integration is used to approximate a definite integral
when finding an exact antiderivative is difficult or impossible.

For a function f(x), we want to calculate:

    integral from a to b of f(x) dx

Simpson's Rule approximates the function using quadratic
polynomials over small intervals.

For an even number n of subintervals, with:

    h = (b - a) / n

the composite Simpson formula is:

    integral ~= h / 3 * [
        f(x0)
        + f(xn)
        + 4 * (f(x1) + f(x3) + ...)
        + 2 * (f(x2) + f(x4) + ...)
    ]

The method generally provides much better accuracy than the
trapezoidal rule for smooth functions.

The number of subintervals must be even.

For sufficiently smooth functions, Simpson's Rule has an error
proportional to:

    O(h^4)

This means that reducing the step size can significantly improve
the approximation.

The implementation below uses only the Python standard library
and supports arbitrary callable functions.
"""

import math
import random
import unittest


def simpson_integrate(function, start, end, intervals=100):
    """
    Approximate a definite integral using composite Simpson's Rule.

    Args:
        function: Function to integrate.
        start: Lower integration limit.
        end: Upper integration limit.
        intervals: Number of subintervals. Must be even.

    Returns:
        Numerical approximation of the definite integral.

    Raises:
        ValueError: If intervals are invalid or start == end.
    """

    if intervals <= 0:
        raise ValueError(
            "Number of intervals must be positive."
        )

    if intervals % 2 != 0:
        raise ValueError(
            "Number of intervals must be even."
        )

    if start == end:
        return 0.0

    step = (end - start) / intervals

    total = (
            function(start)
            + function(end)
    )

    for i in range(1, intervals):
        x = start + i * step

        if i % 2 == 0:
            total += 2 * function(x)
        else:
            total += 4 * function(x)

    return total * step / 3


class TestSimpsonIntegration(unittest.TestCase):

    def test_constant_function(self):
        result = simpson_integrate(
            lambda x: 5,
            0,
            10
        )

        self.assertAlmostEqual(result, 50.0, places=10)

    def test_linear_function(self):
        result = simpson_integrate(
            lambda x: x,
            0,
            10
        )

        self.assertAlmostEqual(result, 50.0, places=10)

    def test_quadratic_function(self):
        result = simpson_integrate(
            lambda x: x ** 2,
            0,
            3
        )

        self.assertAlmostEqual(result, 9.0, places=10)

    def test_cubic_function(self):
        result = simpson_integrate(
            lambda x: x ** 3,
            0,
            2
        )

        self.assertAlmostEqual(result, 4.0, places=10)

    def test_fourth_degree_polynomial(self):
        result = simpson_integrate(
            lambda x: x ** 4,
            0,
            1,
            intervals=100
        )

        self.assertAlmostEqual(
            result,
            1 / 5,
            places=8
        )

    def test_negative_function(self):
        result = simpson_integrate(
            lambda x: -x ** 2,
            0,
            3
        )

        self.assertAlmostEqual(
            result,
            -9.0,
            places=10
        )

    def test_reversed_limits(self):
        result = simpson_integrate(
            lambda x: x ** 2,
            3,
            0
        )

        self.assertAlmostEqual(
            result,
            -9.0,
            places=10
        )

    def test_gaussian_function(self):
        result = simpson_integrate(
            lambda x: math.exp(-x ** 2),
            -1,
            1,
            intervals=200
        )

        expected = math.sqrt(math.pi) * math.erf(1)

        self.assertAlmostEqual(
            result,
            expected,
            places=8
        )

    def test_zero_width_interval(self):
        result = simpson_integrate(
            lambda x: x ** 2,
            5,
            5
        )

        self.assertEqual(result, 0.0)

    def test_odd_number_of_intervals(self):
        with self.assertRaises(ValueError):
            simpson_integrate(
                lambda x: x ** 2,
                0,
                1,
                intervals=99
            )

    def test_invalid_intervals(self):
        with self.assertRaises(ValueError):
            simpson_integrate(
                lambda x: x,
                0,
                1,
                intervals=0
            )


class TestRandomPolynomials(unittest.TestCase):

    def test_random_linear_functions(self):
        random.seed(42)

        for _ in range(100):
            a = random.uniform(-10, 10)
            b = random.uniform(-10, 10)

            start = random.uniform(-5, 5)
            end = random.uniform(-5, 5)

            if math.isclose(start, end):
                continue

            function = (
                lambda x, a=a, b=b:
                a * x + b
            )

            expected = (
                    a * (end ** 2 - start ** 2) / 2
                    + b * (end - start)
            )

            result = simpson_integrate(
                function,
                start,
                end,
                intervals=100
            )

            self.assertAlmostEqual(
                result,
                expected,
                places=8
            )

    def test_random_quadratic_functions(self):
        random.seed(123)

        for _ in range(100):
            a = random.uniform(-5, 5)
            b = random.uniform(-5, 5)
            c = random.uniform(-5, 5)

            start = random.uniform(-5, 5)
            end = random.uniform(-5, 5)

            if math.isclose(start, end):
                continue

            function = (
                lambda x, a=a, b=b, c=c:
                a * x ** 2 + b * x + c
            )

            expected = (
                    a * (end ** 3 - start ** 3) / 3
                    + b * (end ** 2 - start ** 2) / 2
                    + c * (end - start)
            )

            result = simpson_integrate(
                function,
                start,
                end,
                intervals=100
            )

            self.assertAlmostEqual(
                result,
                expected,
                places=8
            )

    def test_random_cubic_functions(self):
        random.seed(456)

        for _ in range(100):
            a = random.uniform(-3, 3)
            b = random.uniform(-3, 3)
            c = random.uniform(-3, 3)
            d = random.uniform(-3, 3)

            start = random.uniform(-3, 3)
            end = random.uniform(-3, 3)

            if math.isclose(start, end):
                continue

            function = (
                lambda x, a=a, b=b, c=c, d=d:
                a * x ** 3
                + b * x ** 2
                + c * x
                + d
            )

            expected = (
                    a * (end ** 4 - start ** 4) / 4
                    + b * (end ** 3 - start ** 3) / 3
                    + c * (end ** 2 - start ** 2) / 2
                    + d * (end - start)
            )

            result = simpson_integrate(
                function,
                start,
                end,
                intervals=100
            )

            self.assertAlmostEqual(
                result,
                expected,
                places=7
            )


if __name__ == "__main__":
    unittest.main()
