"""
Newton's Method for solving systems of nonlinear equations.

Newton's Method can be extended from one equation to a system of
several nonlinear equations.

For a system:

    F(x) = 0

where F is a vector of functions, Newton's iteration is:

    J(x) * delta = -F(x)

    x(next) = x + delta

Here J(x) is the Jacobian matrix containing the partial derivatives
of all functions with respect to all variables.

For a two-variable system:

    f(x, y) = 0
    g(x, y) = 0

the Jacobian is:

        [ df/dx  df/dy ]
    J = [             ]
        [ dg/dx  dg/dy ]

At every iteration we solve a linear system involving the Jacobian.

This implementation uses Gaussian elimination with partial pivoting
to solve the linear system instead of relying on external numerical
libraries.

The method is very powerful, but convergence depends strongly on
the initial approximation. A poor starting point can cause
divergence or convergence to a different solution.
"""

import math
import random
import unittest


def solve_linear_system(matrix, vector):
    """
    Solve A * x = b using Gaussian elimination with partial pivoting.
    """

    n = len(vector)

    if len(matrix) != n:
        raise ValueError("Matrix dimensions do not match.")

    augmented = [
        matrix[i][:] + [vector[i]]
        for i in range(n)
    ]

    for column in range(n):
        pivot = max(
            range(column, n),
            key=lambda row: abs(augmented[row][column])
        )

        if math.isclose(
                augmented[pivot][column],
                0.0,
                abs_tol=1e-15
        ):
            raise ZeroDivisionError(
                "Singular matrix."
            )

        augmented[column], augmented[pivot] = (
            augmented[pivot],
            augmented[column]
        )

        pivot_value = augmented[column][column]

        for j in range(column, n + 1):
            augmented[column][j] /= pivot_value

        for row in range(n):
            if row == column:
                continue

            factor = augmented[row][column]

            for j in range(column, n + 1):
                augmented[row][j] -= (
                        factor * augmented[column][j]
                )

    return [augmented[i][n] for i in range(n)]


def newton_system(
        functions,
        jacobian,
        initial_guess,
        tolerance=1e-10,
        max_iterations=100
):
    """
    Find a solution of a nonlinear system using Newton's Method.

    Args:
        functions: List of functions F(x).
        jacobian: Function returning the Jacobian matrix.
        initial_guess: Initial vector of variables.
        tolerance: Required accuracy.
        max_iterations: Maximum number of iterations.

    Returns:
        A list containing the approximate solution.

    Raises:
        ValueError: If parameters are invalid.
        ZeroDivisionError: If the Jacobian becomes singular.
        RuntimeError: If the method does not converge.
    """

    if tolerance <= 0:
        raise ValueError("Tolerance must be positive.")

    if max_iterations <= 0:
        raise ValueError(
            "Maximum iterations must be positive."
        )

    x = list(initial_guess)

    for _ in range(max_iterations):
        values = [
            function(x)
            for function in functions
        ]

        if max(abs(value) for value in values) <= tolerance:
            return x

        matrix = jacobian(x)

        delta = solve_linear_system(
            matrix,
            [-value for value in values]
        )

        next_x = [
            x[i] + delta[i]
            for i in range(len(x))
        ]

        if max(
                abs(next_x[i] - x[i])
                for i in range(len(x))
        ) <= tolerance:
            return next_x

        x = next_x

    raise RuntimeError(
        "Newton's Method did not converge."
    )


class TestLinearSystemSolver(unittest.TestCase):

    def test_two_by_two_system(self):
        matrix = [
            [2, 1],
            [1, -1]
        ]

        vector = [5, 1]

        result = solve_linear_system(matrix, vector)

        self.assertAlmostEqual(result[0], 2.0)
        self.assertAlmostEqual(result[1], 1.0)

    def test_three_by_three_system(self):
        matrix = [
            [2, 1, -1],
            [-3, -1, 2],
            [-2, 1, 2]
        ]

        vector = [8, -11, -3]

        result = solve_linear_system(matrix, vector)

        self.assertAlmostEqual(result[0], 2.0)
        self.assertAlmostEqual(result[1], 3.0)
        self.assertAlmostEqual(result[2], -1.0)

    def test_singular_matrix(self):
        matrix = [
            [1, 2],
            [2, 4]
        ]

        vector = [3, 6]

        with self.assertRaises(ZeroDivisionError):
            solve_linear_system(matrix, vector)


