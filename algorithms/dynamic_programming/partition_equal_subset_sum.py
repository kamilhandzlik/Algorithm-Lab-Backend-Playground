"""
Dynamic Programming - Partition Equal Subset Sum

Description:
    The Partition Equal Subset Sum problem asks whether a collection
    of positive integers can be divided into two subsets whose sums
    are equal.

    Every number must belong to exactly one of the two subsets.

    For example:

        [1, 5, 11, 5]

    The total sum is:

        22

    Therefore, each subset must have a sum of:

        22 / 2 = 11

    A valid partition is:

        [11]
        [1, 5, 5]

    Both subsets have a sum of 11.

Purpose:
    - Determine whether a collection can be split into equal subsets.
    - Demonstrate the Subset Sum Dynamic Programming technique.
    - Solve problems involving resource allocation.
    - Demonstrate a boolean DP state.

Key observation:
    If the total sum is odd, equal partitioning is impossible.

    For example:

        [1, 2, 4]

    Total:

        7

    Since 7 cannot be divided into two equal integer sums, the answer
    is immediately False.

    If the total sum is even, the problem becomes:

        "Can we select some numbers whose sum is exactly total_sum / 2?"

    This is the classic Subset Sum problem.

State:
    dp[target] represents whether it is possible to construct the
    given target sum using the numbers processed so far.

    Initially:

        dp[0] = True

    because an empty subset can always produce a sum of zero.

Transition:
    For every number, we update the possible sums.

    If a sum was already possible, adding the current number may make
    another sum possible.

    Conceptually:

        dp[current_sum] = dp[current_sum]
            or dp[current_sum - number]

    The second part means that if current_sum - number was achievable,
    then current_sum becomes achievable by adding the current number.

Important implementation detail:
    The DP array is iterated backwards.

    This prevents the same number from being used more than once.

    If we iterated forwards, the current number could potentially be
    reused multiple times during the same iteration.

Complexity:
    Time:
        O(n * target)

    Space:
        O(target)

    where target is half of the total sum.

When to use:
    - Subset selection.
    - Resource allocation.
    - Partition problems.
    - Scheduling.
    - Capacity planning.
    - Combinatorial optimization.

Advantages:
    - Efficient compared with checking every subset.
    - Uses a simple boolean state.
    - Can be implemented with O(target) memory.
    - Demonstrates an important reusable DP pattern.

Disadvantages:
    - Complexity depends on the numerical value of the target,
      not only on the number of elements.
    - Large numbers can make the DP table expensive.
    - This is a pseudo-polynomial algorithm.

Important concept:
    The key transformation is:

        Equal Partition
            ↓
        Half of total sum
            ↓
        Subset Sum

    Recognizing such transformations is one of the most useful skills
    when solving Dynamic Programming problems.

    Another important lesson is that DP often changes the question.

    Instead of asking:

        "How do I divide the entire array?"

    we ask:

        "Which sums are achievable with the numbers I have processed?"
"""
import random
import unittest


def can_partition(numbers):
    if any(number <= 0 for number in numbers):
        raise ValueError("Numbers must be greater than zero")

    total = sum(numbers)

    if total % 2 != 0:
        return False

    target = total // 2

    dp = [False] * (target + 1)
    dp[0] = True

    for number in numbers:
        for current_sum in range(target, number - 1, -1):
            dp[current_sum] = (
                    dp[current_sum] or
                    dp[current_sum - number]
            )

    return dp[target]


class CanPartitionTests(unittest.TestCase):

    def test_basic_true(self):
        numbers = [1, 5, 11, 5]

        result = can_partition(numbers)

        self.assertTrue(result)

    def test_basic_false(self):
        numbers = [1, 2, 3, 5]

        result = can_partition(numbers)

        self.assertFalse(result)

    def test_odd_total_sum(self):
        numbers = [1, 2, 4]

        result = can_partition(numbers)

        self.assertFalse(result)

    def test_single_even_number(self):
        result = can_partition([10])

        self.assertFalse(result)

    def test_two_equal_numbers(self):
        result = can_partition([5, 5])

        self.assertTrue(result)

    def test_two_different_numbers(self):
        result = can_partition([5, 6])

        self.assertFalse(result)

    def test_empty_list(self):
        result = can_partition([])

        self.assertTrue(result)

    def test_multiple_possible_partitions(self):
        numbers = [2, 2, 2, 2]

        result = can_partition(numbers)

        self.assertTrue(result)

    def test_negative_number(self):
        with self.assertRaises(ValueError):
            can_partition([1, -2, 3])

    def test_zero_number(self):
        with self.assertRaises(ValueError):
            can_partition([1, 0, 3])


class CanPartitionRandomTests(unittest.TestCase):

    def brute_force(self, numbers):
        total = sum(numbers)

        if total % 2 != 0:
            return False

        target = total // 2
        length = len(numbers)

        for mask in range(1 << length):
            current_sum = 0

            for i in range(length):
                if mask & (1 << i):
                    current_sum += numbers[i]

            if current_sum == target:
                return True

        return False

    def create_random_numbers(self):
        length = random.randint(0, 12)

        return [
            random.randint(1, 20)
            for _ in range(length)
        ]

    def test_random_against_brute_force(self):
        for _ in range(500):
            numbers = self.create_random_numbers()

            expected = self.brute_force(numbers)
            result = can_partition(numbers)

            self.assertEqual(result, expected)

    def test_random_odd_sums(self):
        for _ in range(500):
            numbers = self.create_random_numbers()

            if sum(numbers) % 2 != 0:
                result = can_partition(numbers)

                self.assertFalse(result)

    def test_random_identical_pairs(self):
        for _ in range(500):
            value = random.randint(1, 100)

            numbers = [value, value]

            result = can_partition(numbers)

            self.assertTrue(result)

    def test_random_single_numbers(self):
        for _ in range(500):
            value = random.randint(1, 1000)

            result = can_partition([value])

            self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
