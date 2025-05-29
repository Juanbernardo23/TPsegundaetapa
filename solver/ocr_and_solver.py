from PIL import Image
from pix2tex.cli import LatexOCR
from sympy.parsing.latex import parse_latex
from sympy import Eq, solve, sympify, symbols, Matrix
from sympy import latex as sympy_latex
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
    cleaned = re.sub(r"\\left|\\right", "", cleaned)
    cleaned = cleaned.replace("{", "(").replace("}", ")")
    cleaned = re.sub(r"\^\(([^()]+)\)", r"^\1", cleaned)
    return cleaned

def detectar_tipo_ejercicio(latex):
    if r"\begin{bmatrix}" in latex or r"\begin{pmatrix}" in latex:
        return "matriz"
    if r"\begin{cases}" in latex or r"\\" in latex:
        return "sistema"
    if "det" in latex or r"\left|" in latex:
        return "determinante"
    if re.search(r"\(([^()]+),([^()]+)\)", latex):  # (x, y)
        return "vector"
    if re.search(r"x\^?2", latex):
        return "cuadratica"
    if re.search(r"(x|y)\s*=", latex):
        return "funcion"
    if "log" in latex:
        return "logaritmica"
    if "e^" in latex:
        return "exponencial"
    if re.search(r"Ax\^2.*By\^2", latex) or "cónica" in latex:
        return "conica"
    return "desconocido"

def solve_from_image(image_path):
    try:
        img = Image.open(image_path).convert("RGB")
        latex_raw = model(img)
        print(f"Ejercicio detectado (raw): {latex_raw}")

        latex = clean_latex_expr(latex_raw)
        print(f"Ejercicio detectado: {latex}")

        if not latex:
            return latex, "No se detectó ninguna expresión."

        tipo = detectar_tipo_ejercicio(latex)
        print(f"Tipo de ejercicio detectado: {tipo}")

        if tipo == "sistema":
            print("Sistema de ecuaciones detectado")
            latex = latex.replace(r"\begin{cases}", "").replace(r"\end{cases}", "")
            ecuaciones_latex = [e.strip() for e in latex.split(r"\\") if e.strip()]
            ecuaciones = [parse_latex(eq) for eq in ecuaciones_latex]
            sol = solve(ecuaciones)
            return latex, f"Soluciones del sistema: {sol}"
        
        elif tipo == "funcion":
            expr = parse_latex(latex)
            if isinstance(expr, Eq) and expr.lhs.name == "y":
                return latex, f"\\text{{Función detectada: }} y = {sympy_latex(expr.rhs)}"

        elif tipo == "logaritmica":
            expr = parse_latex(latex)
            return latex, f"\\text{{Función logarítmica detectada: }} {sympy_latex(expr)}"

        elif tipo == "exponencial":
            expr = parse_latex(latex)
            return latex, f"\\text{{Función exponencial detectada: }} {sympy_latex(expr)}"

        elif tipo == "conica":
            expr = parse_latex(latex)
            return latex, f"\\text{{Ecuación cónica detectada: }} {sympy_latex(expr)}"

        elif tipo == "vector":
            return latex, "\\text{Se detectó un vector. (Pronto se implementará análisis)}"

        elif tipo == "matriz":
            from sympy import Matrix
            matrix = parse_latex(latex)
            det = matrix.det()
            return latex, f"Determinante de la matriz: {det}"

        elif tipo == "cuadratica":
            expr = parse_latex(latex)
            if isinstance(expr, Eq) and expr.lhs.name == "y":
                analisis = analyze_quadratic(expr)
                plot_path = 'static/uploads/plot.png'
                plot_parabola(analisis["a"], analisis["b"], analisis["c"], filepath=plot_path)
                from sympy import latex as sympy_latex
                raices = analisis["x_intercepts"]
                if len(raices) == 2 and raices[0] == -raices[1]:
                    raiz_latex = fr"\pm {sympy_latex(abs(raices[1]))}"
                else:
                    raiz_latex = sympy_latex(raices)
                resultado = (
                    r"\begin{aligned}"
                    fr"\text{{Vértice:}} &\quad {analisis['vertex']} \\\\"
                    fr"\text{{Intersección con el eje }} y: &\quad (0, {analisis['y_intercept']}) \\\\"
                    fr"\text{{Raíces (x):}} &\quad {raiz_latex}"
                    r"\end{aligned}"
)
                return latex, resultado, plot_path
            else:
                return latex, "No se pudo interpretar como una parábola de la forma y = ax^2 + bx + c"

        elif tipo == "vector":
            return latex, "Se detectó un vector. (Análisis por implementar)"

        else:
            expr = parse_latex(latex)
            if isinstance(expr, Eq):
                lhs, rhs = expr.lhs, expr.rhs
                variables = expr.free_symbols
                if len(variables) == 2 and lhs.is_Symbol:
                    from sympy import latex as sympy_latex
                    return latex, f"{sympy_latex(lhs)} \\text{{ está definido como }} {sympy_latex(rhs)}"
                elif len(variables) == 1:
                    var = list(variables)[0]
                    sol = solve(expr, var)
                    return latex, f"{var}: {sol}"
                else:
                    sol = solve(expr)
                    return latex, f"{sol}"
            else:
                sol = sympify(str(expr))
                return latex, f"Resultado simbólico: {sol}"

    except Exception as e:
        return None, f"Ocurrió un error: {e}"