"""
Dynamic Programming - Longest Increasing Subsequence

Description:
    The Longest Increasing Subsequence (LIS) problem asks us to find
    the longest subsequence of a sequence whose elements are strictly
    increasing.

    A subsequence does not need to contain consecutive elements.
    However, the original order of the selected elements must be
    preserved.

    For example:

        [10, 9, 2, 5, 3, 7, 101, 18]

    One Longest Increasing Subsequence is:

        [2, 3, 7, 101]

    Therefore the answer is 4.

    Another valid solution is:

        [2, 5, 7, 101]

    The exact subsequence does not matter when the function only
    returns its length.

Purpose:
    - Find the longest increasing sequence of values.
    - Demonstrate Dynamic Programming.
    - Identify optimal subsequences.
    - Solve ordering and sequence optimization problems.

Problem:
    A naive approach would try every possible subsequence.

    For a sequence containing n elements, there can be up to 2^n
    different subsequences.

    Dynamic Programming avoids checking all of them explicitly.

State:
    dp[i] represents the length of the longest increasing subsequence
    that ends at index i.

    Every element starts as a subsequence of length 1.

Transition:
    For every element i, check all previous elements j.

    If:

        numbers[j] < numbers[i]

    then numbers[i] can be appended to the increasing subsequence
    ending at j.

    Therefore:

        dp[i] = max(
            dp[i],
            dp[j] + 1
        )

    The final answer is the largest value in dp.

Base case:
    Every individual element forms an increasing subsequence of length 1.

    Therefore:

        dp[i] = 1

    for every valid index.

Complexity:
    Time:
        O(n^2)

    Space:
        O(n)

    There is also an O(n log n) solution using binary search, but
    the O(n^2) Dynamic Programming solution is easier to understand
    and is useful for learning the underlying DP concept.

When to use:
    - Sequence analysis.
    - Scheduling.
    - Ranking systems.
    - Time-series analysis.
    - Version comparison.
    - Optimization problems.
    - Problems involving ordered selections.

Advantages:
    - Simple state definition.
    - Easy to understand.
    - Easy to test.
    - Demonstrates optimal substructure clearly.

Disadvantages:
    - O(n^2) time complexity.
    - Can become slow for very large sequences.
    - The optimized O(n log n) solution is preferable for large inputs.

Important concept:
    The key question is:

        "What is the best increasing subsequence that ends at
        this particular element?"

    Once this is known for every element, the global solution is simply
    the largest of those values.

    This is an important Dynamic Programming technique:

        Define the state relative to the position of an element.

    Instead of solving the entire problem at once, solve the best
    possible problem ending at every position.
"""
import random
import unittest


def longest_increasing_subsequence(numbers):
    if not numbers:
        return 0

    dp = [1] * len(numbers)

    for i in range(len(numbers)):
        for j in range(i):
            if numbers[j] < numbers[i]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)


class LongestIncreasingSubsequenceTests(unittest.TestCase):

    def test_basic_case(self):
        numbers = [10, 9, 2, 5, 3, 7, 101, 18]

        result = longest_increasing_subsequence(numbers)

        self.assertEqual(result, 4)

    def test_empty_list(self):
        result = longest_increasing_subsequence([])

        self.assertEqual(result, 0)

    def test_single_element(self):
        result = longest_increasing_subsequence([10])

        self.assertEqual(result, 1)

    def test_already_increasing(self):
        numbers = [1, 2, 3, 4, 5]

        result = longest_increasing_subsequence(numbers)

        self.assertEqual(result, 5)

    def test_decreasing_sequence(self):
        numbers = [5, 4, 3, 2, 1]

        result = longest_increasing_subsequence(numbers)

        self.assertEqual(result, 1)

    def test_duplicate_values(self):
        numbers = [2, 2, 2, 2]

        result = longest_increasing_subsequence(numbers)

        self.assertEqual(result, 1)

    def test_mixed_values(self):
        numbers = [3, 1, 8, 2, 5]

        result = longest_increasing_subsequence(numbers)

        self.assertEqual(result, 3)

    def test_negative_numbers(self):
        numbers = [-5, -1, -3, 0, 2]

        result = longest_increasing_subsequence(numbers)

        self.assertEqual(result, 4)


class LongestIncreasingSubsequenceRandomTests(unittest.TestCase):

    def brute_force(self, numbers):
        best = 0
        length = len(numbers)

        for mask in range(1 << length):
            subsequence = []

            for i in range(length):
                if mask & (1 << i):
                    subsequence.append(numbers[i])

            if self.is_increasing(subsequence):
                best = max(best, len(subsequence))

        return best

    def is_increasing(self, numbers):
        for i in range(1, len(numbers)):
            if numbers[i - 1] >= numbers[i]:
                return False

        return True

    def test_random_against_brute_force(self):
        for _ in range(500):
            length = random.randint(0, 12)

            numbers = [
                random.randint(-20, 20)
                for _ in range(length)
            ]

            expected = self.brute_force(numbers)
            result = longest_increasing_subsequence(numbers)

            self.assertEqual(result, expected)

    def test_random_sorted_sequences(self):
        for _ in range(500):
            length = random.randint(0, 30)

            numbers = sorted(
                random.randint(-100, 100)
                for _ in range(length)
            )

            unique_numbers = list(dict.fromkeys(numbers))

            result = longest_increasing_subsequence(
                unique_numbers
            )

            self.assertEqual(
                result,
                len(unique_numbers)
            )

    def test_random_decreasing_sequences(self):
        for _ in range(500):
            length = random.randint(0, 30)

            numbers = sorted(
                [
                    random.randint(-100, 100)
                    for _ in range(length)
                ],
                reverse=True
            )

            result = longest_increasing_subsequence(numbers)

            if numbers:
                self.assertEqual(result, 1)
            else:
                self.assertEqual(result, 0)

    def test_random_single_element(self):
        for _ in range(500):
            number = random.randint(-1000, 1000)

            result = longest_increasing_subsequence(
                [number]
            )

            self.assertEqual(result, 1)


if __name__ == "__main__":
    unittest.main()
