"""
Mathematical Algorithm - Greatest Common Divisor

Description:
    The Greatest Common Divisor (GCD) of two integers is the largest
    positive integer that divides both numbers without leaving a
    remainder.

    For example:

        gcd(48, 18) = 6

    because:

        48 = 6 * 8
        18 = 6 * 3

    and there is no larger positive integer that divides both values.

    The most famous method for calculating the GCD is the Euclidean
    Algorithm.

Euclidean Algorithm:
    The algorithm is based on the mathematical property:

        gcd(a, b) = gcd(b, a % b)

    This means that the GCD does not change if the larger number is
    replaced by the remainder obtained when dividing it by the
    smaller number.

    For example:

        gcd(48, 18)

    First step:

        48 % 18 = 12

    Therefore:

        gcd(48, 18) = gcd(18, 12)

    Next:

        18 % 12 = 6

    Therefore:

        gcd(18, 12) = gcd(12, 6)

    Next:

        12 % 6 = 0

    When the remainder becomes zero, the other number is the GCD.

    Therefore:

        gcd(12, 6) = 6

Purpose:
    - Calculate the greatest common divisor efficiently.
    - Simplify fractions.
    - Reduce ratios.
    - Work with divisibility problems.
    - Support modular arithmetic.
    - Build mathematical utility functions.

Why the algorithm works:
    Suppose:

        a = q * b + r

    where:

        r = a % b

    Every common divisor of a and b must also divide r.

    Conversely, every common divisor of b and r must also divide a.

    Therefore, a and b have exactly the same common divisors as b
    and r.

    This gives us:

        gcd(a, b) = gcd(b, r)

    Repeating this process eventually produces a remainder of zero.

    The last non-zero remainder is the GCD.

Complexity:
    Time:
        O(log(min(a, b)))

    Space:
        O(1)

    The Euclidean Algorithm is extremely efficient because the
    numbers become smaller very quickly.

Special cases:
    If one number is zero:

        gcd(a, 0) = |a|

    because every number divides zero and the largest positive divisor
    of a is |a|.

    If both numbers are zero, the mathematical definition of the GCD
    is sometimes treated as undefined.

    This implementation returns 0 for:

        gcd(0, 0)

    because this is convenient for a general-purpose programming
    utility.

Negative numbers:
    The GCD is conventionally represented as a positive number.

    Therefore:

        gcd(-48, 18) = 6
        gcd(48, -18) = 6
        gcd(-48, -18) = 6

    The implementation converts the inputs to their absolute values
    before applying the algorithm.

When to use:
    - Fraction reduction.
    - Ratio normalization.
    - Number theory.
    - Modular arithmetic.
    - Cryptographic algorithms.
    - Scheduling recurring events.
    - Algorithms involving divisibility.
    - Simplifying mathematical expressions.

Advantages:
    - Extremely fast.
    - Very small implementation.
    - Uses constant memory.
    - Mathematically elegant.
    - Works for very large integers.

Disadvantages:
    - Only solves the GCD problem.
    - The reasoning behind the modulo transformation can be less
      intuitive for beginners.

Related mathematical algorithms:
    - Least Common Multiple (LCM).
    - Extended Euclidean Algorithm.
    - Modular inverse.
    - Bézout's identity.

Important concept:
    The most important idea is not the implementation itself.

    It is recognizing that a problem can sometimes be transformed
    into an equivalent problem involving smaller values.

    Instead of repeatedly asking:

        "What divides both a and b?"

    we transform:

        gcd(a, b)

    into:

        gcd(b, a % b)

    until the problem becomes trivial.

    This type of mathematical reduction is one of the most powerful
    ideas in algorithm design.
"""
import random
import unittest


def greatest_common_divisor(first, second):
    first = abs(first)
    second = abs(second)

    while second != 0:
        first, second = second, first % second

    return first


def brute_force_gcd(first, second):
    first = abs(first)
    second = abs(second)

    if first == 0:
        return second

    if second == 0:
        return first

    limit = min(first, second)
    greatest = 1

    for number in range(1, limit + 1):
        if first % number == 0 and second % number == 0:
            greatest = number

    return greatest


class GreatestCommonDivisorTests(unittest.TestCase):
    def test_basic_case(self):
        result = greatest_common_divisor(48, 18)
        self.assertEqual(result, 6)

    def test_equal_numbers(self):
        result = greatest_common_divisor(25, 25)
        self.assertEqual(result, 25)

    def test_coprime_numbers(self):
        result = greatest_common_divisor(17, 13)
        self.assertEqual(result, 1)

    def test_first_number_is_zero(self):
        result = greatest_common_divisor(0, 15)
        self.assertEqual(result, 15)

    def test_second_number_is_zero(self):
        result = greatest_common_divisor(15, 0)
        self.assertEqual(result, 15)

    def test_both_numbers_are_zero(self):
        result = greatest_common_divisor(0, 0)
        self.assertEqual(result, 0)

    def test_negative_first_number(self):
        result = greatest_common_divisor(-48, 18)
        self.assertEqual(result, 6)

    def test_negative_second_number(self):
        result = greatest_common_divisor(48, -18)
        self.assertEqual(result, 6)

    def test_both_negative(self):
        result = greatest_common_divisor(-48, -18)
        self.assertEqual(result, 6)

    def test_gcd_of_one(self):
        result = greatest_common_divisor(1, 999)
        self.assertEqual(result, 1)

    def test_large_common_divisor(self):
        result = greatest_common_divisor(1000000, 500000)
        self.assertEqual(result, 500000)


class GreatestCommonDivisorRandomTests(unittest.TestCase):
    def test_random_against_brute_force(self):
        for _ in range(500):
            first = random.randint(-1000, 1000)
            second = random.randint(-1000, 1000)
            expected = brute_force_gcd(
                first,
                second
            )
            result = greatest_common_divisor(
                first,
                second
            )
            self.assertEqual(result, expected)

    def test_random_equal_numbers(self):
        for _ in range(500):
            number = random.randint(-100000, 100000)
            result = greatest_common_divisor(
                number,
                number
            )
            self.assertEqual(
                result,
                abs(number)
            )

    def test_random_with_zero(self):
        for _ in range(500):
            number = random.randint(-100000, 100000)
            result = greatest_common_divisor(
                number,
                0
            )
            self.assertEqual(
                result,
                abs(number)
            )

    def test_random_common_multiples(self):
        for _ in range(500):
            divisor = random.randint(1, 100)
            first_multiplier = random.randint(1, 100)
            second_multiplier = random.randint(1, 100)
            first = divisor * first_multiplier
            second = divisor * second_multiplier
            result = greatest_common_divisor(
                first,
                second
            )
            expected = divisor * greatest_common_divisor(
                first_multiplier,
                second_multiplier
            )
            self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