class TestNewtonSystem(unittest.TestCase):

    def test_simple_linear_system(self):
        functions = [
            lambda v: v[0] + v[1] - 5,
            lambda v: v[0] - v[1] - 1
        ]

        def jacobian(v):
            return [
                [1, 1],
                [1, -1]
            ]

        result = newton_system(
            functions,
            jacobian,
            [0, 0]
        )

        self.assertAlmostEqual(result[0], 3.0)
        self.assertAlmostEqual(result[1], 2.0)

    def test_nonlinear_circle_system(self):
        functions = [
            lambda v: v[0] ** 2 + v[1] ** 2 - 25,
            lambda v: v[0] - v[1] - 1
        ]

        def jacobian(v):
            x, y = v

            return [
                [2 * x, 2 * y],
                [1, -1]
            ]

        result = newton_system(
            functions,
            jacobian,
            [4, 3]
        )

        self.assertAlmostEqual(result[0], 4.0, places=8)
        self.assertAlmostEqual(result[1], 3.0, places=8)

    def test_nonlinear_system_with_squares(self):
        functions = [
            lambda v: v[0] ** 2 + v[1] ** 2 - 13,
            lambda v: v[0] ** 2 - v[1] ** 2 - 5
        ]

        def jacobian(v):
            x, y = v

            return [
                [2 * x, 2 * y],
                [2 * x, -2 * y]
            ]

        result = newton_system(
            functions,
            jacobian,
            [3, 2]
        )

        self.assertAlmostEqual(result[0], 3.0, places=8)
        self.assertAlmostEqual(result[1], 2.0, places=8)

    def test_trigonometric_system(self):
        functions = [
            lambda v: math.sin(v[0]) + v[1] - 1,
            lambda v: v[0] + math.cos(v[1]) - 1
        ]

        def jacobian(v):
            x, y = v

            return [
                [math.cos(x), 1],
                [1, -math.sin(y)]
            ]

        result = newton_system(
            functions,
            jacobian,
            [0.5, 0.5]
        )

        for function in functions:
            self.assertAlmostEqual(
                function(result),
                0.0,
                places=8
            )

    def test_already_at_solution(self):
        functions = [
            lambda v: v[0] - 3,
            lambda v: v[1] + 2
        ]

        def jacobian(v):
            return [
                [1, 0],
                [0, 1]
            ]

        result = newton_system(
            functions,
            jacobian,
            [3, -2]
        )

        self.assertEqual(result, [3, -2])

    def test_invalid_tolerance(self):
        with self.assertRaises(ValueError):
            newton_system(
                [lambda v: v[0] - 1],
                lambda v: [[1]],
                [0],
                tolerance=0
            )

    def test_invalid_iterations(self):
        with self.assertRaises(ValueError):
            newton_system(
                [lambda v: v[0] - 1],
                lambda v: [[1]],
                [0],
                max_iterations=0
            )


class TestRandomSystems(unittest.TestCase):

    def test_random_linear_systems(self):
        random.seed(42)

        for _ in range(100):
            x_root = random.uniform(-20, 20)
            y_root = random.uniform(-20, 20)

            a = random.uniform(1, 5)
            b = random.uniform(1, 5)
            c = random.uniform(1, 5)
            d = random.uniform(1, 5)

            determinant = a * d - b * c

            if abs(determinant) < 0.5:
                continue

            functions = [
                lambda v, a=a, b=b, xr=x_root, yr=y_root:
                a * (v[0] - xr) + b * (v[1] - yr),

                lambda v, c=c, d=d, xr=x_root, yr=y_root:
                c * (v[0] - xr) + d * (v[1] - yr)
            ]

            def jacobian(v, a=a, b=b, c=c, d=d):
                return [
                    [a, b],
                    [c, d]
                ]

            initial_guess = [
                x_root + random.uniform(-10, 10),
                y_root + random.uniform(-10, 10)
            ]

            result = newton_system(
                functions,
                jacobian,
                initial_guess
            )

            self.assertAlmostEqual(
                result[0],
                x_root,
                places=7
            )

            self.assertAlmostEqual(
                result[1],
                y_root,
                places=7
            )

    def test_random_quadratic_systems(self):
        random.seed(123)

        for _ in range(100):
            x_root = random.uniform(1, 10)
            y_root = random.uniform(1, 10)

            functions = [
                lambda v, xr=x_root, yr=y_root:
                v[0] ** 2 - xr ** 2,

                lambda v, yr=y_root:
                v[1] ** 2 - yr ** 2
            ]

            def jacobian(v):
                return [
                    [2 * v[0], 0],
                    [0, 2 * v[1]]
                ]

            initial_guess = [
                x_root * random.uniform(0.5, 1.5),
                y_root * random.uniform(0.5, 1.5)
            ]

            result = newton_system(
                functions,
                jacobian,
                initial_guess
            )

            self.assertAlmostEqual(
                result[0],
                x_root,
                places=7
            )

            self.assertAlmostEqual(
                result[1],
                y_root,
                places=7
            )


if __name__ == "__main__":
    unittest.main()
