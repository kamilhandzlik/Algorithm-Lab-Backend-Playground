"""
Lagrange Points in the Restricted Three-Body Problem
====================================================

The restricted three-body problem describes the motion of a small test
particle influenced by two massive bodies, while the test particle does
not affect the motion of the two massive bodies.

In a rotating reference frame, there are five special equilibrium points
called Lagrange points:

    L1, L2, L3, L4, L5

At these points, the gravitational forces and the apparent forces caused
by the rotating reference frame balance each other.

We use normalized units:

    G = 1
    total mass = 1
    distance between the primary bodies = 1

The masses are represented by:

    m1 = 1 - mu
    m2 = mu

The two primary bodies are located at:

    (-mu, 0)
    (1 - mu, 0)

This places the center of mass at the origin.

The effective potential in the rotating frame is:

    Omega(x, y) =
        (x^2 + y^2)/2
        + (1-mu)/r1
        + mu/r2

where:

    r1 = sqrt((x + mu)^2 + y^2)
    r2 = sqrt((x - 1 + mu)^2 + y^2)

An equilibrium point satisfies:

    dOmega/dx = 0
    dOmega/dy = 0

The collinear points L1, L2 and L3 lie on the x-axis, so their
positions can be found by solving:

    dOmega/dx = 0

using Newton's method.

The triangular points L4 and L5 are known geometrically:

    L4 = (1/2 - mu,  sqrt(3)/2)
    L5 = (1/2 - mu, -sqrt(3)/2)

The implementation also provides the Jacobi constant:

    C = 2*Omega - (vx^2 + vy^2)

which is an important conserved quantity in the circular restricted
three-body problem.

This is a simplified normalized model, but the equations capture the
essential mathematics behind Lagrange-point dynamics.
"""

import math
import random
import unittest


def effective_potential(x, y, mu):
    """
    Calculate the effective potential Omega(x, y).
    """

    if not 0 < mu < 1:
        raise ValueError(
            "mu must be between 0 and 1"
        )

    r1 = math.sqrt(
        (x + mu) ** 2 + y ** 2
    )

    r2 = math.sqrt(
        (x - 1 + mu) ** 2 + y ** 2
    )

    if r1 == 0 or r2 == 0:
        raise ValueError(
            "Potential is singular at a primary body"
        )

    return (
            0.5 * (x * x + y * y)
            + (1 - mu) / r1
            + mu / r2
    )


def effective_potential_x(x, y, mu):
    """
    Calculate dOmega/dx.
    """

    r1_squared = (
            (x + mu) ** 2
            + y ** 2
    )

    r2_squared = (
            (x - 1 + mu) ** 2
            + y ** 2
    )

    r1 = math.sqrt(r1_squared)
    r2 = math.sqrt(r2_squared)

    if r1 == 0 or r2 == 0:
        raise ValueError(
            "Derivative is singular at a primary body"
        )

    return (
            x
            - (1 - mu) * (x + mu) / r1 ** 3
            - mu * (x - 1 + mu) / r2 ** 3
    )


def effective_potential_y(x, y, mu):
    """
    Calculate dOmega/dy.
    """

    r1_squared = (
            (x + mu) ** 2
            + y ** 2
    )

    r2_squared = (
            (x - 1 + mu) ** 2
            + y ** 2
    )

    r1 = math.sqrt(r1_squared)
    r2 = math.sqrt(r2_squared)

    if r1 == 0 or r2 == 0:
        raise ValueError(
            "Derivative is singular at a primary body"
        )

    return (
            y
            - (1 - mu) * y / r1 ** 3
            - mu * y / r2 ** 3
    )


def effective_potential_xx(x, y, mu):
    """
    Calculate the second derivative d²Omega/dx².
    """

    dx1 = x + mu
    dx2 = x - 1 + mu

    r1_squared = dx1 ** 2 + y ** 2
    r2_squared = dx2 ** 2 + y ** 2

    r1 = math.sqrt(r1_squared)
    r2 = math.sqrt(r2_squared)

    if r1 == 0 or r2 == 0:
        raise ValueError(
            "Derivative is singular at a primary body"
        )

    return (
            1
            + (1 - mu)
            * (
                    3 * dx1 ** 2 / r1 ** 5
                    - 1 / r1 ** 3
            )
            + mu
            * (
                    3 * dx2 ** 2 / r2 ** 5
                    - 1 / r2 ** 3
            )
    )


