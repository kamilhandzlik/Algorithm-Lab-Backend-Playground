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