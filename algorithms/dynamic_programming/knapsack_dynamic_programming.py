"""
Dynamic Programming - 0/1 Knapsack Problem

Description:
    Dynamic Programming (DP) is an algorithmic technique used to solve
    problems that contain overlapping subproblems and optimal substructure.

    Instead of solving the same subproblem repeatedly, Dynamic Programming
    stores the result of previously solved subproblems and reuses them.

    The 0/1 Knapsack Problem is a classic example.

    We are given a collection of items. Every item has:

        - A weight.
        - A value.

    We also have a backpack with a maximum weight capacity.

    The goal is to select a subset of items with the highest possible
    total value without exceeding the backpack capacity.

    The "0/1" means that every item can either be selected once or
    not selected at all.

Problem:
    Given:

        weights = [2, 3, 4, 5]
        values  = [3, 4, 5, 6]
        capacity = 5

    We want to find the maximum possible value.

    The optimal solution is:

        Item with weight 2 and value 3
        Item with weight 3 and value 4

    Total:

        Weight = 5
        Value = 7

Why Dynamic Programming works:
    When considering an item, we have two choices:

        1. Do not take the item.
        2. Take the item if it fits.

    Therefore the optimal solution can be expressed as:

        dp[i][capacity] = max(
            dp[i - 1][capacity],
            value[i] + dp[i - 1][capacity - weight[i]]
        )

    The first option means that we do not take the item.

    The second option means that we take the item.

    By storing previous results, we avoid calculating the same
    subproblems repeatedly.

State:
    dp[i][w] represents the maximum value that can be obtained using
    the first i items with a maximum capacity of w.

Transition:
    If the current item does not fit:

        dp[i][w] = dp[i - 1][w]

    If the item fits:

        dp[i][w] = max(
            dp[i - 1][w],
            value + dp[i - 1][w - weight]
        )

Base case:
    If there are no items or the capacity is zero:

        dp[i][0] = 0
        dp[0][w] = 0

Complexity:
    Time:
        O(n * capacity)

    Space:
        O(n * capacity)

    where n is the number of items.

    The algorithm can be optimized to O(capacity) memory by using
    a one-dimensional DP array.

When to use Dynamic Programming:
    - Optimization problems.
    - Counting problems.
    - Path finding.
    - Resource allocation.
    - Scheduling.
    - String algorithms.
    - Financial optimization.
    - Inventory optimization.

Common Dynamic Programming problems:
    - 0/1 Knapsack.
    - Coin Change.
    - Longest Common Subsequence.
    - Longest Increasing Subsequence.
    - Edit Distance.
    - Matrix Chain Multiplication.
    - House Robber.
    - Minimum Path Sum.

Important concept:
    Dynamic Programming is not simply "using a cache".

    A problem is a good candidate for DP when it has:

        1. Overlapping subproblems.
        2. Optimal substructure.

    The most important part of solving a DP problem is identifying
    the correct state and transition.
"""
import random
import unittest


def knapsack(weights, values, capacity):
    if len(weights) != len(values):
        raise ValueError("Weights and values must have the same length")

    if capacity < 0:
        raise ValueError("Capacity cannot be negative")

    item_count = len(weights)

    dp = [
        [0] * (capacity + 1)
        for _ in range(item_count + 1)
    ]

    for i in range(1, item_count + 1):
        weight = weights[i - 1]
        value = values[i - 1]

        if weight < 0:
            raise ValueError("Weight cannot be negative")

        for current_capacity in range(capacity + 1):
            dp[i][current_capacity] = dp[i - 1][current_capacity]

            if weight <= current_capacity:
                dp[i][current_capacity] = max(
                    dp[i][current_capacity],
                    value + dp[i - 1][current_capacity - weight]
                )

    return dp[item_count][capacity]


class KnapsackTests(unittest.TestCase):

    def test_basic_case(self):
        weights = [2, 3, 4, 5]
        values = [3, 4, 5, 6]

        result = knapsack(weights, values, 5)

        self.assertEqual(result, 7)

    def test_empty_items(self):
        result = knapsack([], [], 10)

        self.assertEqual(result, 0)

    def test_zero_capacity(self):
        weights = [1, 2, 3]
        values = [10, 20, 30]

        result = knapsack(weights, values, 0)

        self.assertEqual(result, 0)

    def test_one_item_fits(self):
        result = knapsack([5], [100], 5)

        self.assertEqual(result, 100)

    def test_one_item_does_not_fit(self):
        result = knapsack([6], [100], 5)

        self.assertEqual(result, 0)

    def test_best_item_is_not_most_valuable(self):
        weights = [3, 4, 5]
        values = [4, 5, 10]

        result = knapsack(weights, values, 7)

        self.assertEqual(result, 10)

    def test_same_length_validation(self):
        with self.assertRaises(ValueError):
            knapsack([1, 2], [10], 5)

    def test_negative_capacity(self):
        with self.assertRaises(ValueError):
            knapsack([1], [10], -1)

    def test_negative_weight(self):
        with self.assertRaises(ValueError):
            knapsack([-1], [10], 5)


class KnapsackRandomTests(unittest.TestCase):

    def brute_force(self, weights, values, capacity):
        item_count = len(weights)
        best_value = 0

        for mask in range(1 << item_count):
            total_weight = 0
            total_value = 0

            for i in range(item_count):
                if mask & (1 << i):
                    total_weight += weights[i]
                    total_value += values[i]

            if total_weight <= capacity:
                best_value = max(
                    best_value,
                    total_value
                )

        return best_value

    def test_random_against_brute_force(self):
        for _ in range(500):
            item_count = random.randint(0, 12)

            weights = [
                random.randint(1, 20)
                for _ in range(item_count)
            ]

            values = [
                random.randint(1, 100)
                for _ in range(item_count)
            ]

            capacity = random.randint(0, 50)

            expected = self.brute_force(
                weights,
                values,
                capacity
            )

            result = knapsack(
                weights,
                values,
                capacity
            )

            self.assertEqual(result, expected)

    def test_random_zero_capacity(self):
        for _ in range(500):
            item_count = random.randint(0, 20)

            weights = [
                random.randint(1, 100)
                for _ in range(item_count)
            ]

            values = [
                random.randint(1, 1000)
                for _ in range(item_count)
            ]

            result = knapsack(
                weights,
                values,
                0
            )

            self.assertEqual(result, 0)

    def test_random_single_item(self):
        for _ in range(500):
            weight = random.randint(1, 100)
            value = random.randint(1, 1000)
            capacity = random.randint(0, 100)

            result = knapsack(
                [weight],
                [value],
                capacity
            )

            expected = value if weight <= capacity else 0

            self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
