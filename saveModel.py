#ENTRENAR MODELO PARA GUARDARLO
#BIBLIOGRAFIA
#https://www.youtube.com/watch?v=wi6VoJcLyag
#https://data36.com/polynomial-regression-python-scikit-learn/
import pandas as pd
import numpy as np

data = pd.read_excel('/content/tabla_datos_2002.xlsx')
#guardo la data en un dataframe
target = data['ETPF56']
Y=pd.DataFrame.from_dict(target) #lo que quiero predecir
variables = data[['Mj/m2/d','TMax', 'TMin', 'PVA', 'Viento']]
X=pd.DataFrame.from_dict(variables) #las caracteristicas

#esto es para graficar...
data2 = pd.read_excel('/content/tabla_datos_segundo_semestre.xlsx')
x1 = pd.DataFrame.from_dict(data2['DiaN'])
y1 = pd.DataFrame.from_dict(data2['ETPF56'])
 

#Defining the training and the test data
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.5, shuffle = False)
#print(X_train)
#print(X_test)

#StandardScaler standardizes a feature by subtracting the mean and then scaling to unit variance. Unit variance means dividing all the values by the standard deviation
from sklearn.preprocessing import StandardScaler
scale = StandardScaler()
X = scale.fit_transform(X)

from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures(degree=3) #instance of PolynomialFeatures
x_poly = poly.fit_transform(X_train) #we create the new polynomial features.
poly.fit(X_train, Y_train)

#Creating a polynomial regression model
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(x_poly, Y_train)

prediction = model.predict(poly.fit_transform(X_test)) # We save the predicted values our model predicts based on the previously unseen feature values (X_test).
#print(prediction)

from sklearn.metrics import mean_squared_error
poly_reg_rmse = np.sqrt(mean_squared_error(Y_test, prediction))
#print(poly_reg_rmse)

import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
plt.title("polynomial regression model", size=16)
plt.scatter(x1, y1)
plt.plot(x1, prediction, c="blue")
plt.show()
