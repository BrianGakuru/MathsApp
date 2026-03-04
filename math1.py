import streamlit as st
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import pandas as pd

st.set_page_config(page_title="Mathematics Visualizer", layout="wide")

st.title("📊 Advanced Mathematics Visualizer App")

menu = st.sidebar.selectbox(
    "Select Module",
    [
        "Function Plotter",
        "Matrix Operations",
        "Differential Equations",
        "System of Linear Equations"
    ]
)

# =====================================================
# FUNCTION PLOTTER
# =====================================================

if menu == "Function Plotter":

    st.header("📈 Function Visualizer")

    x = sp.symbols('x')
    user_function = st.text_input("Enter a function in x (e.g., sin(x) + x**2):")

    if user_function:
        try:
            expr = sp.sympify(user_function)
            f = sp.lambdify(x, expr, "numpy")

            x_vals = np.linspace(-10, 10, 400)
            y_vals = f(x_vals)

            fig, ax = plt.subplots()
            ax.plot(x_vals, y_vals)
            ax.set_title(f"Graph of {user_function}")
            ax.grid(True)

            st.pyplot(fig)

        except:
            st.error("Invalid function expression.")

# =====================================================
# MATRIX OPERATIONS
# =====================================================

elif menu == "Matrix Operations":

    st.header("🔢 Matrix Calculator")

    size = st.slider("Select Matrix Size (NxN)", 2, 5)

    st.write("Enter matrix values:")

    matrix_input = []
    for i in range(size):
        row = st.text_input(f"Row {i+1} (comma separated)", key=i)
        if row:
            matrix_input.append([float(val) for val in row.split(",")])

    if len(matrix_input) == size:
        A = np.array(matrix_input)

        st.write("### Matrix A")
        st.write(A)

        st.write("Determinant:", np.linalg.det(A))
        st.write("Inverse:")
        try:
            st.write(np.linalg.inv(A))
        except:
            st.write("Matrix not invertible")

        st.write("Eigenvalues:")
        st.write(np.linalg.eigvals(A))

# =====================================================
# DIFFERENTIAL EQUATIONS
# =====================================================

elif menu == "Differential Equations":

    st.header("📉 Solve First-Order ODE")

    st.write("Equation form: dy/dx = f(y, x)")

    equation = st.text_input("Enter f(y, x) (e.g., x - y):")

    y0 = st.number_input("Initial condition y(0) =", value=1.0)

    if equation:

        try:
            x = sp.symbols('x')
            y = sp.symbols('y')
            expr = sp.sympify(equation)

            f = sp.lambdify((y, x), expr, "numpy")

            def model(y, x):
                return f(y, x)

            x_vals = np.linspace(0, 10, 200)
            solution = odeint(model, y0, x_vals)

            fig, ax = plt.subplots()
            ax.plot(x_vals, solution)
            ax.set_title("ODE Solution")
            ax.grid(True)

            st.pyplot(fig)

        except:
            st.error("Invalid differential equation.")

# =====================================================
# SYSTEM OF LINEAR EQUATIONS
# =====================================================

elif menu == "System of Linear Equations":

    st.header("📐 Solve Linear System Ax = b")

    size = st.slider("Number of Variables", 2, 5)

    st.write("Enter coefficient matrix A:")

    A_input = []
    for i in range(size):
        row = st.text_input(f"A Row {i+1} (comma separated)", key=f"A{i}")
        if row:
            A_input.append([float(val) for val in row.split(",")])

    b_input = st.text_input("Enter RHS vector b (comma separated)")

    if len(A_input) == size and b_input:
        A = np.array(A_input)
        b = np.array([float(val) for val in b_input.split(",")])

        try:
            solution = np.linalg.solve(A, b)
            st.write("### Solution Vector x")
            st.write(solution)
        except:
            st.write("System cannot be solved.")