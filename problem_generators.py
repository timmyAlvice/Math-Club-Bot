import random
import sympy as sp

def generate_quadratic_problem():
    """Генерирует задачу для нахождения критических точек квадратичной функции."""
    x = sp.symbols('x')
    a = random.randint(1, 3)
    b = random.randint(-5, 5)
    c = random.randint(-5, 5)
    function = a*x**2 + b*x + c
    derivative = sp.diff(function, x)
    critical_points = sp.solve(derivative, x)

    solution_explanation = [
        f"Шаг 1: Находим производную функции: {derivative}",
        f"Шаг 2: Решаем уравнение для нахождения критических точек: {derivative} = 0"
    ]

    return function, critical_points, solution_explanation