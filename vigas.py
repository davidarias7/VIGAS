import streamlit as st
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
posicion_p = st.sidebar.slider("Posición de la fuerza P (m desde A):", 0.0, float(longitud_viga),
                               float(longitud_viga / 2))

carga_w = st.sidebar.number_input("Carga Distribuida w (kN/m):", min_value=0.0, max_value=100.0, value=5.0, step=0.5)

# Conversión de ángulos a radianes
rad = np.radians(angulo_p)
px = fuerza_p * np.cos(rad)
py = fuerza_p * np.sin(rad)

# Cálculos de Reacciones
if tipo_apoyo == "Simplemente Apoyada (Apoyo Fijo A + Apoyo Móvil B)":
    ax = -px
    by = ((py * posicion_p) + (carga_w * longitud_viga * (longitud_viga / 2))) / longitud_viga
    ay = py + (carga_w * longitud_viga) - by
    ma = 0.0
else:  # Empotramiento en A
    ax = -px
    ay = py + (carga_w * longitud_viga)
    by = 0.0
    ma = (py * posicion_p) + (carga_w * longitud_viga * (longitud_viga / 2))

# Layout Principal: Esquema visual y Resultados
col_grafico, col_resultados = st.columns([1.2, 1])

with col_grafico:
    st.subheader("🎨 Diagrama de Cuerpo Libre (Esquema)")

    # Representación visual limpia y moderna con HTML/CSS (Sin errores de librerías)
    if tipo_apoyo == "Simplemente Apoyada (Apoyo Fijo A + Apoyo Móvil B)":
        esquema_html = f"""
        <div style="background-color: #f8fafc; padding: 30px; border-radius: 12px; border: 2px dashed #cbd5e1; text-align: center; font-family: sans-serif;">
            <p style="color: #64748b; font-size: 14px; margin-bottom: 10px;"><b>Longitud Total:</b> {longitud_viga} m</p>
            <div style="font-size: 24px; margin: 15px 0; color: #0f172a; font-weight: bold; letter-spacing: 2px;">
                🔺════════════════════════🔵
            </div>
            <div style="display: flex; justify-content: space-between; padding: 0 10px; font-size: 14px; color: #334155;">
                <span><b>Apoyo Fijo (A)</b><br><i>Ax, Ay</i></span>
                <span style="color: #16a34a;"><b>Carga P:</b> {fuerza_p} kN ({angulo_p}°)</span>
                <span><b>Apoyo Móvil (B)</b><br><i>By</i></span>
            </div>
            <p style="margin-top: 15px; color: #ea580c; font-size: 14px;"><b>Carga distribuida (w):</b> {carga_w} kN/m en toda la viga</p>
        </div>
        """
    else:
        esquema_html = f"""
        <div style="background-color: #f8fafc; padding: 30px; border-radius: 12px; border: 2px dashed #cbd5e1; text-align: center; font-family: sans-serif;">
            <p style="color: #64748b; font-size: 14px; margin-bottom: 10px;"><b>Longitud Total:</b> {longitud_viga} m</p>
            <div style="font-size: 24px; margin: 15px 0; color: #0f172a; font-weight: bold; letter-spacing: 2px;">
                🧱══════════════════════════
            </div>
            <div style="display: flex; justify-content: space-between; padding: 0 10px; font-size: 14px; color: #334155;">
                <span><b>Empotramiento (A)</b><br><i>Ax, Ay, Ma</i></span>
                <span style="color: #16a34a;"><b>Carga P:</b> {fuerza_p} kN ({angulo_p}°)</span>
                <span><b>Extremo Libre</b></span>
            </div>
            <p style="margin-top: 15px; color: #ea580c; font-size: 14px;"><b>Carga distribuida (w):</b> {carga_w} kN/m en toda la viga</p>
        </div>
        """
    st.markdown(esquema_html, unsafe_allow_html=True)
    st.info(
        "💡 Este esquema interactivo se actualiza de forma dinámica con los valores que configures en la barra lateral.")

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