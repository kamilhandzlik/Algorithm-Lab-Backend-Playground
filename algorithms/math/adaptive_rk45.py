"""
Adaptive Runge-Kutta-Fehlberg (RK45) method for solving
first-order ordinary differential equations.

The classical RK4 method uses a fixed step size. This can be inefficient:
a small step is required in regions where the solution changes rapidly,
while the same small step is unnecessarily expensive where the solution
changes slowly.

The RK45 method addresses this problem by computing two approximations
of different orders during every step:

    - a fourth-order approximation
    - a fifth-order approximation

Their difference provides an estimate of the local truncation error.

If the estimated error is too large, the step is rejected and repeated
with a smaller step size. If the error is sufficiently small, the step
is accepted and the algorithm may increase the next step size.

We solve equations of the form:

    y' = f(x, y)

with a given initial condition:

    y(x0) = y0

The implementation uses the classical Fehlberg RKF45 coefficients.
"""

import math
import random
import unittest


def rk45(
        f,
        x0,
        y0,
        x_end,
        tolerance=1e-8,
        initial_step=0.1,
        min_step=1e-10,
        max_step=1.0,
):
    """
    Solve y' = f(x, y) using adaptive Runge-Kutta-Fehlberg RK45.

    Returns:
        A list of (x, y) points accepted by the adaptive solver.
    """

    if tolerance <= 0:
        raise ValueError("Tolerance must be positive.")

    if initial_step <= 0:
        raise ValueError("Initial step must be positive.")

    if min_step <= 0:
        raise ValueError("Minimum step must be positive.")

    if max_step <= 0:
        raise ValueError("Maximum step must be positive.")

    if min_step > max_step:
        raise ValueError("Minimum step cannot exceed maximum step.")

    if x0 == x_end:
        return [(x0, y0)]

    direction = 1 if x_end > x0 else -1

    h = min(abs(initial_step), max_step)
    h = max(h, min_step)
    h *= direction

    x = x0
    y = y0

    solution = [(x, y)]

    safety = 0.9
    min_factor = 0.2
    max_factor = 5.0

    while direction * (x_end - x) > 0:
        remaining = x_end - x

        if direction * h > direction * remaining:
            h = remaining

        # RKF45 coefficients
        k1 = f(x, y)

        k2 = f(
            x + h / 4,
            y + h * k1 / 4,
        )

        k3 = f(
            x + 3 * h / 8,
            y + h * (3 * k1 / 32 + 9 * k2 / 32),
        )

        k4 = f(
            x + 12 * h / 13,
            y + h * (
                    1932 * k1 / 2197
                    - 7200 * k2 / 2197
                    + 7296 * k3 / 2197
            ),
        )

        k5 = f(
            x + h,
            y + h * (
                    439 * k1 / 216
                    - 8 * k2
                    + 3680 * k3 / 513
                    - 845 * k4 / 4104
            ),
        )

        k6 = f(
            x + h / 2,
            y + h * (
                    -8 * k1 / 27
                    + 2 * k2
                    - 3544 * k3 / 2565
                    + 1859 * k4 / 4104
                    - 11 * k5 / 40
            ),
        )

        # Fourth-order approximation
        y4 = y + h * (
                25 * k1 / 216
                + 1408 * k3 / 2565
                + 2197 * k4 / 4104
                - k5 / 5
        )

        # Fifth-order approximation
        y5 = y + h * (
                16 * k1 / 135
                + 6656 * k3 / 12825
                + 28561 * k4 / 56430
                - 9 * k5 / 50
                + 2 * k6 / 55
        )

        error = abs(y5 - y4)

        if error == 0:
            factor = max_factor
        else:
            factor = safety * (tolerance / error) ** 0.25
            factor = max(min_factor, min(max_factor, factor))

        # Accept the step
        if error <= tolerance or abs(h) <= min_step:
            x += h
            y = y5
            solution.append((x, y))

        # Adapt step size
        new_step = abs(h) * factor
        new_step = max(min_step, min(max_step, new_step))

        h = direction * new_step

    return solution


