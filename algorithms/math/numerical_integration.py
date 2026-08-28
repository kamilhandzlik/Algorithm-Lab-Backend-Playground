"""
Numerical Mathematics - Simpson's Rule

Description:
    Numerical integration is the process of approximating a definite
    integral using numerical calculations.

    Given a function f(x), we want to calculate:

        integral from a to b of f(x) dx

    In many practical situations, the antiderivative of f(x) is
    difficult or impossible to calculate analytically.

    Numerical integration allows us to approximate the integral by
    evaluating the function at selected points.

Simpson's Rule:
    Simpson's Rule approximates a function using quadratic polynomials.

    For an interval [a, b], with an even number of subintervals n:

        h = (b - a) / n

    and:

        integral ≈ h / 3 * (
            f(x0)
            + 4f(x1)
            + 2f(x2)
            + 4f(x3)
            + ...
            + 2f(x[n-2])
            + 4f(x[n-1])
            + f(xn)
        )

    The coefficients follow a repeating pattern:

        1, 4, 2, 4, 2, 4, ..., 2, 4, 1

    This gives Simpson's Rule significantly better accuracy than
    simply approximating the area using rectangles.

Why an even number of intervals is required:
    Simpson's Rule approximates pairs of intervals using quadratic
    polynomials.

    Therefore the number of subintervals must be even.

    For example:

        n = 10

    is valid.

    But:

        n = 9

    is not valid.

Accuracy:
    For sufficiently smooth functions, the error of the composite
    Simpson's Rule decreases approximately as:

        O(h^4)

    where:

        h = (b - a) / n

    This means that increasing the number of intervals can improve
    the approximation very quickly.

Special property:
    Simpson's Rule integrates every polynomial of degree three or
    lower exactly, assuming ordinary floating-point limitations are
    ignored.

    For example:

        f(x) = x^3 + 2x^2 + x + 5

    will be integrated exactly by Simpson's Rule for any valid
    even number of intervals.

    This property makes polynomials especially useful for testing
    numerical integration implementations.

Purpose:
    - Demonstrate numerical approximation of definite integrals.
    - Practice mathematical programming.
    - Work with floating-point calculations.
    - Demonstrate convergence as the number of intervals increases.
    - Create tests based on analytically known integrals.

When to use:
    - Physics simulations.
    - Engineering calculations.
    - Numerical analysis.
    - Scientific computing.
    - Finance and economics.
    - Probability calculations.
    - Any situation where an analytical antiderivative is unavailable
      or inconvenient.

Advantages:
    - More accurate than the basic trapezoidal rule for many smooth
      functions.
    - Simple implementation.
    - Requires only function evaluations.
    - Works with arbitrary callable functions.

Disadvantages:
    - Requires an even number of intervals.
    - Floating-point arithmetic introduces small numerical errors.
    - Accuracy depends on the smoothness of the function.
    - Very complicated functions may require adaptive integration.

Testing strategy:
    Numerical algorithms should usually be tested against values
    that are known analytically.

    For example:

        integral from 0 to 1 of x^2 dx = 1 / 3

    We can compare the numerical result against:

        1 / 3

    using assertAlmostEqual instead of assertEqual because floating
    point calculations are not always exact.

Random testing:
    Random tests generate polynomials with randomly selected
    coefficients.

    Their exact integral can be calculated analytically.

    This gives us an independent expected value and allows us to
    test hundreds of different functions automatically.

Important concept:
    A numerical algorithm does not necessarily return the exact
    mathematical answer.

    Instead, we should ask:

        "How close is the numerical result to the true value?"

    Therefore, numerical tests usually compare values using a
    tolerance rather than exact equality.
"""

import random
import unittest


def simpson_integral(function, start, end, intervals=100):
    if intervals <= 0:
        raise ValueError("Number of intervals must be positive")

    if intervals % 2 != 0:
        raise ValueError("Number of intervals must be even")

    if start == end:
        return 0.0

    step = (end - start) / intervals

    total = function(start) + function(end)

    for index in range(1, intervals):
        x = start + index * step

        if index % 2 == 0:
            total += 2 * function(x)
        else:
            total += 4 * function(x)

    return total * step / 3


