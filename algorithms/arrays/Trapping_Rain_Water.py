"""
Problem: Trapping Rain Water
Difficulty: Hard
Category: Arrays / Two Pointers

Time Complexity: O(n)
Space Complexity: O(1)
"""
import unittest
import random


def trap(height):
    left = 0
    right = len(height) - 1

    left_max = 0
    right_max = 0

    water = 0

    while left < right:

        if height[left] < height[right]:

            if height[left] >= left_max:
                left_max = height[left]
            else:
                water += left_max - height[left]

            left += 1

        else:

            if height[right] >= right_max:
                right_max = height[right]
            else:
                water += right_max - height[right]

            right -= 1

    return water


class TestTrap(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(
            trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]),
            6
        )

    def test_empty(self):
        self.assertEqual(
            trap([]),
            0
        )

    def test_flat(self):
        self.assertEqual(
            trap([1, 1, 1, 1]),
            0
        )

    def test_descending(self):
        self.assertEqual(
            trap([5, 4, 3, 2, 1]),
            0
        )

    def test_simple_case(self):
        self.assertEqual(
            trap([2, 0, 2]),
            2
        )


def brute_trap(height):
    water = 0

    for i in range(len(height)):
        left_max = max(height[:i + 1])
        right_max = max(height[i:])

        water += min(left_max, right_max) - height[i]

    return water


class TestRandom(unittest.TestCase):

    def test_random_cases(self):
        for _ in range(100):
            size = random.randint(0, 12)

            height = [
                random.randint(0, 10)
                for _ in range(size)
            ]

            self.assertEqual(
                trap(height),
                brute_trap(height)
            )
