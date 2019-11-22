import pandas as pd
import numpy as np
import time
import pickle

#import Orange
base = pd.read_csv('DataFrameVelha1Saida.csv')
base.drop('Unnamed: 0', axis=1, inplace = True)

#Separa os previsores e as respostas (classe).
previsores = base.iloc[:,0:18].values
classe = base.iloc[:,18].values

#Substitui as variaveis categoricas para variaveis numericas.
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
labelEncoder_previsores = LabelEncoder()
previsores[:,0] = labelEncoder_previsores.fit_transform(previsores[:,0])
previsores[:,1] = labelEncoder_previsores.fit_transform(previsores[:,1])
previsores[:,2] = labelEncoder_previsores.fit_transform(previsores[:,2])
previsores[:,3] = labelEncoder_previsores.fit_transform(previsores[:,3])
previsores[:,4] = labelEncoder_previsores.fit_transform(previsores[:,4])
previsores[:,5] = labelEncoder_previsores.fit_transform(previsores[:,5])
previsores[:,6] = labelEncoder_previsores.fit_transform(previsores[:,6])
previsores[:,7] = labelEncoder_previsores.fit_transform(previsores[:,7])
previsores[:,8] = labelEncoder_previsores.fit_transform(previsores[:,8])

#OneHotEncoder

#Escalonamento. As vezes não faz muita diferença, porém facilita a configuração da rede.
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
previsores = scaler.fit_transform(previsores)

#Validação cruzada!    
from sklearn.neural_network import MLPClassifier # Rede Neural.
from sklearn.naive_bayes import GaussianNB # Teste estatistico
from sklearn.tree import DecisionTreeClassifier # Arvore de Decisão
from sklearn.ensemble import RandomForestClassifier # RandomForest
from sklearn.neighbors import KNeighborsClassifier # KNN
from sklearn.linear_model import LogisticRegression #Logistic
from sklearn.svm import SVC

from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold

classe_nayve = []
#Para o NaiveBayes #Melhora os resultados dessa forma.
for i in range(len(classe)):
    classe_nayve.append(np.argmax(classe[i]))
classe_nayve = np.asarray(classe_nayve)

classificador = pickle.load(open('RedeNeuralJogoVelha.sav', 'rb'))

resultados30 = []
for i in range(30):
        
    kfold = StratifiedKFold(n_splits=316,shuffle=True,random_state= i+1)
    resultados = []
    for indice_treinamento, indice_teste in kfold.split(previsores,np.zeros(shape=(previsores.shape[0], 1))):
            
        classificador = MLPClassifier(verbose = True, max_iter=10000,
                                     hidden_layer_sizes=(100,100), tol = 0.00001) # REDE NEURAL.
        #classificador = GaussianNB() # Naive Bayes.
        #classificador = DecisionTreeClassifier() # Arvores de Decisão.
        #classificador = RandomForestClassifier(n_estimators=100,criterion='gini', random_state = 0)
        #classificador = KNeighborsClassifier(n_neighbors=10, metric='minkowski', p=2)
        #classificador = LogisticRegression()
        #classificador = SVC(kernel = 'rbf', random_state = 1,  C = 2.0)
        
        
        classificador.fit(previsores[indice_treinamento], classe[indice_treinamento])
        resultado = classificador.predict(previsores[indice_teste])
        resultados.append(accuracy_score(classe[indice_teste], resultado))
        
    resultados = np.asarray(resultados)
    resultados30.append(resultados.mean())
    print('Teste: {}'.format(i+1))
resultados30 = np.asarray(resultados30)
print('Precisao: {}'.format(resultados30.mean()))          

for i in range(30):
    print(str(resultados30[i]).replace('.',','))


pickle.dump(classificador, open('RedeNeuralJogoVelha.sav', 'wb'))

