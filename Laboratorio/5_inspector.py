#Requirement: scikit-learn 1.0.2
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.ensemble import RandomForestRegressor
from joblib import dump, load

#The Machine learning alogorithm
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_digits
from sklearn.preprocessing import scale

# Para utilizar o arquivo joblib (após o treino da ML)
try:
    clf = load('cls_hping3_rf.joblib')
except FileNotFoundError:
    clf = load('classifier_rf.joblib')

filename = 'classifier.sav'
classifier = joblib.load(filename)

# Para utilizar apenas para visualização
try:
    dt_realtime = pd.read_csv('data/realtime.csv')
except FileNotFoundError:
    dt_realtime = pd.read_csv('realtime.csv')



result = clf.predict(dt_realtime)

with open('.result', 'w') as f:
    f.write(str(result[0]))
