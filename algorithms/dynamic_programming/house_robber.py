"""
Dynamic Programming - House Robber

Description:
    The House Robber problem is a classic Dynamic Programming problem
    based on making a sequence of optimal decisions.

    We are given a row of houses. Each house contains a certain amount
    of money.

    The goal is to determine the maximum amount of money that can be
    collected under one restriction:

        Two adjacent houses cannot both be robbed.

    For example:

        [2, 7, 9, 3, 1]

    The optimal solution is:

        2 + 9 + 1 = 12

    We cannot rob adjacent houses, so after choosing a house we must
    skip the next one.

Purpose:
    - Demonstrate Dynamic Programming with a one-dimensional state.
    - Solve optimization problems involving sequential decisions.
    - Show how a current decision depends on previous decisions.
    - Avoid evaluating the same combinations repeatedly.

Problem:
    At every house we have two choices:

        1. Rob the current house.
        2. Skip the current house.

    If we rob the current house, we cannot rob the previous house.

    Therefore, the best result at position i can be obtained by
    comparing two possibilities:

        Skip current house:
            dp[i - 1]

        Rob current house:
            dp[i - 2] + money[i]

    The recurrence is:

        dp[i] = max(
            dp[i - 1],
            dp[i - 2] + money[i]
        )

State:
    dp[i] represents the maximum amount of money that can be robbed
    from the first i + 1 houses.

Base cases:
    For the first house:

        dp[0] = money[0]

    For the first two houses:

        dp[1] = max(money[0], money[1])

    We choose the more valuable house because the two houses are
    adjacent and cannot both be robbed.

Complexity:
    Time:
        O(n)

    Space:
        O(n)

    The space complexity can be optimized to O(1), because each new
    state only depends on the previous two states.

Optimized approach:
    Instead of storing the entire dp array, we only need:

        previous_previous
        previous

    For every new house:

        current = max(
            previous,
            previous_previous + money
        )

    Then the variables are shifted forward.

When to use:
    - Sequential optimization.
    - Resource selection.
    - Scheduling with conflicts.
    - Choosing non-adjacent elements.
    - Problems involving "take or skip" decisions.

Advantages:
    - Linear time complexity.
    - Very simple state transition.
    - Can be optimized to constant memory.
    - Demonstrates a common Dynamic Programming pattern.

Disadvantages:
    - The recurrence depends on the problem's restrictions.
    - Small changes to the rules can require a different state.
    - The basic version only models a simple adjacency constraint.

Related problems:
    - House Robber II.
    - Maximum sum of non-adjacent elements.
    - Weighted scheduling.
    - Stock trading problems.
    - Resource allocation problems.

Important concept:
    A common Dynamic Programming pattern is:

        Take the current element
        OR
        Skip the current element.

    If taking the current element prevents taking the previous one,
    the state usually needs information about at least two previous
    positions.

    Recognizing this pattern is useful far beyond the House Robber
    problem.
"""
import random
import unittest


def house_robber(money):
    if any(amount < 0 for amount in money):
        raise ValueError("Money values cannot be negative")

    if not money:
        return 0

    if len(money) == 1:
        return money[0]

    dp = [0] * len(money)

    dp[0] = money[0]
    dp[1] = max(money[0], money[1])

    for i in range(2, len(money)):
        dp[i] = max(
            dp[i - 1],
            dp[i - 2] + money[i]
        )

    return dp[-1]


class HouseRobberTests(unittest.TestCase):

    def test_basic_case(self):
        money = [2, 7, 9, 3, 1]

        result = house_robber(money)

        self.assertEqual(result, 12)

    def test_empty_list(self):
        result = house_robber([])

        self.assertEqual(result, 0)

    def test_single_house(self):
        result = house_robber([100])

        self.assertEqual(result, 100)

    def test_two_houses(self):
        result = house_robber([5, 10])

        self.assertEqual(result, 10)

    def test_all_zeroes(self):
        result = house_robber([0, 0, 0, 0])

        self.assertEqual(result, 0)

    def test_three_houses(self):
        result = house_robber([5, 1, 5])

        self.assertEqual(result, 10)

    def test_larger_middle_value(self):
        result = house_robber([2, 10, 3, 1, 7])

        self.assertEqual(result, 17)

    def test_negative_money(self):
        with self.assertRaises(ValueError):
            house_robber([5, -1, 10])


class HouseRobberRandomTests(unittest.TestCase):

    def brute_force(self, money, index=0):
        if index >= len(money):
            return 0

        skip = self.brute_force(
            money,
            index + 1
        )

        rob = money[index] + self.brute_force(
            money,
            index + 2
        )

        return max(skip, rob)

    def create_random_houses(self):
        length = random.randint(0, 15)

        return [
            random.randint(0, 500)
            for _ in range(length)
        ]

    def test_random_against_brute_force(self):
        for _ in range(500):
            money = self.create_random_houses()

            expected = self.brute_force(money)
            result = house_robber(money)

            self.assertEqual(result, expected)

    def test_random_single_house(self):
        for _ in range(500):
            amount = random.randint(0, 1000)

            result = house_robber([amount])

            self.assertEqual(result, amount)

    def test_random_two_houses(self):
        for _ in range(500):
            first = random.randint(0, 1000)
            second = random.randint(0, 1000)

            result = house_robber([
                first,
                second
            ])

            self.assertEqual(
                result,
                max(first, second)
            )

    def test_random_three_houses(self):
        for _ in range(500):
            money = [
                random.randint(0, 1000)
                for _ in range(3)
            ]

            result = house_robber(money)

            expected = max(
                money[0] + money[2],
                money[1]
            )

            self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
