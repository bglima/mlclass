
# coding: utf-8

# In[1]:


import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# Describing the dataset columns



data = pd.read_csv('abalone_dataset.csv')
data.describe()


# ## Checking for null values in each column

# In[3]:


for column in data.columns.values:
    print('{} null values in column \'{}\'.'.format((data[column].isnull()).sum(), column  ))


# ## Checking data types

# In[4]:


data.dtypes


# ## Transforming categorical column to number

# In[5]:


transform_dict = {"sex":{"F": 1, "I":2, "M": 3} }
data.replace( transform_dict, inplace=True )
print(data.dtypes)


# ## Checking class balance and defining class column

# In[6]:


from collections import Counter
import matplotlib.pyplot as plt

def plot_pie(y):
    target_stats = Counter(y)
    labels = list(target_stats.keys())
    sizes = list(target_stats.values())
    explode = tuple([0.1] * len(target_stats))
    
    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, shadow=True,
           autopct='%1.1f%%')
    ax.axis('equal')

# Defining target class dataset
y = data[ data.columns.values[-1] ]

# Plotting
plot_pie(y)  

# Describe
y.describe()


# 
# 
# ## Analyzing distribution of columns

# In[7]:


data.hist(figsize=(20, 20), bins=30)
plt.plot()


# 
# ## Analyzing correlation between columns

# In[8]:


import seaborn as sns

# Function to plot the corr graph
def plot_corr(data):
    # Defining correlation between variables
    correlations = data.corr()

    # plot correlation matrix
    fig = plt.figure(figsize=(20, 20))
    ax = fig.add_subplot(111)
    cax = ax.matshow(correlations, vmin=-1, vmax=1)
    fig.colorbar(cax)
    ticks = np.arange(0, len(data.columns.values), 1)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.set_xticklabels(data.columns.values)
    ax.set_yticklabels(data.columns.values)
    plt.xticks(size = 12)
    plt.yticks(size = 15)
    plt.show()

data.describe()
plot_corr(data)


# ## Creating the X (no-class) dataframe

# In[9]:


from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

print('\nColumns in data: ', data.columns.values)
X = data[ data.columns.values[:-1] ] # Mantaining all columns, except the last one (type column)
print('\nColumns in X; ', X.columns.values)
X.describe()


# ## Splitting dataset into training and test

# In[10]:


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)


# ## Using MLP as neural network
# 
# For futher info, go [here](https://www.kdnuggets.com/2016/10/beginners-guide-neural-networks-python-scikit-learn.html/2).
# 
# MLP is sensible to data scaling, so we need to normalize the data beforehand:
# 

# In[13]:


from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
scaler.fit(X_train) # Fit only to the training data

X_train = scaler.transform(X_train) # Now apply the transformations to the data:
X_test = scaler.transform(X_test)


# ## Training the model

# In[14]:


from sklearn.neural_network import MLPClassifier

# Defining only the hidden layers size. 
mlp = MLPClassifier(hidden_layer_sizes=(30,30,30)) # 3 layers with 30 neurons each

# Fit the moel
mlp.fit(X_train,y_train)

# ## Predictions and evaluation

# In[16]:

predictions = mlp.predict(X_test)
from sklearn.metrics import classification_report,confusion_matrix
print('Confusion matrix: \n', confusion_matrix(y_test,predictions))
print('Classification report: \n', classification_report(y_test,predictions))


#%% Load TARGET data to predict

X_target = pd.read_csv('abalone_app.csv') # Load dataset

X_target.replace( transform_dict, inplace=True )

scaler.transform(X_target) # Scale (normalize) dataset
X_target.describe()
predictions = mlp.predict(X_target) # Make predictions



#%%

# Send result to server

import requests

# Enviando previsões realizadas com o modelo para o servidor
URL = "https://aydanomachado.com/mlclass/03_Validation.php"

#TODO Substituir pela sua chave aqui
DEV_KEY = "BJN"

# json para ser enviado para o servidor
data = {'dev_key':DEV_KEY,
        'predictions':pd.Series(predictions).to_json(orient='values')}

# Enviando requisição e salvando o objeto resposta
r = requests.post(url = URL, data = data)

# Extraindo e imprimindo o texto da resposta
#    pastebin_url = r.text
#    print(" - Resposta do servidor:\n", r.text, "\n")
print( 'UAU CABAMO ACURACY: ', r.json().get('accuracy')    )
