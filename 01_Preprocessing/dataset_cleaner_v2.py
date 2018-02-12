# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 17:49:40 2018

@author: brunolima
"""
import numpy as np
import pandas as pd

# Nomes dos arquivos usados. Necessitam estar presentes no workspace em uso.
old_files = [ 'old_diabetes_dataset.csv', 'old_diabetes_app.csv' ]
new_files = [ 'diabetes_dataset.csv', 'diabetes_app.csv' ]

# Dados referentes ao dataset
n_total = 0
n_heal = 0
n_sick = 0
# Colunas contidas nos datasets
input_cols = ['Pregnancies', 'Glucose', 'BloodPressure', 
              'SkinThickness', 'Insulin', 'BMI', 
              'DiabetesPedigreeFunction', 'Age']
output_col = 'Outcome'
# Valores intrísecos de cada coluna
heal_avg = {} # Dicionario com as médias dos campos dos sadios
sick_avg = {} # Dicionario com as médias dos campos dos doentes
heal_mdn = {} # Dicionario com as medianas dos campos dos sadios
sick_mdn = {} # Dicionario com as medianas dos campos dos doentes

# Carrega o dataset contido num 
def load_dataset( filename ) :
    print ('[INFO] Loading {} ...'.format(filename))
    dataframe = pd.read_csv( filename )
    return dataframe

# Calcula os valores da média e mediana de pessoas.
# Só pode ser usado no conjunto de treinamento, pois necessita da coluna 'Outcome'
def analyze( dataframe ):
    n_total = dataframe.shape[0]
    # Dataset contendo os doentes e os sadios, respectivamente
    df_sick = dataframe[ dataframe[output_col] == 1 ]
    df_heal = dataframe[ dataframe[output_col] == 0 ]
    # Número de pessoas doentes e sadias
    n_sick  = len ( df_sick )
    n_heal  = len ( df_heal )
    # Calculando as médias de cada coluna de ambos os datasets
    for key in input_cols:
        heal_avg[ key ] = df_heal[ key ].mean()
        sick_avg[ key ] = df_sick[ key ].mean()
        heal_mdn[ key ] = df_heal[ key ].median()
        sick_mdn[ key ] = df_sick[ key ].median()
    # Log das infos obtidas
    print('[INFO] Found {} entries. From which..'.format( n_total ))
    print('[INFO] {} people are sick'.format(n_sick))
    print('[INFO] {} people are healthy'.format(n_heal))
    print('[INFO] AVERAGES for HEALTHY columns: {}'.format(heal_avg))
    print('[INFO] AVERAGES for SICK columns: {}'.format(sick_avg))
    print('[INFO] MEDIANS for HEALTHY columns: {}'.format(heal_mdn))
    print('[INFO] MEDIANS for SICK columns: {}'.format(sick_mdn))    
    

# Remove linhas com campos vazios
def remove_empty( dataframe ) :
    dataframe = dataframe.dropna(axis=0, how='any')
    
def main():
    df = df = load_dataset( old_files[0] )
    analyze( df )    
    
if __name__ == '__main__':
    main()
        
#    # Rounding values
#    decimal_places = [ 0, 1, 1, 1, 1, 1, 3, 0 ]
#    places_per_col = pd.Series(decimal_places, index=feature_cols)
#    df = df.round(places_per_col)
#    
#    # Normalizing through MinMax
#    normalize_minmax = []
#    for features in normalize_minmax:
#        df[features] = (df[features]-df[features].min())/(df[features].max()-df[features].min())   
#    # Normalizing through Standard Deviation
#    normalize_mean = feature_cols
#    for features in normalize_mean:  
#        df[features] = (df[features]-df[features].mean())/df[features].std()
#    
#    # Discarding some columns
#    features_to_discard = ['SkinThickness']
#    for features in features_to_discard:
#        df[features] = 1                                                                                                                                                                        
#
#    # Binarizing values
#    features_to_binarize = []
#    for features in features_to_binarize:
#        df[features] = (df[features] > 1).astype(int) 
#    
#    # Saving CSV
#    df.to_csv(new_files[i], index=False, header=True)