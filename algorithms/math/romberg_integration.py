"""
Romberg Integration
===================

Romberg integration is a numerical method for approximating definite
integrals with high accuracy.

The method starts with the trapezoidal rule using progressively finer
partitions. Instead of simply accepting the trapezoidal approximations,
Romberg integration applies Richardson extrapolation to cancel the
leading numerical error terms.

For a sufficiently smooth function, the trapezoidal rule has an error
of approximately:

    I - T(h) = C1*h^2 + C2*h^4 + C3*h^6 + ...

where h is the step size.

Because the error contains even powers of h, we can combine two
approximations with different step sizes and eliminate the leading
error term.

The Romberg table is constructed using:

    R[k][0] = trapezoidal approximation with 2^k intervals

and:

    R[k][j] =
        R[k][j-1]
        + (R[k][j-1] - R[k-1][j-1]) / (4^j - 1)

The final value R[n][n] is usually much more accurate than the original
trapezoidal approximation.

This implementation uses an iterative construction of the Romberg table
and stops when two consecutive diagonal approximations differ by less
than the requested tolerance.
"""

import math
import random
import unittest


def romberg_integration(
        function,
        lower,
        upper,
        tolerance=1e-10,
        max_order=12
):
    """
    Approximate the definite integral of `function` from `lower` to `upper`
    using Romberg integration.

    Parameters
    ----------
    function : callable
        Function to integrate.

    lower : float
        Lower integration limit.

    upper : float
        Upper integration limit.

    tolerance : float
        Desired absolute difference between consecutive Romberg
        diagonal approximations.

    max_order : int
        Maximum order of the Romberg table.

    Returns
    -------
    float
        Numerical approximation of the integral.

    Raises
    ------
    ValueError
        If tolerance or max_order is invalid.
    """

    if tolerance <= 0:
        raise ValueError("tolerance must be positive")

    if max_order < 1:
        raise ValueError("max_order must be at least 1")

    if lower == upper:
        return 0.0

    if lower > upper:
        return -romberg_integration(
            function,
            upper,
            lower,
            tolerance,
            max_order
        )

    previous_row = []

    interval = upper - lower

    # First trapezoidal approximation.
    trapezoidal = (
            0.5 * interval *
            (function(lower) + function(upper))
    )

    previous_row.append(trapezoidal)

    previous_diagonal = trapezoidal

    for order in range(1, max_order):

        number_of_new_points = 2 ** (order - 1)

        step = interval / (2 ** order)

        new_points_sum = 0.0

        for i in range(1, number_of_new_points + 1):
            x = lower + (2 * i - 1) * step
            new_points_sum += function(x)

        trapezoidal = (
                0.5 * previous_row[0]
                + step * new_points_sum
        )

        current_row = [trapezoidal]

        for column in range(1, order + 1):
            factor = 4 ** column

            extrapolated = (
                    current_row[column - 1]
                    + (
                            current_row[column - 1]
                            - previous_row[column - 1]
                    ) / (factor - 1)
            )

            current_row.append(extrapolated)

        current_diagonal = current_row[-1]

        if abs(current_diagonal - previous_diagonal) < tolerance:
            return current_diagonal

        previous_row = current_row
        previous_diagonal = current_diagonal

    return previous_diagonal


class TestRombergIntegration(unittest.TestCase):

    def test_polynomial(self):
        result = romberg_integration(
            lambda x: x ** 2,
            0,
            1
        )

        self.assertAlmostEqual(
            result,
            1 / 3,
            places=10
        )

    def test_fourth_power(self):
        result = romberg_integration(
            lambda x: x ** 4,
            0,
            1
        )

        self.assertAlmostEqual(
            result,
            1 / 5,
            places=10
        )

    def test_sine(self):
        result = romberg_integration(
            math.sin,
            0,
            math.pi
        )

        self.assertAlmostEqual(
            result,
            2.0,
            places=10
        )

    def test_cosine(self):
        result = romberg_integration(
            math.cos,
            0,
            math.pi / 2
        )

        self.assertAlmostEqual(
            result,
            1.0,
            places=10
        )

    def test_exponential(self):
        result = romberg_integration(
            math.exp,
            0,
            1
        )

        self.assertAlmostEqual(
            result,
            math.e - 1,
            places=10
        )

    def test_reversed_limits(self):
        result = romberg_integration(
            lambda x: x ** 2,
            1,
            0
        )

        self.assertAlmostEqual(
            result,
            -1 / 3,
            places=10
        )

    def test_zero_interval(self):
        result = romberg_integration(
            lambda x: x ** 10 + 5 * x,
            3,
            3
        )

        self.assertEqual(result, 0.0)

    def test_gaussian_like_function(self):
        result = romberg_integration(
            lambda x: math.exp(-x ** 2),
            -1,
            1
        )

        expected = 1.493648265624854

        self.assertAlmostEqual(
            result,
            expected,
            places=9
        )

    def test_invalid_tolerance(self):
        with self.assertRaises(ValueError):
            romberg_integration(
                lambda x: x,
                0,
                1,
                tolerance=0
            )

    def test_invalid_order(self):
        with self.assertRaises(ValueError):
            romberg_integration(
                lambda x: x,
                0,
                1,
                max_order=0
            )


class TestRandomRomberg(unittest.TestCase):

    def test_random_polynomials(self):
        random.seed(42)

        for _ in range(20):
            degree = random.randint(1, 5)

            coefficients = [
                random.uniform(-5, 5)
                for _ in range(degree + 1)
            ]

            lower = random.uniform(-2, 0)
            upper = random.uniform(0, 2)

            def polynomial(x, coefficients=coefficients):
                return sum(
                    coefficient * x ** power
                    for power, coefficient
                    in enumerate(coefficients)
                )

            exact = sum(
                coefficient
                * (
                        upper ** (power + 1)
                        - lower ** (power + 1)
                )
                / (power + 1)
                for power, coefficient
                in enumerate(coefficients)
            )

            result = romberg_integration(
                polynomial,
                lower,
                upper
            )

            self.assertAlmostEqual(
                result,
                exact,
                places=8
            )

    def test_random_linear_functions(self):
        random.seed(123)

        for _ in range(20):
            a = random.uniform(-10, 10)
            b = random.uniform(-10, 10)

            lower = random.uniform(-5, 5)
            upper = random.uniform(-5, 5)

            if lower == upper:
                continue

            function = lambda x, a=a, b=b: a * x + b

            exact = (
                    a * (upper ** 2 - lower ** 2) / 2
                    + b * (upper - lower)
            )

            result = romberg_integration(
                function,
                lower,
                upper
            )

            self.assertAlmostEqual(
                result,
                exact,
                places=9
            )


if __name__ == "__main__":
    unittest.main()
