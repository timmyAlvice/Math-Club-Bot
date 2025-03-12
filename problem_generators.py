import random
import sympy as sp
import matplotlib.pyplot as plt
from io import BytesIO


def get_expression_img(expression: str) -> plt.figure:
    expression = f"${expression}$"

    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()

    t = ax.text(
        0.5, 0.5, expression,
        horizontalalignment='center',
        verticalalignment='center',
        fontsize=20, color='black'
    )

    ax.figure.canvas.draw()
    bbox = t.get_window_extent()
    # dpi=80
    fig.set_size_inches(
        bbox.width / 80, 
        bbox.height / 80
    )

    # buf = BytesIO()
    # fig.savefig(buf, format='png', bbox_inches='tight')
    # buf.seek(0)
    fig.savefig('tmp.png', bbox_inches='tight')
    plt.close()


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
        f"Шаг 2: Решаем уравнение для нахождения критических точек: {derivative} = 0",
    ]

    get_expression_img(f"f(x) = {sp.latex(function)}")

    return function, critical_points, solution_explanation