"""
Problem: Longest Increasing Subsequence (LIS) — zwróć sekwencję
Difficulty: Hard
Category: Arrays / Dynamic Programming / Binary Search

Time Complexity: O(n log n)
Space Complexity: O(n)
"""


def longest_increasing_subsequence(arr):
    if not arr:
        return []

    from bisect import bisect_left

    tails = []
    prev = [-1] * len(arr)

    for i, val in enumerate(arr):
        pos = bisect_left([arr[t] for t in tails], val)

        if pos == len(tails):
            tails.append(i)
        else:
            tails[pos] = i

        if pos > 0:
            prev[i] = tails[pos - 1]

    lis = []
    k = tails[-1]
    while k != -1:
        lis.append(arr[k])
        k = prev[k]

    return lis[::-1]


import unittest


class TestLIS(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(
            longest_increasing_subsequence([3, 4, -1, 0, 6, 2, 3]),
            [-1, 0, 2, 3]
        )
        self.assertEqual(
            longest_increasing_subsequence([10, 9, 2, 5, 3, 7, 101, 18]),
            [2, 3, 7, 18]
        )

    def test_edge_cases(self):
        self.assertEqual(longest_increasing_subsequence([]), [])
        self.assertEqual(longest_increasing_subsequence([5]), [5])
        self.assertEqual(longest_increasing_subsequence([5, 5, 5]), [5])

    def test_strict_increasing(self):
        self.assertEqual(
            longest_increasing_subsequence([1, 2, 3, 4, 5]),
            [1, 2, 3, 4, 5]
        )

    def test_strict_decreasing(self):
        self.assertEqual(
            longest_increasing_subsequence([5, 4, 3, 2, 1]),
            [1]
        )
