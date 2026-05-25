import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(page_title="Trayectoria | WellFlow Engine")

st.header("Geometría y Trayectoria Direccional")
st.markdown("Cálculo espacial (Mínima Curvatura) y visualización 3D.")

# 1. Tabla de ingreso de datos
st.subheader("1. Ingreso de Surveys")
datos_iniciales = [
    {"MD (ft)": 0.0, "Inclinación (°)": 0.0, "Azimut (°)": 0.0},
    {"MD (ft)": 1000.0, "Inclinación (°)": 2.5, "Azimut (°)": 45.0},
    {"MD (ft)": 2000.0, "Inclinación (°)": 15.0, "Azimut (°)": 60.0},
    {"MD (ft)": 3000.0, "Inclinación (°)": 45.0, "Azimut (°)": 90.0}
]

tabla_base = pd.DataFrame(datos_iniciales)

surveys = st.data_editor(
    tabla_base,
    num_rows="dynamic",
    use_container_width=True
)

st.divider()

# 2. Motor Matemático
if st.button("Procesar Trayectoria y Graficar 3D"):
    df = surveys.copy().sort_values(by="MD (ft)").reset_index(drop=True)
    
    tvd, north, east = [0.0], [0.0], [0.0]
    
    for i in range(1, len(df)):
        md1, inc1, azi1 = df.loc[i-1, ["MD (ft)", "Inclinación (°)", "Azimut (°)"]]
        md2, inc2, azi2 = df.loc[i, ["MD (ft)", "Inclinación (°)", "Azimut (°)"]]
        
        i1, i2 = np.radians(inc1), np.radians(inc2)
        a1, a2 = np.radians(azi1), np.radians(azi2)
        delta_md = md2 - md1
        
        dl = np.arccos(np.cos(i1) * np.cos(i2) + np.sin(i1) * np.sin(i2) * np.cos(a2 - a1))
        
        if dl != 0:
            rf = (2 / dl) * np.tan(dl / 2)
        else:
            rf = 1.0
            
        delta_tvd = (delta_md / 2) * (np.cos(i1) + np.cos(i2)) * rf
        delta_north = (delta_md / 2) * (np.sin(i1) * np.cos(a1) + np.sin(i2) * np.cos(a2)) * rf
        delta_east = (delta_md / 2) * (np.sin(i1) * np.sin(a1) + np.sin(i2) * np.sin(a2)) * rf
        
        tvd.append(tvd[-1] + delta_tvd)
        north.append(north[-1] + delta_north)
        east.append(east[-1] + delta_east)
        
    df["TVD (ft)"] = tvd
    df["Norte/Sur (ft)"] = north
    df["Este/Oeste (ft)"] = east
    
    # 3. Mostrar Tabla de Resultados
    st.subheader("2. Memoria de Cálculo")
    st.dataframe(df.round(2), use_container_width=True)
    
    # 4. GRÁFICO 3D (La Magia Visual)
    st.subheader("3. Vista Espacial del Pozo")
    
    # Armamos la línea 3D uniendo los puntos
    fig = go.Figure(data=[go.Scatter3d(
        x=df["Este/Oeste (ft)"], # Eje X
        y=df["Norte/Sur (ft)"],  # Eje Y
        z=df["TVD (ft)"],        # Eje Z (Profundidad)
        mode='lines+markers',    # Queremos ver la línea y los puntos de medición
        marker=dict(size=4, color='red'), # Los puntos serán rojos
        line=dict(color='blue', width=5)  # La tubería será azul
    )])
    
    # Ajustamos la "caja" del gráfico
    fig.update_layout(
        scene=dict(
            xaxis_title='Este (+) / Oeste (-)',
            yaxis_title='Norte (+) / Sur (-)',
            zaxis_title='Profundidad TVD (ft)',
            # IMPORTANTE: Invertimos el eje Z porque perforamos hacia abajo
            zaxis=dict(autorange="reversed") 
        ),
        margin=dict(l=0, r=0, b=0, t=0), # Quitamos los bordes blancos extra
        height=600 # Altura del gráfico en la pantalla
    )
    
    # Mostramos el gráfico en la página web
    st.plotly_chart(fig, use_container_width=True)