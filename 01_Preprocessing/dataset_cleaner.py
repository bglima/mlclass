# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 17:49:40 2018

@author: brunolima
"""
import numpy as np
import pandas as pd

csv_files = [ 'old_diabetes_dataset.csv', 'old_diabetes_app.csv' ]

for file in csv_files:
    df = pd.read_csv(file)

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
    df.to_csv(file, index=False, header=True)