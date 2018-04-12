# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 15:24:52 2018

@author: brunolima
"""

from weka.core.converters import Loader
import weka.core.jvm as jvm
import weka.core.serialization as serialization
from weka.classifiers import Classifier
import wekaexamples.helper as helper
import operator
import numpy as np
import pandas as pd
import requests

#starting JVM
jvm.start()

objects = serialization.read_all("myModelLMT.model")
cls = Classifier(jobject=objects[0])
print(cls)

# load CSV file
helper.print_title("Loading ARFF file")
loader = Loader(classname="weka.core.converters.CSVLoader")
test = loader.load_file("abalone_app.csv")
test.class_is_last()


#%%
# output predictions
y_pred = np.ndarray([]).astype(int)

print("# - actual - predicted - error - distribution")
for index, inst in enumerate(test): 
   pred = cls.classify_instance(inst)
    
   dist = cls.distribution_for_instance(inst)

   max_index, value = max(enumerate(dist), key=operator.itemgetter(1))
   
   predicted= max_index + 1 
   print( index, predicted )
   
   y_pred = np.append( y_pred, predicted )
y_pred = y_pred[1:]
print(y_pred)

#%%

# Enviando previsões realizadas com o modelo para o servidor
URL = "https://aydanomachado.com/mlclass/03_Validation.php"

#TODO Substituir pela sua chave aqui
DEV_KEY = "BJN"

# json para ser enviado para o servidor
data = {'dev_key':DEV_KEY,
        'predictions':pd.Series(y_pred).to_json(orient='values')}

# Enviando requisição e salvando o objeto resposta
r = requests.post(url = URL, data = data)

# Extraindo e imprimindo o texto da resposta
#    pastebin_url = r.text
#    print(" - Resposta do servidor:\n", r.text, "\n")
print( 'UAU CABAMO ACURACY: ', r.json().get('accuracy')    )

#%%

#stopping JVM
jvm.stop()