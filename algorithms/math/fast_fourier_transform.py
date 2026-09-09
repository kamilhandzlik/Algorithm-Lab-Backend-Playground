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
"""
calculus_numerical.py

Problem description:
---------------------
Implement two numerical calculus routines and verify their correctness:

1. numerical_derivative(f, x, h=1e-5)
   Approximates f'(x) using the central difference formula:
       f'(x) ≈ (f(x + h) - f(x - h)) / (2h)

2. numerical_integral(f, a, b, n=1000)
   Approximates the definite integral ∫[a, b] f(x) dx using Simpson's Rule:
       ∫[a, b] f(x) dx ≈ (h/3) * [f(x0) + 4*f(x1) + 2*f(x2) + ... + 4*f(x_{n-1}) + f(xn)]
   where n must be even and h = (b - a) / n.

The correctness of both routines is checked against functions whose exact
derivatives / integrals are known analytically (polynomials, sin, exp, etc.),
as well as against randomly generated polynomials, where the exact result
can be computed symbolically from the coefficients.
"""

import math
import random
import unittest


def numerical_derivative(f, x, h=1e-5):
    """Approximate f'(x) via the central difference formula."""
    return (f(x + h) - f(x - h)) / (2 * h)


def numerical_integral(f, a, b, n=1000):
    """Approximate the definite integral of f over [a, b] using Simpson's Rule."""
    if n % 2 == 1:
        n += 1  # Simpson's rule requires an even number of subintervals

    h = (b - a) / n
    total = f(a) + f(b)

    for i in range(1, n):
        x_i = a + i * h
        coefficient = 4 if i % 2 == 1 else 2
        total += coefficient * f(x_i)

    return (h / 3) * total


def poly_value(coeffs, x):
    """Evaluate polynomial sum(c_i * x^i) at point x."""
    return sum(c * x**i for i, c in enumerate(coeffs))


def poly_integral_exact(coeffs, a, b):
    """Exact definite integral of a polynomial with given coefficients over [a, b]."""
    def antiderivative(x):
        return sum((c / (i + 1)) * x**(i + 1) for i, c in enumerate(coeffs))
    return antiderivative(b) - antiderivative(a)


def poly_derivative_exact(coeffs, x):
    """Exact derivative of a polynomial with given coefficients, evaluated at x."""
    return sum(i * c * x**(i - 1) for i, c in enumerate(coeffs) if i >= 1)


class TestNumericalDerivative(unittest.TestCase):
    def test_derivative_of_square(self):
        # f(x) = x^2, f'(x) = 2x
        result = numerical_derivative(lambda x: x**2, 3.0)
        self.assertAlmostEqual(result, 6.0, places=4)

    def test_derivative_of_sin(self):
        # f(x) = sin(x), f'(x) = cos(x)
        result = numerical_derivative(math.sin, math.pi / 4)
        self.assertAlmostEqual(result, math.cos(math.pi / 4), places=4)

    def test_derivative_of_exp(self):
        # f(x) = e^x, f'(x) = e^x
        result = numerical_derivative(math.exp, 1.0)
        self.assertAlmostEqual(result, math.exp(1.0), places=4)


class TestNumericalIntegral(unittest.TestCase):
    def test_integral_of_constant(self):
        # ∫[0,5] 3 dx = 15
        result = numerical_integral(lambda x: 3, 0, 5)
        self.assertAlmostEqual(result, 15.0, places=6)

    def test_integral_of_square(self):
        # ∫[0,1] x^2 dx = 1/3
        result = numerical_integral(lambda x: x**2, 0, 1)
        self.assertAlmostEqual(result, 1 / 3, places=6)

    def test_integral_of_sin(self):
        # ∫[0, pi] sin(x) dx = 2
        result = numerical_integral(math.sin, 0, math.pi)
        self.assertAlmostEqual(result, 2.0, places=6)


class TestRandomizedAgainstAnalytical(unittest.TestCase):
    """Randomized tests comparing numerical results with exact analytical formulas
    for randomly generated polynomials."""

    def setUp(self):
        random.seed()  # non-deterministic seed each run

    def test_random_polynomial_integrals(self):
        for _ in range(20):
            degree = random.randint(1, 5)
            coeffs = [random.uniform(-10, 10) for _ in range(degree + 1)]
            a = random.uniform(-5, 5)
            b = a + random.uniform(0.1, 5)

            expected = poly_integral_exact(coeffs, a, b)
            actual = numerical_integral(lambda x: poly_value(coeffs, x), a, b, n=2000)

            self.assertAlmostEqual(actual, expected, places=3)

    def test_random_polynomial_derivatives(self):
        for _ in range(20):
            degree = random.randint(1, 5)
            coeffs = [random.uniform(-10, 10) for _ in range(degree + 1)]
            x = random.uniform(-5, 5)

            expected = poly_derivative_exact(coeffs, x)
            actual = numerical_derivative(lambda x: poly_value(coeffs, x), x)

            self.assertAlmostEqual(actual, expected, places=3)


if __name__ == "__main__":
    unittest.main()