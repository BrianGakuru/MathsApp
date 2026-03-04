import streamlit as st
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from scipy.integrate import odeint

st.set_page_config(page_title="Academic Mathematics Lab", layout="wide")

st.title("🎓 Academic Mathematics Visualization Lab")
st.markdown("An interactive demonstration tool for university-level mathematics.")

tabs = st.tabs([
    "📈 Function Analysis",
    "🔢 Matrix Laboratory",
    "📉 Differential Equations",
    "📐 Linear Systems"
])

# ============================================================
# 1️⃣ FUNCTION ANALYSIS
# ============================================================

with tabs[0]:

    st.header("Function Visualization & Calculus")

    x = sp.symbols('x')
    function_input = st.text_input("Enter function in x:", "sin(x) + x**2")

    if function_input:
        try:
            expr = sp.sympify(function_input)

            st.latex(f"f(x) = {sp.latex(expr)}")

            # Derivatives
            first_derivative = sp.diff(expr, x)
            second_derivative = sp.diff(expr, x, 2)

            st.subheader("First Derivative")
            st.latex(sp.latex(first_derivative))

            st.subheader("Second Derivative")
            st.latex(sp.latex(second_derivative))

            # Plot
            f = sp.lambdify(x, expr, "numpy")
            x_vals = np.linspace(-10, 10, 400)
            y_vals = f(x_vals)

            fig, ax = plt.subplots()
            ax.plot(x_vals, y_vals)
            ax.set_title("Function Plot")
            ax.grid(True)

            st.pyplot(fig)

        except:
            st.error("Invalid function.")

# ============================================================
# 2️⃣ MATRIX LAB
# ============================================================

with tabs[1]:

    st.header("Matrix Operations Laboratory")

    size = st.slider("Matrix size (NxN)", 2, 4)

    matrix = []
    for i in range(size):
        row = st.text_input(f"Row {i+1} (comma separated)", key=f"m{i}")
        if row:
            matrix.append([float(val) for val in row.split(",")])

    if len(matrix) == size:
        A = np.array(matrix)

        st.subheader("Matrix A")
        st.latex(sp.latex(sp.Matrix(A)))

        st.write("Determinant:")
        st.latex(sp.latex(sp.Matrix(A).det()))

        try:
            st.write("Inverse:")
            st.latex(sp.latex(sp.Matrix(A).inv()))
        except:
            st.write("Matrix not invertible.")

        st.write("Eigenvalues:")
        eigenvals = sp.Matrix(A).eigenvals()
        st.write(eigenvals)

# ============================================================
# 3️⃣ DIFFERENTIAL EQUATIONS
# ============================================================

with tabs[2]:

    st.header("First-Order Differential Equation Solver")
    st.markdown("Solve equations of form: dy/dx = f(y, x)")

    equation = st.text_input("Enter f(y, x):", "x - y")
    y0 = st.number_input("Initial condition y(0):", value=1.0)

    if equation:
        try:
            x = sp.symbols('x')
            y = sp.symbols('y')
            expr = sp.sympify(equation)

            st.latex(r"\frac{dy}{dx} = " + sp.latex(expr))

            f = sp.lambdify((y, x), expr, "numpy")

            def model(y, x):
                return f(y, x)

            x_vals = np.linspace(0, 10, 200)
            solution = odeint(model, y0, x_vals)

            fig, ax = plt.subplots()
            ax.plot(x_vals, solution)
            ax.set_title("ODE Solution Curve")
            ax.grid(True)

            st.pyplot(fig)

        except:
            st.error("Invalid equation.")

# ============================================================
# 4️⃣ LINEAR SYSTEMS
# ============================================================

with tabs[3]:

    st.header("Solve Linear System Ax = b")

    size = st.slider("Number of variables", 2, 4, key="linear")

    A = []
    for i in range(size):
        row = st.text_input(f"A Row {i+1}", key=f"A{i}")
        if row:
            A.append([float(val) for val in row.split(",")])

    b_input = st.text_input("Vector b (comma separated)")

    if len(A) == size and b_input:
        A_matrix = np.array(A)
        b = np.array([float(val) for val in b_input.split(",")])

        try:
            solution = np.linalg.solve(A_matrix, b)
            st.subheader("Solution Vector")
            st.write(solution)
        except:
            st.error("System has no unique solution.")