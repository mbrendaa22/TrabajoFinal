import pickle 
import pandas as pd
import numpy as np
import streamlit as st
from io import BytesIO
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import logging

logging.basicConfig(
    filename='logs.txt',
    format='%(asctime)s - %(levelname)s - %(message)s',  # Formato de registro
    level=logging.INFO  # Nivel de registro
)

st.header(' :blue[_Trabajo Final: Comparación de modelos de regresión para predecir la evapotranspiración potencial diaria y calcular la pérdida de agua por hectárea en la zona sur de Mendoza_] :blue_book: ')
st.subheader('Autora: Brenda Daiana Martinez Lujan')
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
df = pd.read_excel('./archivoEjemplo.xlsx', engine='openpyxl')
df_copy = df.astype('str')
#print(f"Dataframe:\n {df}")

with st.expander(":raised_hand_with_fingers_splayed:  ¿COMO FUNCIONA? "):
    st.write("""Subirás un archivo con datos meteorológicos diarios como el siguiente ejemplo, 
    luego te pediré que ingreses cuántas hectareas tienes y obtendrás como resultado un archivo excel descargable con la predicción de la ETO y la perdida de agua por hectarea en litros por día""")
    st.table(df_copy)

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
    st.write("La radiacion debe estar en en MJ/m²/día (MegaJulios por m²/día). Usa la siguiente formula:")
    st.latex(r"R * 0,0036")
    st.write("Donde R es la radiación en W/m²/dia (Vatios por m²/día) ")
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

def monitorearPrediccion():
    ############# MONITOREAR PREDICCIÓN #############
    try:
        data = pd.read_excel('./datosEntrenarModelo.xlsx', engine='openpyxl')
        # Definir variables independientes y target
        target = data['ETPF56']
        y = pd.DataFrame.from_dict(target) 
        variables = data[['Mj/m2/d','TMax', 'TMin', 'PVA', 'Viento']]
        X = pd.DataFrame.from_dict(variables) 

        new_pred = pd.DataFrame(predictionETO)
        # Separar datos en conjunto de entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=len(new_pred), random_state=42)            
                
        from sklearn.metrics import mean_squared_error, mean_absolute_error
        new_pred = new_pred.to_numpy().squeeze()
        model_rmse = np.sqrt(mean_squared_error(y_test, new_pred))
        logging.info("Error cuadrático medio de la raíz: Mide la cantidad de error que hay entre dos conjuntos de datos.")
        logging.info(f'RMSE: {model_rmse}')
        logging.info("Error absoluto medio: Mide la diferencia absoluta promedio entre el valor predicho y el real.")
        logging.info(f"MAE: {mean_absolute_error(y_test, new_pred)}")
        logging.info(f'Desviación de RMSE: {model_rmse - 0.512}')

    except ValueError as e:
        # Manejo del error capturado
        error_message = str(e)
        print("Error:", error_message)
        logging.error(f'Esto es una advertencia importante. {e}')
        st.error(f"Para poder monitorear la predicción el tamaño de prueba debe ser positivo y más pequeño que el número de muestras (1095). Muestras de su archivo: {len(df_uploaded_file)}.")
    ############# MONITOREAR PREDICCIÓN #############

