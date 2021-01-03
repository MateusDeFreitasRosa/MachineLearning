# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 19:29:46 2019

@author: mateu
"""
import csv
import random
# X -> 1
# O -> 0

####################################################  -- > Mineração de Dados! <--
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

def SaveData(tab, respostaTab, c):
    aux = ''
    for i in tab:
        for j in i:
            aux += j
            aux += ','
            
    aux += ('0' if tab[1][1] == 'b' else '1')
    aux += ','
    
    for i in range(3):
        if contColLines(tab, 'cols', i,'x') == 2:
            aux+='1'
        elif contColLines(tab, 'cols', i,'o') == 2:
            aux+='2'
        else:
            aux+='0'
        aux+=','
    
    for i in range(3):
        if contColLines(tab, 'lines', i,'x') == 2:
            aux+='1'
        elif contColLines(tab, 'lines', i,'o') == 2:
            aux+='2'
        else:
            aux+='0'       
        aux+=','
        
    if (tab[0][0] == 'x' and tab[1][1] == 'x' and tab[2][2] =='b') or \
        (tab[1][1] == 'x' and tab[2][2] == 'x' and tab[0][0] == 'b')or \
        (tab[0][0] == 'x' and tab[2][2] == 'x' and tab[1][1] == 'b'):
        aux+='1'
    elif (tab[0][0] == 'o' and tab[1][1] == 'o' and tab[2][2] =='b') or \
        (tab[1][1] == 'o' and tab[2][2] == 'o' and tab[0][0] =='b') or \
        (tab[0][0] == 'o' and tab[2][2] == 'o' and tab[1][1] =='b'):
        aux+='2'
    else:
        aux+='0'
    
    aux+=','
    
    if (tab[0][2] == 'x' and tab[1][1] == 'x' and tab[2][0] =='b') or \
        (tab[1][1] == 'x' and tab[2][0] == 'x' and tab[0][2] == 'b')or \
        (tab[0][2] == 'x' and tab[2][0] == 'x' and tab[1][1] == 'b'):
        aux+='1'
    elif (tab[0][2] == 'o' and tab[1][1] == 'o' and tab[2][0] =='b') or \
        (tab[1][1] == 'o' and tab[2][0] == 'o' and tab[0][2] =='b') or \
        (tab[0][2] == 'o' and tab[2][0] == 'o' and tab[1][1] =='b'):
        aux+='2'
    else:
        aux+='0'
        
    aux+=','
    a,b = respostaTab
    contI = 0
    for i in range(3):
        contI +=1
        contJ = 0
        for j in range(3):
            contJ +=1
            if (i == a and j == b):
                aux += '1'
            else:
                aux += '0'
            if not (contI == 3 and contJ == 3):
                aux +=','
    print(aux)
    c.writerow([aux])
############################################################################################################    

##Script IA Jogo da velha.
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
    

biggerNow = -10000
pos = ()
rewards = 0
verificando = []
def WhereThrow(tab):
    global rewards
    global biggerNow
    global pos
    corrigir = False
    
    t1 = [['b', 'x', 'b'], ['b', 'o', 'x'], ['b', 'b', 'b']]
    t2 = [['b', 'x', 'b'], ['x', 'o', 'b'], ['b', 'b', 'b']]
    t3 = [['b', 'b', 'b'], ['b', 'o', 'x'], ['b', 'x', 'b']]
    t4 = [['b', 'b', 'b'], ['x', 'o', 'b'], ['b', 'x', 'b']]
    
    if t1 == tab or t2 == tab or t3 == tab or t4 == tab:
        corrigir = True
    
    if t1 == tab and corrigir == True:
        pos=(0,2)
    elif t2 == tab and corrigir == True:
        pos=(0,0)
    elif t3 == tab and corrigir == True:
        pos=(2,2)
    elif t4 == tab and corrigir == True:
        pos=(2,0)
        
    if corrigir == False:
        r,win = Victory(tab)
        if (finish(tab) == True or win != None):
            r,win = Victory(tab)
            rewards += r 
            #print('Rewards: {}'.format(rewards))
            return
        else:
            willWin = False
            victories = []
            for i in range(3):
                for j in range(3):
                    if (tab[i][j] == 'b'):
                        tab[i][j] = mark(tab)
                        r,win = Victory(tab)
                        
                        if win == 'o':
                            willWin = True
                            victories.append((i,j))
                        tab[i][j] = 'b'
                        
            if (willWin == True):
                while(victories.__len__() != 0 ):
                    a,b = victories.pop()
                    tab[a][b] = mark(tab)
                    
                    if not verificando:
                        verificando.append((a,b))
                        r,win = Victory(tab)
                        if win == 'o':
                            rewards += 10
                            for i in range(3):
                                for j in range(3):
                                        
                                    if tab[i][j] == 'b':
                                        tab[i][j] = 'x'
                                        r,win = Victory(tab)
                                        if  win == 'x':
                                            rewards -= 200
                                        tab[i][j] = 'b'    
                    
                    WhereThrow(tab)
                    tab[a][b] = 'b'
                   
                    l,f = verificando[0]
                            
                    if tab[l][f] == 'b':
                        if (rewards > biggerNow):
                            biggerNow = rewards
                            pos = (a,b)
                        verificando.pop()
                        rewards = 0
                        
            else:          
                for l in range(3):
                    for k in range(3):
                        if (tab[l][k] == 'b'):
                            tab[l][k] = mark(tab)
                            if not verificando:
                                verificando.append((l,k))
                                r,win = Victory(tab)
                                if win == 'o':
                                    rewards += 10
                                for i in range(3):
                                    for j in range(3):
                                        
                                        if tab[i][j] == 'b':
                                            tab[i][j] = 'x'
                                            r,win = Victory(tab)
                                            if  win == 'x':
                                                rewards -= 200
                                            tab[i][j] = 'b'            
                            WhereThrow(tab)
                            
                            tab[l][k] = 'b'
                            a,b = verificando[0]
                            
                            if tab[a][b] == 'b':
                                if (rewards > biggerNow):
                                    biggerNow = rewards
                                    pos = (l,k)
                                verificando.pop()
                                rewards = 0


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


def startJogoVelha():
    c = csv.writer(open('Data_JogoVelha.csv', 'w', newline=''), delimiter =';')
    c.writerow(['TL,TM,TR,ML,MM,MR,BL,BM,BL,MID,TMBL,TMBM,TMBR,LMRT,LMRM,LMRB,DP,DS,RTL,RTM,RTR,RML,RMM,RMR,RBL,RBM,RBR'])
    cont = 0
    while True:    
        tabuleiro = [['b','b','b'], ['b','b','b'], ['b','b','b']]
        ImprimeTabuleiro(tabuleiro)
        usual = []
        proPlay = False
        global biggerNow
        
        while True:
            
            if (mark(tabuleiro) == 'x'):
                print('Vez do Jogador\nMarque uma posição. -> informando a linha e a coluna')
                print('OBS: Linha e coluna se iniciam de 0 à 2\n\n')
                #a = int(input('Digite a Linha'))
                #b = int(input('Digite a Coluna'))
                
                if cont >= 2500:
                    proPlay = False
                    for i in range(3):
                        for j in range(3):
                            if tabuleiro[i][j] == 'b': 
                                tabuleiro[i][j] = 'o'
                                r,w = Victory(tabuleiro)
                                if w == 'o':
                                    proPlay = True
                                    a = i
                                    b = j
                                tabuleiro[i][j] = 'b'
                                
                if cont < 2500 or proPlay == False:
                    a = random.randint(0,2)
                    b = random.randint(0,2)
                    while(usual.__contains__((a,b))):
                        a = random.randint(0,2)
                        b = random.randint(0,2)
                    
                
                usual.append((a,b))
            
                tabuleiro[a][b] = mark(tabuleiro)
            else:
                biggerNow = -1000000
                print('Vez da IA.\n\n')
                WhereThrow(tabuleiro)
                print('ENTER PARA CONTINUAR')
                #input()
                a,b = pos
                usual.append(pos)
                SaveData(tabuleiro, pos, c)
                tabuleiro[a][b] = mark(tabuleiro)
            
           # ImprimeTabuleiro(tabuleiro)
            #print('Big: {}'.format(biggerNow))
            #print('Onde jogar: {}'.format(pos))
            #print('Tabuleiro modificado.')
            for l in tabuleiro:
                print(l)
                
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
        cont+=1
        print(cont)
        if (cont > 3000):
                break
        #print('Deseja jogar novamente? - Finish para terminar')
        #if (input().lower() == 'finish' or cont > 200):
         #   break
        

startJogoVelha()



