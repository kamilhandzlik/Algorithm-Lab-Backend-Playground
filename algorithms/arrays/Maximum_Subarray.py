"""
Problem: Maximum Subarray
Difficulty: Medium
Category: Arrays / Dynamic Programming

Description:
Given an integer array nums, find the contiguous subarray
which has the largest sum and return its sum.

Time Complexity: O(n)
Space Complexity: O(1)

Approach:
- Kadane's algorithm
- track current sum and max sum

Edge cases:
- all negative numbers
- single element
"""

def max_subarray(nums):
    max_sum = nums[0]
    current_sum = nums[0]

    for num in nums[1:]:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)

    return max_sum


def test_max_subarray_basic():
    assert max_subarray([-2,1,-3,4,-1,2,1,-5,4]) == 6

def test_max_subarray_all_negative():
    assert max_subarray([-5, -1, -8]) == -1

def test_max_subarray_single():
    assert max_subarray([5]) == 5

def test_max_subarray_all_positive():
    assert max_subarray([1,2,3,4]) == 10

def test_max_subarray_mix():
    assert max_subarray([3, -2, 5, -1]) == 6