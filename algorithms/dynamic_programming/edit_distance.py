"""
Dynamic Programming - Edit Distance

Description:
    Edit Distance, also known as Levenshtein Distance, is a classic
    Dynamic Programming problem.

    The goal is to determine the minimum number of operations required
    to transform one string into another.

    Three operations are allowed:

        - Insertion of a character.
        - Deletion of a character.
        - Substitution of one character with another.

    For example:

        "cat" -> "cut"

    requires one substitution:

        a -> u

    Therefore the edit distance is 1.

Purpose:
    - Compare strings.
    - Measure similarity between text values.
    - Detect spelling differences.
    - Implement fuzzy search.
    - Support autocomplete systems.
    - Compare versions of text.
    - Build typo-tolerant search systems.

Problem:
    A naive recursive implementation repeatedly solves the same
    subproblems.

    For two strings of length n and m, this can result in exponential
    time complexity.

    Dynamic Programming stores the result for every pair of prefixes,
    avoiding repeated calculations.

State:
    dp[i][j] represents the minimum number of operations required
    to transform the first i characters of the first string into
    the first j characters of the second string.

Base cases:

    dp[i][0] = i

    Transforming a string of length i into an empty string requires
    deleting all i characters.

    dp[0][j] = j

    Transforming an empty string into a string of length j requires
    inserting all j characters.

Transition:
    If the current characters are equal:

        dp[i][j] = dp[i - 1][j - 1]

    No operation is required.

    If the characters are different, we choose the cheapest operation:

        Insertion:
            dp[i][j - 1] + 1

        Deletion:
            dp[i - 1][j] + 1

        Substitution:
            dp[i - 1][j - 1] + 1

    Therefore:

        dp[i][j] = min(
            dp[i][j - 1] + 1,
            dp[i - 1][j] + 1,
            dp[i - 1][j - 1] + 1
        )

Complexity:
    Time:
        O(n * m)

    Space:
        O(n * m)

    where n and m are the lengths of the two strings.

When to use:
    - Fuzzy search.
    - Spell checking.
    - Autocomplete.
    - Duplicate detection.
    - Text comparison.
    - Data cleaning.
    - Matching user input against known values.

Advantages:
    - Produces the optimal edit distance.
    - Relatively simple state representation.
    - Works with arbitrary strings.
    - Useful in many real-world text-processing systems.

Disadvantages:
    - O(n * m) complexity can become expensive for very long strings.
    - It calculates a full matrix even when only the distance is needed.
    - Specialized algorithms may be preferable for very large datasets.

Common backend usage:
    - Search engines.
    - User input validation.
    - Product search.
    - Name matching.
    - Address matching.
    - Spell correction.
    - Duplicate record detection.

Important concept:
    The important part of this problem is not the matrix itself.

    The important part is recognizing that every solution can be
    reduced to smaller prefixes of the two strings.

    Once dp[i][j] is defined, every state depends only on previously
    calculated states.
"""
import random
import string
import unittest


def edit_distance(first, second):
    rows = len(first)
    columns = len(second)

    dp = [
        [0] * (columns + 1)
        for _ in range(rows + 1)
    ]

    for i in range(rows + 1):
        dp[i][0] = i

    for j in range(columns + 1):
        dp[0][j] = j

    for i in range(1, rows + 1):
        for j in range(1, columns + 1):
            if first[i - 1] == second[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                insertion = dp[i][j - 1] + 1
                deletion = dp[i - 1][j] + 1
                substitution = dp[i - 1][j - 1] + 1

                dp[i][j] = min(
                    insertion,
                    deletion,
                    substitution
                )

    return dp[rows][columns]


class EditDistanceTests(unittest.TestCase):

    def test_identical_strings(self):
        result = edit_distance("hello", "hello")

        self.assertEqual(result, 0)

    def test_single_substitution(self):
        result = edit_distance("cat", "cut")

        self.assertEqual(result, 1)

    def test_single_insertion(self):
        result = edit_distance("cat", "cats")

        self.assertEqual(result, 1)

    def test_single_deletion(self):
        result = edit_distance("cats", "cat")

        self.assertEqual(result, 1)

    def test_empty_first_string(self):
        result = edit_distance("", "hello")

        self.assertEqual(result, 5)

    def test_empty_second_string(self):
        result = edit_distance("hello", "")

        self.assertEqual(result, 5)

    def test_both_empty(self):
        result = edit_distance("", "")

        self.assertEqual(result, 0)

    def test_completely_different_strings(self):
        result = edit_distance("abc", "xyz")

        self.assertEqual(result, 3)

    def test_classic_example(self):
        result = edit_distance("kitten", "sitting")

        self.assertEqual(result, 3)

    def test_repeated_characters(self):
        result = edit_distance("aaaa", "aa")

        self.assertEqual(result, 2)


class EditDistanceRandomTests(unittest.TestCase):

    def brute_force(self, first, second):
        if not first:
            return len(second)

        if not second:
            return len(first)

        if first[0] == second[0]:
            return self.brute_force(
                first[1:],
                second[1:]
            )

        insertion = self.brute_force(
            first,
            second[1:]
        )

        deletion = self.brute_force(
            first[1:],
            second
        )

        substitution = self.brute_force(
            first[1:],
            second[1:]
        )

        return 1 + min(
            insertion,
            deletion,
            substitution
        )

    def random_string(self):
        length = random.randint(0, 7)

        return "".join(
            random.choice("abc")
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

            result = edit_distance(
                first,
                second
            )

            self.assertEqual(result, expected)

    def test_random_identical_strings(self):
        for _ in range(500):
            value = self.random_string()

            result = edit_distance(
                value,
                value
            )

            self.assertEqual(result, 0)

    def test_random_empty_first_string(self):
        for _ in range(500):
            value = self.random_string()

            result = edit_distance(
                "",
                value
            )

            self.assertEqual(result, len(value))

    def test_random_empty_second_string(self):
        for _ in range(500):
            value = self.random_string()

            result = edit_distance(
                value,
                ""
            )

            self.assertEqual(result, len(value))


if __name__ == "__main__":
    unittest.main()
