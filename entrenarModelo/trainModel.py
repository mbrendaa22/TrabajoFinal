import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import openpyxl

# Cargar datos desde archivo xlsx usando pandas
data = pd.read_excel('./datosEntrenarModelo.xlsx', engine='openpyxl')

print('data', data)
# Definir variables independientes y target
# guardar en un dataframe solo las variables que nos importan
target = data['ETPF56']
y = pd.DataFrame.from_dict(target) 
variables = data[['Mj/m2/d','TMax', 'TMin', 'PVA', 'Viento']]
X = pd.DataFrame.from_dict(variables) 

# Separar datos en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=365/1096)

# Crear modelo de bosque aleatorio con 100 árboles
rf_model = RandomForestRegressor(n_estimators=100)

# Entrenar modelo con conjunto de entrenamiento
rf_model.fit(X_train, y_train)

# Hacer predicciones con conjunto de prueba
y_pred = rf_model.predict(X_test)

# ------------------------------- # 
# ----- GUARDAR y_pred.xlsx ----- # 
# ------ PARA LUEGO MONITOREAR -- # 
# ------------------------------- # 
# Convertir el array en un DataFrame
df = pd.DataFrame({'y_pred': y_pred})
# Guardar el DataFrame en un archivo Excel
df.to_excel('y_pred.xlsx', index=False)

# ------------------------------- # 
# ----- E V A L U A T I O N------ # 
# ------------------------------- # 
from sklearn.metrics import r2_score

# The coefficient of determination: 1 is perfect prediction
coeficiente = r2_score(y_test, y_pred)
mensaje = "Observacion: {:.0%} de los datos se ajusta al modelo. Es decir, {:.0%} de variación en y explicada por variables x.".format(coeficiente, coeficiente)
print(mensaje)

# Guardar modelo
import pickle
pickle.dump(rf_model, open('ModeloEntrenado.sav', 'wb')) #writebinary