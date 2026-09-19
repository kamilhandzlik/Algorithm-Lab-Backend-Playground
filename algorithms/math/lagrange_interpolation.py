"""
Lagrange Polynomial Interpolation.

Polynomial interpolation is a numerical method used to construct
a polynomial that passes through a given set of data points.

Given n distinct points:

    (x0, y0), (x1, y1), ..., (xn-1, yn-1)

there exists exactly one polynomial of degree at most n - 1
that passes through all of these points.

The Lagrange interpolation formula is:

    P(x) = sum(i=0 to n-1) yi * Li(x)

where:

    Li(x) = product(j != i) (x - xj) / (xi - xj)

Each Li(x) is called a Lagrange basis polynomial.

The important property of the basis polynomials is:

    Li(xj) = 1  when i = j
    Li(xj) = 0  when i != j

Therefore, each data point contributes exactly its own y-value
to the resulting polynomial.

This implementation evaluates the interpolation polynomial directly
without explicitly constructing its coefficients.

The method is useful for estimating values between known data points,
but interpolation outside the original data range is extrapolation
and can become numerically unstable.
"""

import math
import random
import unittest


def lagrange_interpolation(points, x):
    """
    Evaluate the Lagrange interpolation polynomial at x.

    Args:
        points: Iterable containing (x, y) pairs.
        x: Position at which the polynomial should be evaluated.

    Returns:
        Interpolated value P(x).

    Raises:
        ValueError: If there are not enough points or if two points
            have the same x-coordinate.
    """

    points = list(points)

    if len(points) == 0:
        raise ValueError("At least one point is required.")

    x_values = [point[0] for point in points]

    if len(set(x_values)) != len(x_values):
        raise ValueError(
            "All x-coordinates must be distinct."
        )

    result = 0.0

    for i, (xi, yi) in enumerate(points):
        basis = 1.0

        for j, (xj, _) in enumerate(points):
            if i == j:
                continue

            basis *= (x - xj) / (xi - xj)

        result += yi * basis

    return result


class TestLagrangeInterpolation(unittest.TestCase):

    def test_single_point(self):
        points = [(3, 7)]

        result = lagrange_interpolation(points, 100)

        self.assertAlmostEqual(result, 7.0)

    def test_two_points(self):
        points = [
            (0, 0),
            (2, 4)
        ]

        result = lagrange_interpolation(points, 1)

        self.assertAlmostEqual(result, 2.0)

    def test_linear_function(self):
        points = [
            (0, 5),
            (2, 9)
        ]

        result = lagrange_interpolation(points, 10)

        self.assertAlmostEqual(result, 25.0)

    def test_quadratic_function(self):
        points = [
            (0, 1),
            (1, 4),
            (2, 9)
        ]

        result = lagrange_interpolation(points, 3)

        self.assertAlmostEqual(result, 16.0)

    def test_cubic_function(self):
        points = [
            (0, 1),
            (1, 2),
            (2, 9),
            (3, 28)
        ]

        result = lagrange_interpolation(points, 4)

        self.assertAlmostEqual(result, 65.0)

    def test_interpolation_at_known_point(self):
        points = [
            (-2, 10),
            (0, 5),
            (3, 20),
            (7, -4)
        ]

        for x, y in points:
            result = lagrange_interpolation(points, x)

            self.assertAlmostEqual(result, y)

    def test_negative_coordinates(self):
        points = [
            (-2, 4),
            (-1, 1),
            (0, 0),
            (1, 1),
            (2, 4)
        ]

        result = lagrange_interpolation(points, 1.5)

        self.assertAlmostEqual(result, 2.25)

    def test_fractional_coordinates(self):
        points = [
            (0.0, 0.0),
            (0.5, 0.25),
            (1.0, 1.0)
        ]

        result = lagrange_interpolation(points, 0.75)

        self.assertAlmostEqual(result, 0.5625)

    def test_empty_points(self):
        with self.assertRaises(ValueError):
            lagrange_interpolation([], 5)

    def test_duplicate_x_coordinates(self):
        points = [
            (1, 2),
            (1, 5)
        ]

        with self.assertRaises(ValueError):
            lagrange_interpolation(points, 3)


class TestRandomPolynomials(unittest.TestCase):

    def test_random_linear_polynomials(self):
        random.seed(42)

        for _ in range(100):
            a = random.uniform(-10, 10)
            b = random.uniform(-10, 10)

            function = lambda x, a=a, b=b: a * x + b

            points = [
                (-2, function(-2)),
                (0, function(0))
            ]

            x = random.uniform(-10, 10)

            result = lagrange_interpolation(points, x)

            self.assertAlmostEqual(
                result,
                function(x),
                places=8
            )

    def test_random_quadratic_polynomials(self):
        random.seed(123)

        for _ in range(100):
            a = random.uniform(-5, 5)
            b = random.uniform(-5, 5)
            c = random.uniform(-5, 5)

            function = (
                lambda x, a=a, b=b, c=c:
                a * x ** 2 + b * x + c
            )

            points = [
                (-2, function(-2)),
                (0, function(0)),
                (3, function(3))
            ]

            x = random.uniform(-2, 3)

            result = lagrange_interpolation(points, x)

            self.assertAlmostEqual(
                result,
                function(x),
                places=8
            )

    def test_random_cubic_polynomials(self):
        random.seed(456)

        for _ in range(100):
            a = random.uniform(-2, 2)
            b = random.uniform(-2, 2)
            c = random.uniform(-2, 2)
            d = random.uniform(-2, 2)

            function = (
                lambda x, a=a, b=b, c=c, d=d:
                a * x ** 3 + b * x ** 2 + c * x + d
            )

            points = [
                (-2, function(-2)),
                (-1, function(-1)),
                (1, function(1)),
                (3, function(3))
            ]

            x = random.uniform(-2, 3)

            result = lagrange_interpolation(points, x)

            self.assertAlmostEqual(
                result,
                function(x),
                places=7
            )


if __name__ == "__main__":
    unittest.main()
