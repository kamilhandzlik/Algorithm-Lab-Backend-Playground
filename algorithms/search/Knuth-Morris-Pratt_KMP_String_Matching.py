"""
Problem: Knuth-Morris-Pratt (KMP) String Matching

Category:
- Algorithms
- String Algorithms
- Pattern Matching

Description:
This project implements the Knuth-Morris-Pratt (KMP)
string matching algorithm.

KMP efficiently searches for all occurrences of a pattern
within a text by avoiding unnecessary comparisons.

Instead of restarting from the beginning of the pattern
after a mismatch, KMP uses a precomputed Longest Prefix
Suffix (LPS) table to determine how far the pattern
can be shifted.

This algorithm is commonly used in:
- text editors
- search engines
- DNA sequence analysis
- plagiarism detection
- bioinformatics

Features:
- efficient pattern matching
- linear time complexity
- prefix table preprocessing
- multiple match detection

Time Complexity:
- Build LPS: O(m)
- Search: O(n)

Space Complexity:
- O(m)
"""

import random
import string
import unittest


def build_lps(pattern):
    lps = [0] * len(pattern)

    length = 0
    index = 1

    while index < len(pattern):

        if pattern[index] == pattern[length]:

            length += 1
            lps[index] = length
            index += 1

        elif length != 0:

            length = lps[length - 1]

        else:

            lps[index] = 0
            index += 1

    return lps


def kmp_search(text, pattern):
    if not pattern:
        return []

    lps = build_lps(pattern)

    result = []

    text_index = 0
    pattern_index = 0

    while text_index < len(text):

        if text[text_index] == pattern[pattern_index]:

            text_index += 1
            pattern_index += 1

            if pattern_index == len(pattern):
                result.append(
                    text_index - pattern_index
                )

                pattern_index = lps[pattern_index - 1]

        elif pattern_index != 0:

            pattern_index = lps[pattern_index - 1]

        else:

            text_index += 1

    return result


class TestKMP(unittest.TestCase):

    def test_single_match(self):
        self.assertEqual(
            kmp_search(
                "hello world", "world"), [6])

    def test_multiple_matches(self):
        self.assertEqual(
            kmp_search("abababab", "abab"), [0, 2, 4])

    def test_no_match(self):
        self.assertEqual(
            kmp_search("abcdef", "xyz"), [])

    def test_empty_pattern(self):
        self.assertEqual(
            kmp_search("abcdef", ""), [])


class TestRandom(unittest.TestCase):

    def test_random_strings(self):
        alphabet = string.ascii_lowercase

        for _ in range(100):
            text = "".join(random.choice(alphabet) for _ in range(100))

            start = random.randint(0, 90)

            pattern = text[start:start + 5]

            result = kmp_search(text, pattern)

            self.assertIn(start, result)


if __name__ == "__main__":
    unittest.main()
