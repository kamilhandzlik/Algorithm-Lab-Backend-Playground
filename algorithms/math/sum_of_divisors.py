"""
Problem matematyczny:
Dla danej liczby n oblicz sumę wszystkich jej dodatnich dzielników.

Przykład:
n = 12
Dzielniki: 1, 2, 3, 4, 6, 12
Suma = 28

Zadanie:
Zaimplementuj funkcję sum_of_divisors(n), która zwraca sumę wszystkich dodatnich dzielników n.
Funkcja musi działać szybko nawet dla dużych n (np. do 10^7).

Wskazówka:
Można iterować tylko do sqrt(n), a dzielniki dodawać parami.
"""
import pytest
import random


def sum_of_divisors(n: int) -> int:
    if n <= 0:
        return 0

    total = 0
    i = 1
    while i * i <= n:
        if n % i == 0:
            total += i
            if i != n // i:
                total += n // i
        i += 1
    return total


def test_basic():
    assert sum_of_divisors(1) == 1
    assert sum_of_divisors(6) == 12
    assert sum_of_divisors(12) == 28
    assert sum_of_divisors(36) == 91


def test_prime_numbers():
    assert sum_of_divisors(7) == 8
    assert sum_of_divisors(13) == 14
    assert sum_of_divisors(29) == 30


def test_edge_cases():
    assert sum_of_divisors(0) == 0
    assert sum_of_divisors(-5) == 0


def test_large_number():
    assert sum_of_divisors(10_000) == 27387


def brute(n):
    return sum(i for i in range(1, n + 1) if n % i == 0)


def test_random():
    for _ in range(200):
        n = random.randint(1, 10000)
        assert sum_of_divisors(n) == brute(n)


if __name__ == "__main__":
    print(sum_of_divisors(12))  # 28
    print(sum_of_divisors(1))  # 1
    print(sum_of_divisors(36))  # 91
