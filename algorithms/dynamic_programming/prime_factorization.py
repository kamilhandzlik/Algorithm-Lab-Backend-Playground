"""
Mathematical Algorithm - Prime Factorization

Description:
    Prime factorization is the process of representing a positive
    integer as a product of prime numbers.

    Every integer greater than 1 has a unique prime factorization.

    For example:

        84 = 2 * 2 * 3 * 7

    Therefore, the prime factorization of 84 is:

        [2, 2, 3, 7]

    The same factorization can also be written using exponents:

        84 = 2^2 * 3 * 7

Purpose:
    - Find all prime factors of a positive integer.
    - Demonstrate mathematical decomposition.
    - Demonstrate how mathematical observations can reduce the
      number of operations required by an algorithm.
    - Provide a reusable utility for number theory problems.

Basic approach:
    A simple way to find prime factors is to try every integer from
    2 to n.

    However, this is unnecessary.

    If a number n has a factor greater than its square root, then
    the corresponding paired factor must be smaller than the square
    root.

    For example:

        36 = 4 * 9

    Although 9 is greater than sqrt(36), its corresponding factor 4
    is smaller than sqrt(36).

    Therefore, when searching for factors, we only need to test
    possible divisors up to sqrt(n).

Algorithm:
    Start with the smallest prime number:

        2

    While the current number is divisible by the current divisor,
    divide it and add the divisor to the result.

    Then move to the next possible divisor.

    For example:

        n = 84

    Divide by 2:

        84 / 2 = 42

    Divide by 2 again:

        42 / 2 = 21

    21 is no longer divisible by 2.

    Try 3:

        21 / 3 = 7

    7 is not divisible by 3.

    Try 4, 5 and 6.

    Once the divisor becomes greater than the square root of the
    remaining number, any remaining value greater than 1 must itself
    be prime.

    In this case:

        7

    is added directly.

    Final result:

        [2, 2, 3, 7]

Important optimization:
    After checking the divisor 2, we do not need to test even
    divisors again.

    We can therefore test:

        2, 3, 5, 7, 9, 11, ...

    instead of:

        2, 3, 4, 5, 6, 7, 8, 9, ...

    This removes half of the remaining candidates.

Complexity:
    Time:
        O(sqrt(n))

    Space:
        O(log(n))

    The space complexity comes from storing the prime factors.
    In the worst case, a number can contain many small prime factors.

When to use:
    - Number theory.
    - Cryptography.
    - Divisibility problems.
    - Calculating divisors.
    - Simplifying mathematical expressions.
    - Finding the number of divisors.
    - Calculating Euler's totient function.
    - Problems involving prime decomposition.

Advantages:
    - Simple implementation.
    - Much faster than testing every number up to n.
    - Uses a useful mathematical observation.
    - Produces a reusable representation of a number.

Disadvantages:
    - O(sqrt(n)) can still be too slow for extremely large integers.
    - For very large numbers, more advanced algorithms such as
      Pollard's Rho may be required.

Important concept:
    A common algorithmic optimization is to ask:

        "Do I really need to check every possible value?"

    Here, the answer is no.

    If a composite number has a factorization:

        n = a * b

    and both a and b were greater than sqrt(n), then:

        a * b > n

    which is impossible.

    Therefore, every composite number has at least one factor that
    is less than or equal to its square root.

    This single observation reduces the search space dramatically.
"""
import random
import unittest


def prime_factorization(number):
    if number < 2:
        raise ValueError("Number must be at least 2")

    factors = []

    while number % 2 == 0:
        factors.append(2)
        number //= 2

    divisor = 3

    while divisor * divisor <= number:
        while number % divisor == 0:
            factors.append(divisor)
            number //= divisor

        divisor += 2

    if number > 1:
        factors.append(number)

    return factors


def multiply_factors(factors):
    result = 1

    for factor in factors:
        result *= factor

    return result


def is_prime(number):
    if number < 2:
        return False

    if number == 2:
        return True

    if number % 2 == 0:
        return False

    divisor = 3

    while divisor * divisor <= number:
        if number % divisor == 0:
            return False

        divisor += 2

    return True


class PrimeFactorizationTests(unittest.TestCase):
    def test_smallest_prime(self):
        result = prime_factorization(2)
        self.assertEqual(result, [2])

    def test_prime_number(self):
        result = prime_factorization(17)
        self.assertEqual(result, [17])

    def test_power_of_two(self):
        result = prime_factorization(32)
        self.assertEqual(result, [2, 2, 2, 2, 2])

    def test_basic_composite_number(self):
        result = prime_factorization(84)
        self.assertEqual(
            result,
            [2, 2, 3, 7]
        )

    def test_square(self):
        result = prime_factorization(49)
        self.assertEqual(result, [7, 7])

    def test_product_of_two_primes(self):
        result = prime_factorization(77)
        self.assertEqual(
            result,
            [7, 11]
        )

    def test_large_power(self):
        result = prime_factorization(243)
        self.assertEqual(
            result,
            [3, 3, 3, 3, 3]
        )

    def test_prime_near_square_root(self):
        result = prime_factorization(97)
        self.assertEqual(result, [97])

    def test_invalid_number(self):
        with self.assertRaises(ValueError):
            prime_factorization(1)

    def test_zero(self):
        with self.assertRaises(ValueError):
            prime_factorization(0)

    def test_negative_number(self):
        with self.assertRaises(ValueError):
            prime_factorization(-10)

    def test_multiplication_of_factors(self):
        factors = prime_factorization(360)
        result = multiply_factors(factors)
        self.assertEqual(result, 360)

    def test_all_factors_are_prime(self):
        factors = prime_factorization(7560)
        for factor in factors:
            self.assertTrue(is_prime(factor))


class PrimeFactorizationRandomTests(unittest.TestCase):
    def test_random_reconstruction(self):
        for _ in range(500):
            number = random.randint(2, 100000)
            factors = prime_factorization(number)
            result = multiply_factors(factors)
            self.assertEqual(result, number)

    def test_random_prime_numbers(self):
        for _ in range(500):
            number = random.randint(2, 10000)
            if not is_prime(number):
                continue
            factors = prime_factorization(number)
            self.assertEqual(
                factors,
                [number]
            )

    def test_random_composite_numbers(self):
        for _ in range(500):
            first = random.randint(2, 500)
            second = random.randint(2, 500)
            number = first * second
            factors = prime_factorization(number)
            self.assertEqual(
                multiply_factors(factors),
                number
            )
            for factor in factors:
                self.assertTrue(is_prime(factor))

    def test_random_prime_products(self):
        for _ in range(500):
            first = random.randint(2, 100)
            second = random.randint(2, 100)
            while not is_prime(first):
                first = random.randint(2, 100)
            while not is_prime(second):
                second = random.randint(2, 100)
            number = first * second
            factors = prime_factorization(number)
            self.assertEqual(
                multiply_factors(factors),
                number
            )
            for factor in factors:
                self.assertTrue(is_prime(factor))

    def test_random_powers_of_two(self):
        for _ in range(500):
            exponent = random.randint(1, 15)
            number = 2 ** exponent
            factors = prime_factorization(number)
            self.assertEqual(
                factors,
                [2] * exponent
            )


if __name__ == "__main__":
    unittest.main()
