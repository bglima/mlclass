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
heal_std = {} # Dicionario com os desvios padroes dos sadios
sick_std = {} # Dicionario com os desvios padroes dos doentes

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
        heal_std[ key ] = df_heal[ key ].std()
        sick_std[ key ] = df_sick[ key ].std()
    # Log das infos obtidas
#    print('[INFO] Found {} entries. From which..'.format( n_total ))
#    print('[INFO] {} people are sick'.format(n_sick))
#    print('[INFO] {} people are healthy'.format(n_heal))
#    print('\n[INFO] AVERAGES for HEALTHY columns:')
#    pprint(heal_avg)
#    print('\n[INFO] MEDIANS for HEALTHY columns:')
#    pprint(heal_mdn)
#    print('\n[INFO] STD DEVIATION for HEALTHY columns:')
#    pprint(heal_std)
#    
#    print('\n[INFO] AVERAGES for SICK columns:')
#    pprint(sick_avg)
#    print('\n[INFO] MEDIANS for SICK columns:')
#    pprint(sick_mdn)
#    print('\n[INFO] STD DEVIATION for SICK columns:')
#    pprint(sick_std)
    
    return n_total, n_heal, n_sick, heal_avg, heal_mdn, heal_std, sick_avg, sick_mdn, sick_std
    
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
    n_total, n_heal, n_sick, heal_avg, heal_mdn, heal_std, sick_avg, sick_mdn, sick_std = analyze( train_df )    
    # Removendo campos vazios -- ANULA O FILL-EMPTY
    #train_df = remove_empty(train_df)
    # Preenchendo os campos vazios -- APENAS SE remove_empty NÃO FOR USADO
    train_df = fill_empty(train_df,   ['avg', 'avg', 'avg', 'avg', 'avg', 'avg', 'avg', 'avg'] )
    
    
    # =====> CONJUNTO DE TESTES <=====
    test_df = load_dataset( old_files[1] )
    
    # ======> OPERAÇÕES EM AMBOS <=====
    df_list = [train_df, test_df]
    for i in range(0, 2):
        # Normalizando os valores
        df_list[i] = normalize(df_list[i],    ['mmx', 'mmx', 'mmx', 'mmx', 'mmx', 'mmx', 'mmx', 'mmx'] )
        # Discartando algumas colunas. 0 significa manter.
        df_list[i] = discard_cols(df_list[i],    [1, 0, 0, 0, 0, 0, 0, 1] )
        # Setando pesos
        df_list[i] = set_weights(df_list[i],  weights)
        # Arredonando as casas decimais
        df_list[i] = round_values(df_list[i], [ 5,   5,   5,  5,  5,  5,  5,  5] )  
        # Salvando o CSV
        df_list[i].to_csv(new_files[i], index=False, header=True)         
     
    return test()

        
if __name__ == '__main__':
    weights = [ 6.6,   2.35,  5.99 , 0.75,  2.99 ,-7.18 , 8.68, -4.83]
# # Norma minmax, discartando 1 e 8, substituindo vazios pela média, arredondando com 5 dp
# Max prec from [ 6.6   2.35  5.99  0.75  2.99 -7.18  8.68 -4.83] with 0.78061224489796    

    max_prec = 0
    max_weight = []
    curr_prec = step(weights)
    print('Acc for {} w/o thresh: {}'.format(weights, curr_prec))
    
    for i in range (0, 150):
        max_rand = 10    
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