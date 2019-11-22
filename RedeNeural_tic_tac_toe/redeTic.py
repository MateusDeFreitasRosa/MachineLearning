# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 00:25:56 2019

@author: mateu
"""
import pandas as pd
import numpy as np
import pickle
#base = pd.read_csv('DataFrameVelha.csv')
#base.drop('Unnamed: 0', axis=1, inplace = True)

#Adicionando Rede Neural ao Jogo
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

classificador_RedeNeural = pickle.load(open('Classficador_RedeNeural_JogodaVelha.sav', 'rb'))
classificador_LogisticRegression = pickle.load(open('Classificador_LogisticRegression_JogodaVelha.sav', 'rb'))
classificador_RandomForest = pickle.load(open('Classificador_RandomForest_JogodaVelha.sav', 'rb'))
scaler = pickle.load(open('scaler_JogodaVelha.sav', 'rb'))



#Jogo da Velha

def finish(tab):
    for i in tab:
        for j in i:
            if (j == 'b'):
                return False
    return True

def mark(tab):
    cont = 0
    for i in tab:
        for k in i:
            if (k != 'b'):
                cont+=1
    if (cont%2 == 0):
        return 'x'
    else:
        return 'o'

def Victory(tab):
    deepth = 1
    for i in tab:
        for j in i:
            if j == 'b':
                deepth +=1
            
    xWin = ['x','x','x']
    oWin = ['o','o','o']
    if (tab[0][0:3] == xWin or tab[1][0:3] == xWin or tab[2][0:3] == xWin):
        return (-10 + deepth, 'x')
    if ([tab[0][0],tab[1][0],tab[2][0]] == xWin):
        return (-10 + deepth, 'x')
    if([tab[0][1],tab[1][1],tab[2][1]] == xWin):
         return (-10 + deepth, 'x')
    if([tab[0][2],tab[1][2],tab[2][2]] == xWin):
         return (-10 + deepth, 'x')
    if([tab[0][2],tab[1][1],tab[2][0]] == xWin or [tab[0][0],tab[1][1],tab[2][2]] == xWin):
         return (-10 + deepth, 'x')
    
    if (tab[0][0:3] == oWin or tab[1][0:3] == oWin or tab[2][0:3] == oWin):
         return (10 - deepth,'o')
    if ([tab[0][0],tab[1][0],tab[2][0]] == oWin):
        return (10 - deepth,'o')
    if([tab[0][1],tab[1][1],tab[2][1]] == oWin):
        return (10 - deepth,'o')
    if([tab[0][2],tab[1][2],tab[2][2]] == oWin):
        return (10 - deepth,'o')
    if([tab[0][2],tab[1][1],tab[2][0]] == oWin or [tab[0][0],tab[1][1],tab[2][2]] == oWin):
        return (10 - deepth,'o')
    return (0,None)


def ImprimeTabuleiro(tab):
    line = 0
    print('   0\t1\t2')
    for l in tab:
        print(str(line)+'  ', end='')
        for k in l:
            if (k == 'b'):
                print('.\t', end='')
            else:
                print(k+'\t', end='')
        print('\n')
        line+=1
        
def contColLines(tab,what,pos,player):
    cont = 0
    block = False
    
    contraPlayer = 'x' if player == 'o' else 'o'
    
    if (what == 'lines'):
        for i in range(3):
            if tab[pos][i] == player:
                cont+=1
            elif tab[pos][i] == contraPlayer:
                block = True
                
    elif (what == 'cols'):
        for i in range(3):
            if tab[i][pos] == player:
                cont+=1
            elif tab[i][pos] == contraPlayer:
                block = True
                
    return cont if block == False else 0     

    
def TabuleiroParaRedeNeural(tab):
    var = []
    global guardaTab
    for i in range(3):
        for j in range(3):
            if tab[i][j] == 'b':
                var.append('0')
            elif tab[i][j] == 'o':
                var.append('1')
            elif tab[i][j] == 'x':
                var.append('2')
    
    var.append('0' if (tab[1][1] == 'b') else '1')
    
    for i in range(3):
        if contColLines(tab, 'cols', i,'x') == 2:
            var.append('1')
        elif contColLines(tab, 'cols', i,'o') == 2:
            var.append('2')
        else:
            var.append('0')
    
    for i in range(3):
        if contColLines(tab, 'lines', i,'x') == 2:
            var.append('1')
        elif contColLines(tab, 'lines', i,'o') == 2:
            var.append('2')
        else:
            var.append('0')
        
    if (tab[0][0] == 'x' and tab[1][1] == 'x' and tab[2][2] =='b') or \
        (tab[1][1] == 'x' and tab[2][2] == 'x' and tab[0][0] == 'b')or \
        (tab[0][0] == 'x' and tab[2][2] == 'x' and tab[1][1] == 'b'):
        var.append('1')
    elif (tab[0][0] == 'o' and tab[1][1] == 'o' and tab[2][2] =='b') or \
        (tab[1][1] == 'o' and tab[2][2] == 'o' and tab[0][0] =='b') or \
        (tab[0][0] == 'o' and tab[2][2] == 'o' and tab[1][1] =='b'):
        var.append('2')
    else:
        var.append('0')

    
    if (tab[0][2] == 'x' and tab[1][1] == 'x' and tab[2][0] =='b') or \
        (tab[1][1] == 'x' and tab[2][0] == 'x' and tab[0][2] == 'b')or \
        (tab[0][2] == 'x' and tab[2][0] == 'x' and tab[1][1] == 'b'):
        var.append('1')
    elif (tab[0][2] == 'o' and tab[1][1] == 'o' and tab[2][0] =='b') or \
        (tab[1][1] == 'o' and tab[2][0] == 'o' and tab[0][2] =='b') or \
        (tab[0][2] == 'o' and tab[2][0] == 'o' and tab[1][1] =='b'):
        var.append('2')
    else:
        var.append('0')
        
    var = np.array((var), dtype = float)
    var = var.reshape(1,-1)
    
    return var

def Decide(vetorResultados):
    resultado = [int(0)]*9
    
    for i in vetorResultados:
        resultado[int(i)] +=1 
    
    resultado = np.asarray(resultado)
    
    if resultado.max() >= 2:
        return resultado.argmax()
    else:
        return vetorResultados[0] # Isso representa que o maior peso é atribuido a RedeNeural.

def Start():
    tabuleiro = [['b','b','b'], ['b','b','b'], ['b','b','b']]
    #guardaTab = []
    while True:
        
        while True:
            ImprimeTabuleiro(tabuleiro)
            if (mark(tabuleiro) == 'x'):
                print('Vez do Jogador\nMarque uma posição. -> informando a linha e a coluna')
                print('OBS: Linha e coluna se iniciam de 0 à 2\n\n')
                a = int(input('Digite a Linha'))
                b = int(input('Digite a Coluna'))
                tabuleiro[a][b] = mark(tabuleiro)
                TabuleiroParaRedeNeural(tabuleiro)
            
            else:
                print('Vez da IA')
                #where = len(guardaTab)
                resultado_RedeNeural = classificador_RedeNeural.predict(TabuleiroParaRedeNeural(tabuleiro))
                resultado_LogisticRegression = classificador_LogisticRegression.predict(TabuleiroParaRedeNeural(tabuleiro))
                resultado_RandomForest = classificador_RandomForest.predict(TabuleiroParaRedeNeural(tabuleiro))
                print('Opnião RedeNeural: {}'.format(resultado_RedeNeural[0]))
                print('Opnião LogisticRegression: {}'.format(resultado_LogisticRegression[0]))
                print('Opnião RandomForest: {}'.format(resultado_RandomForest[0]))
                
                vetorResultados = [resultado_RedeNeural, resultado_LogisticRegression, resultado_RandomForest]
                
                jogar = Decide(vetorResultados)
                tabuleiro[int(jogar/3)][jogar%3] = mark(tabuleiro)
                
                input()
                
            r,win = Victory(tabuleiro)
            if win != None or finish(tabuleiro):
                break
                
        r, win = Victory(tabuleiro)  
        if win ==  'x':
            print('Jogador venceu')
        elif win == 'o':
            print('Bot venceu')
        else:
            print('Empate')
        print('Fim de Jogo')
        tabuleiro = [['b','b','b'], ['b','b','b'], ['b','b','b']]
        print('Deseja jogar novamente? - Finish para terminar')
        if (input().lower() == 'finish'):
            break
            
Start()        
        
        
#
#xgboost
#Disciplina SOO
#GS1519-MC Sistemas Operacionais 
#senha: 123pinSO
        
        
        