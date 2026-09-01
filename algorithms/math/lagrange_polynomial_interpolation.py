"""
Mathematical Algorithm - Lagrange Polynomial Interpolation

Description:
    Lagrange interpolation is a mathematical method for constructing
    a polynomial that passes through a given set of data points.

    Given n distinct points:

        (x0, y0)
        (x1, y1)
        ...
        (xn, yn)

    Lagrange interpolation constructs a polynomial P(x) such that:

        P(x0) = y0
        P(x1) = y1
        ...
        P(xn) = yn

    The polynomial is represented using Lagrange basis polynomials:

        P(x) = y0 * L0(x)
             + y1 * L1(x)
             + ...
             + yn * Ln(x)

    where:

        Li(x) = product((x - xj) / (xi - xj))

    for every j different from i.

Purpose:
    - Reconstruct a polynomial from known data points.
    - Estimate values between known measurements.
    - Demonstrate polynomial interpolation.
    - Practice numerical mathematics.
    - Demonstrate how mathematical formulas can be translated
      directly into executable code.

Example:
    Suppose we have the points:

        (0, 1)
        (1, 3)
        (2, 7)

    These points belong to the polynomial:

        f(x) = x^2 + x + 1

    because:

        f(0) = 1
        f(1) = 3
        f(2) = 7

    Lagrange interpolation can reconstruct the polynomial from the
    points without knowing the original formula.

Important property:
    If we have n distinct x-coordinates, there exists exactly one
    polynomial of degree at most n - 1 that passes through all points.

    For example:

        2 points  -> degree at most 1
        3 points  -> degree at most 2
        4 points  -> degree at most 3

    This property makes interpolation deterministic as long as all
    x-coordinates are distinct.

Algorithm:
    For every known point (xi, yi), construct its Lagrange basis
    polynomial Li(x).

    Initially:

        basis = 1

    For every other point xj:

        basis *= (x - xj) / (xi - xj)

    After calculating the basis polynomial, multiply it by yi and
    add it to the final result.

    The complete result is:

        P(x) = sum(yi * Li(x))

Complexity:
    Time:
        O(n^2)

    Space:
        O(1) additional space apart from the input points.

    For every interpolation point xi, the algorithm needs to iterate
    over all other points.

When to use:
    - Numerical analysis.
    - Scientific computing.
    - Estimating values from discrete measurements.
    - Computer graphics.
    - Physics and engineering.
    - Signal processing.
    - Mathematical modelling.

Advantages:
    - Simple mathematical formulation.
    - Easy to implement.
    - Does not require solving a system of linear equations explicitly.
    - Works directly with arbitrary sets of distinct points.

Disadvantages:
    - O(n^2) time complexity for evaluating the polynomial.
    - Can become numerically unstable for large datasets.
    - Using a high-degree polynomial for many points can produce
      undesirable oscillations.

Numerical precision:
    This implementation uses floating-point arithmetic.

    Therefore, results should normally be compared using a tolerance
    rather than exact equality.

    For example:

        assertAlmostEqual(result, expected)

    is more appropriate than:

        assertEqual(result, expected)

Random testing:
    Random tests can generate a polynomial with random coefficients.

    For example:

        f(x) = 3x^3 - 2x^2 + 7x - 4

    We can generate several points from this polynomial, give only
    those points to the interpolation algorithm, and then ask it to
    calculate the polynomial at another random x-coordinate.

    The expected result can be calculated directly from the original
    polynomial.

    This creates an independent oracle for testing the interpolation
    algorithm.

Important concept:
    Interpolation is not the same as extrapolation.

    Interpolation estimates values inside the range covered by the
    known points.

    Extrapolation estimates values outside that range and can be much
    less reliable, especially for high-degree polynomials.

    The mathematical algorithm itself can perform both operations,
    but the quality of the estimate depends strongly on the problem.
"""

import random
import unittest


def lagrange_interpolation(points, x):
    if not points:
        raise ValueError("At least one point is required")

    x_values = [point[0] for point in points]

    if len(x_values) != len(set(x_values)):
        raise ValueError("X coordinates must be distinct")

    result = 0.0

    for i, (xi, yi) in enumerate(points):
        basis = 1.0

        for j, (xj, _) in enumerate(points):
            if i == j:
                continue

            basis *= (x - xj) / (xi - xj)

        result += yi * basis

    return result


def polynomial_value(coefficients, x):
    result = 0.0

    for power, coefficient in enumerate(coefficients):
        result += coefficient * x ** power

    return result


class LagrangeInterpolationTests(unittest.TestCase):

    def test_single_point(self):
        points = [(2, 10)]

        result = lagrange_interpolation(points, 2)

        self.assertAlmostEqual(result, 10.0)

    def test_linear_function(self):
        points = [
            (0, 1),
            (1, 3)
        ]

        result = lagrange_interpolation(points, 0.5)

        self.assertAlmostEqual(result, 2.0)

    def test_quadratic_function(self):
        points = [
            (0, 1),
            (1, 3),
            (2, 7)
        ]

        result = lagrange_interpolation(points, 1.5)

        self.assertAlmostEqual(result, 4.75)

    def test_cubic_function(self):
        points = [
            (0, 1),
            (1, 3),
            (2, 15),
            (3, 49)
        ]

        result = lagrange_interpolation(points, 1.5)

        self.assertAlmostEqual(result, 7.0)

    def test_interpolation_at_known_point(self):
        points = [
            (0, 5),
            (2, 9),
            (4, 17)
        ]

        result = lagrange_interpolation(points, 2)

        self.assertAlmostEqual(result, 9.0)

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

    def test_empty_points(self):
        with self.assertRaises(ValueError):
            lagrange_interpolation([], 5)

    def test_duplicate_x_coordinates(self):
        points = [
            (1, 5),
            (1, 10)
        ]

        with self.assertRaises(ValueError):
            lagrange_interpolation(points, 2)


class LagrangeInterpolationRandomTests(unittest.TestCase):

    def generate_polynomial(self):
        degree = random.randint(0, 5)

        coefficients = [
            random.randint(-10, 10)
            for _ in range(degree + 1)
        ]

        return coefficients

    def generate_distinct_points(self, coefficients):
        degree = len(coefficients) - 1
        x_values = random.sample(
            range(-20, 21),
            degree + 1
        )

        return [
            (
                x,
                polynomial_value(coefficients, x)
            )
            for x in x_values
        ]

    def test_random_polynomials(self):
        for _ in range(500):
            coefficients = self.generate_polynomial()
            points = self.generate_distinct_points(coefficients)

            x = random.uniform(-10, 10)

            expected = polynomial_value(
                coefficients,
                x
            )

            result = lagrange_interpolation(
                points,
                x
            )

            self.assertAlmostEqual(
                result,
                expected,
                delta=1e-6
            )

    def test_random_known_points(self):
        for _ in range(500):
            coefficients = self.generate_polynomial()
            points = self.generate_distinct_points(coefficients)

            point = random.choice(points)

            result = lagrange_interpolation(
                points,
                point[0]
            )

            self.assertAlmostEqual(
                result,
                point[1],
                delta=1e-6
            )

    def test_random_linear_functions(self):
        for _ in range(500):
            a = random.randint(-100, 100)
            b = random.randint(-100, 100)

            points = [
                (0, b),
                (1, a + b)
            ]

            x = random.uniform(-10, 10)

            expected = a * x + b

            result = lagrange_interpolation(
                points,
                x
            )

            self.assertAlmostEqual(
                result,
                expected,
                delta=1e-6
            )


if __name__ == "__main__":
    unittest.main()