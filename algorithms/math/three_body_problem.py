"""
Three-Body Problem Using the Fourth-Order Runge-Kutta Method
=============================================================

The three-body problem describes the gravitational interaction of three
bodies.

Unlike the two-body problem, there is generally no simple closed-form
solution for the complete motion of three mutually interacting bodies.

For each body:

    d(position) / dt = velocity

    d(velocity) / dt = gravitational acceleration

For body i, the acceleration caused by body j is:

    a_ij = G * m_j * (r_j - r_i) / |r_j - r_i|^3

The total acceleration of a body is the sum of the contributions from
the other two bodies.

The state of the system is represented as:

    [
        x1, y1, vx1, vy1,
        x2, y2, vx2, vy2,
        x3, y3, vx3, vy3
    ]

This gives twelve first-order differential equations.

The equations are integrated with the fourth-order Runge-Kutta method.

The implementation uses two-dimensional motion and a gravitational
constant G. All quantities must use mutually consistent units.

The file also provides functions for calculating:

    - total kinetic energy,
    - total gravitational potential energy,
    - total mechanical energy.

For an ideal isolated three-body system, total mechanical energy is
constant. Numerical integration introduces a small error, so the energy
will not be perfectly constant, but a sufficiently small RK4 step should
keep the drift small.

The three-body problem is an important example of why numerical methods
are necessary in celestial mechanics: even deterministic gravitational
systems can exhibit extremely complicated and sensitive trajectories.
"""

import math
import random
import unittest


def vector_add(first, second):
    """
    Add two vectors component by component.
    """

    return [
        a + b
        for a, b in zip(first, second)
    ]


def vector_scale(vector, scalar):
    """
    Multiply every component of a vector by a scalar.
    """

    return [
        value * scalar
        for value in vector
    ]


