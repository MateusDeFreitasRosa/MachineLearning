import pandas as pd
import numpy as np
import time
import pickle

base = pd.read_csv('.csv')
base.drop('Unnamed: 0', inplace = True, axis=1)
###################################################

def SaveDataFrame(base):
    name = input('Nomeie o arquivo.')
    base.to_csv(name+'.csv')

#Exclusão de repetições
def DeleteRepetitions(base):
    for i in range(len(base)):
        print('Verificando: {}'.format(i))
        if not base.TL[i] == 'drop':
            t = base.iloc[i,:].values
            for j in range(i+1,len(base)):
                if np.all(t == base.loc[j,:].values):
                    if not base.TL[j] == 'drop':
                        base.TL[j] = 'drop'
    
    base.drop(base[base.TL == 'drop'].index, inplace = True, axis=0)
    print('Tamanho da base de dados: {}'.format(len(base)))

inicio = time.time()
DeleteRepetitions(base)
fim = time.time()
print('Execução durou: {}'.format(fim-inicio))

base2 = pd.read_csv('DataFrameVelha.csv')
#############################################DataFrameVelha1Saida##################################

#Separa os previsores e as respostas (classe).
previsores = base.iloc[:,0:18].values
classe = base.iloc[:,18].values

#Resumindo 8 camadas de saida para uma (O resultado acaba ficamando melhor dessa maneira).
for i in range(len(classe)):
    base.RTL[i] = classe[i].argmax()

base.to_csv('DataFrameVelha1Saida.csv')

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

#Separando dados entre treinamento e teste.
from sklearn.model_selection import train_test_split
previsores_treinamento, previsores_teste, classe_treinamento, classe_teste = train_test_split(previsores,classe,test_size=0.10,random_state=0)

#Criação da rede neural do scikit.
from sklearn.neural_network import MLPClassifier
#10000 interações, com uma tolerancia de .0001, 
classificador = MLPClassifier(verbose = True, max_iter=10000,
                              hidden_layer_sizes=(100,100,100), tol = 0.0001)
classificador.fit(previsores,classe)
resultado = classificador.predict(previsores)

from sklearn.linear_model import LogisticRegression
classificador_LogisticRegression = LogisticRegression(max_iter=1000, verbose = True, random_state=0)
classificador_LogisticRegression.fit(previsores,classe)
resultado = classificador_LogisticRegression.predict(previsores)

from sklearn.ensemble import RandomForestClassifier
classificador_RandomForest = RandomForestClassifier(n_estimators=100)
classificador_RandomForest.fit(previsores,classe)
resultado = classificador_RandomForest.predict(previsores)


from sklearn.metrics import confusion_matrix, accuracy_score
score = 0
score = accuracy_score(classe,resultado)
matriz = confusion_matrix(classe_teste,resultado) 


#### Salve classifier
pickle.dump(classificador, open('Classficador_RedeNeural_JogodaVelha.sav', 'wb'))
pickle.dump(classificador_LogisticRegression, open('Classificador_LogisticRegression_JogodaVelha.sav', 'wb'))
pickle.dump(classificador_RandomForest, open('Classificador_RandomForest_JogodaVelha.sav', 'wb'))
pickle.dump(scaler, open('scaler_JogodaVelha.sav', 'wb'))



#Validação cruzada!
from sklearn.model_selection import StratifiedKFold
kfold = StratifiedKFold(n_splits=10,shuffle=True,random_state=0)
resultados = []
    
for indice_treinamento, indice_teste in kfold.split(previsores,np.zeros(shape=(previsores.shape[0], 1))):
    classificador.fit(previsores[indice_treinamento], classe[indice_treinamento])
    resultado = classificador.predict(previsores[indice_teste])
    resultados.append(accuracy_score(classe[indice_teste], resultado))
    
resultados = np.asarray(resultados)
print('Media de acerto: {}'.format(resultados.mean()))