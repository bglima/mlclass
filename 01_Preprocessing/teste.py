# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 17:03:57 2018

@author: brunolima
"""

import numpy as np
import pandas as pd
from diabetes_csv import vai
from time import sleep

old_files = [ 'old_diabetes_dataset.csv', 'old_diabetes_app.csv' ]
new_files = [ 'diabetes_dataset.csv', 'diabetes_app.csv' ]

for i in range(0, len(old_files) ):
    df = pd.read_csv(old_files[i])

    # Drop missing data
    #df = df.dropna(axis=0, how='any')

    # carrega os nomes das colunas
    feature_cols = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
                    'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']

    # Medias
    average = {}
    median = {}
    for key in feature_cols:
        # Calculando a media da presente chave
        average[key] = df[key].mean()
        median[key] = df[key].median()

        
    # Substituindo valores nulos    
#    df['Pregnancies'] = df['Pregnancies'].replace(np.NaN, 0)
#    df['Glucose'] = df['Glucose'].replace(np.NaN, median['Glucose'])
#    df['BloodPressure'] = df['BloodPressure'].replace(np.NaN, median['BloodPressure'])
#    df['SkinThickness'] = df['SkinThickness'].replace(np.NaN, median['SkinThickness'])
#    df['Insulin'] = df['Insulin'].replace(np.NaN, 0)
#    df['BMI'] = df['BMI'].replace(np.NaN, median['BMI'])
#    df['DiabetesPedigreeFunction'] = df['DiabetesPedigreeFunction'].replace(np.NaN, median['DiabetesPedigreeFunction'])
#    df['Age'] = df['Age'].replace(np.NaN, median['Age'])
    
    # Default substitution
    for key in feature_cols:
        df[key] = df[key].replace(np.NaN, average[key])


    # Transforming column
    df['Pregnancies'] =  df['Pregnancies'] / df['Age'] 
    
    # Normalizing by MinMax
    to_ignore = []
    gen = (key for key in feature_cols if key not in to_ignore)

    normalize_minmax = gen
    for features in normalize_minmax:
        df[features] = (df[features]-df[features].min())/(df[features].max()-df[features].min()) 
    # Normalizing through Standard Deviation
    normalize_mean = []
    for features in normalize_mean:  
        df[features] = (df[features]-df[features].mean())/df[features].std()
    
    # Discarding some columns
    features_to_discard = []
    for features in features_to_discard:
        df[features] = 1                                                                                                                                                                        

    # Binarizing values
    features_to_binarize = []
    for features in features_to_binarize:
        df[features] = (df[features] > 0).astype(int) 

    # Rounding values    
    decimal_places = [ 3, 3, 3, 3, 3, 3, 3, 3 ]
    places_per_col = pd.Series(decimal_places, index=feature_cols)
    df = df.round(places_per_col)    
   
    # Giving more wheight to some
    df['Glucose'] = df['Glucose'] * 2.1
    df['Insulin'] = df['Insulin'] * 1.8
    df['Pregnancies'] = df['Pregnancies'] * 1.1
    df['SkinThickness'] = df['SkinThickness'] * 1.3

    df.to_csv(new_files[i], index=False, header=True)
    

accuracy = vai()
print('Minha acc eh: {}'.format(accuracy))    

# FOr future experiments
max_peso = 0
max_acc = 0
for j in range(-15, 16):
     peso = (2 + float(j) / 10.0 )
     new_df = pd.read_csv(old_files[i])
     new_df['Age'] = df['Age'] * peso
     # Saving CSV
     new_df.to_csv(new_files[0], index=False, header=True)
     new_df.to_csv(new_files[1], index=False, header=True)
     
     new_acc = vai()
     print('Peso atual: {}, Acc atual: {}'.format(peso, new_acc))       
     if new_acc > max_acc:
         max_acc = new_acc

     sleep(0.5) 
        
        