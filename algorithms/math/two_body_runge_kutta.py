"""
Two-Body Problem Using the Fourth-Order Runge-Kutta Method
===========================================================

The classical two-body problem describes the gravitational motion of two
bodies interacting through Newton's law of universal gravitation.

For a simplified planar system, the acceleration of body 1 relative to
body 2 can be written as:

    ax = -mu * x / r^3
    ay = -mu * y / r^3

where:

    r = sqrt(x^2 + y^2)

and:

    mu = G * (m1 + m2)

is the gravitational parameter of the system.

Instead of solving the second-order equations directly, we rewrite them
as a first-order system:

    dx/dt  = vx
    dy/dt  = vy
    dvx/dt = -mu*x/r^3
    dvy/dt = -mu*y/r^3

The complete state vector is therefore:

    [x, y, vx, vy]

and the system can be integrated using the fourth-order Runge-Kutta
method.

For a circular orbit with radius r, the required orbital velocity is:

    v = sqrt(mu / r)

The specific mechanical energy is:

    E = (vx^2 + vy^2)/2 - mu/r

For an ideal two-body system without numerical error, this quantity
remains constant.

This implementation provides:

    1. The differential equations of the two-body problem.
    2. A generic RK4 step for vector-valued systems.
    3. A complete orbit simulator.
    4. Specific orbital energy calculation.

The implementation uses dimensionless or arbitrary consistent units.
For example, one may choose:

    mu = 1
    r  = 1

which gives a circular orbital velocity of:

    v = 1

and an orbital period of:

    T = 2*pi
"""

import math
import random
import unittest


def add_vectors(first, second):
    """
    Add two vectors component by component.
    """

    return [
        a + b
        for a, b in zip(first, second)
    ]


def scale_vector(vector, scalar):
    """
    Multiply every vector component by a scalar.
    """

    return [
        value * scalar
        for value in vector
    ]


def rk4_step(function, time, state, step_size):
    """
    Perform one fourth-order Runge-Kutta step for a system of ODEs.

    The system has the general form:

        y' = f(t, y)

    where y is a vector.
    """

    k1 = function(
        time,
        state
    )

    state_k2 = add_vectors(
        state,
        scale_vector(k1, step_size / 2)
    )

    k2 = function(
        time + step_size / 2,
        state_k2
    )

    state_k3 = add_vectors(
        state,
        scale_vector(k2, step_size / 2)
    )

    k3 = function(
        time + step_size / 2,
        state_k3
    )

    state_k4 = add_vectors(
        state,
        scale_vector(k3, step_size)
    )

    k4 = function(
        time + step_size,
        state_k4
    )

    result = []

    for index in range(len(state)):

        value = (
            state[index]
            + step_size / 6
            * (
                k1[index]
                + 2 * k2[index]
                + 2 * k3[index]
                + k4[index]
            )
        )

        result.append(value)

    return result


def two_body_derivatives(mu):
    """
    Create the differential-equation function for the relative
    two-body problem.

    State:

        [x, y, vx, vy]
    """

    if mu <= 0:
        raise ValueError("mu must be positive")

    def derivatives(time, state):

        x, y, vx, vy = state

        radius_squared = x * x + y * y
        radius = math.sqrt(radius_squared)

        if radius == 0:
            raise ValueError(
                "The bodies cannot occupy the same position"
            )

        acceleration_factor = (
            -mu / (radius ** 3)
        )

        ax = acceleration_factor * x
        ay = acceleration_factor * y

        return [
            vx,
            vy,
            ax,
            ay
        ]

    return derivatives


def simulate_orbit(
    initial_state,
    mu,
    final_time,
    step_size
):
    """
    Simulate a two-body orbit.

    Returns a list of states:

        [
            [x, y, vx, vy],
            ...
        ]
    """

    if step_size <= 0:
        raise ValueError(
            "step_size must be positive"
        )

    if final_time < 0:
        raise ValueError(
            "final_time must not be negative"
        )

    if len(initial_state) != 4:
        raise ValueError(
            "state must contain [x, y, vx, vy]"
        )

    derivatives = two_body_derivatives(mu)

    state = list(initial_state)
    time = 0.0

    states = [state.copy()]

    while time < final_time - 1e-15:

        h = min(
            step_size,
            final_time - time
        )

        state = rk4_step(
            derivatives,
            time,
            state,
            h
        )

        time += h

        states.append(state.copy())

    return states


def specific_energy(state, mu):
    """
    Calculate the specific mechanical energy:

        E = v^2 / 2 - mu / r
    """

    x, y, vx, vy = state

    radius = math.sqrt(
        x * x + y * y
    )

    if radius == 0:
        raise ValueError(
            "Radius cannot be zero"
        )

    velocity_squared = (
        vx * vx
        + vy * vy
    )

    return (
        velocity_squared / 2
        - mu / radius
    )


def circular_velocity(radius, mu):
    """
    Calculate the velocity required for a circular orbit.
    """

    if radius <= 0:
        raise ValueError(
            "radius must be positive"
        )

    if mu <= 0:
        raise ValueError(
            "mu must be positive"
        )

    return math.sqrt(mu / radius)


class TestVectorOperations(unittest.TestCase):

    def test_add_vectors(self):
        result = add_vectors(
            [1, 2, 3],
            [4, 5, 6]
        )

        self.assertEqual(
            result,
            [5, 7, 9]
        )

    def test_scale_vector(self):
        result = scale_vector(
            [1, -2, 3],
            2
        )

        self.assertEqual(
            result,
            [2, -4, 6]
        )


