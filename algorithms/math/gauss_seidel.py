"""
Gauss-Seidel Iterative Method for solving linear systems.

The Gauss-Seidel Method is an iterative numerical algorithm used
to solve a system of linear equations:

    A * x = b

where A is a square matrix, x is the vector of unknowns, and b
is the right-hand-side vector.

For each equation, the method solves for one variable and
immediately uses the newly calculated value when computing the
next variable.

For a system of n equations, the iteration is:

    x_i = (b_i - sum(A_ij * x_j)) / A_ii

where values already calculated during the current iteration are
used immediately.

The method can converge very quickly for suitable matrices.
In particular, strict diagonal dominance is a common sufficient
condition for convergence.

Unlike direct methods such as Gaussian elimination, Gauss-Seidel
does not solve the system in a fixed number of arithmetic steps.
Instead, it repeatedly improves an approximation until the
residual becomes sufficiently small.

This implementation checks for zero diagonal elements and stops
when the maximum change between two successive approximations
falls below the requested tolerance.
"""

import math
import random
import unittest


def gauss_seidel(
        matrix,
        vector,
        initial_guess=None,
        tolerance=1e-10,
        max_iterations=1000
):
    """
    Solve a linear system using the Gauss-Seidel Method.

    Args:
        matrix: Square coefficient matrix A.
        vector: Right-hand-side vector b.
        initial_guess: Initial approximation of the solution.
        tolerance: Required numerical accuracy.
        max_iterations: Maximum number of iterations.

    Returns:
        A list containing the approximate solution.

    Raises:
        ValueError: If dimensions or parameters are invalid.
        ZeroDivisionError: If a diagonal element is zero.
        RuntimeError: If the method does not converge.
    """

    if tolerance <= 0:
        raise ValueError("Tolerance must be positive.")

    if max_iterations <= 0:
        raise ValueError(
            "Maximum iterations must be positive."
        )

    n = len(vector)

    if n == 0:
        raise ValueError("System cannot be empty.")

    if len(matrix) != n:
        raise ValueError(
            "Matrix must have the same number of rows "
            "as the vector has elements."
        )

    for row in matrix:
        if len(row) != n:
            raise ValueError("Matrix must be square.")

    for i in range(n):
        if math.isclose(matrix[i][i], 0.0, abs_tol=1e-15):
            raise ZeroDivisionError(
                "Diagonal elements must be non-zero."
            )

    if initial_guess is None:
        x = [0.0] * n
    else:
        if len(initial_guess) != n:
            raise ValueError(
                "Initial guess has incorrect dimensions."
            )

        x = list(initial_guess)

    for _ in range(max_iterations):
        previous = x[:]

        for i in range(n):
            sum_before = 0.0
            sum_after = 0.0

            for j in range(i):
                sum_before += matrix[i][j] * x[j]

            for j in range(i + 1, n):
                sum_after += matrix[i][j] * previous[j]

            x[i] = (
                           vector[i]
                           - sum_before
                           - sum_after
                   ) / matrix[i][i]

        maximum_change = max(
            abs(x[i] - previous[i])
            for i in range(n)
        )

        if maximum_change <= tolerance:
            return x

    raise RuntimeError(
        "Gauss-Seidel Method did not converge."
    )


def residual(matrix, solution, vector):
    """
    Calculate the maximum absolute residual of A*x - b.
    """

    values = []

    for i in range(len(vector)):
        calculated = sum(
            matrix[i][j] * solution[j]
            for j in range(len(solution))
        )

        values.append(
            abs(calculated - vector[i])
        )

    return max(values)


