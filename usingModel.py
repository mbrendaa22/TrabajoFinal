from sklearn.preprocessing import PolynomialFeatures
import pickle 
import numpy as np
import pandas as pd
import openpyxl
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import load_workbook
import streamlit as st
import config

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
    st.write("¿No sabes cómo obtener la presion de vapor actual? ¡Yo te ayudo!")
    st.write("Usa la siguiente formula: 0.6108 **(17.27 * T / (T + 237.3)) * rhmed / 10 ")
    st.write("Donde T: temperatura media, rhmed: humedad relativa media")

# Crea una barra de carga de archivos
with st.expander("¿Todo listo? SUBE TU ARCHIVO "):
    uploaded_file = st.file_uploader("Subir:", type="xlsx")

    # Verifica si se ha cargado un archivo
    if uploaded_file is not None:
        # Si se ha cargado un archivo, lee el archivo con pandas
        st.write(f"Has cargado el archivo: {uploaded_file.name}")
        dfUploadFile = pd.read_excel(uploaded_file)
        # Muestra el contenido del archivo en una tabla
        st.dataframe(dfUploadFile)
    #else:
        # Si no se ha cargado un archivo, muestra un mensaje
        #st.write("No has cargado ningún archivo")

# se carga el modelo entrenado para hacer predicciones
#model = pickle.load(open('C:/Users/bdmartinez/Desktop/_TRABAJO_FINAL/PolynomialRegressionPrediction/model.sav', 'rb')) #read binary
model = pickle.load(open(config.PATH, 'rb'))
# se hace la prediccion
poly = PolynomialFeatures(degree=3)
prediction = model.predict(poly.fit_transform(dfUploadFile)) 
 
#se crea un archivo excel
#wr = pd.ExcelWriter('archivoFinal.xlsx', engine='xlsxwriter')  

#print("Para saber cuánta pérdida de agua hay por hectarea ingrese por favor el número de hectareas:")
ha = st.text_input("¿Cuántas hectáreas tienes?")
#ha= int(input())

if ha:
  # el ciclo for itera sobre cada preddicion de la lista prediction
  df2 = pd.DataFrame()
  for p in prediction:

    # se obtiene x a partir de la prediccion y la variable ha
    x = (p[0] * ha)/1
    # se redondea a dos decimales
    aguaPerdidaPorHa = np.round(x, decimals=2)
    # se crea una lista d con los valores redondeados
    d = aguaPerdidaPorHa #_Esto esta medio al dope
    # se agrega cada valor de d al dataframe df2
    df2 = df2.append({'AguaPerdida': d}, ignore_index=True)
    # se crea una columna al dataframe df1 con los valores de la lista prediccion
    df1['ETO'] = prediction

  df2 = df2.to_csv().encode('utf-8')
  st.download_button(label='Descargar datos en csv', data = df2 ,file_name='prediccion.csv', mime='./csv') #esto te genera un boton que te descarga el csv con los datos
  df2 #Esto debería plotearse solo en streamlit


  # se abre el archivo excel y se escriben los datos de df1 y df2
  with pd.ExcelWriter("C:/Users/breee/Desktop/PolynomialRegressionPrediction/archivo.xlsx") as writer: 
    df1.to_excel(writer, sheet_name='Resultado', index=True)
    df2.to_excel(writer, sheet_name='Resultado', index=False, startcol=7)

  print("Los resultados han sido guardado en el siguiente archivo: archivo.xlsx")

  # se guardan los cambios
  writer.save()
  writer.close()
else:
    # Si el usuario no ha escrito nada, muestra un mensaje
    st.write("Es necesario introducir la cantidad de hectareas que tienes para obtener el resultado final")