class TestTwoBodyProblem(unittest.TestCase):

    def test_circular_velocity(self):
        velocity = circular_velocity(
            radius=1,
            mu=1
        )

        self.assertAlmostEqual(
            velocity,
            1.0,
            places=12
        )

    def test_initial_acceleration(self):
        derivatives = two_body_derivatives(
            mu=1
        )

        result = derivatives(
            0,
            [1, 0, 0, 1]
        )

        self.assertAlmostEqual(
            result[0],
            0.0
        )

        self.assertAlmostEqual(
            result[1],
            1.0
        )

        self.assertAlmostEqual(
            result[2],
            -1.0
        )

        self.assertAlmostEqual(
            result[3],
            0.0
        )

    def test_circular_orbit(self):
        """
        For mu = 1 and r = 1:

            v = 1

        The orbital period is:

            T = 2*pi
        """

        mu = 1.0
        radius = 1.0
        velocity = circular_velocity(
            radius,
            mu
        )

        initial_state = [
            radius,
            0.0,
            0.0,
            velocity
        ]

        states = simulate_orbit(
            initial_state,
            mu,
            2 * math.pi,
            0.01
        )

        final_state = states[-1]

        self.assertAlmostEqual(
            final_state[0],
            1.0,
            places=6
        )

        self.assertAlmostEqual(
            final_state[1],
            0.0,
            places=6
        )

        self.assertAlmostEqual(
            final_state[2],
            0.0,
            places=6
        )

        self.assertAlmostEqual(
            final_state[3],
            1.0,
            places=6
        )

    def test_energy_conservation(self):
        """
        Numerical integration should approximately conserve
        specific mechanical energy.
        """

        mu = 1.0

        initial_state = [
            1.0,
            0.0,
            0.0,
            1.0
        ]

        states = simulate_orbit(
            initial_state,
            mu,
            2 * math.pi,
            0.02
        )

        initial_energy = specific_energy(
            states[0],
            mu
        )

        final_energy = specific_energy(
            states[-1],
            mu
        )

        self.assertAlmostEqual(
            final_energy,
            initial_energy,
            places=7
        )

    def test_circular_orbit_radius(self):
        mu = 1.0
        radius = 3.0

        velocity = circular_velocity(
            radius,
            mu
        )

        initial_state = [
            radius,
            0.0,
            0.0,
            velocity
        ]

        states = simulate_orbit(
            initial_state,
            mu,
            2 * math.pi * math.sqrt(radius ** 3 / mu),
            0.02
        )

        final_state = states[-1]

        final_radius = math.sqrt(
            final_state[0] ** 2
            + final_state[1] ** 2
        )

        self.assertAlmostEqual(
            final_radius,
            radius,
            places=5
        )

    def test_zero_final_time(self):
        initial_state = [
            1.0,
            2.0,
            3.0,
            4.0
        ]

        result = simulate_orbit(
            initial_state,
            mu=1.0,
            final_time=0.0,
            step_size=0.1
        )

        self.assertEqual(
            len(result),
            1
        )

        self.assertEqual(
            result[0],
            initial_state
        )

    def test_invalid_mu(self):
        with self.assertRaises(ValueError):
            two_body_derivatives(0)

    def test_collision(self):
        derivatives = two_body_derivatives(
            mu=1
        )

        with self.assertRaises(ValueError):
            derivatives(
                0,
                [0, 0, 1, 0]
            )


class TestRandomTwoBody(unittest.TestCase):

    def test_random_circular_orbits(self):
        """
        Randomized test of circular orbits.

        For each radius:

            v = sqrt(mu / r)

        and therefore the radius should remain approximately constant.
        """

        random.seed(42)

        for _ in range(10):

            mu = random.uniform(
                0.5,
                5.0
            )

            radius = random.uniform(
                0.5,
                3.0
            )

            velocity = circular_velocity(
                radius,
                mu
            )

            initial_state = [
                radius,
                0.0,
                0.0,
                velocity
            ]

            period = (
                2
                * math.pi
                * math.sqrt(
                    radius ** 3 / mu
                )
            )

            states = simulate_orbit(
                initial_state,
                mu,
                period,
                period / 500
            )

            final_state = states[-1]

            final_radius = math.sqrt(
                final_state[0] ** 2
                + final_state[1] ** 2
            )

            self.assertAlmostEqual(
                final_radius,
                radius,
                places=4
            )

    def test_random_energy_conservation(self):
        """
        Check approximate energy conservation for random
        non-circular bound orbits.
        """

        random.seed(123)

        for _ in range(10):

            mu = random.uniform(
                0.5,
                3.0
            )

            radius = random.uniform(
                1.0,
                3.0
            )

            circular_v = circular_velocity(
                radius,
                mu
            )

            velocity = random.uniform(
                0.7 * circular_v,
                1.2 * circular_v
            )

            initial_state = [
                radius,
                0.0,
                0.0,
                velocity
            ]

            initial_energy = specific_energy(
                initial_state,
                mu
            )

            states = simulate_orbit(
                initial_state,
                mu,
                3.0,
                0.01
            )

            final_energy = specific_energy(
                states[-1],
                mu
            )

            self.assertAlmostEqual(
                final_energy,
                initial_energy,
                places=5
            )


if __name__ == "__main__":
    unittest.main()