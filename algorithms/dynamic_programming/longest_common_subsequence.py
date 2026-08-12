"""
Dynamic Programming - Longest Common Subsequence

Description:
    The Longest Common Subsequence (LCS) problem is a classic Dynamic
    Programming problem.

    Given two sequences, the goal is to find the longest sequence that
    appears in both inputs while preserving the relative order of
    elements.

    The elements do not need to be next to each other.

    For example:

        First sequence:
            ABCBDAB

        Second sequence:
            BDCAB

    One possible Longest Common Subsequence is:

        BCAB

    Its length is 4.

    LCS is different from Longest Common Substring.

    A substring must contain consecutive elements, while a subsequence
    only needs to preserve the order of elements.

Problem:
    Given two strings, find the length of their Longest Common
    Subsequence.

State:
    dp[i][j] represents the length of the longest common subsequence
    between the first i characters of the first string and the first j
    characters of the second string.

Transition:
    If the current characters are equal:

        dp[i][j] = dp[i - 1][j - 1] + 1

    If they are different:

        dp[i][j] = max(
            dp[i - 1][j],
            dp[i][j - 1]
        )

    The first option skips a character from the first string.

    The second option skips a character from the second string.

Base case:
    If either sequence is empty, the LCS length is zero.

        dp[0][j] = 0
        dp[i][0] = 0

Complexity:
    Time:
        O(n * m)

    Space:
        O(n * m)

    where n and m are the lengths of the two sequences.

Why Dynamic Programming works:
    The same prefixes of the two strings appear in many different
    recursive branches.

    Calculating those prefixes repeatedly would lead to exponential
    complexity.

    Dynamic Programming stores the result for every pair of prefixes
    and reuses those results.

When to use:
    - Comparing sequences.
    - Comparing versions of data.
    - DNA sequence analysis.
    - Diff algorithms.
    - Text comparison.
    - Pattern analysis.
    - Version control systems.

Related problems:
    - Longest Common Substring.
    - Edit Distance.
    - Longest Increasing Subsequence.
    - Shortest Common Supersequence.

Important concept:
    The key to solving LCS is identifying the correct state.

    Instead of asking:

        "What is the LCS of these two complete strings?"

    Dynamic Programming asks:

        "What is the LCS of the first i characters and the first j
        characters?"

    Once that state is defined, the transition becomes straightforward.
"""
import random
import string
import unittest


def longest_common_subsequence(first, second):
    rows = len(first)
    columns = len(second)

    dp = [
        [0] * (columns + 1)
        for _ in range(rows + 1)
    ]

    for i in range(1, rows + 1):
        for j in range(1, columns + 1):
            if first[i - 1] == second[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(
                    dp[i - 1][j],
                    dp[i][j - 1]
                )

    return dp[rows][columns]


class LongestCommonSubsequenceTests(unittest.TestCase):

    def test_basic_case(self):
        result = longest_common_subsequence(
            "ABCBDAB",
            "BDCAB"
        )

        self.assertEqual(result, 4)

    def test_identical_strings(self):
        result = longest_common_subsequence(
            "HELLO",
            "HELLO"
        )

        self.assertEqual(result, 5)

    def test_completely_different_strings(self):
        result = longest_common_subsequence(
            "ABC",
            "XYZ"
        )

        self.assertEqual(result, 0)

    def test_empty_first_string(self):
        result = longest_common_subsequence(
            "",
            "ABC"
        )

        self.assertEqual(result, 0)

    def test_empty_second_string(self):
        result = longest_common_subsequence(
            "ABC",
            ""
        )

        self.assertEqual(result, 0)

    def test_both_empty(self):
        result = longest_common_subsequence("", "")

        self.assertEqual(result, 0)

    def test_repeated_characters(self):
        result = longest_common_subsequence(
            "AAAA",
            "AA"
        )

        self.assertEqual(result, 2)

    def test_single_character_match(self):
        result = longest_common_subsequence(
            "ABC",
            "XBX"
        )

        self.assertEqual(result, 1)

    def test_single_character_mismatch(self):
        result = longest_common_subsequence(
            "A",
            "B"
        )

        self.assertEqual(result, 0)


class LongestCommonSubsequenceRandomTests(unittest.TestCase):

    def brute_force(self, first, second):
        best = 0
        length = len(first)

        for mask in range(1 << length):
            subsequence = []

            for i in range(length):
                if mask & (1 << i):
                    subsequence.append(first[i])

            candidate = "".join(subsequence)

            if len(candidate) <= best:
                continue

            if self.is_subsequence(candidate, second):
                best = len(candidate)

        return best

    def is_subsequence(self, candidate, sequence):
        position = 0

        for character in sequence:
            if position < len(candidate) and candidate[position] == character:
                position += 1

        return position == len(candidate)

    def random_string(self):
        length = random.randint(0, 10)

        return "".join(
            random.choice(string.ascii_lowercase)
            for _ in range(length)
        )

    def test_random_against_brute_force(self):
        for _ in range(500):
            first = self.random_string()
            second = self.random_string()

            expected = self.brute_force(
                first,
                second
            )

            result = longest_common_subsequence(
                first,
                second
            )

            self.assertEqual(result, expected)

    def test_random_identical_strings(self):
        for _ in range(500):
            value = self.random_string()

            result = longest_common_subsequence(
                value,
                value
            )

            self.assertEqual(
                result,
                len(value)
            )

    def test_random_reversed_strings(self):
        for _ in range(500):
            value = self.random_string()
            reversed_value = value[::-1]

            result = longest_common_subsequence(
                value,
                reversed_value
            )

            self.assertGreaterEqual(result, 0)
            self.assertLessEqual(result, len(value))

    def test_random_empty_strings(self):
        for _ in range(500):
            value = self.random_string()

            result = longest_common_subsequence(
                "",
                value
            )

            self.assertEqual(result, 0)


if __name__ == "__main__":
    unittest.main()
