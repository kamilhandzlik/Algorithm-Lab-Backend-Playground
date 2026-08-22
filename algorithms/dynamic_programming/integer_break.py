"""
Dynamic Programming - Integer Break

Description:
    The Integer Break problem asks us to split a positive integer n
    into at least two positive integers so that the product of those
    integers is as large as possible.

    For example:

        n = 10

    One possible partition is:

        10 = 3 + 3 + 4

    Its product is:

        3 * 3 * 4 = 36

    The maximum possible product is therefore 36.

Purpose:
    - Solve a mathematical optimization problem using Dynamic Programming.
    - Demonstrate how a mathematical problem can be expressed as a
      collection of smaller subproblems.
    - Find the maximum product obtainable by splitting an integer.
    - Demonstrate optimal substructure.

Problem:
    For every integer n, we can choose a first part k and leave the
    remaining value:

        n - k

    The remaining value can either be left as a single number or
    broken into smaller parts.

    Therefore, for every possible k we consider:

        k * (n - k)

    and:

        k * dp[n - k]

    The first expression means that we stop splitting the remaining
    value.

    The second expression means that we continue splitting the
    remaining value optimally.

State:
    dp[n] represents the maximum product obtainable by breaking n
    into at least two positive integers.

Base case:
    The smallest useful value is:

        dp[2] = 1

    because:

        2 = 1 + 1

    and:

        1 * 1 = 1

Transition:
    For every possible first part k:

        dp[n] = max(
            dp[n],
            k * (n - k),
            k * dp[n - k]
        )

    We compare both possibilities because the remaining part may
    produce a better result when it is split further.

Example:

    n = 10

    One optimal solution is:

        10 = 3 + 3 + 4

    giving:

        3 * 3 * 4 = 36

Complexity:
    Time:
        O(n^2)

    Space:
        O(n)

    The algorithm considers every possible split for every value
    from 2 to n.

Mathematical observation:
    There is also a mathematical solution based on the fact that
    splitting an integer into parts close to 3 tends to maximize
    the product.

    However, the Dynamic Programming solution is useful because it
    demonstrates a general optimization technique without relying
    on that mathematical theorem.

When to use:
    - Mathematical optimization.
    - Integer partition problems.
    - Problems involving optimal decomposition.
    - Learning Dynamic Programming.
    - Problems where a value can be recursively divided into smaller
      independent parts.

Advantages:
    - Straightforward recurrence.
    - Easy to verify.
    - Does not require a specialized mathematical formula.
    - Demonstrates optimal substructure clearly.

Disadvantages:
    - O(n^2) time complexity.
    - Less efficient than the mathematical O(1) approach.
    - The DP table grows linearly with n.

Important concept:
    The key question is:

        "If I make the first split here, what is the best possible
        result for the remaining value?"

    This transforms one large mathematical problem into many smaller
    optimization problems.

    This is a useful pattern whenever a mathematical object can be
    recursively decomposed into smaller objects.
"""
import random
import unittest


def integer_break(number):
    if number < 2:
        raise ValueError("Number must be at least 2")

    if number == 2:
        return 1

    dp = [0] * (number + 1)

    dp[2] = 1

    for current in range(3, number + 1):
        for first_part in range(1, current):
            remaining = current - first_part

            dp[current] = max(
                dp[current],
                first_part * remaining,
                first_part * dp[remaining]
            )

    return dp[number]


def integer_break_formula(number):
    if number < 2:
        raise ValueError("Number must be at least 2")

    if number == 2:
        return 1

    if number == 3:
        return 2

    remainder = number % 3

    if remainder == 0:
        return 3 ** (number // 3)

    if remainder == 1:
        return 4 * 3 ** ((number - 4) // 3)

    return 2 * 3 ** (number // 3)


class IntegerBreakTests(unittest.TestCase):
    def test_two(self):
        result = integer_break(2)
        self.assertEqual(result, 1)

    def test_three(self):
        result = integer_break(3)
        self.assertEqual(result, 2)

    def test_four(self):
        result = integer_break(4)
        self.assertEqual(result, 4)

    def test_five(self):
        result = integer_break(5)
        self.assertEqual(result, 6)

    def test_ten(self):
        result = integer_break(10)
        self.assertEqual(result, 36)

    def test_eighteen(self):
        result = integer_break(18)
        self.assertEqual(result, 729)

    def test_invalid_number(self):
        with self.assertRaises(ValueError):
            integer_break(1)

    def test_negative_number(self):
        with self.assertRaises(ValueError):
            integer_break(-5)


class IntegerBreakRandomTests(unittest.TestCase):
    def test_random_against_mathematical_formula(self):
        for _ in range(500):
            number = random.randint(2, 100)
            expected = integer_break_formula(number)
            result = integer_break(number)
            self.assertEqual(result, expected)

    def test_random_small_values(self):
        for _ in range(500):
            number = random.randint(2, 20)
            result = integer_break(number)
            expected = integer_break_formula(number)
            self.assertEqual(result, expected)

    def test_random_values_divisible_by_three(self):
        for _ in range(500):
            number = random.randint(1, 30) * 3
            result = integer_break(number)
            expected = 3 ** (number // 3)
            self.assertEqual(result, expected)

    def test_random_values_with_remainder_one(self):
        for _ in range(500):
            number = random.randint(1, 30) * 3 + 1
            if number < 4:
                continue
            result = integer_break(number)
            expected = 4 * 3 ** ((number - 4) // 3)
            self.assertEqual(result, expected)

    def test_random_values_with_remainder_two(self):
        for _ in range(500):
            number = random.randint(1, 30) * 3 + 2
            result = integer_break(number)
            expected = 2 * 3 ** (number // 3)
            self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