def rk4_step(function, time, state, step_size):
    """
    Perform one fourth-order Runge-Kutta step for a vector-valued ODE.
    """

    k1 = function(time, state)

    state_k2 = vector_add(
        state,
        vector_scale(
            k1,
            step_size / 2
        )
    )

    k2 = function(
        time + step_size / 2,
        state_k2
    )

    state_k3 = vector_add(
        state,
        vector_scale(
            k2,
            step_size / 2
        )
    )

    k3 = function(
        time + step_size / 2,
        state_k3
    )

    state_k4 = vector_add(
        state,
        vector_scale(
            k3,
            step_size
        )
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


def three_body_derivatives(
        masses,
        gravitational_constant=1.0
):
    """
    Create the differential equations for three gravitationally
    interacting bodies.

    State format:

        [
            x1, y1, vx1, vy1,
            x2, y2, vx2, vy2,
            x3, y3, vx3, vy3
        ]
    """

    if len(masses) != 3:
        raise ValueError(
            "Exactly three masses are required"
        )

    if any(mass <= 0 for mass in masses):
        raise ValueError(
            "All masses must be positive"
        )

    if gravitational_constant <= 0:
        raise ValueError(
            "gravitational_constant must be positive"
        )

    def derivatives(time, state):

        if len(state) != 12:
            raise ValueError(
                "State must contain 12 values"
            )

        positions = [
            (state[0], state[1]),
            (state[4], state[5]),
            (state[8], state[9])
        ]

        velocities = [
            (state[2], state[3]),
            (state[6], state[7]),
            (state[10], state[11])
        ]

        accelerations = []

        for i in range(3):

            ax = 0.0
            ay = 0.0

            xi, yi = positions[i]

            for j in range(3):

                if i == j:
                    continue

                xj, yj = positions[j]

                dx = xj - xi
                dy = yj - yi

                distance_squared = (
                        dx * dx
                        + dy * dy
                )

                distance = math.sqrt(
                    distance_squared
                )

                if distance == 0:
                    raise ValueError(
                        "Two bodies cannot occupy "
                        "the same position"
                    )

                factor = (
                        gravitational_constant
                        * masses[j]
                        / distance ** 3
                )

                ax += factor * dx
                ay += factor * dy

            accelerations.append(
                (ax, ay)
            )

        result = []

        for index in range(3):
            vx, vy = velocities[index]
            ax, ay = accelerations[index]

            result.extend([
                vx,
                vy,
                ax,
                ay
            ])

        return result

    return derivatives


def simulate_three_body_system(
        initial_state,
        masses,
        final_time,
        step_size,
        gravitational_constant=1.0
):
    """
    Simulate the three-body system using RK4.

    Returns a list containing the complete state at every integration
    step.
    """

    if len(initial_state) != 12:
        raise ValueError(
            "Initial state must contain 12 values"
        )

    if step_size <= 0:
        raise ValueError(
            "step_size must be positive"
        )

    if final_time < 0:
        raise ValueError(
            "final_time must not be negative"
        )

    derivatives = three_body_derivatives(
        masses,
        gravitational_constant
    )

    state = list(initial_state)
    time = 0.0

    states = [
        state.copy()
    ]

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

        states.append(
            state.copy()
        )

    return states


def total_kinetic_energy(state, masses):
    """
    Calculate total kinetic energy:

        K = sum(1/2 * m_i * v_i^2)
    """

    if len(masses) != 3:
        raise ValueError(
            "Exactly three masses are required"
        )

    kinetic_energy = 0.0

    for index, mass in enumerate(masses):
        base = index * 4

        vx = state[base + 2]
        vy = state[base + 3]

        velocity_squared = (
                vx * vx
                + vy * vy
        )

        kinetic_energy += (
                0.5
                * mass
                * velocity_squared
        )

    return kinetic_energy


def total_potential_energy(
        state,
        masses,
        gravitational_constant=1.0
):
    """
    Calculate gravitational potential energy:

        U = -G * sum(
            m_i * m_j / r_ij
        )
    """

    if len(masses) != 3:
        raise ValueError(
            "Exactly three masses are required"
        )

    positions = [
        (state[0], state[1]),
        (state[4], state[5]),
        (state[8], state[9])
    ]

    potential_energy = 0.0

    for i in range(3):

        for j in range(i + 1, 3):

            xi, yi = positions[i]
            xj, yj = positions[j]

            dx = xj - xi
            dy = yj - yi

            distance = math.sqrt(
                dx * dx
                + dy * dy
            )

            if distance == 0:
                raise ValueError(
                    "Two bodies cannot occupy "
                    "the same position"
                )

            potential_energy -= (
                    gravitational_constant
                    * masses[i]
                    * masses[j]
                    / distance
            )

    return potential_energy


def total_energy(
        state,
        masses,
        gravitational_constant=1.0
):
    """
    Calculate total mechanical energy.
    """

    return (
            total_kinetic_energy(
                state,
                masses
            )
            + total_potential_energy(
        state,
        masses,
        gravitational_constant
    )
    )


class TestThreeBody(unittest.TestCase):

    def test_vector_add(self):
        result = vector_add(
            [1, 2, 3],
            [4, 5, 6]
        )

        self.assertEqual(
            result,
            [5, 7, 9]
        )

    def test_vector_scale(self):
        result = vector_scale(
            [1, -2, 3],
            2
        )

        self.assertEqual(
            result,
            [2, -4, 6]
        )

    def test_derivative_dimensions(self):
        derivatives = three_body_derivatives(
            [1, 1, 1]
        )

        state = [
            -1, 0, 0, 0,
            1, 0, 0, 0,
            0, 1, 0, 0
        ]

        result = derivatives(
            0,
            state
        )

        self.assertEqual(
            len(result),
            12
        )

    def test_symmetric_configuration(self):
        """
        Three equal masses placed symmetrically around the origin.

        The accelerations should point toward the center of the
        configuration.
        """

        masses = [1, 1, 1]

        state = [
            1, 0, 0, 0,
            -0.5, math.sqrt(3) / 2, 0, 0,
            -0.5, -math.sqrt(3) / 2, 0, 0
        ]

        derivatives = three_body_derivatives(
            masses
        )

        result = derivatives(
            0,
            state
        )

        # The first body's acceleration should point
        # approximately in the negative x direction.
        self.assertLess(
            result[2],
            0
        )

        self.assertAlmostEqual(
            result[3],
            0.0,
            places=12
        )

    def test_kinetic_energy(self):
        state = [
            0, 0, 2, 0,
            0, 0, 0, 3,
            0, 0, 1, 1
        ]

        result = total_kinetic_energy(
            state,
            [1, 2, 3]
        )

        expected = (
                0.5 * 1 * 4
                + 0.5 * 2 * 9
                + 0.5 * 3 * 2
        )

        self.assertAlmostEqual(
            result,
            expected,
            places=12
        )

    def test_energy(self):
        state = [
            1, 0, 0, 1,
            -1, 0, 0, -1,
            0, 2, 1, 0
        ]

        kinetic = total_kinetic_energy(
            state,
            [1, 1, 1]
        )

        potential = total_potential_energy(
            state,
            [1, 1, 1]
        )

        result = total_energy(
            state,
            [1, 1, 1]
        )

        self.assertAlmostEqual(
            result,
            kinetic + potential,
            places=12
        )

    def test_stationary_system_has_gravity(self):
        """
        Bodies initially at rest should immediately begin accelerating
        toward each other.
        """

        masses = [1, 1, 1]

        state = [
            -1, 0, 0, 0,
            0, 0, 0, 0,
            1, 0, 0, 0
        ]

        derivatives = three_body_derivatives(
            masses
        )

        result = derivatives(
            0,
            state
        )

        self.assertGreater(
            result[2],
            0
        )

        self.assertLess(
            result[10],
            0
        )

    def test_zero_final_time(self):
        state = [
            1, 0, 0, 0,
            0, 1, 0, 0,
            -1, 0, 0, 0
        ]

        result = simulate_three_body_system(
            state,
            [1, 1, 1],
            final_time=0,
            step_size=0.1
        )

        self.assertEqual(
            len(result),
            1
        )

        self.assertEqual(
            result[0],
            state
        )

    def test_invalid_mass_count(self):
        with self.assertRaises(ValueError):
            three_body_derivatives(
                [1, 1]
            )

    def test_invalid_mass(self):
        with self.assertRaises(ValueError):
            three_body_derivatives(
                [1, -1, 1]
            )

    def test_collision(self):
        derivatives = three_body_derivatives(
            [1, 1, 1]
        )

        state = [
            0, 0, 0, 0,
            0, 0, 1, 0,
            1, 0, 0, 0
        ]

        with self.assertRaises(ValueError):
            derivatives(
                0,
                state
            )


class TestRandomThreeBody(unittest.TestCase):

    def test_random_energy_consistency(self):
        """
        The energy calculated by total_energy must always equal the sum
        of kinetic and potential energy.
        """

        random.seed(42)

        for _ in range(20):

            masses = [
                random.uniform(0.5, 3.0)
                for _ in range(3)
            ]

            state = []

            for _ in range(3):
                state.extend([
                    random.uniform(-3, 3),
                    random.uniform(-3, 3),
                    random.uniform(-1, 1),
                    random.uniform(-1, 1)
                ])

            kinetic = total_kinetic_energy(
                state,
                masses
            )

            potential = total_potential_energy(
                state,
                masses
            )

            result = total_energy(
                state,
                masses
            )

            self.assertAlmostEqual(
                result,
                kinetic + potential,
                places=12
            )

    def test_random_short_simulations(self):
        """
        Verify that short simulations produce finite numerical states
        for randomly generated non-colliding configurations.
        """

        random.seed(123)

        for _ in range(10):

            masses = [
                random.uniform(0.5, 2.0)
                for _ in range(3)
            ]

            state = [
                -2, 0, 0, 0.5,
                2, 0, 0, -0.5,
                0, 3, -0.5, 0
            ]

            states = simulate_three_body_system(
                state,
                masses,
                final_time=0.1,
                step_size=0.005
            )

            final_state = states[-1]

            for value in final_state:
                self.assertTrue(
                    math.isfinite(value)
                )


if __name__ == "__main__":
    unittest.main()
