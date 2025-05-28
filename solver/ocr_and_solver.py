from PIL import Image
from pix2tex.cli import LatexOCR
from sympy.parsing.latex import parse_latex
from sympy import Eq, solve, sympify, symbols
import re
import matplotlib.pyplot as plt
import numpy as np

model = LatexOCR()

def analyze_quadratic(expr):
    x = symbols('x')
    poly = expr.rhs
    a = poly.coeff(x, 2)
    b = poly.coeff(x, 1)
    c = poly.coeff(x, 0)

    vertex_x = -b / (2*a)
    vertex_y = poly.subs(x, vertex_x)
    y_intercept = c
    x_intercepts = solve(poly, x)

    return {
        "a": a,
        "b": b,
        "c": c,
        "vertex": (vertex_x, vertex_y),
        "x_intercepts": x_intercepts,
        "y_intercept": y_intercept
    }

def plot_parabola(a, b, c, filepath='static/uploads/plot.png'):
    x = np.linspace(-10, 10, 400)
    y = a * x**2 + b * x + c
    plt.figure()
    plt.plot(x, y, label=f'y = {a}x² + {b}x + {c}')
    plt.axhline(0, color='black', lw=0.5)
    plt.axvline(0, color='black', lw=0.5)
    plt.scatter([0], [c], color='blue', label=f'Intersección eje Y: (0, {c})')
    plt.legend()
    plt.grid(True)
    plt.savefig(filepath)
    plt.close()

def clean_latex_expr(latex):
    cleaned = re.sub(r"\\(mathbf|mathrm|text|mathit)\s*\{([^{}]*)\}", r"\2", latex)
    cleaned = cleaned.replace(r"\scriptstyle", "").strip()
    return cleaned

def solve_from_image(image_path):
    try:
        img = Image.open(image_path).convert("RGB")
        latex_raw = model(img)
        print(f"Ejercicio detectado (raw): {latex_raw}")

        latex = clean_latex_expr(latex_raw)
        print(f"Ejercicio detectado: {latex}")

        if not latex:
            return latex, "No se detectó ninguna expresión."

        # ----------- Sistema de ecuaciones -----------
        if r"\\" in latex or r"\begin{cases}" in latex:
            print("Sistema de ecuaciones detectado")

            # Limpiar delimitadores de sistemas
            latex = latex.replace(r"\begin{cases}", "").replace(r"\end{cases}", "")
            ecuaciones_latex = [e.strip() for e in latex.split(r"\\") if e.strip()]
            ecuaciones = [parse_latex(eq) for eq in ecuaciones_latex]

            sol = solve(ecuaciones)
            return latex, f"Soluciones del sistema: {sol}"

        # ----------- Expresión o ecuación individual -----------
        expr = parse_latex(latex)

        if isinstance(expr, Eq):
            lhs, rhs = expr.lhs, expr.rhs
            variables = expr.free_symbols

            # Función explícita: y = x^2 + 3
            if len(variables) == 2 and lhs.is_Symbol:
                from sympy import latex as sympy_latex  # arriba del archivo
                return latex, f"{sympy_latex(lhs)} \\text{{ está definido como }} {sympy_latex(rhs)}"

            if len(variables) == 1:
                var = list(variables)[0]
                sol = solve(expr, var)
                return latex, f"{var}: {sol}"
            else:
                sol = solve(expr)
                return latex, f"{sol}"

        else:
            # Expresión simbólica (sin igualdad)
            sol = sympify(str(expr))
            return latex, f"Resultado simbólico: {sol}"

    except Exception as e:
        return None, f"Ocurrió un error: {e}"
