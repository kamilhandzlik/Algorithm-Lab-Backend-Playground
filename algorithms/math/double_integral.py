import numpy as np
import matplotlib.pyplot as plt
import random

# W numpy >= 2.0 funkcja nazywa się `trapezoid`, w starszych wersjach `trapz`
_trapz = getattr(np, "trapezoid", None) or np.trapz


def double_integral(f, ax, bx, ay, by, nx=200, ny=200):
    """
    Numeryczne liczenie całki podwójnej na prostokącie [ax,bx] x [ay,by]
    metodą trapezów (dwukrotne całkowanie trapezoidalne - dokładniejsze
    niż zwykła suma Riemanna na siatce z liniowymi punktami końcowymi).
    """
    x = np.linspace(ax, bx, nx)
    y = np.linspace(ay, by, ny)

    xx, yy = np.meshgrid(x, y)
    values = np.asarray(f(xx, yy), dtype=float)

    # f może zwrócić skalar (np. funkcja stała ignorująca x, y) -
    # trzeba go rozgłosić (broadcast) na kształt siatki
    if values.shape != xx.shape:
        values = np.broadcast_to(values, xx.shape)

    # Całkujemy najpierw po x (dla każdego y), potem wynik po y
    integral_over_x = _trapz(values, x, axis=1)
    result = _trapz(integral_over_x, y)

    return result


def plot_function(f, ax, bx, ay, by, resolution=200):
    """
    Generuje wykres 3D funkcji f(x,y) na zadanym obszarze.
    """
    x = np.linspace(ax, bx, resolution)
    y = np.linspace(ay, by, resolution)
    xx, yy = np.meshgrid(x, y)
    zz = f(xx, yy)

    fig = plt.figure(figsize=(10, 6))
    ax3d = fig.add_subplot(111, projection='3d')
    ax3d.plot_surface(xx, yy, zz, cmap='viridis')
    ax3d.set_title("Wizualizacja funkcji f(x,y)")
    ax3d.set_xlabel("x")
    ax3d.set_ylabel("y")
    ax3d.set_zlabel("f(x,y)")
    plt.tight_layout()
    return fig


def test_constant_function():
    f = lambda x, y: 5
    result = double_integral(f, 0, 2, 0, 3)
    assert np.isclose(result, 5 * 2 * 3, atol=1e-2)


def test_linear_function():
    f = lambda x, y: x + y

    # ∫0^1 ∫0^1 (x+y) dx dy = 1
    result = double_integral(f, 0, 1, 0, 1)
    assert np.isclose(result, 1.0, atol=1e-2)


def test_quadratic_function():
    f = lambda x, y: x ** 2 + y ** 2
    # ∫0^1 ∫0^1 (x^2 + y^2) dx dy = 2/3
    result = double_integral(f, 0, 1, 0, 1)
    assert np.isclose(result, 2 / 3, atol=1e-2)


def test_asymmetric_domain():
    f = lambda x, y: x * y
    # ∫1^2 ∫0^3 xy dx dy = (∫1^2 x dx)*(∫0^3 y dy) = (3/2)*(9/2) = 27/4
    result = double_integral(f, 1, 2, 0, 3)
    assert np.isclose(result, 27 / 4, atol=1e-2)


def test_random_positive_functions():
    for _ in range(50):
        ax, bx = sorted([random.uniform(0, 5), random.uniform(0, 5)])
        ay, by = sorted([random.uniform(0, 5), random.uniform(0, 5)])

        scale = random.uniform(0.1, 5)
        f = lambda x, y, s=scale: s * (np.sin(x) ** 2 + np.cos(y) ** 2)

        result = double_integral(f, ax, bx, ay, by)

        assert result >= 0
        assert result <= scale * (bx - ax) * (by - ay) * 2  # górne ograniczenie


if __name__ == "__main__":
    test_linear_function()
    test_quadratic_function()
    test_constant_function()
    test_asymmetric_domain()
    test_random_positive_functions()
    print("Wszystkie testy przeszły pomyślnie.")