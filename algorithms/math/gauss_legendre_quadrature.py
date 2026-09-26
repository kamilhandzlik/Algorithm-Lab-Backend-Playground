"""
Gauss-Legendre Quadrature
=========================

Gauss-Legendre quadrature is a numerical integration method that
approximates a definite integral by evaluating the function at specially
chosen points called quadrature nodes.

For an integral over [-1, 1]:

    integral(f(x), -1, 1) ~= sum(w_i * f(x_i))

where:

    x_i = roots of the Legendre polynomial P_n(x)

and:

    w_i

are the corresponding quadrature weights.

The important property of the n-point Gauss-Legendre rule is that it
integrates every polynomial of degree up to:

    2n - 1

exactly, assuming exact arithmetic.

For an arbitrary interval [a, b], we transform it to [-1, 1] using:

    x = (a + b) / 2 + (b - a) / 2 * t

and therefore:

    integral(f(x), a, b)
        =
    (b - a) / 2 * integral(
        f((a + b)/2 + (b - a)t/2),
        -1,
        1
    )

The roots of the Legendre polynomial are found numerically using
Newton's method.

The derivative of the Legendre polynomial is evaluated using:

    P'_n(x) =
        n / (x^2 - 1) * (x * P_n(x) - P_(n-1)(x))

The corresponding weights are:

    w_i =
        2 / ((1 - x_i^2) * P'_n(x_i)^2)

This implementation computes the nodes and weights dynamically instead
of using a hard-coded table.
"""

import math
import random
import unittest


def legendre_polynomial(n, x):
    """
    Evaluate the Legendre polynomial P_n(x) using recurrence.

    P_0(x) = 1
    P_1(x) = x

    P_n(x) =
        ((2n - 1)xP_(n-1)(x) - (n - 1)P_(n-2)(x)) / n
    """

    if n < 0:
        raise ValueError("n must be non-negative")

    if n == 0:
        return 1.0

    if n == 1:
        return x

    previous = 1.0
    current = x

    for degree in range(2, n + 1):
        next_value = (
                             (2 * degree - 1) * x * current
                             - (degree - 1) * previous
                     ) / degree

        previous = current
        current = next_value

    return current


def legendre_derivative(n, x):
    """
    Evaluate the derivative P'_n(x).
    """

    if n < 1:
        raise ValueError("n must be at least 1")

    if abs(abs(x) - 1.0) < 1e-15:
        raise ValueError(
            "Derivative formula is singular at x = +/-1"
        )

    return (
            n
            * (
                    x * legendre_polynomial(n, x)
                    - legendre_polynomial(n - 1, x)
            )
            / (x * x - 1.0)
    )


def gauss_legendre_nodes_weights(
        number_of_points,
        tolerance=1e-14,
        max_iterations=100
):
    """
    Calculate Gauss-Legendre nodes and weights on [-1, 1].

    Only half of the roots need to be calculated because Legendre
    polynomials have symmetric roots.
    """

    if number_of_points < 1:
        raise ValueError(
            "number_of_points must be at least 1"
        )

    if tolerance <= 0:
        raise ValueError("tolerance must be positive")

    nodes = [0.0] * number_of_points
    weights = [0.0] * number_of_points

    half = (number_of_points + 1) // 2

    for i in range(half):

        # Initial approximation of the i-th positive root.
        x = math.cos(
            math.pi
            * (i + 0.75)
            / (number_of_points + 0.5)
        )

        for _ in range(max_iterations):

            polynomial = legendre_polynomial(
                number_of_points,
                x
            )

            derivative = legendre_derivative(
                number_of_points,
                x
            )

            new_x = x - polynomial / derivative

            if abs(new_x - x) < tolerance:
                x = new_x
                break

            x = new_x

        else:
            raise RuntimeError(
                "Newton iteration did not converge"
            )

        derivative = legendre_derivative(
            number_of_points,
            x
        )

        weight = (
                2.0
                / (
                        (1.0 - x * x)
                        * derivative * derivative
                )
        )

        left = i
        right = number_of_points - 1 - i

        nodes[left] = -x
        nodes[right] = x

        weights[left] = weight
        weights[right] = weight

    return nodes, weights


def gauss_legendre_integrate(
        function,
        lower,
        upper,
        number_of_points=5
):
    """
    Approximate the integral of function over [lower, upper]
    using Gauss-Legendre quadrature.
    """

    if number_of_points < 1:
        raise ValueError(
            "number_of_points must be at least 1"
        )

    if lower == upper:
        return 0.0

    if lower > upper:
        return -gauss_legendre_integrate(
            function,
            upper,
            lower,
            number_of_points
        )

    nodes, weights = gauss_legendre_nodes_weights(
        number_of_points
    )

    midpoint = (lower + upper) / 2.0
    half_length = (upper - lower) / 2.0

    result = 0.0

    for node, weight in zip(nodes, weights):
        transformed_x = (
                midpoint
                + half_length * node
        )

        result += (
                weight
                * function(transformed_x)
        )

    return half_length * result


