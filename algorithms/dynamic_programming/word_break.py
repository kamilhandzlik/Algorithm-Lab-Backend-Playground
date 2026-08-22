"""
Dynamic Programming - Word Break

Description:
    The Word Break problem asks whether a given string can be
    completely constructed by concatenating words from a provided
    dictionary.

    Every dictionary word may be used multiple times.

    For example:

        text = "leetcode"

        dictionary = ["leet", "code"]

    The string can be split into:

        "leet" + "code"

    Therefore the result is True.

    Another example:

        text = "catsandog"

        dictionary = ["cats", "dog", "sand", "and", "cat"]

    There is no valid way to construct the complete string, so the
    result is False.

Purpose:
    - Determine whether a string can be segmented into valid words.
    - Demonstrate Dynamic Programming over string prefixes.
    - Avoid repeatedly solving the same substring problems.
    - Model problems where a solution is built from smaller valid parts.

Problem:
    A naive recursive implementation could try every possible place
    where the string can be split.

    For example:

        "applepenapple"

    could be split in many different ways.

    Many of the resulting suffixes are identical, which means a
    naive recursive implementation repeatedly solves the same
    subproblems.

    Dynamic Programming stores whether every prefix can be constructed.

State:
    dp[i] represents whether the first i characters of the string
    can be completely constructed using dictionary words.

    In other words:

        dp[i] = True

    means that:

        text[:i]

    can be segmented into valid dictionary words.

Base case:
    dp[0] = True

    An empty string can be constructed using zero words.

Transition:
    For every position i, we check whether there is a previous
    position j such that:

        dp[j] == True

    and:

        text[j:i]

    exists in the dictionary.

    If both conditions are satisfied:

        dp[i] = True

    This means that the prefix ending at i can be constructed by
    taking an already valid prefix and appending one dictionary word.

Example:

    text = "leetcode"

    dictionary = {"leet", "code"}

    When processing "leet":

        dp[4] = True

    Later, "code" starts at position 4.

    Because:

        dp[4] == True

    and:

        "code" is in the dictionary,

    we can set:

        dp[8] = True

Complexity:
    Time:
        O(n^2)

    Space:
        O(n)

    where n is the length of the input string.

    The exact practical performance can also depend on the number
    and length of words in the dictionary.

When to use:
    - Text segmentation.
    - Tokenization.
    - Dictionary-based validation.
    - Natural language processing.
    - Autocomplete systems.
    - Input parsing.
    - URL or identifier parsing.
    - Problems involving valid prefixes.

Advantages:
    - Simple state representation.
    - Efficient compared with exploring every possible split.
    - Easy to test.
    - Works naturally with reusable dictionary entries.

Disadvantages:
    - The basic O(n^2) implementation can become expensive for
      very long strings.
    - Large dictionaries may require additional optimizations.
    - The basic algorithm only answers whether segmentation is
      possible; it does not return the actual words.

Important concept:
    The key question is not:

        "Can I split the entire string?"

    Instead, ask:

        "Can I construct every prefix of the string?"

    Once a prefix is known to be valid, it becomes a building block
    for solving the rest of the problem.

    This is another common Dynamic Programming pattern:

        Valid previous state
            +
        Valid transition
            =
        Valid current state
"""
import random
import unittest


def word_break(text, dictionary):
    dictionary = set(dictionary)

    dp = [False] * (len(text) + 1)
    dp[0] = True

    for end in range(1, len(text) + 1):
        for start in range(end):
            if not dp[start]:
                continue

            word = text[start:end]

            if word in dictionary:
                dp[end] = True
                break

    return dp[len(text)]


class WordBreakTests(unittest.TestCase):

    def test_basic_case(self):
        result = word_break(
            "leetcode",
            ["leet", "code"]
        )

        self.assertTrue(result)

    def test_multiple_words(self):
        result = word_break(
            "applepenapple",
            ["apple", "pen"]
        )

        self.assertTrue(result)

    def test_impossible_segmentation(self):
        result = word_break(
            "catsandog",
            ["cats", "dog", "sand", "and", "cat"]
        )

        self.assertFalse(result)

    def test_empty_string(self):
        result = word_break(
            "",
            ["cat", "dog"]
        )

        self.assertTrue(result)

    def test_single_word(self):
        result = word_break(
            "python",
            ["python"]
        )

        self.assertTrue(result)

    def test_word_not_in_dictionary(self):
        result = word_break(
            "python",
            ["java", "ruby"]
        )

        self.assertFalse(result)

    def test_word_can_be_reused(self):
        result = word_break(
            "aaaaaa",
            ["aa"]
        )

        self.assertTrue(result)

    def test_single_character_words(self):
        result = word_break(
            "abc",
            ["a", "b", "c"]
        )

        self.assertTrue(result)

    def test_overlapping_words(self):
        result = word_break(
            "cars",
            ["car", "ca", "rs"]
        )

        self.assertTrue(result)

    def test_empty_dictionary(self):
        result = word_break(
            "hello",
            []
        )

        self.assertFalse(result)


class WordBreakRandomTests(unittest.TestCase):

    def brute_force(self, text, dictionary):
        dictionary = set(dictionary)
        memo = {}

        def solve(start):
            if start == len(text):
                return True

            if start in memo:
                return memo[start]

            for end in range(start + 1, len(text) + 1):
                word = text[start:end]

                if word not in dictionary:
                    continue

                if solve(end):
                    memo[start] = True
                    return True

            memo[start] = False

            return False

        return solve(0)

    def random_word(self):
        length = random.randint(1, 4)

        return "".join(
            random.choice("abc")
            for _ in range(length)
        )

    def random_text(self):
        length = random.randint(0, 12)

        return "".join(
            random.choice("abc")
            for _ in range(length)
        )

    def random_dictionary(self):
        dictionary = set()

        for _ in range(random.randint(0, 10)):
            dictionary.add(
                self.random_word()
            )

        return list(dictionary)

    def test_random_against_brute_force(self):
        for _ in range(500):
            text = self.random_text()
            dictionary = self.random_dictionary()

            expected = self.brute_force(
                text,
                dictionary
            )

            result = word_break(
                text,
                dictionary
            )

            self.assertEqual(result, expected)

    def test_random_empty_text(self):
        for _ in range(500):
            dictionary = self.random_dictionary()

            result = word_break(
                "",
                dictionary
            )

            self.assertTrue(result)

    def test_random_single_word(self):
        for _ in range(500):
            word = self.random_word()

            result = word_break(
                word,
                [word]
            )

            self.assertTrue(result)

    def test_random_repeated_word(self):
        for _ in range(500):
            word = self.random_word()
            repetitions = random.randint(1, 8)

            text = word * repetitions

            result = word_break(
                text,
                [word]
            )

            self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
