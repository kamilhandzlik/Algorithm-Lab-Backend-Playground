"""
Szybkie mnożenie wielomianów za pomocą FFT (Fast Fourier Transform).

Dane są dwa wielomiany:
A(x) = a_0 + a_1 x + ... + a_{n-1} x^{n-1}
B(x) = b_0 + b_1 x + ... + b_{m-1} x^{m-1}

Reprezentujemy je jako listy współczynników: [a_0, a_1, ..., a_{n-1}] oraz [b_0, ..., b_{m-1}].

Zadanie:
Zaimplementuj funkcję multiply_polynomials(a, b), która zwraca listę współczynników
wielomianu C(x) = A(x) * B(x), obliczoną za pomocą FFT w czasie O(n log n).

Wymagania:
- obsługa współczynników rzeczywistych (float, int)
- wynik zaokrąglany do najbliższej liczby całkowitej
- poprawne działanie dla pustych i jednokrotnych wielomianów
"""

import math
import cmath
import random
import unittest


def _next_power_of_two(n: int) -> int:
    p = 1
    while p < n:
        p <<= 1
    return p


def _fft(a, invert: bool):
    n = len(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]

    length = 2
    while length <= n:
        ang = 2 * math.pi / length * (-1 if invert else 1)
        wlen = complex(math.cos(ang), math.sin(ang))
        for i in range(0, n, length):
            w = 1 + 0j
            for j in range(i, i + length // 2):
                u = a[j]
                v = a[j + length // 2] * w
                a[j] = u + v
                a[j + length // 2] = u - v
                w *= wlen
        length <<= 1

    if invert:
        for i in range(n):
            a[i] /= n


def multiply_polynomials(a, b):
    if not a or not b:
        return []
    n = len(a) + len(b) - 1
    size = _next_power_of_two(n)

    fa = [complex(x, 0) for x in a] + [0j] * (size - len(a))
    fb = [complex(x, 0) for x in b] + [0j] * (size - len(b))

    _fft(fa, False)
    _fft(fb, False)

    for i in range(size):
        fa[i] *= fb[i]

    _fft(fa, True)

    res = [int(round(fa[i].real)) for i in range(n)]
    while len(res) > 1 and res[-1] == 0:
        res.pop()
    return res


class TestFFTPolynomialMultiplication(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(multiply_polynomials([1], [1]), [1])
        self.assertEqual(multiply_polynomials([1, 1], [1, 1]), [1, 2, 1])
        self.assertEqual(multiply_polynomials([2, 0, 3], [1, 4]), [2, 8, 3, 12])

    def test_empty(self):
        self.assertEqual(multiply_polynomials([], []), [])
        self.assertEqual(multiply_polynomials([1, 2], []), [])
        self.assertEqual(multiply_polynomials([], [3, 4]), [])

    def test_random_small(self):
        def brute(a, b):
            n = len(a)
            m = len(b)
            if n == 0 or m == 0:
                return []
            res = [0] * (n + m - 1)
            for i in range(n):
                for j in range(m):
                    res[i + j] += a[i] * b[j]
            while len(res) > 1 and res[-1] == 0:
                res.pop()
            return res

        for _ in range(100):
            n = random.randint(0, 8)
            m = random.randint(0, 8)
            a = [random.randint(-5, 5) for _ in range(n)]
            b = [random.randint(-5, 5) for _ in range(m)]
            self.assertEqual(multiply_polynomials(a, b), brute(a, b))

    def test_large_structure(self):
        a = [1] * 128
        b = [1] * 128
        res = multiply_polynomials(a, b)
        self.assertEqual(len(res), 255)
        self.assertEqual(res[0], 1)
        self.assertEqual(res[-1], 1)
        self.assertEqual(res[127], 128)


if __name__ == "__main__":
    print(multiply_polynomials([1, 2, 3], [4, 5]))
    unittest.main()
