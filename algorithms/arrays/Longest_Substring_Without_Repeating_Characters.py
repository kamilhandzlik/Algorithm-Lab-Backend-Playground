"""
Problem: Longest Substring Without Repeating Characters
Difficulty: Medium
Category: Sliding Window

Time Complexity: O(n)
Space Complexity: O(n)
"""


def longest_substring(s):
    char_set = set()
    left = 0
    max_length = 0

    for right in range(len(s)):
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1

        char_set.add(s[right])
        max_length = max(max_length, right - left + 1)

    return max_length


import unittest


class TestLongestSubstring(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(longest_substring("abcabcbb"), 3)

    def test_all_same(self):
        self.assertEqual(longest_substring("bbbbb"), 1)

    def test_mixed(self):
        self.assertEqual(longest_substring("pwwkew"), 3)

    def test_empty(self):
        self.assertEqual(longest_substring(""), 0)

    def test_single(self):
        self.assertEqual(longest_substring("a"), 1)


import random
import string


def brute_longest_substring(s):
    max_len = 0

    for i in range(len(s)):
        seen = set()
        for j in range(i, len(s)):
            if s[j] in seen:
                break
            seen.add(s[j])
            max_len = max(max_len, j - i + 1)

    return max_len


class TestRandom(unittest.TestCase):

    def test_random_strings(self):
        for _ in range(100):
            length = random.randint(0, 10)
            s = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

            self.assertEqual(
                longest_substring(s),
                brute_longest_substring(s)
            )
