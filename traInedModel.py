from sklearn.preprocessing import PolynomialFeatures
import pickle 
import numpy as np
import pandas as pd
from openpyxl import Workbook
#from openpyxl.utils.dataframe import dataframe_to_rows
import openpyxl
#from openpyxl import load_workbook
import streamlit as st
from io import BytesIO
from config import MODEL, ARCHIVO_EJEMPLO


st.title('Evapotranspiracion Predictiva :farmer:')
st.markdown("""
Esta plataforma ayuda a los agricultores a estimar la pérdida de agua por hectárea a través de la evapotranspiración. 
Utilizamos un modelo predictivo basado en datos meteorológicos para proporcionar estimaciones precisas de la evapotranspiración. 
Esto ayuda a los agricultores a tomar decisiones informadas sobre el riego y a optimizar el uso del agua en sus cultivos. 
""")

st.markdown("""Es importante que sepas que este modelo fue entrenado con datos diarios de la estación meteorológica de La Llave, Mendoza Argentina :flag-ar: . 
Por lo tanto estamos hablando de una zona con una elevación sobre el nivel del mar de 780m y una latitud de  34° 51' S aprox.
Los datos usados fueron: Radiación, Temperatura Máxima, Temperatura Minima, Presión de vapor del aire y Viento. El método usado para el cálculo de la evapotranspiración (ETO) 
fue el método Penman Monteith de la Organización de las Naciones Unidas para la Agricultura y la Alimentación (FAO) y la herramienta usada para calcular la ETO fue AGROCLIMA. 
""")

# se carga el archivo
df = pd.read_excel(ARCHIVO_EJEMPLO, engine='openpyxl')

with st.expander(":raised_hand_with_fingers_splayed:  ¿COMO FUNCIONA? "):
    st.write("""Subirás un archivo con datos meteorológicos diarios como el siguiente ejemplo, 
    luego te pediré que ingreses cuántas hectareas tienes y obtendrás como resultado un archivo excel descargable con la predicción de la ETO y la perdida de agua por hectarea""")
    st.table(df)

    # Escribir DataFrame en objeto BytesIO con formato Excel
    sampleExcel = BytesIO()
    writer = pd.ExcelWriter(sampleExcel, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Hoja1', index=False)
    writer.save()  
    sampleExcel_bytes = sampleExcel.getvalue()

    # Crear botón de descarga
    st.download_button(label='¡Descarga el archivo de ejemplo!', data=sampleExcel_bytes, file_name='archivoEjemplo.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

with st.expander(" :boom: INFORMACIÓN IMPORTANTE ANTES DE SUBIR TU ARCHIVO :boom:"):
    st.write(":arrow_right: La radiación debe estar en MJ/m²/día")
    st.write("Usa la siguiente formula: $$R * 0,0036$$")
    st.write(":arrow_right: ¿No sabes cómo obtener la presion de vapor actual? ¡Yo te ayudo!")
    st.write("Usa la siguiente formula: 0.6108 **(17.27 * T / (T + 237.3)) * rhmed / 10 ")
    st.write("Donde T: temperatura media, rhmed: humedad relativa media")

# Crear formulario para introducir archivo y ha
boolean = False
with st.form("my_form"):
  st.write("¿Todo listo?")
  uploaded_file = st.file_uploader("Sube tu archivo:", type="xlsx")
  
  # Verifica si se ha cargado un archivo
  if uploaded_file is not None:
      # Si se ha cargado un archivo, lee el archivo con pandas
      st.write(f"Has cargado el archivo: {uploaded_file.name}")
  else:
      # Si no se ha cargado un archivo, muestra un mensaje
      st.write("La extensión debe ser: .xlsx")
  
  ha = st.number_input('¿Cuántas hectáreas tienes?', step = 1, value = 1)

  # submit button.
  submitted = st.form_submit_button("Submit :white_check_mark:")
  
  if submitted:
        
      df_uploaded_file = pd.read_excel(uploaded_file, engine='openpyxl')   

      # se carga el modelo entrenado para hacer predicciones
      model = pickle.load(open('ModeloEntrenado.sav', 'rb')) #read binary
      # se hace la prediccion con el archivo que sube el usuario
      poly = PolynomialFeatures(degree=3)
      predictionETO = model.predict(poly.fit_transform(df_uploaded_file))
      print(predictionETO)

      # ha = hectárea
      if ha:
      # el ciclo for itera sobre cada prediccion de la lista prediction
        df2 = pd.DataFrame()
        for p in predictionETO:
          #print(p[0])
          # se obtiene aP(agua perdida) a partir de la prediccion ETO y la variable ha
          aP = (p[0] * ha)/1
          # se redondea a dos decimales
          aguaPerdidaPorHa = np.round(aP, decimals=2)
          # se agrega cada valor de d al dataframe df2
          df2 = df2.append({'AguaPerdida': aguaPerdidaPorHa}, ignore_index=True)
          # se crea una columna al dataframe df1 con los valores de la lista prediccion
          df_uploaded_file['ETO'] = predictionETO

        # se escribe en un archivo excel los datos de df_uploaded_file y df2
        def generar_excel(df_uploaded_file, df2):
          excel = BytesIO()
          with pd.ExcelWriter(excel, engine='openpyxl') as writer: 
              df_uploaded_file.to_excel(writer, sheet_name='Resultado', index=True, engine='openpyxl')
              df2.to_excel(writer, sheet_name='Resultado', index=False, startcol=7, engine='openpyxl')
          return excel.getvalue()

        # se guardan los cambios
        writer.save()
        writer.close()
        boolean = True
      else:
            st.write("Debe ingresar cuántas hectáreas tiene. ")
            

if boolean:
  excel_bytes = generar_excel(df_uploaded_file, df2)
  st.download_button(label='Descargar archivo', data=excel_bytes , file_name='prediccion.xlsx', mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


# a parte de la opcion de descarga aca queria mostrar el resultado en una tabla pero no puedo leer el archivo.. me sale Excel xlsx file not supported.
  #df_prediccion = pd.read_excel(writer)
  #st.table(df_prediccion)
