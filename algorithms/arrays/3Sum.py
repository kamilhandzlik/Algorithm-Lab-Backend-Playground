"""
Problem: 3Sum
Difficulty: Medium
Category: Arrays / Two Pointers

Time Complexity: O(n^2)
Space Complexity: O(1) (bez liczenia wyniku)
d
"""

def three_sum(nums):
    nums.sort()
    result = []

    for i in range(len(nums)):
        # pomijamy duplikaty
        if i > 0 and nums[i] == nums[i - 1]:
            continue

        left = i + 1
        right = len(nums) - 1

        while left < right:
            total = nums[i] + nums[left] + nums[right]

            if total == 0:
                result.append([nums[i], nums[left], nums[right]])

                # skip duplikaty
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1

                left += 1
                right -= 1

            elif total < 0:
                left += 1
            else:
                right -= 1

    return result


import unittest

class TestThreeSum(unittest.TestCase):

    def test_basic(self):
        result = three_sum([-1,0,1,2,-1,-4])
        expected = [[-1,-1,2], [-1,0,1]]
        self.assertEqual(sorted(result), sorted(expected))

    def test_no_solution(self):
        self.assertEqual(three_sum([1,2,3]), [])

    def test_all_zero(self):
        self.assertEqual(three_sum([0,0,0,0]), [[0,0,0]])

    def test_empty(self):
        self.assertEqual(three_sum([]), [])

    def test_small(self):
        self.assertEqual(three_sum([0,1]), [])


import random

def brute_three_sum(nums):
    result = set()

    n = len(nums)
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                if nums[i] + nums[j] + nums[k] == 0:
                    triplet = tuple(sorted([nums[i], nums[j], nums[k]]))
                    result.add(triplet)

    return sorted([list(t) for t in result])


class TestRandom(unittest.TestCase):

    def test_random_cases(self):
        for _ in range(100):
            size = random.randint(0, 8)
            nums = [random.randint(-5, 5) for _ in range(size)]

            self.assertEqual(
                sorted(three_sum(nums)),
                brute_three_sum(nums)
            )