# Crear formulario para introducir archivo y hectáreas
boolean = False
with st.form("my_form"):
    st.write("¿Todo listo?")
    uploaded_file = st.file_uploader("Sube tu archivo:", type="xlsx")

    try:
        # Verifica si se ha cargado un archivo
        if uploaded_file is not None:
            # Si se ha cargado un archivo, lee el archivo con pandas
            st.write(f"Has cargado el archivo: {uploaded_file.name}")
        else:
            # Si no se ha cargado un archivo, muestra un mensaje
            st.write(f"La extensión del archivo debe ser: .xlsx")    
            logging.warning(f'¡Cuidado! El usuario se olvidó cargar un archivo o la extensión estaba mal')
            
        ha = st.number_input('¿Cuántas hectáreas tienes?', step = 1, value = 1, min_value=1) 

        submitted = st.form_submit_button("Submit :white_check_mark:")
    
        if submitted:
            
            df_uploaded_file = pd.read_excel(uploaded_file, engine='openpyxl') 

            # se carga el modelo entrenado para hacer predicciones
            rf_model = pickle.load(open('./ModeloEntrenado.sav', 'rb')) #read binary
            # se hace la prediccion con el archivo que sube el usuario
            predictionETO = rf_model.predict(df_uploaded_file)

            # ha = hectárea
            # calcular la perdida de agua por hectárea teniendo en cuenta lo siguiente:
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

                # Dar info al usuario sobre lo que está visualizando
                with st.expander(" :information_source: INFORMACIÓN QUE TE GUSTARÍA SABER PARA UNA MEJOR INTERPRETACIÓN :bookmark_tabs:"):            
                    st.write(" :thinking_face: ¿Qué es la ETO?")
                    st.write("""La evapotranspiración del cultivo de referencia (ETo) representa
                                la pérdida de agua de una superficie cultivada estándar.
                                El concepto de evapotranspiración de referencia se introdujo para estudiar la
                                demanda de evapotranspiración de la atmósfera, independientemente del tipo y
                                desarrollo del cultivo, y de las prácticas de manejo.""")
                    st.write(" :straight_ruler: Unidad de la ETO")
                    st.write(""" La evapotranspiración se expresa normalmente en milímetros (mm) por unidad de
                                tiempo. La unidad de tiempo puede ser una hora, día, 10 días, mes o incluso un completo período de cultivo o un año. """)
                    st.write(" 	:straight_ruler: ¿Como se mide?")
                    st.write("""Como una hectárea tiene una superficie de 10 000 m2 y 1 milímetro es igual a 0,001 m, 
                            una pérdida de 1 mm de agua corresponde a una pérdida de 10 m3 de agua por
                            hectárea. Es decir 1 mm día-1 es equivalente 10 m3 ha-1 día-1.""")
                    st.write(":rainbow: ¿Qué parámetros climáticos afectan a la ETO?")
                    st.write("Los principales parámetros climáticos que afectan la evapotranspiración son la radiación, la temperatura del aire, la humedad atmosférica y la velocidad del viento.")

                plt.style.use('bmh')
                fig, ax = plt.subplots()
                ax.bar(np.arange(len(df2))+1, df2['Pérdida(litros/ha/día)']) # np.arange(len(df2))+1 crea una secuencia numérica de 1 a la cantidad de filas en df2, que son los valores del eje X
                ax.set_xlabel('Día')
                ax.set_ylabel('Cantidad de agua perdida (litros/ha/día)')
                st.pyplot(fig)

                plt.style.use('tableau-colorblind10')
                fig, ax = plt.subplots()
                ax.bar(np.arange(len(df_uploaded_file))+1,  df_uploaded_file['ETO'] )
                ax.set_xlabel('Día')
                ax.set_ylabel('Eto')
                st.pyplot(fig)

                st.divider() 
                with st.expander("Entonces... ¿Cómo interpretar los resultados? :thinking_face: "):
                    st.caption(" '_En un día soleado y cálido :sun_with_face: , la pérdida de agua por evapotranspiración será mayor que en un día nublado y fresco._' :barely_sunny:")
                    st.write("""Sin embargo, es importante tener en cuenta que la ETo puede variar significativamente según la ubicación geográfica,
                            el clima local y las condiciones específicas de cada región.""")
                    st.write("Podríamos, entonces considerar lo siguiente:")
                    st.write(""" :snowman: Invierno: La evapotranspiración de referencia (ETo) tiende a ser más baja debido a las temperaturas frías y la menor cantidad de luz solar.
                                En algunas regiones, es posible que haya una menor tasa de evapotranspiración debido a la presencia de nieve o heladas.
                                """)
                    st.write(""" :sunny: Verano: En verano, la ETo tiende a ser más alta debido a las temperaturas cálidas y la mayor cantidad de luz solar. :thermometer:
                                En esta época, la tasa de evapotranspiración puede ser alta debido a la mayor demanda de agua por parte de las plantas y la mayor tasa de evaporación del suelo""")
                    st.write(""" :sunflower: Primavera: La ETo aumenta gradualmente a medida que las temperaturas se vuelven más cálidas y hay más luz solar.""")
                    st.write(""" :fallen_leaf: Otoño: La ETo disminuye gradualmente a medida que las temperaturas se enfrían y los días se acortan.""")

                # se escribe en un archivo excel los datos de df_uploaded_file y df2
                def generar_excel(df_uploaded_file, df2):
                    excel = BytesIO()
                    with pd.ExcelWriter(excel, engine='openpyxl') as writer: 
                        df_uploaded_file.to_excel(writer, sheet_name='Resultado', index=True, engine='openpyxl')
                        df2.to_excel(writer, sheet_name='Resultado', index=False, startcol=7, engine='openpyxl')
                    return excel.getvalue()

                monitorearPrediccion()
                # se guardan los cambios
                writer.save()
                writer.close()
                boolean = True 

    except ValueError as e:
        # Manejo del error capturado
        error_message = str(e)
        print("Error:", error_message)
        logging.error(f'Debes cargar un archivo. {e}')
        st.error(f"Debes cargar un archivo.")        


if boolean:
    excel_bytes = generar_excel(df_uploaded_file, df2)
    st.download_button(label='Descargar archivo', data=excel_bytes , file_name='Resultado.xlsx', mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")