def find_collinear_point(
        mu,
        initial_guess,
        tolerance=1e-12,
        max_iterations=100
):
    """
    Find L1, L2 or L3 using Newton's method.

    Since the collinear points lie on the x-axis, y = 0 and we solve:

        dOmega/dx = 0
    """

    if not 0 < mu < 1:
        raise ValueError(
            "mu must be between 0 and 1"
        )

    if tolerance <= 0:
        raise ValueError(
            "tolerance must be positive"
        )

    x = initial_guess

    for _ in range(max_iterations):

        function_value = effective_potential_x(
            x,
            0.0,
            mu
        )

        derivative_value = effective_potential_xx(
            x,
            0.0,
            mu
        )

        if abs(derivative_value) < 1e-15:
            raise RuntimeError(
                "Newton method encountered "
                "a nearly zero derivative"
            )

        new_x = (
                x
                - function_value / derivative_value
        )

        if abs(new_x - x) < tolerance:
            return new_x

        x = new_x

    raise RuntimeError(
        "Newton method did not converge"
    )


def lagrange_points(mu):
    """
    Calculate all five Lagrange points.

    Initial guesses are selected according to the expected regions:

        L1: between the two bodies
        L2: beyond the smaller body
        L3: beyond the larger body
    """

    if not 0 < mu < 1:
        raise ValueError(
            "mu must be between 0 and 1"
        )

    l1_guess = 1 - mu - 0.1
    l2_guess = 1 - mu + 0.1
    l3_guess = -mu - 1.0

    l1_x = find_collinear_point(
        mu,
        l1_guess
    )

    l2_x = find_collinear_point(
        mu,
        l2_guess
    )

    l3_x = find_collinear_point(
        mu,
        l3_guess
    )

    triangular_x = 0.5 - mu
    triangular_y = math.sqrt(3) / 2

    return {
        "L1": (l1_x, 0.0),
        "L2": (l2_x, 0.0),
        "L3": (l3_x, 0.0),
        "L4": (triangular_x, triangular_y),
        "L5": (triangular_x, -triangular_y)
    }


def jacobi_constant(x, y, vx, vy, mu):
    """
    Calculate the Jacobi constant:

        C = 2*Omega - v^2
    """

    return (
            2 * effective_potential(
        x,
        y,
        mu
    )
            - vx * vx
            - vy * vy
    )


def distance_to_primary(x, y, primary, mu):
    """
    Calculate distance to one of the two primary bodies.

    primary = 1 -> larger primary
    primary = 2 -> smaller primary
    """

    if primary == 1:

        px = -mu

    elif primary == 2:

        px = 1 - mu

    else:

        raise ValueError(
            "primary must be 1 or 2"
        )

    return math.sqrt(
        (x - px) ** 2
        + y ** 2
    )


class TestEffectivePotential(unittest.TestCase):

    def test_symmetry(self):
        mu = 0.2

        left = effective_potential(
            0.1,
            0.5,
            mu
        )

        right = effective_potential(
            0.1,
            -0.5,
            mu
        )

        self.assertAlmostEqual(
            left,
            right,
            places=12
        )

    def test_l4_potential(self):
        mu = 0.1

        points = lagrange_points(mu)

        x, y = points["L4"]

        derivative_x = effective_potential_x(
            x,
            y,
            mu
        )

        derivative_y = effective_potential_y(
            x,
            y,
            mu
        )

        self.assertAlmostEqual(
            derivative_x,
            0.0,
            places=10
        )

        self.assertAlmostEqual(
            derivative_y,
            0.0,
            places=10
        )

    def test_l5_potential(self):
        mu = 0.1

        points = lagrange_points(mu)

        x, y = points["L5"]

        derivative_x = effective_potential_x(
            x,
            y,
            mu
        )

        derivative_y = effective_potential_y(
            x,
            y,
            mu
        )

        self.assertAlmostEqual(
            derivative_x,
            0.0,
            places=10
        )

        self.assertAlmostEqual(
            derivative_y,
            0.0,
            places=10
        )


