"""
Dynamic Programming - Coin Change

Description:
    The Coin Change problem is a classic Dynamic Programming problem.

    Given a collection of coin denominations and a target amount,
    the goal is to determine the minimum number of coins required
    to create that amount.

    Each coin can be used any number of times.

    For example:

        coins = [1, 5, 10, 25]
        amount = 30

    The optimal solution is:

        25 + 5

    Therefore the answer is 2 coins.

Purpose:
    - Find an optimal combination of reusable elements.
    - Demonstrate Dynamic Programming.
    - Avoid solving the same subproblem repeatedly.
    - Find the minimum number of operations needed to reach a target.

Problem:
    A naive recursive solution would try every possible combination
    of coins.

    This creates many repeated calculations.

    For example, when calculating the minimum number of coins for
    amount 30, the algorithm may repeatedly need to calculate the
    answer for amount 25, amount 20, amount 15, and so on.

    Dynamic Programming stores these results and reuses them.

State:
    dp[amount] represents the minimum number of coins required
    to create the given amount.

Base case:

    dp[0] = 0

    No coins are required to create an amount of zero.

Transition:
    For every amount, try every available coin.

    If the coin can be used:

        dp[amount] = min(
            dp[amount],
            dp[amount - coin] + 1
        )

    The +1 represents the coin that we have just added.

Example:

    coins = [1, 3, 4]
    amount = 6

    The optimal solution is:

        3 + 3

    Therefore:

        dp[6] = 2

    A greedy algorithm might choose:

        4 + 1 + 1

    which uses 3 coins.

    This demonstrates why a greedy approach does not always produce
    the optimal solution.

Base case:
    dp[0] = 0

    Every other value initially represents an unreachable amount.

Complexity:
    Time:
        O(amount * number_of_coins)

    Space:
        O(amount)

When to use:
    - Optimization problems.
    - Resource allocation.
    - Minimum-cost problems.
    - Scheduling.
    - Currency and denomination problems.
    - Problems where the same smaller states appear repeatedly.

Advantages:
    - Finds the optimal solution.
    - Avoids repeated calculations.
    - Simple state representation.
    - Can be implemented iteratively.

Disadvantages:
    - Can require significant memory for very large targets.
    - Not every optimization problem can be solved efficiently
      with Dynamic Programming.
    - The correct state and transition must be identified first.

Important concept:
    Dynamic Programming works by building the solution from smaller
    subproblems.

    Instead of asking:

        "How do I make the target amount?"

    we ask:

        "What is the minimum number of coins needed for every smaller
        amount?"

    Once those answers are known, the solution for the target can
    be constructed from them.
"""
import random
import unittest


def coin_change(coins, amount):
    if amount < 0:
        raise ValueError("Amount cannot be negative")

    if any(coin <= 0 for coin in coins):
        raise ValueError("Coins must be greater than zero")

    dp = [float("inf")] * (amount + 1)
    dp[0] = 0

    for current_amount in range(1, amount + 1):
        for coin in coins:
            if coin <= current_amount:
                dp[current_amount] = min(
                    dp[current_amount],
                    dp[current_amount - coin] + 1
                )

    if dp[amount] == float("inf"):
        return -1

    return dp[amount]


class CoinChangeTests(unittest.TestCase):

    def test_basic_case(self):
        result = coin_change([1, 5, 10, 25], 30)

        self.assertEqual(result, 2)

    def test_dynamic_programming_beats_greedy(self):
        result = coin_change([1, 3, 4], 6)

        self.assertEqual(result, 2)

    def test_zero_amount(self):
        result = coin_change([1, 2, 5], 0)

        self.assertEqual(result, 0)

    def test_single_coin(self):
        result = coin_change([5], 15)

        self.assertEqual(result, 3)

    def test_impossible_amount(self):
        result = coin_change([2], 3)

        self.assertEqual(result, -1)

    def test_exact_coin(self):
        result = coin_change([1, 5, 10], 10)

        self.assertEqual(result, 1)

    def test_duplicate_coins(self):
        result = coin_change([1, 1, 5, 5], 10)

        self.assertEqual(result, 2)

    def test_negative_amount(self):
        with self.assertRaises(ValueError):
            coin_change([1, 2, 5], -1)

    def test_zero_coin(self):
        with self.assertRaises(ValueError):
            coin_change([0, 1, 2], 10)

    def test_negative_coin(self):
        with self.assertRaises(ValueError):
            coin_change([1, -2, 5], 10)


class CoinChangeRandomTests(unittest.TestCase):

    def brute_force(self, coins, amount):
        if amount == 0:
            return 0

        best = float("inf")

        for coin in coins:
            if coin > amount:
                continue

            result = self.brute_force(
                coins,
                amount - coin
            )

            if result != -1:
                best = min(best, result + 1)

        if best == float("inf"):
            return -1

        return best

    def test_random_against_brute_force(self):
        for _ in range(500):
            coin_count = random.randint(1, 5)

            coins = random.sample(
                range(1, 10),
                coin_count
            )

            amount = random.randint(0, 30)

            expected = self.brute_force(
                coins,
                amount
            )

            result = coin_change(
                coins,
                amount
            )

            self.assertEqual(result, expected)

    def test_random_zero_amount(self):
        for _ in range(500):
            coins = random.sample(
                range(1, 20),
                random.randint(1, 10)
            )

            result = coin_change(coins, 0)

            self.assertEqual(result, 0)

    def test_random_single_coin(self):
        for _ in range(500):
            coin = random.randint(1, 20)
            multiplier = random.randint(0, 20)

            amount = coin * multiplier

            result = coin_change(
                [coin],
                amount
            )

            self.assertEqual(result, multiplier)

    def test_random_result_is_valid(self):
        for _ in range(500):
            coins = random.sample(
                range(1, 15),
                random.randint(1, 6)
            )

            amount = random.randint(0, 50)

            result = coin_change(
                coins,
                amount
            )

            if result != -1:
                self.assertGreaterEqual(result, 0)

            if amount == 0:
                self.assertEqual(result, 0)


if __name__ == "__main__":
    unittest.main()
