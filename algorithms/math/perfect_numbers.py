"""
Problem matematyczny:
Znajdź wszystkie liczby doskonałe w zakresie od 1 do n.

Definicja:
Liczba doskonała to taka liczba, której suma jej właściwych dzielników
(jedynie dodatnich, bez samej liczby) jest równa tej liczbie.

Przykłady:
6  -> 1 + 2 + 3 = 6
28 -> 1 + 2 + 4 + 7 + 14 = 28

Zadanie:
Zaimplementuj funkcję perfect_numbers(n), która zwraca listę wszystkich
liczb doskonałych w zakresie [1, n].

Wymagania:
- n może być duże (do ~1_000_000)
- funkcja musi działać szybko
- użyj optymalnego liczenia sumy dzielników do sqrt(n)
"""
import unittest
import random


def sum_of_proper_divisors(x: int) -> int:
    if x <= 1:
        return 0
    total = 1
    i = 2
    while i * i <= x:
        if x % i == 0:
            total += i
            if i != x // i:
                total += x // i
        i += 1
    return total


def perfect_numbers(n: int):
    return [i for i in range(1, n + 1) if sum_of_proper_divisors(i) == i]


class TestPerfectNumbers(unittest.TestCase):

    def test_known_values(self):

        self.assertEqual(perfect_numbers(1), [])
        self.assertEqual(perfect_numbers(6), [6])
        self.assertEqual(perfect_numbers(28), [6, 28])
        self.assertEqual(perfect_numbers(500), [6, 28, 496])

    def test_no_false_positives(self):

        res = perfect_numbers(1000)
        for x in res:
            self.assertEqual(sum_of_proper_divisors(x), x)

    def test_random_small(self):

        def brute(x):
            return sum(i for i in range(1, x) if x % i == 0)

        for _ in range(50):
            n = random.randint(1, 200)
            expected = [i for i in range(1, n + 1) if brute(i) == i]
            self.assertEqual(perfect_numbers(n), expected)


if __name__ == "__main__":
    print("Perfect numbers up to 10000:")
    print(perfect_numbers(10000))

    unittest.main()
