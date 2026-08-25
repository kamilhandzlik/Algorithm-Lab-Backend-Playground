"""
Mathematical Algorithm - Egyptian Fractions

Description:
    An Egyptian fraction represents a positive fraction as a sum of
    distinct unit fractions.

    A unit fraction is a fraction whose numerator is equal to 1.

    For example:

        2 / 3 = 1 / 2 + 1 / 6

    Both fractions on the right side are unit fractions.

    Another example:

        5 / 6 = 1 / 2 + 1 / 3

    Egyptian fractions were used in ancient Egyptian mathematics and
    provide an interesting example of decomposing a mathematical
    object into simpler components.

Purpose:
    - Convert a proper fraction into Egyptian fraction notation.
    - Demonstrate a mathematical greedy algorithm.
    - Demonstrate how choosing the locally largest possible unit
      fraction can lead to a complete solution.
    - Practice working with fractions using integer arithmetic.

Greedy strategy:
    At every step, we choose the largest unit fraction that does not
    exceed the remaining fraction.

    For a fraction:

        numerator / denominator

    the largest possible unit fraction is:

        1 / ceil(denominator / numerator)

    After choosing that unit fraction, we subtract it from the
    remaining fraction and repeat the process.

Example:

        4 / 13

    The first unit fraction is:

        1 / ceil(13 / 4)
        = 1 / 4

    Therefore:

        4 / 13 - 1 / 4
        = 3 / 52

    Now process:

        3 / 52

    The next unit fraction is:

        1 / ceil(52 / 3)
        = 1 / 18

    Therefore:

        3 / 52 - 1 / 18
        = 1 / 468

    The final representation is:

        4 / 13 = 1 / 4 + 1 / 18 + 1 / 468

Why integer arithmetic is used:
    Floating-point numbers can introduce rounding errors.

    For example, values such as:

        1 / 3

    cannot be represented exactly using ordinary binary floating
    point numbers.

    Instead of using floats, this implementation keeps the fraction
    as two integers:

        numerator
        denominator

    and performs all calculations using integer arithmetic.

Simplification:
    After every subtraction, the resulting fraction is reduced using
    the Greatest Common Divisor.

    For example:

        6 / 18

    becomes:

        1 / 3

    This keeps the numbers smaller and makes the algorithm easier
    to reason about.

Complexity:
    The number of iterations depends on the input fraction.

    For ordinary inputs, the algorithm is very fast, but there is
    no simple O(n) bound in terms of the numerator and denominator
    because the number of generated unit fractions depends on the
    structure of the fraction.

When to use:
    - Mathematical exercises.
    - Fraction decomposition.
    - Number theory.
    - Algorithm demonstrations.
    - Problems involving greedy mathematical transformations.

Advantages:
    - Very simple strategy.
    - Uses only integer arithmetic.
    - Produces exact results.
    - Each generated fraction is a unit fraction.
    - The resulting unit fractions are distinct.

Disadvantages:
    - The greedy strategy does not necessarily produce the shortest
      possible Egyptian fraction representation.
    - Some fractions can produce relatively long representations.
    - The algorithm is mainly useful for mathematical and educational
      purposes rather than typical backend business logic.

Important concept:
    This algorithm demonstrates an important difference between
    Dynamic Programming and Greedy Algorithms.

    Dynamic Programming often explores and remembers multiple
    possibilities.

    A Greedy Algorithm makes the best-looking local decision and
    continues from there.

    Here, the local decision is:

        Choose the largest possible unit fraction.

    This produces a valid Egyptian fraction representation.
"""


def greatest_common_divisor(first, second):
    first = abs(first)
    second = abs(second)

    while second != 0:
        first, second = second, first % second

    return first


def simplify_fraction(numerator, denominator):
    divisor = greatest_common_divisor(
        numerator,
        denominator
    )

    return (
        numerator // divisor,
        denominator // divisor
    )


def egyptian_fraction(numerator, denominator):
    if numerator <= 0:
        raise ValueError("Numerator must be positive")

    if denominator <= 0:
        raise ValueError("Denominator must be positive")

    if numerator >= denominator:
        raise ValueError("Fraction must be proper")

    result = []

    while numerator != 0:
        unit_denominator = (
            denominator + numerator - 1
        ) // numerator

        result.append(unit_denominator)

        numerator = (
            numerator * unit_denominator
            - denominator
        )

        denominator *= unit_denominator

        numerator, denominator = simplify_fraction(
            numerator,
            denominator
        )

    return result


def reconstruct_fraction(unit_denominators):
    numerator = 0
    denominator = 1

    for unit_denominator in unit_denominators:
        numerator = (
            numerator * unit_denominator
            + denominator
        )

        denominator *= unit_denominator

        numerator, denominator = simplify_fraction(
            numerator,
            denominator
        )

    return numerator, denominator


import random
import unittest


class EgyptianFractionTests(unittest.TestCase):

    def test_two_thirds(self):
        result = egyptian_fraction(2, 3)

        self.assertEqual(result, [2, 6])

    def test_five_sixths(self):
        result = egyptian_fraction(5, 6)

        self.assertEqual(result, [2, 3])

    def test_four_thirteenths(self):
        result = egyptian_fraction(4, 13)

        self.assertEqual(result, [4, 18, 468])

    def test_one_half(self):
        result = egyptian_fraction(1, 2)

        self.assertEqual(result, [2])

    def test_one_third(self):
        result = egyptian_fraction(1, 3)

        self.assertEqual(result, [3])

    def test_one_hundredth(self):
        result = egyptian_fraction(1, 100)

        self.assertEqual(result, [100])

    def test_result_reconstructs_original_fraction(self):
        numerator, denominator = reconstruct_fraction(
            egyptian_fraction(7, 10)
        )

        self.assertEqual(numerator, 7)
        self.assertEqual(denominator, 10)

    def test_invalid_numerator(self):
        with self.assertRaises(ValueError):
            egyptian_fraction(0, 5)

    def test_invalid_denominator(self):
        with self.assertRaises(ValueError):
            egyptian_fraction(3, 0)

    def test_improper_fraction(self):
        with self.assertRaises(ValueError):
            egyptian_fraction(5, 3)


class EgyptianFractionRandomTests(unittest.TestCase):

    def test_random_fractions_reconstruct_correctly(self):
        for _ in range(500):
            denominator = random.randint(2, 100)
            numerator = random.randint(1, denominator - 1)

            unit_denominators = egyptian_fraction(
                numerator,
                denominator
            )

            result = reconstruct_fraction(
                unit_denominators
            )

            expected = simplify_fraction(
                numerator,
                denominator
            )

            self.assertEqual(result, expected)

    def test_random_results_contain_only_unit_fractions(self):
        for _ in range(500):
            denominator = random.randint(2, 100)
            numerator = random.randint(1, denominator - 1)

            result = egyptian_fraction(
                numerator,
                denominator
            )

            for unit_denominator in result:
                self.assertGreater(unit_denominator, 1)

    def test_random_denominators_are_distinct(self):
        for _ in range(500):
            denominator = random.randint(2, 100)
            numerator = random.randint(1, denominator - 1)

            result = egyptian_fraction(
                numerator,
                denominator
            )

            self.assertEqual(
                len(result),
                len(set(result))
            )

    def test_random_numerator_is_positive(self):
        for _ in range(500):
            denominator = random.randint(2, 100)
            numerator = random.randint(1, denominator - 1)

            result = egyptian_fraction(
                numerator,
                denominator
            )

            self.assertGreaterEqual(
                len(result),
                1
            )


if __name__ == "__main__":
    unittest.main()