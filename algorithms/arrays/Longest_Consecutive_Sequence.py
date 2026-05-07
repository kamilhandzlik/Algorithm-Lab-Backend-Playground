"""
Problem: Longest Consecutive Sequence
Difficulty: Medium
Category: Arrays / HashSet

Time Complexity: O(n)
Space Complexity: O(n)

"""
import unittest
import random


def longest_consecutive(nums):
    num_set = set(nums)
    longest = 0

    for num in num_set:

        if num - 1 not in num_set:

            current = num
            length = 1

            while current + 1 in num_set:
                current += 1
                length += 1

            longest = max(longest, length)

    return longest


class TestLongestConsecutive(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(
            longest_consecutive([100, 4, 200, 1, 3, 2]),
            4
        )

    def test_empty(self):
        self.assertEqual(
            longest_consecutive([]),
            0
        )

    def test_single(self):
        self.assertEqual(
            longest_consecutive([7]),
            1
        )

    def test_duplicates(self):
        self.assertEqual(
            longest_consecutive([1, 2, 2, 3]),
            3
        )

    def test_negative(self):
        self.assertEqual(
            longest_consecutive([-1, 0, 1, 2]),
            4
        )


def brute_longest_consecutive(nums):
    nums = sorted(set(nums))

    if not nums:
        return 0

    longest = 1
    current = 1

    for i in range(1, len(nums)):
        if nums[i] == nums[i - 1] + 1:
            current += 1
        else:
            longest = max(longest, current)
            current = 1

    return max(longest, current)


class TestRandom(unittest.TestCase):

    def test_random_cases(self):
        for _ in range(100):
            size = random.randint(0, 15)

            nums = [
                random.randint(-10, 10)
                for _ in range(size)
            ]

            self.assertEqual(
                longest_consecutive(nums),
                brute_longest_consecutive(nums)
            )
