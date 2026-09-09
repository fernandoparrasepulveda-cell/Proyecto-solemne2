import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import json

# Configuración básica de la pestaña del navegador
st.set_page_config(page_title="Red de Farmacias", layout="wide")
st.title("Análisis de Farmacias en Chile")
st.write("Exploración de la red de abastecimiento médico para respuestas rápidas y turnos.")

# Aquí va la URL directa a la API (formato JSON)
url_api = "https://midas.minsal.cl/farmacia_v2/WS/getLocales.php"

if st.button("Cargar datos de Farmacias"):
    # Hacemos la petición a la API
    respuesta = requests.get(url_api)
    
    if respuesta.status_code == 200:
        st.success("¡Datos obtenidos correctamente!")
        datos = respuesta.json()
        
        # Convertimos los datos a un DataFrame (Tabla)
        df = pd.DataFrame(datos)
        
        # Mostramos la tabla interactiva en la web
        st.subheader("Base de Datos Activa")
        st.dataframe(df)
        
        # Filtro interactivo por Región
        st.subheader("Filtrar por Región")
        # Aseguramos de que exista la columna correspondiente a la región
        if 'fk_region' in df.columns:
            region_seleccionada = st.selectbox("Selecciona un ID de región", df['fk_region'].unique())
            
            # Filtramos la tabla
            df_filtrado = df[df['fk_region'] == region_seleccionada]
            st.write(f"Farmacias encontradas en esta región: {len(df_filtrado)}")
            st.dataframe(df_filtrado)
            # Gráfico de análisis por región
            st.subheader("Análisis Visual: Cantidad de Farmacias por Región")
            conteo_regiones = df['fk_region'].value_counts()
            
            fig, ax = plt.subplots()
            conteo_regiones.plot(kind='bar', ax=ax, color='skyblue')
            ax.set_title("Distribución de Locales")
            ax.set_xlabel("Región")
            ax.set_ylabel("Cantidad")
            
            st.pyplot(fig)
        else:
            st.warning("No se encontró la columna de regiones en estos datos.")
    else:
        st.error("Error al conectar con la API.")