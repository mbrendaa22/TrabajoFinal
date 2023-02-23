from sklearn.preprocessing import PolynomialFeatures
import streamlit as st
print(st.__version__)
import pandas as pd
import openpyxl


st.title('Evapotranspiracion Predictiva')
st.markdown("""
Nuestra aplicación ayuda a los agricultores a estimar la pérdida de agua por hectárea a través de la evapotranspiración. 
Utilizamos un modelo predictivo basado en datos meteorológicos para proporcionar estimaciones precisas de la evapotranspiración. 
Esto ayuda a los agricultores a tomar decisiones informadas sobre el riego y a optimizar el uso del agua en sus cultivos. 
¡Prueba la aplicación gratis hoy mismo y descubre cómo puede mejorar tu rendimiento!
""")

st.markdown("""Es importante que sepas que este modelo fue entrenado con datos diarios de la estación meteorológica de La Llave, Mendoza Argentina. 
Por lo tanto estamos hablando de una zona con una elevación sobre el nivel del mar de 780m y una latitud de  34° 51' S aprox.
Los datos usados fueron: Radiación, Temperatura Máxima, Temperatura Minima, Presión de vapor del aire y Viento. El método usado para el cálculo de la evapotranspiración (ETO) 
fue el método Penman Monteith de la Organización de las Naciones Unidas para la Agricultura y la Alimentación (FAO) 
""")

file = 'C:/Users/breee/Desktop/PolynomialRegressionPrediction/LIBRO_DE_PRUEBA.xlsx'
# se carga el archivo
df1 = pd.read_excel(file)


with st.expander("¿COMO FUNCIONA?"):
    st.write("""Subirás un archivo con datos diarios metereológicos diarios como el siguiente ejemplo, 
    luego te pediré que ingreses cuántas hectareas tienes y obtendrás como resultado un archivo excel descargable con la predicción de la ETO y la perdida de agua por hectarea""")
    st.table(df1)
    st.download_button(label='¡Descarga el archivo de ejemplo!', data='C:/Users/breee/Desktop/PolynomialRegressionPrediction/archivoEjemplo.xlsx', file_name='archivoEjemplo.xlsx') 
with st.expander("INFORMACIÓN IMPORTANTE ANTES DE SUBIR TU ARCHIVO"):
    st.write("La radiación debe estar en MJ/m²/día")
    st.write("Usa la siguiente formula: $$R * 0,0036$$")
    st.write("Donde R: es la Radiación en W/m2/d")
    st.write("----------------------------------------------")
    st.write("¿No sabes cómo obtener la presion de vapor actual?")
    st.write("Usa la siguiente formula: 0.6108 **(17.27 * T / (T + 237.3)) * rhmed / 10 ")
    st.write("Donde T: temperatura media, rhmed: humedad relativa media")

# Crea una barra de carga de archivos
with st.expander("¿Todo listo? SUBE TU ARCHIVO "):
    uploaded_file = st.file_uploader("Subir:", type="xlsx")

    # Verifica si se ha cargado un archivo
    if uploaded_file is not None:
        # Si se ha cargado un archivo, lee el archivo con pandas
        st.write(f"Has cargado el archivo: {uploaded_file.name}")
        df = pd.read_excel(uploaded_file)
        # Muestra el contenido del archivo en una tabla
        st.dataframe(df)
    else:
        # Si no se ha cargado un archivo, muestra un mensaje
        st.write("No has cargado ningún archivo")



