"""
Problem: Two Sum
Difficulty: Easy
Category: Arrays / HashMap

Description:
Given an array of integers nums and an integer target,
return indices of the two numbers such that they add up to target.

Time Complexity: O(n)
Space Complexity: O(n)

Approach:
- iterate once
- store seen numbers in dict
- check complement

Edge cases:
- no solution (optional handling)
- duplicates
"""

def two_sum(nums, target):
    seen = {}

    for i, num in enumerate(nums):
        complement = target - num

        if complement in seen:
            return [seen[complement], i]

        seen[num] = i

    return []  # jeśli brak rozwiązania