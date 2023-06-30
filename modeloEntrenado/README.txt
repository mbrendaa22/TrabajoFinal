En el directorio "modeloEntrenado" se encuentran los siguientes archivos:

archivoEjemplo.xlsx: Este archivo es un ejemplo que se muestra al usuario como referencia.

datosEntrenarModelo.xlsx: Contiene los datos utilizados en el código trainModel.py para entrenar el modelo. 
En este caso se usa para poder monitorear los nuevos datos contra los datos de entrenamiento.

PosiblesEjemplosDeUser: Carpeta que contiene archivos de ejemplo excel que se utilizan como pruebas de usuario.

ModeloEntrenado.sav: Es el modelo obtenido a partir del código trainModel.py en colab y se utiliza para realizar predicciones.

Además de los archivos, se encuentran los siguientes scripts:

config.py: Este archivo contiene las rutas a los archivos .xlsx utilizados en la aplicación.

trainedModel.py: Es un archivo que utiliza librerías de Python para generar una interfaz al usuario, 
permitiéndole utilizar la aplicación. Utiliza el modelo guardado en ModeloEntrenado.sav para realizar 
predicciones con los nuevos datos ingresados por el usuario
