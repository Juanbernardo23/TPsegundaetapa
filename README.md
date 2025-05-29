# 🧠 Math Solver con Pix2Tex

Este es un programa web que permite resolver problemas matemáticos a partir de una **imagen**. Utiliza **Pix2Tex** para reconocer expresiones en LaTeX desde una imagen, y **SymPy** para resolverlas simbólicamente o gráficamente. El resultado se presenta de forma clara con **MathJax** y gráficos generados dinámicamente (por ejemplo, parábolas).

---

## 🚀 ¿Qué puede hacer este programa?

- ✅ Leer expresiones matemáticas desde una imagen (`.png`, `.jpg`, etc.)
- ✅ Detectar y resolver:
  - Ecuaciones cuadráticas y graficarlas
  - Sistemas de ecuaciones lineales
  - Matrices y determinantes
  - Vectores (próximamente análisis vectorial)
  - Funciones polinómicas, exponenciales y logarítmicas
  - Cónicas (en progreso)
  - Funciones definidas como `y = f(x)`
- ✅ Mostrar el ejercicio detectado en LaTeX
- ✅ Presentar la solución con formato limpio (MathJax)
- ✅ Generar gráficos si corresponde (por ejemplo, parábolas)

---

## 📁 Estructura de Archivos

### `1. app.py` – 🌐 Servidor Flask

- Lanza la aplicación web en `localhost`.
- Recibe la imagen del usuario.
- Llama a `solve_from_image()` y envía los resultados al HTML.
- Muestra:
  - El ejercicio en LaTeX
  - La solución simbólica o textual
  - La gráfica (si aplica)

---

### `2. ocr_and_solver.py` – 🧠 Lógica de OCR + resolución

- Usa `Pix2Tex` (`LatexOCR`) para convertir una imagen en texto LaTeX.
- Limpia el LaTeX con `clean_latex_expr()` para evitar errores de OCR.
- Detecta automáticamente el tipo de ejercicio (cuadrática, sistema, matriz, etc.).
- Resuelve simbólicamente con `SymPy`.
- Dibuja gráficos con `matplotlib` si aplica (por ejemplo, parábolas).
- Devuelve:
  - La expresión original
  - La solución
  - La ruta de la gráfica (si existe)

---

### `3. index.html` – 🖥️ Interfaz Web

- Permite subir una imagen.
- Muestra:
  - El LaTeX renderizado con **MathJax**
  - La solución renderizada
  - Una gráfica si se generó
- Estilo limpio y moderno con HTML + CSS básico.

---

## 📘 Glosario

| Término               | Significado                                                                 |
|-----------------------|------------------------------------------------------------------------------|
| **Pix2Tex**           | Modelo que convierte una imagen con fórmulas matemáticas en código LaTeX.   |
| **SymPy**             | Librería de Python para álgebra simbólica (resolver, simplificar, etc.).     |
| **MathJax**           | Librería JavaScript que renderiza LaTeX en el navegador.                    |
| **Flask**             | Microframework web en Python usado para construir la app.                   |
| **LaTeX**             | Lenguaje de marcado usado para escribir fórmulas matemáticas.               |
| **`solve()`**         | Función de SymPy para resolver ecuaciones.                                  |
| **`parse_latex()`**   | Convierte una expresión LaTeX a una forma que SymPy pueda manipular.        |
| **`plot_parabola()`** | Función que genera una imagen de la parábola correspondiente.               |
| **Sistema de ecuaciones** | Conjunto de ecuaciones que se resuelven en simultáneo.                    |
| **Cónica**            | Figura geométrica (circunferencia, parábola, elipse, hipérbola).            |

---

## 🛠 Requisitos

- Python 3.8+
- Librerías:
  - `flask`
  - `sympy`
  - `matplotlib`
  - `pix2tex` (requiere instalación de `torch` y modelos OCR)

---

## 📌 Cómo ejecutar

```bash
python app.py
