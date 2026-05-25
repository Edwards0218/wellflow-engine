import streamlit as st

# Configuración de la página principal
st.set_page_config(
    page_title="WellFlow Engine",
    page_icon="⚙️",
    layout="centered"
)

# Diseño de la portada
st.title("⚙️ WellFlow Engine")
st.subheader("Plataforma Integral de Cálculos para Hidrocarburos")

st.divider()

st.markdown("""
Bienvenido al motor de cálculos operativos. 

👈 **Utiliza el menú lateral** para navegar entre los diferentes módulos de ingeniería disponibles:

* **Volumen Anular:** Cálculos de fluidos, capacidades y desplazamientos de bomba.
* *(Próximamente)* **Geometría y Trayectoria:** Análisis direccional y ploteo.
""")

st.info("Sistema en línea y operando correctamente.")