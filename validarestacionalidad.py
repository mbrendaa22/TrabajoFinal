# -*- coding: utf-8 -*-
"""validarEstacionalidad.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oOzXLHKynHiO5eDR_i2D7tOMnJ1Ed-f3
"""

#ANALIZAR LA ESTACIONALIDAD CON LA PRUEBA DE DICKY
from statsmodels.tsa.stattools import adfuller
fichero = open('/content/ETO.csv')
lineas = fichero.readlines() 

result = adfuller(lineas)
   
labels = ['ADF Test Statistic','p-value','#Lags Used','Number of Observations']
for value,label in zip(result,labels):
	print(label+' : '+str(value) )
if result[1] <= 0.05:
    print("Strong evidence against the null hypothesis(Ho), reject the null hypothesis. Data is stationary")
else:
    print("Weak evidence against null hypothesis, indicating it is non-stationary")

#VALIDO LO DE ARRIBA ES BASICAMENTE LO MISMO XD
from pandas import read_csv
from matplotlib import pyplot
from numpy import log

fichero = open('/content/ETO.csv')
X = fichero.readlines() 
result = adfuller(X)
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])
print('Critical Values:')
for key, value in result[4].items():
	print('\t%s: %.3f' % (key, value))