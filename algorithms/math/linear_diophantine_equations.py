"""
Linear Diophantine Equations.

A linear Diophantine equation is an equation of the form:

    ax + by = c

where a, b, c, x, and y are integers.

Unlike ordinary linear equations over the real numbers, a linear
Diophantine equation requires integer solutions. This restriction makes
the problem fundamentally different from solving the equation with
ordinary algebra.

The key mathematical fact is:

    ax + by = c

has an integer solution if and only if:

    gcd(a, b) divides c.

The Extended Euclidean Algorithm allows us to find integers x and y
such that:

    ax + by = gcd(a, b)

Once such a pair is known, it can be multiplied by:

    c / gcd(a, b)

to obtain a solution of the original equation.

This implementation returns one integer solution (x, y), or None when
no integer solution exists.

For example:

    15x + 25y = 5

has:

    gcd(15, 25) = 5

Since 5 is divisible by 5, integer solutions exist.

The Extended Euclidean Algorithm can find:

    15 * 2 + 25 * (-1) = 5

so one solution is:

    x = 2
    y = -1

There are infinitely many solutions. If (x0, y0) is one solution,
then all solutions are:

    x = x0 + (b / gcd(a, b)) * t

    y = y0 - (a / gcd(a, b)) * t

for any integer t.

Time complexity of the Extended Euclidean Algorithm is:

    O(log(min(|a|, |b|)))

Space complexity is:

    O(log(min(|a|, |b|)))

because the recursive implementation uses the call stack.

Advantages:
- Very efficient for large integers.
- Provides both the GCD and Bézout coefficients.
- Works naturally with modular arithmetic.
- Can be used to find modular inverses.

Disadvantages:
- The mathematical reasoning is less intuitive than ordinary
  equation solving.
- A solution is not necessarily unique.
- Additional constraints are required if a specific solution is needed,
  for example a positive solution or a solution within a given range.
"""

import random
import unittest


def extended_gcd(first, second):
    """
    Return gcd(first, second) and Bézout coefficients x and y.

    The returned values satisfy:

        first * x + second * y = gcd(first, second)

    The GCD is always non-negative.
    """
    if second == 0:
        return abs(first), 1 if first >= 0 else -1, 0

    quotient = first // second
    remainder = first % second

    gcd, x, y = extended_gcd(second, remainder)

    return gcd, y, x - quotient * y


def solve_diophantine(first, second, target):
    """
    Solve:

        first * x + second * y = target

    and return one integer solution (x, y).

    Return None if no integer solution exists.

    Raise ValueError if both coefficients are zero.
    """
    if first == 0 and second == 0:
        raise ValueError("Both coefficients cannot be zero")

    gcd, x, y = extended_gcd(first, second)

    if target % gcd != 0:
        return None

    multiplier = target // gcd

    return x * multiplier, y * multiplier


class LinearDiophantineEquationTests(unittest.TestCase):
    def test_basic_solution(self):
        result = solve_diophantine(15, 25, 5)

        self.assertIsNotNone(result)

        x, y = result

        self.assertEqual(15 * x + 25 * y, 5)

    def test_multiple_solutions(self):
        result = solve_diophantine(6, 9, 3)

        self.assertIsNotNone(result)

        x, y = result

        self.assertEqual(6 * x + 9 * y, 3)

    def test_no_solution(self):
        result = solve_diophantine(6, 9, 4)

        self.assertIsNone(result)

    def test_zero_target(self):
        result = solve_diophantine(15, 25, 0)

        self.assertIsNotNone(result)

        x, y = result

        self.assertEqual(15 * x + 25 * y, 0)

    def test_negative_coefficients(self):
        result = solve_diophantine(-15, 25, 5)

        self.assertIsNotNone(result)

        x, y = result

        self.assertEqual(-15 * x + 25 * y, 5)

    def test_both_coefficients_zero(self):
        with self.assertRaises(ValueError):
            solve_diophantine(0, 0, 10)

    def test_first_coefficient_zero(self):
        result = solve_diophantine(0, 5, 10)

        self.assertIsNotNone(result)

        x, y = result

        self.assertEqual(5 * y, 10)

    def test_second_coefficient_zero(self):
        result = solve_diophantine(5, 0, 10)

        self.assertIsNotNone(result)

        x, y = result

        self.assertEqual(5 * x, 10)

    def test_negative_target(self):
        result = solve_diophantine(15, 25, -5)

        self.assertIsNotNone(result)

        x, y = result

        self.assertEqual(15 * x + 25 * y, -5)

    def test_large_coefficients(self):
        first = 123456789
        second = 987654321
        target = 9

        result = solve_diophantine(first, second, target)

        self.assertIsNotNone(result)

        x, y = result

        self.assertEqual(first * x + second * y, target)


class LinearDiophantineEquationRandomTests(unittest.TestCase):
    def test_random_solvable_equations(self):
        for _ in range(1000):
            first = random.randint(-100000, 100000)
            second = random.randint(-100000, 100000)

            if first == 0 and second == 0:
                continue

            expected_x = random.randint(-1000, 1000)
            expected_y = random.randint(-1000, 1000)

            target = first * expected_x + second * expected_y

            result = solve_diophantine(first, second, target)

            self.assertIsNotNone(result)

            x, y = result

            self.assertEqual(first * x + second * y, target)

    def test_random_unsolvable_equations(self):
        for _ in range(1000):
            first = random.randint(1, 100000)
            second = random.randint(1, 100000)

            gcd, _, _ = extended_gcd(first, second)

            target = random.randint(1, 100000)

            if target % gcd == 0:
                target += 1

            result = solve_diophantine(first, second, target)

            if target % gcd != 0:
                self.assertIsNone(result)

    def test_random_known_solutions(self):
        for _ in range(1000):
            first = random.randint(-10000, 10000)
            second = random.randint(-10000, 10000)

            if first == 0 and second == 0:
                continue

            expected_x = random.randint(-100, 100)
            expected_y = random.randint(-100, 100)

            target = first * expected_x + second * expected_y

            result = solve_diophantine(first, second, target)

            self.assertIsNotNone(result)

            x, y = result

            self.assertEqual(
                first * x + second * y,
                first * expected_x + second * expected_y
            )


if __name__ == "__main__":
    unittest.main()