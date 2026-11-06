import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Configuración de la página
st.set_page_config(
    page_title="UCACUE - Calculadora de Estática",
    page_icon="🏗️",
    layout="wide"
)

# Encabezado principal
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>UCACUE</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #4B5563;'>Facultad de Ingeniería - Cátedra de Estática</h3>",
            unsafe_allow_html=True)
st.markdown("---")

# Sidebar - Parámetros de entrada
st.sidebar.header("⚙️ Configuración de la Viga")

tipo_apoyo = st.sidebar.selectbox(
    "Selecciona el tipo de viga:",
    ["Simplemente Apoyada (Apoyo Fijo A + Apoyo Móvil B)", "Viga en Voladizo (Empotramiento en A)"]
)

longitud_viga = st.sidebar.number_input("Longitud total de la viga L (m):", min_value=1.0, max_value=20.0, value=6.0,
                                        step=0.5)

st.sidebar.subheader("📌 Cargas Aplicadas")
fuerza_p = st.sidebar.number_input("Fuerza Puntual P (kN):", min_value=0.0, max_value=500.0, value=20.0, step=1.0)
angulo_p = st.sidebar.slider("Ángulo de P (grados respecto a la horizontal):", 0, 180, 90)
posicion_p = st.sidebar.slider("Posición de la fuerza P (m desde A):", 0.0, float(longitud_viga), longitud_viga / 2)

carga_w = st.sidebar.number_input("Carga Distribuida w (kN/m):", min_value=0.0, max_value=100.0, value=5.0, step=0.5)

# Conversión de ángulos a radianes
rad = np.radians(angulo_p)
px = fuerza_p * np.cos(rad)
py = fuerza_p * np.sin(rad)

# Cálculos de Reacciones
if tipo_apoyo == "Simplemente Apoyada (Apoyo Fijo A + Apoyo Móvil B)":
    # ΣFx = 0 -> Ax + Px = 0  => Ax = -Px
    ax = -px

    # ΣMA = 0 -> (Py * pos_p) + (w * L * L/2) - (By * L) = 0
    by = ((py * posicion_p) + (carga_w * longitud_viga * (longitud_viga / 2))) / longitud_viga

    # ΣFy = 0 -> Ay + By - Py - (w * L) = 0 => Ay = Py + (w * L) - By
    ay = py + (carga_w * longitud_viga) - by
    ma = 0.0

else:  # Empotramiento en A
    # ΣFx = 0 -> Ax + Px = 0  => Ax = -Px
    ax = -px

    # ΣFy = 0 -> Ay - Py - (w * L) = 0 => Ay = Py + (w * L)
    ay = py + (carga_w * longitud_viga)
    by = 0.0

    # ΣMA = 0 -> MA - (Py * pos_p) - (w * L * L/2) = 0 => MA = (Py * pos_p) + (w * L^2 / 2)
    ma = (py * posicion_p) + (carga_w * longitud_viga * (longitud_viga / 2))

# Layout Principal: Gráfico a la izquierda, Resultados a la derecha
col_grafico, col_resultados = st.columns([1.2, 1])

with col_grafico:
    st.subheader("🎨 Diagrama de Cuerpo Libre (DCL)")

    fig, ax_plt = plt.subplots(figsize=(8, 4))

    # Dibujar la viga
    ax_plt.plot([0, longitud_viga], [0, 0], color="black", linewidth=8, label="Viga")

    # Dibujar Apoyos en A y B
    if tipo_apoyo == "Simplemente Apoyada (Apoyo Fijo A + Apoyo Móvil B)":
        # Apoyo Fijo en A (Triángulo)
        triangulo_a = plt.Polygon([[-0.2, -0.4], [0.2, -0.4], [0, 0]], color="red")
        ax_plt.add_patch(triangulo_a)
        ax_plt.text(0, -0.7, "A (Fijo)", horizontalalignment='center', fontweight='bold')

        # Apoyo Móvil en B (Círculo)
        circulo_b = plt.Circle((longitud_viga, -0.2), 0.2, color="blue")
        ax_plt.add_patch(circulo_b)
        ax_plt.text(longitud_viga, -0.7, "B (Móvil)", horizontalalignment='center', fontweight='bold')
    else:
        # Empotramiento en A (Línea tramada vertical)
        ax_plt.plot([0, 0], [-0.8, 0.8], color="brown", linewidth=6)
        for y_hatch in np.linspace(-0.8, 0.8, 9):
            ax_plt.plot([-0.3, 0], [y_hatch - 0.1, y_hatch], color="brown", linewidth=2)
        ax_plt.text(0, -1.1, "A (Empotramiento)", horizontalalignment='center', fontweight='bold')

    # Dibujar Fuerza Puntual P
    if fuerza_p > 0:
        dx = -0.8 * np.cos(rad)
        dy = -0.8 * np.sin(rad)
        ax_plt.arrow(posicion_p - dx, -dy, dx, dy, head_width=0.15, head_length=0.15, fc='green', ec='green',
                     linewidth=2)
        ax_plt.text(posicion_p, 0.3, f'P = {fuerza_p} kN', color='green', fontweight='bold',
                    horizontalalignment='center')

    # Dibujar Carga Distribuida w
    if carga_w > 0:
        x_w = np.linspace(0, longitud_viga, 10)
        for xw in x_w:
            ax_plt.arrow(xw, 0.6, 0, -0.4, head_width=0.08, head_length=0.1, fc='orange', ec='orange')
        ax_plt.plot([0, longitud_viga], [0.6, 0.6], color='orange', linestyle='--')
        ax_plt.text(longitud_viga / 2, 0.75, f'w = {carga_w} kN/m', color='orange', fontweight='bold',
                    horizontalalignment='center')

    # Ajustes estéticos de la gráfica
    ax_plt.set_xlim(-1, longitud_viga + 1)
    ax_plt.set_ylim(-1.5, 1.5)
    ax_plt.set_aspect('equal')
    ax_plt.axis('off')
    st.pyplot(fig)

