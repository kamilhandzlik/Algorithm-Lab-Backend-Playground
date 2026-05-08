"""
Problem: Container With Most Water
Difficulty: Medium
Category: Arrays / Two Pointers

Time Complexity: O(n)
Space Complexity: O(1)
"""
import unittest
import random


def max_area(heights):
    left = 0
    right = len(heights) - 1

    best = 0

    while left < right:

        width = right - left
        height = min(heights[left], heights[right])

        area = width * height
        best = max(best, area)

        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1

    return best


class TestMaxArea(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(
            max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]),
            49
        )

    def test_small(self):
        self.assertEqual(
            max_area([1, 1]),
            1
        )

    def test_increasing(self):
        self.assertEqual(
            max_area([1, 2, 3, 4, 5]),
            6
        )

    def test_decreasing(self):
        self.assertEqual(
            max_area([5, 4, 3, 2, 1]),
            6
        )

    def test_single_peak(self):
        self.assertEqual(
            max_area([1, 100, 1]),
            2
        )


def brute_max_area(heights):
    best = 0

    for i in range(len(heights)):
        for j in range(i + 1, len(heights)):
            width = j - i
            height = min(heights[i], heights[j])

            best = max(best, width * height)

    return best


class TestRandom(unittest.TestCase):

    def test_random_cases(self):
        for _ in range(100):
            size = random.randint(2, 10)

            heights = [
                random.randint(1, 20)
                for _ in range(size)
            ]

            self.assertEqual(
                max_area(heights),
                brute_max_area(heights)
            )
