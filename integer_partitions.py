"""
Problem matematyczny:
Policz liczbę podziałów całkowitych liczby n (integer partitions).

Definicja:
Podział liczby n to sposób zapisania jej jako sumy liczb dodatnich,
gdzie kolejność składników nie ma znaczenia.

Przykład:
n = 5
Podziały:
5
4+1
3+2
3+1+1
2+2+1
2+1+1+1
1+1+1+1+1

Liczba podziałów: 7

Zadanie:
Zaimplementuj funkcję partitions(n), która zwraca liczbę podziałów n.
Wymagania:
- n może być duże (do ~200)
- wynik może być ogromny → zwracamy int
- użyj dynamicznego programowania lub memoizacji
- algorytm musi być znacznie szybszy niż brute force

Wskazówka:
Można użyć klasycznej rekurencji:
p(n, k) = p(n, k-1) + p(n-k, k)
gdzie p(n, k) to liczba podziałów n z maksymalnym składnikiem k.
"""
import random


def partitions(n: int) -> int:
    """
    Zwraca liczbę podziałów całkowitych liczby n.
    Implementacja oparta na klasycznej rekurencji z memoizacją.
    """

    memo = {}

    def p(n, k):
        if n == 0:
            return 1
        if n < 0 or k == 0:
            return 0
        if (n, k) in memo:
            return memo[(n, k)]
        # p(n, k) = p(n, k-1) + p(n-k, k)
        memo[(n, k)] = p(n, k - 1) + p(n - k, k)
        return memo[(n, k)]

    return p(n, n)


def _known_values():
    #
    return {
        1: 1,
        2: 2,
        3: 3,
        4: 5,
        5: 7,
        6: 11,
        7: 15,
        8: 22,
        9: 30,
        10: 42,
        20: 627,
        30: 5604,
        40: 37338,
        50: 204226,
    }


def test_basic():
    known = _known_values()
    for n, expected in known.items():
        assert partitions(n) == expected


def test_monotonicity():
    for i in range(1, 50):
        assert partitions(i + 1) >= partitions(i)


def test_zero_and_negative():
    assert partitions(0) == 1
    assert partitions(-5) == 0


def brute_partitions(n):
    if n == 0:
        return 1
    ways = 0

    def dfs(rem, last):
        nonlocal ways
        if rem == 0:
            ways += 1
            return
        for x in range(1, last + 1):
            if x <= rem:
                dfs(rem - x, x)

    dfs(n, n)
    return ways


def test_random_small():
    for _ in range(20):
        n = random.randint(1, 15)
        assert partitions(n) == brute_partitions(n)


if __name__ == "__main__":
    for i in [5, 10, 20, 50, 100, 150]:
        print(f"p({i}) = {partitions(i)}")