with col_resultados:
    st.subheader("📊 Resultados de las Reacciones")

    st.metric(label="Reacción Horizontal en A ($A_x$)", value=f"{ax:.2f} kN")
    st.metric(label="Reacción Vertical en A ($A_y$)", value=f"{ay:.2f} kN")

    if tipo_apoyo == "Simplemente Apoyada (Apoyo Fijo A + Apoyo Móvil B)":
        st.metric(label="Reacción Vertical en B ($B_y$)", value=f"{by:.2f} kN")
    else:
        st.metric(label="Momento de Empotramiento en A ($M_A$)", value=f"{ma:.2f} kN·m")

st.markdown("---")

# Sección paso a paso de las ecuaciones de equilibrio
with st.expander("📖 **Ver paso a paso el cálculo de ecuaciones de equilibrio**"):
    st.markdown("### 1. Descomposición de Fuerzas")
    st.latex(rf"P_x = P \cdot \cos(\theta) = {fuerza_p} \cdot \cos({angulo_p}^\circ) = {px:.2f} \text{{ kN}}")
    st.latex(rf"P_y = P \cdot \sin(\theta) = {fuerza_p} \cdot \sin({angulo_p}^\circ) = {py:.2f} \text{{ kN}}")

    st.markdown("### 2. Sumatoria de Fuerzas en $X$ ($\sum F_x = 0$)")
    st.latex(rf"A_x + P_x = 0 \implies A_x = -({px:.2f}) = \mathbf{{{ax:.2f} \text{{ kN}}}}")

    if tipo_apoyo == "Simplemente Apoyada (Apoyo Fijo A + Apoyo Móvil B)":
        st.markdown("### 3. Sumatoria de Momentos en $A$ ($\sum M_A = 0$)")
        st.latex(rf"(P_y \cdot x_P) + \left(w \cdot L \cdot \frac{{L}}{{2}}\right) - (B_y \cdot L) = 0")
        st.latex(
            rf"({py:.2f} \cdot {posicion_p}) + \left({carga_w} \cdot {longitud_viga} \cdot \frac{{{longitud_viga}}}{{2}}\right) - (B_y \cdot {longitud_viga}) = 0")
        st.latex(rf"B_y = \mathbf{{{by:.2f} \text{{ kN}}}}")

        st.markdown("### 4. Sumatoria de Fuerzas en $Y$ ($\sum F_y = 0$)")
        st.latex(rf"A_y + B_y - P_y - (w \cdot L) = 0")
        st.latex(
            rf"A_y + {by:.2f} - {py:.2f} - ({carga_w} \cdot {longitud_viga}) = 0 \implies A_y = \mathbf{{{ay:.2f} \text{{ kN}}}}")
    else:
        st.markdown("### 3. Sumatoria de Fuerzas en $Y$ ($\sum F_y = 0$)")
        st.latex(
            rf"A_y - P_y - (w \cdot L) = 0 \implies A_y = {py:.2f} + ({carga_w} \cdot {longitud_viga}) = \mathbf{{{ay:.2f} \text{{ kN}}}}")

        st.markdown("### 4. Sumatoria de Momentos en $A$ ($\sum M_A = 0$)")
        st.latex(rf"M_A - (P_y \cdot x_P) - \left(w \cdot L \cdot \frac{{L}}{{2}}\right) = 0")
        st.latex(
            rf"M_A = ({py:.2f} \cdot {posicion_p}) + \left({carga_w} \cdot {longitud_viga} \cdot \frac{{{longitud_viga}}}{{2}}\right) = \mathbf{{{ma:.2f} \text{{ kN}}\cdot\text{{m}}}}")