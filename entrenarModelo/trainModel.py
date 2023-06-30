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
rf_model = RandomForestRegressor(n_estimators=100, oob_score=True, random_state=42)

# Entrenar modelo con conjunto de entrenamiento
rf_model.fit(X_train, y_train)

# Hacer predicciones con conjunto de prueba
y_pred = rf_model.predict(X_test)
print('predicted:', y_pred[87])
expected = y_test
print('expected:', expected.values[87])

# ------------------------------- # 
# ----- E V A L U A T I O N------ # 
# ------------------------------- # 
from sklearn.metrics import mean_squared_error
model_rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print('RMSE: ', model_rmse)

from sklearn.metrics import r2_score
# The coefficient of determination: 1 is perfect prediction
coeficiente = r2_score(y_test, y_pred)
mensaje = "Observacion: {:.0%} de los datos se ajusta al modelo. Es decir, {:.0%} de variación en y explicada por variables x.".format(coeficiente, coeficiente)
print(mensaje)

# Obtener la puntuación OOB (R2)
oob_score = rf_model.oob_score_
print("Puntuación OOB:", oob_score)

# Guardar modelo
import pickle
pickle.dump(rf_model, open('ModeloEntrenado.sav', 'wb')) #writebinary