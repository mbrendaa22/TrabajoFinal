from sklearn.preprocessing import PolynomialFeatures
import pickle 
import numpy as np
import pandas as pd
from openpyxl import Workbook
import openpyxl
import streamlit as st
from io import BytesIO
from config import MODEL, ARCHIVO_EJEMPLO
import matplotlib.pyplot as plt

st.header(' :blue[_Trabajo Final: Comparación de modelos de regresión para predecir la evapotranspiración potencial diaria y calcular la pérdida de agua por hectárea en la zona sur de Mendoza_] :blue_book: ')
st.subheader('Alumna: Brenda Martinez')
st.title('Evapotranspiracion Predictiva :farmer:')
st.markdown("""
Esta plataforma ayuda a los agricultores a estimar la pérdida de agua por hectárea a través de la evapotranspiración. 
Utilizamos un modelo predictivo basado en datos meteorológicos para proporcionar estimaciones precisas de la evapotranspiración. 
Esto ayuda a los agricultores a tomar decisiones informadas sobre el riego y a optimizar el uso del agua en sus cultivos. 
""")

st.markdown("""Es importante que sepas que este modelo fue entrenado con datos diarios de la estación meteorológica de La Llave, Mendoza Argentina :flag-ar: . 
Por lo tanto estamos hablando de una zona con una elevación sobre el nivel del mar de 780m y una latitud de  34° 51' S aprox.
Los datos usados fueron: Radiación, Temperatura Máxima, Temperatura Mínima, Presión de vapor del aire y Viento. El método usado para el cálculo de la evapotranspiración (ETO) 
fue el método Penman Monteith de la Organización de las Naciones Unidas para la Agricultura y la Alimentación (FAO) y la herramienta usada para calcular la ETO fue AGROCLIMA. 
""")

# se carga el archivo de ejemplo
df = pd.read_excel(ARCHIVO_EJEMPLO, engine='openpyxl')

with st.expander(":raised_hand_with_fingers_splayed:  ¿COMO FUNCIONA? "):
    st.write("""Subirás un archivo con datos meteorológicos diarios como el siguiente ejemplo, 
    luego te pediré que ingreses cuántas hectareas tienes y obtendrás como resultado un archivo excel descargable con la predicción de la ETO y la perdida de agua por hectarea en litros por día""")
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
    st.write(" :loudspeaker: ¡Algunos datos necesitan ser tratados antes de proceder!")
    st.write(":arrow_right: Radiación  ")
    st.write("La radiacion debe estar en en MJ/m²/día. Usa la siguiente formula:")
    st.latex(r"R * 0,0036")
    st.write("Donde R es la radiación en W/m²/dia ")
    st.write(":arrow_right: Presión de vapor actual")
    st.latex(r"0.6108 ^ (17.27 * T / (T + 237.3)) * rhmed / 10 ")
    st.write("Donde T: temperatura media, rhmed: humedad relativa media")
    st.write(":arrow_right: Viento")
    st.write(" :books: En estaciones meteorológicas los anemómetros se colocan a una altura estándar de 10m y en agrometeorología a 2m o 3m. ")
    st.write("Para el cálculo de la ET se requiere la velocidad del viento medida a 2m sobre la superficie. :books: ")
    st.latex(r"u2 = uz*(4,87/ln(67,8 z - 5,42))")
    st.write('''Donde: u2: velocidad del viento a 2 m sobre la superficie 
    uz: velocidad del viento a z m sobre la superficie 
    z: altura de medición sobre la superficie''')

# Crear formulario para introducir archivo y hectáreas
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

    submitted = st.form_submit_button("Submit :white_check_mark:")
  
    if submitted:
        
      df_uploaded_file = pd.read_excel(uploaded_file, engine='openpyxl')   

      # se carga el modelo entrenado para hacer predicciones
      rf_model = pickle.load(open('ModeloEntrenado.sav', 'rb')) #read binary
      # se hace la prediccion con el archivo que sube el usuario
      predictionETO = rf_model.predict(df_uploaded_file)

      # ha = hectárea
      # si ha ingresado las hectareas el siguiente paso es calcular la perdida de agua por hectárea teniendo en cuenta lo siguiente:
      # perder 1 mm día-1 es equivalente 10 m3 ha-1 día-1 segun la FAO
      if ha:
      # el ciclo for itera sobre cada prediccion de la lista prediction
        df2 = pd.DataFrame()
        for p in predictionETO:
            roundETo = np.round(p, decimals=2)
            perdida_m3_ha_dia = roundETo * 10 * ha # pérdida en metros cúbicos por hectárea y día 
            aguaPerdida_litros_m2_dia = perdida_m3_ha_dia*1000 # pérdida en litros por hectárea y día
            df2 = df2.append({'Pérdida(litros/ha/día)': aguaPerdida_litros_m2_dia}, ignore_index=True)
            # se crea una columna al dataframe df1 con los valores de la lista prediccion
            df_uploaded_file['ETO'] = np.round(predictionETO, decimals=2)

        plt.style.use('dark_background')
        fig, ax = plt.subplots()
        ax.bar(np.arange(len(df2))+1, df2['Pérdida(litros/ha/día)']) # np.arange(len(df2))+1 crea una secuencia numérica de 1 a la cantidad de filas en df2, que son los valores del eje X
        ax.set_xlabel('Día')
        ax.set_ylabel('Cantidad de agua perdida (litros/ha/día)')
        st.pyplot(fig)

        plt.style.use('dark_background')
        fig, ax = plt.subplots()
        ax.bar(np.arange(len(df_uploaded_file))+1,  df_uploaded_file['ETO'] )
        ax.set_xlabel('Día')
        ax.set_ylabel('Eto')
        st.pyplot(fig)


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
            

if boolean:
    excel_bytes = generar_excel(df_uploaded_file, df2)
    st.download_button(label='Descargar archivo', data=excel_bytes , file_name='Resultado.xlsx', mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    