class TestRK45(unittest.TestCase):

    def test_exponential_growth(self):
        """
        y' = y
        y(0) = 1

        Exact solution:
            y = e^x
        """

        solution = rk45(
            lambda x, y: y,
            0.0,
            1.0,
            1.0,
            tolerance=1e-9,
        )

        x, y = solution[-1]

        self.assertAlmostEqual(x, 1.0)
        self.assertAlmostEqual(y, math.e, places=7)

    def test_exponential_decay(self):
        """
        y' = -2y
        y(0) = 1

        Exact solution:
            y = e^(-2x)
        """

        solution = rk45(
            lambda x, y: -2 * y,
            0.0,
            1.0,
            2.0,
            tolerance=1e-9,
        )

        x, y = solution[-1]

        expected = math.exp(-4)

        self.assertAlmostEqual(x, 2.0)
        self.assertAlmostEqual(y, expected, places=8)

    def test_linear_equation(self):
        """
        y' = 2x
        y(0) = 3

        Exact solution:
            y = x^2 + 3
        """

        solution = rk45(
            lambda x, y: 2 * x,
            0.0,
            3.0,
            5.0,
            tolerance=1e-9,
        )

        x, y = solution[-1]

        self.assertAlmostEqual(x, 5.0)
        self.assertAlmostEqual(y, 28.0, places=8)

    def test_sine_solution(self):
        """
        y' = cos(x)
        y(0) = 0

        Exact solution:
            y = sin(x)
        """

        solution = rk45(
            lambda x, y: math.cos(x),
            0.0,
            0.0,
            math.pi,
            tolerance=1e-9,
        )

        x, y = solution[-1]

        self.assertAlmostEqual(x, math.pi)
        self.assertAlmostEqual(y, 0.0, places=8)

    def test_backward_integration(self):
        """
        Integrate backwards:

            y' = y
            y(1) = e

        Therefore:

            y(0) = 1
        """

        solution = rk45(
            lambda x, y: y,
            1.0,
            math.e,
            0.0,
            tolerance=1e-9,
        )

        x, y = solution[-1]

        self.assertAlmostEqual(x, 0.0)
        self.assertAlmostEqual(y, 1.0, places=7)

    def test_zero_derivative(self):
        """
        y' = 0

        The solution must remain constant.
        """

        solution = rk45(
            lambda x, y: 0.0,
            0.0,
            17.5,
            10.0,
            tolerance=1e-10,
        )

        for _, y in solution:
            self.assertAlmostEqual(y, 17.5, places=10)

    def test_adaptive_step_changes(self):
        """
        A rapidly changing function should cause the adaptive
        solver to use different step sizes.
        """

        solution = rk45(
            lambda x, y: 100 * math.cos(100 * x),
            0.0,
            0.0,
            1.0,
            tolerance=1e-8,
            initial_step=0.2,
            max_step=0.5,
        )

        steps = [
            solution[i + 1][0] - solution[i][0]
            for i in range(len(solution) - 1)
        ]

        self.assertGreater(len(steps), 10)
        self.assertGreater(len(set(round(step, 10) for step in steps)), 1)


class TestRK45Random(unittest.TestCase):

    def test_random_exponential_equations(self):
        """
        Randomized test for:

            y' = a*y

        with exact solution:

            y(x) = y0 * exp(a*x)
        """

        random.seed(42)

        for _ in range(20):
            a = random.uniform(-3.0, 3.0)
            y0 = random.uniform(-2.0, 2.0)
            x_end = random.uniform(0.1, 2.0)

            solution = rk45(
                lambda x, y, a=a: a * y,
                0.0,
                y0,
                x_end,
                tolerance=1e-9,
            )

            _, numerical = solution[-1]

            expected = y0 * math.exp(a * x_end)

            self.assertAlmostEqual(
                numerical,
                expected,
                places=7,
            )

    def test_random_polynomials(self):
        """
        Randomized polynomial differential equations:

            y' = a*x^2 + b*x + c

        Exact solution:

            y = a*x^3/3 + b*x^2/2 + c*x + y0
        """

        random.seed(123)

        for _ in range(20):
            a = random.uniform(-5.0, 5.0)
            b = random.uniform(-5.0, 5.0)
            c = random.uniform(-5.0, 5.0)
            y0 = random.uniform(-5.0, 5.0)
            x_end = random.uniform(0.1, 3.0)

            solution = rk45(
                lambda x, y, a=a, b=b, c=c:
                a * x * x + b * x + c,
                0.0,
                y0,
                x_end,
                tolerance=1e-9,
            )

            _, numerical = solution[-1]

            expected = (
                    a * x_end ** 3 / 3
                    + b * x_end ** 2 / 2
                    + c * x_end
                    + y0
            )

            self.assertAlmostEqual(
                numerical,
                expected,
                places=7,
            )


if __name__ == "__main__":
    unittest.main()
