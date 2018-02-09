# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 17:49:40 2018

@author: brunolima
"""
import numpy as np
import pandas as pd

#df = pd.read_csv('old_diabetes_dataset.csv')
df = pd.read_csv('old_diabetes_app.csv')

# carrega os nomes das colunas
feature_cols = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
                'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']

# Normalizing csv
df['DiabetesPedigreeFunction'] = (df['DiabetesPedigreeFunction']-df['DiabetesPedigreeFunction'].min())/(df['DiabetesPedigreeFunction'].max()-df['DiabetesPedigreeFunction'].min())
df['Insulin'] = (df['Insulin']-df['Insulin'].min())/(df['Insulin'].max()-df['Insulin'].min())

# Medias
average = {}
for key in feature_cols:
    # Calculando a media da presente chave
    average[key] = df[key].mean()

    # Substituindo valores nulos de DiabetesPedigreeFunction 
    df[key] = df[key].replace(np.NaN, average[key])


# Saving CSV
#df.to_csv('diabetes_dataset.csv', index=False, header=True)
df.to_csv('diabetes_app.csv', index=False, header=True)