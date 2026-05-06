"""
Problem: Find Minimum in Rotated Sorted Array
Difficulty: Medium
Category: Binary Search

Time Complexity: O(log n)
Space Complexity: O(1)
"""
import random
import unittest


def find_min(nums):
    left = 0
    right = len(nums) - 1

    while left < right:
        mid = (left + right) // 2

        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid

    return nums[left]


class TestFindMin(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(find_min([4, 5, 6, 7, 0, 1, 2]), 0)

    def test_no_rotation(self):
        self.assertEqual(find_min([1, 2, 3, 4, 5]), 1)

    def test_small(self):
        self.assertEqual(find_min([2, 1]), 1)

    def test_single(self):
        self.assertEqual(find_min([10]), 10)

    def test_two_elements(self):
        self.assertEqual(find_min([3, 1]), 1)


def rotate_array(arr, k):
    return arr[k:] + arr[:k]


def brute_find_min(nums):
    return min(nums)


class TestRandom(unittest.TestCase):

    def test_random_rotations(self):
        for _ in range(100):
            size = random.randint(1, 10)
            base = sorted(random.sample(range(-20, 20), size))

            k = random.randint(0, size - 1)
            nums = rotate_array(base, k)

            self.assertEqual(
                find_min(nums),
                brute_find_min(nums)
            )