class TestGaussSeidel(unittest.TestCase):

    def test_two_by_two_system(self):
        matrix = [
            [4, 1],
            [2, 3]
        ]

        vector = [9, 13]

        result = gauss_seidel(matrix, vector)

        self.assertAlmostEqual(result[0], 1.4, places=8)
        self.assertAlmostEqual(result[1], 3.4, places=8)

    def test_known_solution(self):
        matrix = [
            [5, 1, 1],
            [1, 6, 1],
            [1, 1, 7]
        ]

        expected = [2.0, 3.0, 4.0]

        vector = [
            sum(
                matrix[i][j] * expected[j]
                for j in range(3)
            )
            for i in range(3)
        ]

        result = gauss_seidel(matrix, vector)

        for actual, expected_value in zip(result, expected):
            self.assertAlmostEqual(
                actual,
                expected_value,
                places=8
            )

    def test_zero_initial_guess(self):
        matrix = [
            [4, 1],
            [2, 3]
        ]

        vector = [9, 13]

        result = gauss_seidel(
            matrix,
            vector,
            initial_guess=[0, 0]
        )

        self.assertAlmostEqual(result[0], 1.4, places=8)
        self.assertAlmostEqual(result[1], 3.4, places=8)

    def test_residual(self):
        matrix = [
            [10, 1],
            [2, 10]
        ]

        vector = [21, 22]

        result = gauss_seidel(matrix, vector)

        self.assertLess(
            residual(matrix, result, vector),
            1e-8
        )

    def test_empty_system(self):
        with self.assertRaises(ValueError):
            gauss_seidel([], [])

    def test_non_square_matrix(self):
        matrix = [
            [1, 2, 3],
            [4, 5, 6]
        ]

        vector = [1, 2]

        with self.assertRaises(ValueError):
            gauss_seidel(matrix, vector)

    def test_wrong_vector_size(self):
        matrix = [
            [4, 1],
            [2, 3]
        ]

        vector = [9]

        with self.assertRaises(ValueError):
            gauss_seidel(matrix, vector)

    def test_zero_diagonal(self):
        matrix = [
            [0, 1],
            [2, 3]
        ]

        vector = [1, 2]

        with self.assertRaises(ZeroDivisionError):
            gauss_seidel(matrix, vector)

    def test_invalid_tolerance(self):
        with self.assertRaises(ValueError):
            gauss_seidel(
                [[2, 1], [1, 2]],
                [3, 3],
                tolerance=0
            )

    def test_invalid_iterations(self):
        with self.assertRaises(ValueError):
            gauss_seidel(
                [[2, 1], [1, 2]],
                [3, 3],
                max_iterations=0
            )

    def test_wrong_initial_guess(self):
        with self.assertRaises(ValueError):
            gauss_seidel(
                [[2, 1], [1, 2]],
                [3, 3],
                initial_guess=[0]
            )


class TestRandomSystems(unittest.TestCase):

    def test_random_diagonally_dominant_systems(self):
        random.seed(42)

        for _ in range(100):
            size = random.randint(2, 6)

            matrix = []

            for i in range(size):
                row = []

                off_diagonal_sum = 0.0

                for j in range(size):
                    if i == j:
                        row.append(0.0)
                    else:
                        value = random.uniform(-2, 2)
                        row.append(value)
                        off_diagonal_sum += abs(value)

                diagonal = (
                        off_diagonal_sum
                        + random.uniform(1, 5)
                )

                row[i] = diagonal
                matrix.append(row)

            expected = [
                random.uniform(-10, 10)
                for _ in range(size)
            ]

            vector = [
                sum(
                    matrix[i][j] * expected[j]
                    for j in range(size)
                )
                for i in range(size)
            ]

            result = gauss_seidel(
                matrix,
                vector,
                tolerance=1e-9,
                max_iterations=5000
            )

            for actual, expected_value in zip(
                    result,
                    expected
            ):
                self.assertAlmostEqual(
                    actual,
                    expected_value,
                    places=6
                )

    def test_random_two_by_two_systems(self):
        random.seed(123)

        for _ in range(100):
            a = random.uniform(2, 10)
            d = random.uniform(2, 10)
            b = random.uniform(-1, 1)
            c = random.uniform(-1, 1)

            matrix = [
                [a, b],
                [c, d]
            ]

            expected = [
                random.uniform(-20, 20),
                random.uniform(-20, 20)
            ]

            vector = [
                a * expected[0] + b * expected[1],
                c * expected[0] + d * expected[1]
            ]

            result = gauss_seidel(
                matrix,
                vector,
                tolerance=1e-10
            )

            self.assertAlmostEqual(
                result[0],
                expected[0],
                places=7
            )

            self.assertAlmostEqual(
                result[1],
                expected[1],
                places=7
            )


if __name__ == "__main__":
    unittest.main()