class SimpsonIntegralTests(unittest.TestCase):

    def test_constant_function(self):
        result = simpson_integral(lambda x: 5, 0, 10, 10)

        self.assertAlmostEqual(result, 50.0, places=10)

    def test_linear_function(self):
        result = simpson_integral(lambda x: x, 0, 10, 10)

        self.assertAlmostEqual(result, 50.0, places=10)

    def test_quadratic_function(self):
        result = simpson_integral(lambda x: x ** 2, 0, 1, 10)

        self.assertAlmostEqual(result, 1 / 3, places=10)

    def test_cubic_function(self):
        result = simpson_integral(lambda x: x ** 3, 0, 2, 10)

        self.assertAlmostEqual(result, 4.0, places=10)

    def test_polynomial(self):
        result = simpson_integral(lambda x: x ** 3 + 2 * x ** 2 + x + 5, 0, 2, 10)

        expected = 64 / 3

        self.assertAlmostEqual(result, expected, places=10)

    def test_negative_interval(self):
        result = simpson_integral(lambda x: x ** 2, -1, 1, 10)

        self.assertAlmostEqual(result, 2 / 3, places=10)

    def test_reversed_interval(self):
        result = simpson_integral(lambda x: x, 10, 0, 10)

        self.assertAlmostEqual(result, -50.0, places=10)

    def test_zero_length_interval(self):
        result = simpson_integral(lambda x: x ** 2, 5, 5, 10)

        self.assertEqual(result, 0.0)

    def test_odd_intervals(self):
        with self.assertRaises(ValueError):
            simpson_integral(lambda x: x, 0, 1, 9)

    def test_zero_intervals(self):
        with self.assertRaises(ValueError):
            simpson_integral(lambda x: x, 0, 1, 0)

    def test_negative_intervals(self):
        with self.assertRaises(ValueError):
            simpson_integral(lambda x: x, 0, 1, -2)


class SimpsonIntegralRandomTests(unittest.TestCase):

    def generate_polynomial(self):
        degree = random.randint(0, 3)

        coefficients = [
            random.randint(-10, 10)
            for _ in range(degree + 1)
        ]

        def function(x):
            result = 0

            for power, coefficient in enumerate(coefficients):
                result += coefficient * x ** power

            return result

        def exact_integral(start, end):
            result = 0

            for power, coefficient in enumerate(coefficients):
                new_power = power + 1

                result += coefficient * (
                        end ** new_power - start ** new_power
                ) / new_power

            return result

        return function, exact_integral

    def test_random_polynomials(self):
        for _ in range(500):
            function, exact_integral = self.generate_polynomial()

            start = random.uniform(-5, 5)
            end = random.uniform(-5, 5)
            intervals = random.choice([10, 20, 50, 100])

            expected = exact_integral(start, end)

            result = simpson_integral(
                function,
                start,
                end,
                intervals
            )

            self.assertAlmostEqual(
                result,
                expected,
                places=7
            )

    def test_random_cubic_polynomials_are_exact(self):
        for _ in range(500):
            coefficients = [
                random.randint(-20, 20)
                for _ in range(4)
            ]

            def function(x):
                return (
                        coefficients[0]
                        + coefficients[1] * x
                        + coefficients[2] * x ** 2
                        + coefficients[3] * x ** 3
                )

            start = random.uniform(-3, 3)
            end = random.uniform(-3, 3)

            expected = (
                    coefficients[0] * (end - start)
                    + coefficients[1] * (end ** 2 - start ** 2) / 2
                    + coefficients[2] * (end ** 3 - start ** 3) / 3
                    + coefficients[3] * (end ** 4 - start ** 4) / 4
            )

            result = simpson_integral(
                function,
                start,
                end,
                10
            )

            self.assertAlmostEqual(
                result,
                expected,
                places=8
            )

    def test_random_constant_functions(self):
        for _ in range(500):
            value = random.uniform(-100, 100)
            start = random.uniform(-10, 10)
            end = random.uniform(-10, 10)

            expected = value * (end - start)

            result = simpson_integral(
                lambda x: value,
                start,
                end,
                10
            )

            self.assertAlmostEqual(
                result,
                expected,
                places=10
            )


if __name__ == "__main__":
    unittest.main()
