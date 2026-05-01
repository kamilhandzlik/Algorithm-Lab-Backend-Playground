"""
Problem: Product of Array Except Self
Difficulty: Medium
Category: Arrays

Time Complexity: O(n)
Space Complexity: O(1) (bez liczenia outputu)
"""

def product_except_self(nums):
    n = len(nums)
    result = [1] * n

    # prefix
    left = 1
    for i in range(n):
        result[i] = left
        left *= nums[i]

    # suffix
    right = 1
    for i in range(n - 1, -1, -1):
        result[i] *= right
        right *= nums[i]

    return result



import unittest

class TestProductExceptSelf(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(
            product_except_self([1,2,3,4]),
            [24,12,8,6]
        )

    def test_with_zero(self):
        self.assertEqual(
            product_except_self([1,2,0,4]),
            [0,0,8,0]
        )

    def test_two_zeros(self):
        self.assertEqual(
            product_except_self([0,2,0,4]),
            [0,0,0,0]
        )

    def test_single_element(self):
        self.assertEqual(
            product_except_self([5]),
            [1]
        )

    def test_negatives(self):
        self.assertEqual(
            product_except_self([-1,1,-1,1]),
            [-1,1,-1,1]
        )