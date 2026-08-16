"""
Dynamic Programming - Minimum Path Sum

Description:
    The Minimum Path Sum problem is a classic Dynamic Programming
    problem involving optimization on a two-dimensional grid.

    Each cell in the grid contains a non-negative cost.

    Starting from the top-left cell, the goal is to reach the
    bottom-right cell while minimizing the total cost of all cells
    visited along the path.

    Movement is restricted to:

        - Right.
        - Down.

    For example:

        grid = [
            [1, 3, 1],
            [1, 5, 1],
            [4, 2, 1]
        ]

    One optimal path is:

        1 -> 3 -> 1 -> 1 -> 1

    The total cost is:

        7

Purpose:
    - Find the cheapest path through a grid.
    - Demonstrate Dynamic Programming on a two-dimensional state.
    - Solve optimization problems with restricted movement.
    - Avoid repeatedly calculating the same paths.

Problem:
    A naive recursive solution would explore every possible path
    from the starting cell to the destination.

    Many of those paths share the same intermediate cells.

    Dynamic Programming calculates the optimal cost for every cell
    once and reuses those results.

State:
    dp[i][j] represents the minimum cost required to reach cell
    (i, j) from the top-left corner.

Transition:
    A cell can only be reached from:

        - The cell above it.
        - The cell to its left.

    Therefore:

        dp[i][j] = grid[i][j] + min(
            dp[i - 1][j],
            dp[i][j - 1]
        )

    The current cell's cost is added to the cheapest way of reaching
    one of its two possible predecessor cells.

Base case:
    The starting cell is:

        dp[0][0] = grid[0][0]

    The first row can only be reached by moving right.

    The first column can only be reached by moving down.

Complexity:
    Time:
        O(rows * columns)

    Space:
        O(rows * columns)

    The algorithm can also be optimized to O(columns) additional
    memory because each row only depends on the previous row and
    the current row.

When to use:
    - Grid optimization.
    - Path planning.
    - Game maps.
    - Robotics.
    - Resource allocation.
    - Cost optimization.
    - Network routing models.
    - Image and matrix processing.

Advantages:
    - Simple state representation.
    - Efficient compared with exploring every possible path.
    - Easy to extend to related grid problems.
    - Clearly demonstrates optimal substructure.

Disadvantages:
    - The basic implementation requires O(rows * columns) memory.
    - Movement restrictions must be compatible with the recurrence.
    - Different movement rules may require a different DP state.

Important concept:
    The key question is:

        "What is the minimum cost of reaching this cell?"

    Once the answer is known for every cell, the answer for the
    destination is simply the value stored in the bottom-right cell.

    This is a common Dynamic Programming pattern:

        Current state = local cost + best previous state
"""
import random
import unittest


def minimum_path_sum(grid):
    if not grid:
        return 0

    if not grid[0]:
        return 0

    rows = len(grid)
    columns = len(grid[0])

    if any(len(row) != columns for row in grid):
        raise ValueError("Grid must be rectangular")

    if any(
            cell < 0
            for row in grid
            for cell in row
    ):
        raise ValueError("Grid values cannot be negative")

    dp = [
        [0] * columns
        for _ in range(rows)
    ]

    dp[0][0] = grid[0][0]

    for column in range(1, columns):
        dp[0][column] = (
                dp[0][column - 1] +
                grid[0][column]
        )

    for row in range(1, rows):
        dp[row][0] = (
                dp[row - 1][0] +
                grid[row][0]
        )

    for row in range(1, rows):
        for column in range(1, columns):
            dp[row][column] = grid[row][column] + min(
                dp[row - 1][column],
                dp[row][column - 1]
            )

    return dp[rows - 1][columns - 1]


class MinimumPathSumTests(unittest.TestCase):

    def test_basic_grid(self):
        grid = [
            [1, 3, 1],
            [1, 5, 1],
            [4, 2, 1]
        ]

        result = minimum_path_sum(grid)

        self.assertEqual(result, 7)

    def test_single_cell(self):
        result = minimum_path_sum([[5]])

        self.assertEqual(result, 5)

    def test_single_row(self):
        grid = [[1, 2, 3, 4]]

        result = minimum_path_sum(grid)

        self.assertEqual(result, 10)

    def test_single_column(self):
        grid = [
            [1],
            [2],
            [3],
            [4]
        ]

        result = minimum_path_sum(grid)

        self.assertEqual(result, 10)

    def test_all_ones(self):
        grid = [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1]
        ]

        result = minimum_path_sum(grid)

        self.assertEqual(result, 5)

    def test_zero_values(self):
        grid = [
            [0, 1],
            [1, 0]
        ]

        result = minimum_path_sum(grid)

        self.assertEqual(result, 1)

    def test_empty_grid(self):
        result = minimum_path_sum([])

        self.assertEqual(result, 0)

    def test_empty_row(self):
        result = minimum_path_sum([[]])

        self.assertEqual(result, 0)

    def test_non_rectangular_grid(self):
        grid = [
            [1, 2],
            [3]
        ]

        with self.assertRaises(ValueError):
            minimum_path_sum(grid)

    def test_negative_value(self):
        grid = [
            [1, -2],
            [3, 4]
        ]

        with self.assertRaises(ValueError):
            minimum_path_sum(grid)


class MinimumPathSumRandomTests(unittest.TestCase):

    def brute_force(self, grid, row=0, column=0):
        rows = len(grid)
        columns = len(grid[0])

        if row == rows - 1 and column == columns - 1:
            return grid[row][column]

        if row == rows - 1:
            return (
                    grid[row][column] +
                    self.brute_force(grid, row, column + 1)
            )

        if column == columns - 1:
            return (
                    grid[row][column] +
                    self.brute_force(grid, row + 1, column)
            )

        right = self.brute_force(
            grid,
            row,
            column + 1
        )

        down = self.brute_force(
            grid,
            row + 1,
            column
        )

        return grid[row][column] + min(
            right,
            down
        )

    def create_random_grid(self):
        rows = random.randint(1, 6)
        columns = random.randint(1, 6)

        return [
            [
                random.randint(0, 20)
                for _ in range(columns)
            ]
            for _ in range(rows)
        ]

    def test_random_against_brute_force(self):
        for _ in range(500):
            grid = self.create_random_grid()

            expected = self.brute_force(grid)
            result = minimum_path_sum(grid)

            self.assertEqual(result, expected)

    def test_random_single_cells(self):
        for _ in range(500):
            value = random.randint(0, 1000)

            result = minimum_path_sum([[value]])

            self.assertEqual(result, value)

    def test_random_single_rows(self):
        for _ in range(500):
            length = random.randint(1, 30)

            grid = [[
                random.randint(0, 100)
                for _ in range(length)
            ]]

            expected = sum(grid[0])
            result = minimum_path_sum(grid)

            self.assertEqual(result, expected)

    def test_random_single_columns(self):
        for _ in range(500):
            length = random.randint(1, 30)

            grid = [
                [random.randint(0, 100)]
                for _ in range(length)
            ]

            expected = sum(row[0] for row in grid)
            result = minimum_path_sum(grid)

            self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