class TestLagrangePoints(unittest.TestCase):

    def test_five_points_exist(self):
        points = lagrange_points(0.1)

        self.assertEqual(
            len(points),
            5
        )

        for name in [
            "L1",
            "L2",
            "L3",
            "L4",
            "L5"
        ]:
            self.assertIn(
                name,
                points
            )

    def test_l1_between_bodies(self):
        mu = 0.1

        points = lagrange_points(mu)

        l1_x, l1_y = points["L1"]

        primary_1 = -mu
        primary_2 = 1 - mu

        self.assertGreater(
            l1_x,
            primary_1
        )

        self.assertLess(
            l1_x,
            primary_2
        )

        self.assertAlmostEqual(
            l1_y,
            0.0,
            places=12
        )

    def test_l2_outside_smaller_body(self):
        mu = 0.1

        points = lagrange_points(mu)

        l2_x, l2_y = points["L2"]

        smaller_body_x = 1 - mu

        self.assertGreater(
            l2_x,
            smaller_body_x
        )

        self.assertAlmostEqual(
            l2_y,
            0.0,
            places=12
        )

    def test_l3_outside_larger_body(self):
        mu = 0.1

        points = lagrange_points(mu)

        l3_x, l3_y = points["L3"]

        larger_body_x = -mu

        self.assertLess(
            l3_x,
            larger_body_x
        )

        self.assertAlmostEqual(
            l3_y,
            0.0,
            places=12
        )

    def test_l4_geometry(self):
        mu = 0.25

        points = lagrange_points(mu)

        x, y = points["L4"]

        self.assertAlmostEqual(
            x,
            0.5 - mu,
            places=12
        )

        self.assertAlmostEqual(
            y,
            math.sqrt(3) / 2,
            places=12
        )

    def test_l5_geometry(self):
        mu = 0.25

        points = lagrange_points(mu)

        x, y = points["L5"]

        self.assertAlmostEqual(
            x,
            0.5 - mu,
            places=12
        )

        self.assertAlmostEqual(
            y,
            -math.sqrt(3) / 2,
            places=12
        )

    def test_l4_l5_symmetry(self):
        mu = 0.2

        points = lagrange_points(mu)

        l4_x, l4_y = points["L4"]
        l5_x, l5_y = points["L5"]

        self.assertAlmostEqual(
            l4_x,
            l5_x,
            places=12
        )

        self.assertAlmostEqual(
            l4_y,
            -l5_y,
            places=12
        )

    def test_lagrange_points_are_equilibrium_points(self):
        mu = 0.1

        points = lagrange_points(mu)

        for x, y in points.values():
            derivative_x = effective_potential_x(
                x,
                y,
                mu
            )

            derivative_y = effective_potential_y(
                x,
                y,
                mu
            )

            self.assertAlmostEqual(
                derivative_x,
                0.0,
                places=9
            )

            self.assertAlmostEqual(
                derivative_y,
                0.0,
                places=9
            )


class TestJacobiConstant(unittest.TestCase):

    def test_stationary_lagrange_point(self):
        mu = 0.1

        points = lagrange_points(mu)

        x, y = points["L4"]

        result = jacobi_constant(
            x,
            y,
            0.0,
            0.0,
            mu
        )

        expected = 3.0 - mu * (1 - mu)

        self.assertAlmostEqual(
            result,
            expected,
            places=10
        )

    def test_velocity_reduces_jacobi_constant(self):
        mu = 0.1

        x, y = lagrange_points(mu)["L4"]

        stationary = jacobi_constant(
            x,
            y,
            0.0,
            0.0,
            mu
        )

        moving = jacobi_constant(
            x,
            y,
            1.0,
            0.0,
            mu
        )

        self.assertAlmostEqual(
            stationary - moving,
            1.0,
            places=12
        )


class TestDistances(unittest.TestCase):

    def test_l4_distances_are_equal(self):
        mu = 0.1

        x, y = lagrange_points(mu)["L4"]

        r1 = distance_to_primary(
            x,
            y,
            1,
            mu
        )

        r2 = distance_to_primary(
            x,
            y,
            2,
            mu
        )

        self.assertAlmostEqual(
            r1,
            r2,
            places=12
        )

        self.assertAlmostEqual(
            r1,
            1.0,
            places=12
        )

    def test_invalid_primary(self):
        with self.assertRaises(ValueError):
            distance_to_primary(
                0,
                0,
                3,
                0.1
            )


class TestRandomLagrangeSystems(unittest.TestCase):

    def test_random_triangular_points(self):
        random.seed(42)

        for _ in range(20):

            mu = random.uniform(
                0.001,
                0.499
            )

            points = lagrange_points(mu)

            for name in ["L4", "L5"]:
                x, y = points[name]

                dx = effective_potential_x(
                    x,
                    y,
                    mu
                )

                dy = effective_potential_y(
                    x,
                    y,
                    mu
                )

                self.assertAlmostEqual(
                    dx,
                    0.0,
                    places=10
                )

                self.assertAlmostEqual(
                    dy,
                    0.0,
                    places=10
                )

    def test_random_collinear_points(self):
        random.seed(123)

        for _ in range(20):

            mu = random.uniform(
                0.001,
                0.499
            )

            points = lagrange_points(mu)

            for name in [
                "L1",
                "L2",
                "L3"
            ]:
                x, y = points[name]

                derivative = effective_potential_x(
                    x,
                    0.0,
                    mu
                )

                self.assertAlmostEqual(
                    derivative,
                    0.0,
                    places=9
                )


if __name__ == "__main__":
    unittest.main()