class TestLegendrePolynomial(unittest.TestCase):

    def test_first_polynomials(self):
        self.assertAlmostEqual(
            legendre_polynomial(0, 0.5),
            1.0
        )

        self.assertAlmostEqual(
            legendre_polynomial(1, 0.5),
            0.5
        )

        self.assertAlmostEqual(
            legendre_polynomial(2, 0.5),
            -0.125
        )

        self.assertAlmostEqual(
            legendre_polynomial(3, 0.5),
            -0.4375
        )

    def test_known_polynomial(self):
        x = 0.3

        expected = (
                (35 * x ** 4
                 - 30 * x ** 2
                 + 3)
                / 8
        )

        result = legendre_polynomial(4, x)

        self.assertAlmostEqual(
            result,
            expected,
            places=12
        )


class TestGaussLegendre(unittest.TestCase):

    def test_weights_sum_to_two(self):
        for number_of_points in range(1, 11):
            _, weights = gauss_legendre_nodes_weights(
                number_of_points
            )

            self.assertAlmostEqual(
                sum(weights),
                2.0,
                places=12
            )

    def test_nodes_are_symmetric(self):
        for number_of_points in range(1, 11):

            nodes, _ = gauss_legendre_nodes_weights(
                number_of_points
            )

            for i in range(number_of_points):
                self.assertAlmostEqual(
                    nodes[i],
                    -nodes[-1 - i],
                    places=12
                )

    def test_integral_of_constant(self):
        result = gauss_legendre_integrate(
            lambda x: 5.0,
            -3,
            7,
            number_of_points=2
        )

        self.assertAlmostEqual(
            result,
            50.0,
            places=12
        )

    def test_x_squared(self):
        result = gauss_legendre_integrate(
            lambda x: x ** 2,
            0,
            3,
            number_of_points=2
        )

        self.assertAlmostEqual(
            result,
            9.0,
            places=12
        )

    def test_sine(self):
        result = gauss_legendre_integrate(
            math.sin,
            0,
            math.pi,
            number_of_points=8
        )

        self.assertAlmostEqual(
            result,
            2.0,
            places=12
        )

    def test_exponential(self):
        result = gauss_legendre_integrate(
            math.exp,
            0,
            1,
            number_of_points=8
        )

        self.assertAlmostEqual(
            result,
            math.e - 1,
            places=12
        )

    def test_reversed_interval(self):
        result = gauss_legendre_integrate(
            lambda x: x ** 2,
            2,
            -2,
            number_of_points=3
        )

        self.assertAlmostEqual(
            result,
            -16 / 3,
            places=12
        )

    def test_zero_interval(self):
        result = gauss_legendre_integrate(
            lambda x: math.sin(x),
            5,
            5,
            number_of_points=5
        )

        self.assertEqual(
            result,
            0.0
        )

    def test_invalid_number_of_points(self):
        with self.assertRaises(ValueError):
            gauss_legendre_integrate(
                lambda x: x,
                0,
                1,
                number_of_points=0
            )


class TestRandomGaussLegendre(unittest.TestCase):

    def test_random_polynomials(self):
        random.seed(42)

        for _ in range(30):
            degree = random.randint(0, 9)

            coefficients = [
                random.uniform(-5, 5)
                for _ in range(degree + 1)
            ]

            lower = random.uniform(-3, 0)
            upper = random.uniform(0, 3)

            def polynomial(
                    x,
                    coefficients=coefficients
            ):
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

            result = gauss_legendre_integrate(
                polynomial,
                lower,
                upper,
                number_of_points=5
            )

            self.assertAlmostEqual(
                result,
                exact,
                places=9
            )

    def test_random_linear_functions(self):
        random.seed(123)

        for _ in range(30):
            a = random.uniform(-10, 10)
            b = random.uniform(-10, 10)

            lower = random.uniform(-5, 5)
            upper = random.uniform(-5, 5)

            function = (
                lambda x, a=a, b=b:
                a * x + b
            )

            exact = (
                    a * (upper ** 2 - lower ** 2) / 2
                    + b * (upper - lower)
            )

            result = gauss_legendre_integrate(
                function,
                lower,
                upper,
                number_of_points=2
            )

            self.assertAlmostEqual(
                result,
                exact,
                places=10
            )


if __name__ == "__main__":
    unittest.main()
