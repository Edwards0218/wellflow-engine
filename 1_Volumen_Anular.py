import streamlit as st

st.set_page_config(page_title="Volumen Anular | WellFlow Engine")

st.header("Cálculo Avanzado de Volumen Anular")
st.markdown("Herramienta rápida para operaciones de circulación y limpieza de pozo.")

# Organización en columnas
col1, col2 = st.columns(2)

with col1:
    st.subheader("Datos del Pozo")
    id_casing = st.number_input("ID del Casing / Hueco (pulgadas)", min_value=0.0, value=7.00)
    profundidad = st.number_input("Longitud de la sección (pies)", min_value=0.0, value=1000.0)

with col2:
    st.subheader("Datos de la Sarta y Bomba")
    od_pipe = st.number_input("OD de la Tubería (pulgadas)", min_value=0.0, value=3.50)
    pump_output = st.number_input("Rendimiento de Bomba (bbl/stk)", min_value=0.001, value=0.119, format="%.3f")
    spm = st.number_input("Velocidad de Bombeo (SPM)", min_value=1, value=60)

st.divider()

# Botón de ejecución
if st.button("Calcular Desplazamiento"):
    if id_casing > od_pipe:
        # Matemática
        capacidad_anular = (id_casing**2 - od_pipe**2) / 1029.4
        volumen_total = capacidad_anular * profundidad
        total_strokes = volumen_total / pump_output
        tiempo_minutos = total_strokes / spm
        
        st.success("Cálculo ejecutado correctamente")
        
        # Mostrar resultados
        col3, col4, col5 = st.columns(3)
        col3.metric(label="Volumen Anular", value=f"{round(volumen_total, 1)} bbl")
        col4.metric(label="Emboladas Totales", value=f"{int(total_strokes)} stk")
        col5.metric(label="Tiempo de Bombeo", value=f"{round(tiempo_minutos, 1)} min")
    else:
        st.error("Error lógico: El diámetro interno debe ser mayor al externo de la tubería.")