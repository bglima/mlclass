# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 17:49:40 2018

@author: brunolima
"""
import numpy as np
import pandas as pd
from pprint import pprint
from diabetes_csv import test
from time import sleep

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
#    print ('[INFO] Loading {} ...'.format(filename))
    dataframe = pd.read_csv( filename )
    return dataframe

# Calcula os valores da média e mediana de pessoas.
# Só pode ser usado no conjunto de treinamento, pois necessita da coluna 'Outcome'
def analyze( dataframe ):
    n_total = dataframe.shape[0]
    # Dataset contendo os doentes e os sadios, respectivamente
    df_heal = dataframe[ dataframe[output_col] == 0 ]
    df_sick = dataframe[ dataframe[output_col] == 1 ]
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
#    print('[INFO] Found {} entries. From which..'.format( n_total ))
#    print('[INFO] {} people are sick'.format(n_sick))
#    print('[INFO] {} people are healthy'.format(n_heal))
#    print('\n[INFO] AVERAGES for HEALTHY columns:')
#    pprint(heal_avg)
#    print('\n[INFO] MEDIANS for HEALTHY columns:')
#    pprint(heal_mdn)
#    print('\n[INFO] AVERAGES for SICK columns:')
#    pprint(sick_avg)
#    print('\n[INFO] MEDIANS for SICK columns:')
#    pprint(sick_mdn)
    
    return n_total, n_heal, n_sick, heal_avg, heal_mdn, sick_avg, sick_mdn
    
# Remove linhas com campos vazios
def remove_empty( dataframe ) :
    new_dataframe = dataframe.dropna(axis=0, how='any')
    return new_dataframe

# Preenche campos vazios com um valor específico
def fill_empty( dataframe, fill_with ):
    # Dicionário com os nomes das colunas como chave
    fill_per_col =  pd.Series(fill_with, index=input_cols)  
    # Copiando e salvando referência para doentes e sadios
    new_dataframe = dataframe.copy()
    df_heal = new_dataframe.loc[new_dataframe[output_col] == 0]
    df_sick = new_dataframe.loc[new_dataframe[output_col] == 1]

    # Para cada parâmetro na lista, idtendifique o tipo
    for key in input_cols:
        # Preencha todos os campos nulos da coluna com 0
        if fill_per_col[ key ] == 'zero':
            new_dataframe[ key ].fillna( 0, inplace=True )
        # Preencha todos os campos nulos da coluna pela média do respectivo Outcome
        elif fill_per_col[ key ] == 'avg':
            new_dataframe.loc[ new_dataframe[output_col] == 0, key ] = df_heal[ key ].fillna( heal_avg[ key ] ) 
            new_dataframe.loc[ new_dataframe[output_col] == 1, key ] = df_sick[ key ].fillna( sick_avg[ key ] ) 
        elif fill_per_col[ key ] == 'mdn':
            new_dataframe.loc[ new_dataframe[output_col] == 0, key ] = df_heal[ key ].fillna( heal_mdn[ key ] ) 
            new_dataframe.loc[ new_dataframe[output_col] == 1, key ] = df_sick[ key ].fillna( sick_mdn[ key ] ) 
    return new_dataframe

# Define o número de casas decimais para cada coluna do dataframe
def round_values( dataframe, decimal_places ) :
    places_per_col = pd.Series(decimal_places, index=input_cols)
    new_dataframe = dataframe.round(places_per_col)    
    return new_dataframe

# Normaliza os valores através de uma função específica.
def normalize( dataframe, normalize_with):
    # Copiando dataframe
    new_dataframe = dataframe.copy()
    # Dicionário com os nomes das colunas como chave
    norm_per_col =  pd.Series(normalize_with, index=input_cols)  
    # Para cada parâmetro na lista, idtendifique o tipo
    for key in input_cols:
        # Preencha todos os campos nulos da coluna com 0
        if  norm_per_col[ key ] == 'mmx':
            new_dataframe[ key ] = ( new_dataframe[key] - new_dataframe[key].min())/(new_dataframe[key].max()-new_dataframe[key].min())   
        elif norm_per_col[ key ] == 'std':
            new_dataframe[ key ] = ( new_dataframe[key] - new_dataframe[key].mean())/new_dataframe[key].std()
    return new_dataframe

# Atribui peso a colunas específicas
def set_weights( dataframe, weight_with ):
    # Copiando dataframe
    new_dataframe = dataframe.copy()
    # Dicionário com os nomes das colunas como chave
    weight_per_col =  pd.Series(weight_with, index=input_cols)
    # Para cada parâmetro na lista, idtendifique o tipo
    for key in input_cols:
        new_dataframe[ key ] = new_dataframe[key] * float( weight_per_col[key] )
    return new_dataframe    

# Discarta o valor de certas colunas
def discard_cols( dataframe, discard_with ):
    # Copiando dataframe
    new_dataframe = dataframe.copy()
    # Dicionário com os nomes das colunas como chave
    discard_per_col =  pd.Series(discard_with, index=input_cols)
    # Para cada parâmetro na lista, idtendifique o tipo
    for key in input_cols:
        if discard_per_col[ key ]: new_dataframe[ key ] = 1
    return new_dataframe  

def step( weights ):
    # =====> CONJUNTO DE TREINO <=====
    train_df = load_dataset( old_files[0] )
    # Extraindo dados do conjunto de treino
    n_total, n_heal, n_sick, heal_avg, heal_mdn, sick_avg, sick_mdn = analyze( train_df )    
    # Removendo campos vazios -- ANULA O FILL-EMPTY
    train_df = remove_empty(train_df)
    # Preenchendo os campos vazios -- APENAS SE remove_empty NÃO FOR USADO
    # train_df = fill_empty(train_df,   ['avg', 'avg', 'avg', 'avg', 'avg', 'avg', 'avg', 'avg'] )
    
    
    # =====> CONJUNTO DE TESTES <=====
    test_df = load_dataset( old_files[1] )
    
    # ======> OPERAÇÕES EM AMBOS <=====
    df_list = [train_df, test_df]
    for i in range(0, 2):
        # Normalizando os valores
        df_list[i] = normalize(df_list[i],    ['mmx', 'mmx', 'mmx', 'mmx', 'mmx', 'mmx', 'mmx', 'mmx'] )
        # Discartando algumas colunas. 0 significa manter.
        df_list[i] = discard_cols(df_list[i],    [0, 0, 0, 0, 0, 0, 0, 1] )
        # Setando pesos
        df_list[i] = set_weights(df_list[i],  weights)
        # Arredonando as casas decimais
        df_list[i] = round_values(df_list[i], [ 3,   3,   3,   3,   3,   3,   3,   3] )  
        # Salvando o CSV
        df_list[i].to_csv(new_files[i], index=False, header=True)         
     
    return test()

        
if __name__ == '__main__':
    weights = [ 8.08,  7.03, -1.33, 10.47,  1.39, -0.34, -0.86,  4.11]
# =========>    weights = [ 8.08,  7.03, -1.33, 10.47,  1.39, -0.34, -0.86,  4.11]
# =========>    weights = [ 7.96,  9.73,  2.13, 14.47, -0.2,   2.18,  2.34,  1.5 ]
# 
# Max prec from [ 8.08  7.03 -1.33 10.47  1.39 -0.34 -0.86  4.11] with 0.86734693877551 discarding 8 e removendo vazios
# Max prec from [ 8.63  7.09 -1.57 10.93  1.12 -0.56 -0.99  4.29] with 0.85714285714286 discarding 8 e removendo vazios
# Max prec from [ 8.62  7.81 -0.7  12.43  0.17  3.24 -0.74  4.24] with 0.85204081632653 discarding 8 e removendo vazios
# Max prec from [ 6.47  5.65  0.08  8.82  0.65 -0.23 -1.01  0.75] with 0.85204081632653 discarding 8 e removendo vazios
# Max prec from [ 8.23  7.12 -1.71 10.38  0.08  2.01 -0.6   1.88] with 0.8469387755102 discarding 8 e removendo vazios
# Max prec from [10.92  8.05  1.37 12.   -0.96  0.15  4.87  1.05] with 0.84183673469388 discarding 8 e removendo vazios
# Max prec from [10.42  9.45  0.82 16.85  0.38 -1.4  -0.85 -1.79] with 0.84183673469388 discarding 8 e removendo vazios
# Max prec from [11.79  9.16 -2.06 12.53 -1.29  0.3  -0.51 -0.43] with 0.83163265306122 discarding 8 e removendo vazios
# Max prec from [ 7.96  9.73  2.13 14.47 -0.2   2.18  2.34  1.5 ] with 0.82142857142857 discarding 8 e removendo vazios
# Max prec from [ 4.07 10.95  4.25  9.84  4.26  3.34  6.74  4.61] with 0.81632653061224 discarding nothing e removendo vazios
# Max prec from [ 4.06 10.95  4.18  9.74  4.41  3.49  6.48  4.56] with 0.81632653061224 discarding nothing e removendo vazios
# Max prec from [ 3.19 10.46  3.8   9.37  3.75  3.22  5.78  4.25] with 0.81122448979592 discarding nothing e removendo vazios
# Max prec from [2.05 9.28 3.   8.13 2.89 2.3  4.54 4.09] with 0.81122448979592 discarding 6 and 8    
# Max prec from [4.72 7.55 2.6  7.7  1.87 4.85 2.74 1.1 ] with 0.80102040816327 doscardomg 8    
# Max prec from [1.75 6.96 1.76 6.65 1.61 2.69 2.11 1.01] with 0.80102040816327 discarding 8
# Max prec from [2.37 6.39 1.77 7.53 4.81 2.13 3.83 4.51] with 0.79591836734694 discading nothing    
# Max prec from [5.84 6.45 2.12 1.68 1.21 5.49 4.73 2.86] with 0.81632653061224 discarding 4, 6 and 8
# Max prec from [5.99 6.52 2.25 0.78 1.2  5.14 4.84 2.33] with 0.81122448979592 discarding 4, 6 and 8
# Max prec from [5.08 5.94 1.77 1.41 0.92 5.25 4.43 2.63] with 0.81122448979592 discarding 4, 6 and 8
# Max prec from [5.03 5.27 1.49 0.76 0.35 5.16 3.55 2.44] with 0.80612244897959 discarding 6 and 8
# Max prec from [4.98 4.61 1.92 0.72 0.6  5.51 2.98 2.81] with 0.79081632653061 discarding 6 and 8
# Acc for [4.31 3.78 1.45 0.66 0.35 4.62 2.69 2.31] is 0.79081632653061 discarding 6 and 8
# Acc for [1.64 3.51 1.55 3.98 2.54 1.71 2.11 2.32] is 0.79591836734694 
# Acc for [1.05 1.06 1.1  1.08 1.04 1.06 1.   1.04] is 0.79081632653061    
# Acc for [1.0, 1.0, 1.0, 0.3, 0.9, 1.0, 3.0, 0.9] is: 0.78
# Acc for [1.62 3.49 1.49 3.92 2.45 1.68 2.08 2.29] is: 0.79
# Acc for [1.14 1.6  1.37 0.05 1.11 1.28 3.72 1.44] is: 0.78061224489796
   
    max_prec = 0
    max_weight = []
    curr_prec = step(weights)
    print('Acc for {} w/o thresh: {}'.format(weights, curr_prec))
    
    for i in range (0, 80):
        max_rand = 1.0
        thresh = (np.random.rand(8) * max_rand) - max_rand / 2.0
        thresh = np.round(thresh, 2)
        
        new_weights = weights + thresh
        
        curr_prec = step(new_weights)
        curr_loss = 1 - curr_prec
        
        if curr_prec > max_prec: 
            max_prec = curr_prec
            max_weight = new_weights
        
        print('Acc for {} is {}'.format(new_weights, curr_prec))
    
    print('\nMax prec from {} with {}'.format(max_weight, max_prec))