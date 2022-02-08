# -*- coding: utf-8 -*-
"""RF-Covid-19.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QbnNMvQfQLL_J2woTT6UjvfxfSxu1D_K
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import metrics
import matplotlib.pyplot as plt

dataset = pd.read_csv('https://raw.githubusercontent.com/pateltanvi2992/Covid-19-Classification-dataset/main/Corona-1.csv')

dataset = dataset[dataset.cough != "None"]
dataset["cough"] = dataset["cough"].astype(str).astype(int)
dataset = dataset[dataset.fever != "None"]
dataset["fever"] = dataset["fever"].astype(str).astype(int)
dataset["sore_throat"] = dataset["sore_throat"].astype(str).astype(int)
dataset["shortness_of_breath"] = dataset["shortness_of_breath"].astype(str).astype(int)
dataset["head_ache"] = dataset["head_ache"].astype(str).astype(int)
dataset = dataset[dataset.corona_result != "other"]
dataset = dataset[dataset.gender != "None"]
dataset = dataset[dataset.age_60_and_above != "None"]

print(dataset['gender'].unique())

print(dataset['test_indication'].unique())

from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()

encoder.fit(dataset['gender'])
dataset['gender'] = encoder.transform(dataset['gender'])

encoder.fit(dataset['age_60_and_above'])
dataset['age_60_and_above'] = encoder.transform(dataset['age_60_and_above'])

encoder.fit(dataset['test_indication'])
dataset['test_indication'] = encoder.transform(dataset['test_indication'])

from sklearn.preprocessing import LabelEncoder
y=dataset.iloc[:,6]
le = LabelEncoder()
y = le.fit_transform(y)
X=dataset.iloc[:,[1,2,3,4,5,7,8,9]]

from sklearn.model_selection import train_test_split 
from sklearn.ensemble import RandomForestClassifier 

#split the dataset into training (70%) and testing (30%) sets
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3,random_state=1) 

RFclassifier= RandomForestClassifier(n_estimators= 10, criterion="entropy") 

RFclassifier.fit(X_train, y_train)

import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 1200
#define metrics
y_pred_proba = RFclassifier.predict_proba(X_test)[::,1]
fpr, tpr, _ = metrics.roc_curve(y_test,  y_pred_proba)
auc = metrics.roc_auc_score(y_test, y_pred_proba)

#create ROC curve
plt.plot(fpr,tpr,label="AUC="+str(auc))
plt.plot([0,1],[0,1],'r--')
plt.ylabel('Sensitivity')
plt.xlabel('1 – specificity')
plt.legend(loc=4)
plt.show()

from sklearn.metrics import accuracy_score,confusion_matrix
y_pred=RFclassifier.predict(X_test)
accuracy_score(y_test,y_pred)

RF_matrix=confusion_matrix(y_test,y_pred)

from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
f1_score(y_test, y_pred, average='weighted')

precision_score(y_test,y_pred)

recall_score(y_test,y_pred)

accuracy_score(y_test,y_pred)

import seaborn as sns
RF_matrix=confusion_matrix(y_test,y_pred)
sns.heatmap(RF_matrix, annot=True, cmap='Reds')
