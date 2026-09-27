"""
Fourth-Order Runge-Kutta Method
==============================

The fourth-order Runge-Kutta method (RK4) is a numerical method for
solving ordinary differential equations of the form:

    y'(t) = f(t, y)

with an initial condition:

    y(t0) = y0

Instead of approximating the derivative only once during each step,
RK4 evaluates the derivative four times:

    k1 = f(t_n, y_n)

    k2 = f(t_n + h/2, y_n + h*k1/2)

    k3 = f(t_n + h/2, y_n + h*k2/2)

    k4 = f(t_n + h, y_n + h*k3)

The next value is then calculated as:

    y_(n+1) =
        y_n + h/6 * (k1 + 2*k2 + 2*k3 + k4)

The method has fourth-order accuracy. For sufficiently smooth problems,
the global truncation error is proportional to h^4.

This implementation supports scalar first-order ODEs.

Examples:

    y' = y
    y(0) = 1

has the analytical solution:

    y(t) = e^t

Another useful example is the harmonic oscillator:

    y'' + y = 0

which can be transformed into the first-order system:

    x' = v
    v' = -x

This file focuses on the scalar RK4 algorithm, while the tests verify
its accuracy on equations with known analytical solutions.
"""

import math
import random
import unittest


def runge_kutta_4(
        function,
        initial_time,
        initial_value,
        final_time,
        step_size
):
    """
    Solve y' = f(t, y) using the fourth-order Runge-Kutta method.

    Parameters
    ----------
    function : callable
        Function f(t, y) defining the differential equation.

    initial_time : float
        Initial value of t.

    initial_value : float
        Initial value y(t0).

    final_time : float
        Time at which the solution should be returned.

    step_size : float
        Maximum integration step.

    Returns
    -------
    float
        Numerical approximation of y(final_time).
    """

    if step_size <= 0:
        raise ValueError("step_size must be positive")

    if initial_time == final_time:
        return initial_value

    t = initial_time
    y = initial_value

    direction = 1.0 if final_time > initial_time else -1.0

    while direction * (final_time - t) > 1e-15:
        remaining = final_time - t

        h = direction * min(
            abs(step_size),
            abs(remaining)
        )

        k1 = function(t, y)

        k2 = function(
            t + h / 2,
            y + h * k1 / 2
        )

        k3 = function(
            t + h / 2,
            y + h * k2 / 2
        )

        k4 = function(
            t + h,
            y + h * k3
        )

        y += (
                h
                / 6
                * (
                        k1
                        + 2 * k2
                        + 2 * k3
                        + k4
                )
        )

        t += h

    return y


class TestRungeKutta4(unittest.TestCase):

    def test_exponential_growth(self):
        """
        y' = y
        y(0) = 1

        Exact solution:

            y(t) = e^t
        """

        result = runge_kutta_4(
            lambda t, y: y,
            0,
            1,
            1,
            0.01
        )

        self.assertAlmostEqual(
            result,
            math.e,
            places=9
        )

    def test_linear_function(self):
        """
        y' = 2t
        y(0) = 3

        Exact solution:

            y(t) = t^2 + 3
        """

        result = runge_kutta_4(
            lambda t, y: 2 * t,
            0,
            3,
            5,
            0.01
        )

        self.assertAlmostEqual(
            result,
            28.0,
            places=10
        )

    def test_decay(self):
        """
        y' = -y
        y(0) = 1

        Exact solution:

            y(t) = e^(-t)
        """

        result = runge_kutta_4(
            lambda t, y: -y,
            0,
            1,
            2,
            0.01
        )

        self.assertAlmostEqual(
            result,
            math.exp(-2),
            places=10
        )

    def test_logistic_equation(self):
        """
        Logistic equation:

            y' = y * (1 - y)

        with:

            y(0) = 0.5

        Exact solution:

            y(t) = 1 / (1 + e^(-t))
        """

        result = runge_kutta_4(
            lambda t, y: y * (1 - y),
            0,
            0.5,
            2,
            0.01
        )

        expected = 1 / (1 + math.exp(-2))

        self.assertAlmostEqual(
            result,
            expected,
            places=9
        )

    def test_sine_solution(self):
        """
        y' = cos(t)
        y(0) = 0

        Exact solution:

            y(t) = sin(t)
        """

        result = runge_kutta_4(
            lambda t, y: math.cos(t),
            0,
            0,
            math.pi,
            0.01
        )

        self.assertAlmostEqual(
            result,
            0.0,
            places=10
        )

    def test_nonzero_initial_time(self):
        """
        y' = 2t
        y(2) = 5

        Exact solution:

            y(t) = t^2 + 1
        """

        result = runge_kutta_4(
            lambda t, y: 2 * t,
            2,
            5,
            4,
            0.01
        )

        self.assertAlmostEqual(
            result,
            17.0,
            places=10
        )

    def test_zero_interval(self):
        result = runge_kutta_4(
            lambda t, y: y * y,
            3,
            7,
            3,
            0.1
        )

        self.assertEqual(
            result,
            7
        )

    def test_backward_integration(self):
        """
        y' = y
        y(1) = e

        Integrating backwards to t = 0 should give:

            y(0) = 1
        """

        result = runge_kutta_4(
            lambda t, y: y,
            1,
            math.e,
            0,
            0.01
        )

        self.assertAlmostEqual(
            result,
            1.0,
            places=9
        )

    def test_invalid_step(self):
        with self.assertRaises(ValueError):
            runge_kutta_4(
                lambda t, y: y,
                0,
                1,
                1,
                0
            )


class TestRandomRungeKutta(unittest.TestCase):

    def test_random_polynomial_derivatives(self):
        """
        Test equations:

            y' = a*t^2 + b*t + c

        Their analytical solution is:

            y(t) =
                a*t^3/3
                + b*t^2/2
                + c*t
                + y0
        """

        random.seed(123)

        for _ in range(20):
            a = random.uniform(-5, 5)
            b = random.uniform(-5, 5)
            c = random.uniform(-5, 5)

            y0 = random.uniform(-5, 5)
            final_time = random.uniform(0, 3)

            result = runge_kutta_4(
                lambda t, y, a=a, b=b, c=c:
                a * t * t + b * t + c,
                0,
                y0,
                final_time,
                0.05
            )

            expected = (
                    y0
                    + a * final_time ** 3 / 3
                    + b * final_time ** 2 / 2
                    + c * final_time
            )

            self.assertAlmostEqual(
                result,
                expected,
                places=9
            )

    def test_random_linear_time_equations(self):
        """
        Test equations:

            y' = a*t + b
        """

        random.seed(999)

        for _ in range(20):
            a = random.uniform(-10, 10)
            b = random.uniform(-10, 10)
            y0 = random.uniform(-10, 10)
            final_time = random.uniform(0, 5)

            result = runge_kutta_4(
                lambda t, y, a=a, b=b:
                a * t + b,
                0,
                y0,
                final_time,
                0.1
            )

            expected = (
                    y0
                    + a * final_time ** 2 / 2
                    + b * final_time
            )

            self.assertAlmostEqual(
                result,
                expected,
                places=9
            )


if __name__ == "__main__":
    unittest.main()
