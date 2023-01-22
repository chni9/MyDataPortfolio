#%% Importation des modules necessaires
import numpy as np
import matplotlib.pyplot as plt
import string
import math
import time
import random



#%% Création du jeu
alphabet = list(string.ascii_uppercase)
dict_alpha = {"A": 1, "B": 2, "C" : 3, "D" : 4, "E" : 5, "F" : 6, "G" : 7, "H" : 8, "I" : 9, "J" : 10, "K" : 11, "L" : 12, "M" : 13, "N" : 14, "O" : 15}
dict_num = {1 : "A", 2 : "B", 3 : "C", 4 : "D", 5 :"E", 6 : "F", 7 : "G", 8 : "H", 9 : "I", 10 : "J", 11 : "K", 12 : "L", 13 : "M", 14 : "N", 15 : "O"}
"""Creation du position et initialisation du nombre de pions de départ"""
position=[]
for i in range(20):
    M=[]
    for j in range(20):
        if i < 16 and j < 16 :
            M.append(".")
        else :
            M.append(" ")
    position.append(M)

""" Affichage du plateau """
def Affichage(L):
    s=""
    for i in range(len(L)):
        for j in range(len(L[0])):
            if((i==0) and j>9):
                s+=str(L[i][j])+" "
            if(i>=0 and j<=9):
                s+=str(L[i][j])+" "
            if(i>0 and j>9):
                s+=str(L[i][j])+"  " 
        s+="\n"
    return s

position[0][0] = "*"
for k in range(1,len(position)):
    if k < 16 :
        position[k][0] = alphabet[k-1]
        position[0][k] = k
print(Affichage(position))

def Creation_Position(position, action, player) :
    """ Création de la position de jeu (plateau) en fonction de l'action en paramètre"""
    new_position = []
    
    for i in range(16):
        M = []
        for j in range(16):
            if position[i][j] == 'X':
                M.append('X')
            elif position[i][j] == 'O':
                M.append('O')
            else :
                M.append('.')
        new_position.append(M)
            
    new_position[0][0] = '*'
    for k in range(1,len(new_position)):
        new_position[k][0] = alphabet[k-1]
        new_position[0][k] = k
        
    """ Affectation de l'action sur le plateau """
    ligne = action[0]
    colonne = action[1]
    new_position[ligne][colonne] = player
    return new_position    
    

""" Definition d'une action (utilisé pour joueur) """
def Action():
    done = False
    while(not done):
        ligne, colonne = ActionGuidee()
        if (position[ligne][colonne] == "."):
            position[ligne][colonne] = 'O'
            done = True
        else :
            print("Cette position est déjà utilisée. Réessayez...")
    return [ligne, colonne]

""" Liste contenant la ligne et la colonne saisies par le joueur """
def ActionGuidee():
    ligne = dict_alpha[input("Saisissez la ligne où vous souhaitez placer votre pion : ").upper()]
    colonne = int(input("Saisissez la colonne où vous souhaitez placer votre pion : "))
    return [ligne,colonne]

""" Donne la matrice de toutes les positions de jeu possibles à partir de la position de jeu actuelle """
def Actions_Possibles(position, player):
    if(player):
        player = "X"
    else :
        player = "O"
    actions = []
    matrice_position = []
    """Détermination d'une liste de toutes les actions possibles """
    for i in range(len(position)):
        for j in range(len(position[0])):
            if(position[i][j] == "."):
                actions.append([i,j])
    """ Détermination d'une matrice de toutes les positions du jeu à partir de la matrice des actions possibles"""
    for act in actions :
        old_position = position
        new_position = Creation_Position(old_position, act, player)
        matrice_position.append((new_position, act))
    return matrice_position

""" Liste des position possibles de jeu (utilisée pour joueur) """
def Liste_Positions_Possibles(position):
    M = []
    for i in range(len(position)):
        for j in range(len(position[0])):
            if(position[i][j]=="."):
                M.append([i,j])
    return M


""" Permet de vérifier si un pion est bien dans le plateau """
def InPlateau(position):
    test = False
    if(position[0] >= 1 and position[0] <= 15 and position[1] >= 1 and position[1] <= 15):
        test = True
    return test

""" Donne la condition d'arrêt ainsi que le vainqueur """
def is_end(position):
    Acheck = []
    gagnant = None
    for i in range(1,16):
        for j in range(1,16):
            if(position[i][j] != '.'):
                Acheck.append((i,j))
    for pos in Acheck:
        i,j = pos[0],pos[1]
        
        """Pour les lignes"""
        if(InPlateau([i+1,j]) and InPlateau([i+2,j]) and InPlateau([i+3,j]) and InPlateau([i+4,j])):
            if(position[i][j] == position[i+1][j] == position[i+2][j] == position[i+3][j] == position[i+4][j] != '.' ):
                gagnant = position[i][j]
                
        if(InPlateau([i-1,j]) and InPlateau([i-2,j]) and InPlateau([i-3,j]) and InPlateau([i-4,j])):
            if(position[i][j] == position[i-1][j] == position[i-2][j] == position[i-3][j] == position[i-4][j] != '.' ):
                gagnant = position[i][j]
        
        """Pour les colonnes"""
        if(InPlateau([i,j+1]) and InPlateau([i,j+2]) and InPlateau([i,j+3]) and InPlateau([i,j+4])):
            if(position[i][j] == position[i][j+1] == position[i][j+2] == position[i][j+3] == position[i][j+4] != '.' ):
                gagnant = position[i][j]
                
        if(InPlateau([i,j-1]) and InPlateau([i,j-2]) and InPlateau([i,j-3]) and InPlateau([i,j-4])):        
            if(position[i][j] == position[i][j-1] == position[i][j-2] == position[i][j-3] == position[i][j-4] != '.' ):
                gagnant = position[i][j]
        
        """Pour les diagonales"""
        if(InPlateau([i+1,j+1]) and InPlateau([i+2,j+2]) and InPlateau([i+3,j+3]) and InPlateau([i+4,j+4])):
            if(position[i][j] == position[i+1][j+1] == position[i+2][j+2] == position[i+3][j+3] == position[i+4][j+4] != '.' ):
                gagnant = position[i][j]
                
        if(InPlateau([i-1,j-1]) and InPlateau([i-2,j-2]) and InPlateau([i-3,j-3]) and InPlateau([i-4,j-4])):
            if(position[i][j] == position[i-1][j-1] == position[i-2][j-2] == position[i-3][j-3] == position[i-4][j-4] != '.' ):
                gagnant = position[i][j]
                
        if(InPlateau([i+1,j-1]) and InPlateau([i+2,j-2]) and InPlateau([i+3,j-3]) and InPlateau([i+4,j-4])):
            if(position[i][j] == position[i+1][j-1] == position[i+2][j-2] == position[i+3][j-3] == position[i+4][j-4] != '.' ):
                gagnant = position[i][j]
                
        if(InPlateau([i-1,j+1]) and InPlateau([i-2,j+2]) and InPlateau([i-3,j+3]) and InPlateau([i-4,j+4])):
            if(position[i][j] == position[i-1][j+1] == position[i-2][j+2] == position[i-3][j+3] == position[i-4][j+4] != '.' ):
                gagnant = position[i][j]
                
    return gagnant





#%% IA alpha beta

"""Fonction donnant un score au gagnant """
def utility(position, maxplayer):
    """Egalité"""
    if is_end(position) == None:  
        return 0
        """Humain gagne (max)"""
    elif is_end(position) == 'X':
        return -10000
        """IA gagne (min)"""
    elif is_end(position) == 'O':
        return 10000

    
""" Algorithme MinMax alpha beta """
def Minimax(position, depth, alpha, beta, maxplayer, L):
    if depth == 0 and is_end(position[0]) != None:
        return utility(position[0], maxplayer), position[1], L
    elif depth == 0 and is_end(position[0]) == None :
        action = position[1]
        score = AnalyseMax(maxplayer, position[0]) +  AnalyseMin(maxplayer, position[0])
        L.append((score, action))
        return score, action, L    
            
    if maxplayer :
        maxEval = - math.inf
        for next_position in Actions_Possibles(position[0], maxplayer) :
            evaluation, action, L = Minimax(next_position, depth - 1, alpha, beta, False, L)
            maxEval = max(maxEval, evaluation)
            alpha = max(alpha,evaluation)
            if beta <= alpha :
                break
            L.append((maxEval, action))
        return maxEval, action, L
    
    else :
        minEval = math.inf
        for next_position in Actions_Possibles(position[0], maxplayer) :
            evaluation, action, L = Minimax(next_position, depth - 1, alpha, beta, True, L)
            minEval = min(minEval, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha :
                break
            L.append((minEval, action))
        return minEval, action, L
    

""" Evaluation du score de chaque disposition en fonction du nombre de pions consécutifs et d'ouvertures (heuristique) """
def Heuristique(position) :
    action = [0, 0]
    score = 0
    """ Test manuelle des dispositions """
    for i in range (16) :
        for j in range (16):
            """ Attaque """
            """ Horizontale """
            if position[i][j] == 'X' :
                if position[i][j+1] == 'X' :
                    if position[i][j+2] == 'X' :
                        if position [i][j+3] == 'X' :
                            if position [i][j+4] == '.' :
                                return [i,j+4]
                            elif position [i][j-1] == '.' :
                                return [i,j-1]
                            """ 3 consécutifs """
                        elif position [i][j+3] == '.'  and position[i][j+4] == 'X':
                            return [i,j+3]
                        elif position [i][j-1] == '.'  and position[i][j-2] == 'X':
                            return [i,j-1]
                        elif position [i][j+3] == '.' and position [i][j-1] == '.' and position[i][j+4] == '.' and score < 50:
                            score = 50 
                            action = [i,j+3]
                        elif position [i][j+3] == '.' and position [i][j-1] == '.' and position[i][j-2] == '.' and score < 50:
                            score = 50 
                            action = [i,j-1]
                        elif position [i][j+3] == '.' and position [i][j+4] == '.' and score < 20:
                            score = 20 
                            action = [i,j+4] 
                        elif position [i][j-1] == '.' and position [i][j-2] == '.' and score < 20: 
                            score = 20
                            action = [i,j-2]
                        elif position [i][j+3] == '.' and position [i][j-1] == '.' and score < 20:
                            score = 20
                            action = [i,j+3]
                    """ 2 consécutifs """ 
                    if position [i][j+2] == '.' and position [i][j+3] == 'X' and position[i][j+4] == 'X' : # 2 à la suite
                        return [i,j+2]
                    elif position [i][j+2] == '.' and position [i][j+3] == 'X' and position[i][j+4] == '.' and position [i][j-1] == '.' and score < 50 : 
                        score = 50
                        action = [i,j+2]
                    elif position [i][j+2] == '.' and position [i][j-1] == '.' and position[i][j-2] == 'X' and position [i][j-3] == '.' and score < 50:
                        score = 50
                        action = [i,j-1]
                    elif position [i][j-1] == '.' and position [i][j-2] == 'X'  and position [i][j-3] == '.'and score < 20:
                        score = 20
                        action = [i,j-3]
                    elif position [i][j-1] == '.' and position [i][j-2] == '.'  and position [i][j-3] == 'X' and score < 20:
                        score = 20
                        action = [i,j-2]
                    elif position [i][j+2] == '.' and position [i][j+3] == '.' and position[i][j+4] == 'X' and score < 20:
                        score = 20
                        action = [i,j+3]
                    elif position [i][j-1] == '.' and position [i][j-2] == '.' and position[i][j-3] == 'X' and score<20:
                        score = 20
                        action = [i,j-2]
                    elif position [i][j+2] == '.' and position [i][j-1] == '.' and position[i][j-2] == 'X' and score<20:
                        score = 20
                        action = [i,j-1]
                    elif position [i][j+2] == '.' and position [i][j+3] == 'X' and position[i][j+4] == '.' and score<20:
                        score = 20
                        action = [i,j+2]
                    elif position [i][j+2] == '.' and position [i][j+3] == '.' and position[i][j+4] == '.' and score<10:
                        score = 10
                        action = [i,j+3]
                    elif position [i][j-1] == '.' and position [i][j-2] == '.' and position[i][j-3] == '.' and score< 10:
                        score = 10
                        action = [i,j-2]
                    elif position [i][j-1] == '.' and position [i][j+1] == '.' and position[i][j+2] == '.' and score<10:
                        score = 10
                        action = [i,j+1]
                    elif position [i][j-1] == '.' and position [i][j-2] == '.' and position[i][j+1] == '.' and score<10:
                        score = 10
                        action = [i,j-1]
                """ 1 consécutif """
                if position [i][j+2] == 'X' and position [i][j+1] == '.' and position[i][j+3] == '.' and position[i][j+4] == 'X' and score<15:
                    score = 15
                    action = [i,j+3]
                elif position [i][j+2] == 'X' and position [i][j+1] == '.' and position[i][j+3] == '.' and position[i][j+4] == '.' and score<10:
                    score = 10
                    action = [i,j+3]
                elif position [i][j+2] == '.' and position [i][j+1] == '.' and position[i][j+3] == 'X' and position[i][j+4] == '.' and score<10:
                    score = 10
                    action = [i,j+2]
                elif position [i][j-1] == '.' and position [i][j+1] == '.' and position[i][j+3] == '.' and position[i][j+2] == 'X' and score<10:
                    score = 10
                    action = [i,j+1]
                elif position [i][j-1] == '.' and position [i][j+1] == '.' and position[i][j+2] == '.' and position[i][j+3] == 'X' and score<10:
                    score = 10
                    action = [i,j+1]
                elif position [i][j-1] == '.' and position [i][j-2] == '.' and position[i][j+1] == '.' and position[i][j+2] == 'X' and score<10:
                    score = 10
                    action = [i,j+1]
                elif position [i][j+2] == '.' and position [i][j+1] == '.' and position[i][j+3] == '.' and position[i][j+4] == 'X' and score< 7:
                    score = 7
                    action = [i,j+3]
                elif position [i][j+1] == '.' and position [i][j+2] == '.' and position[i][j+3] == '.' and position[i][j+4] == '.' and score<5:
                    score = 5
                    action = [i,j+2]
                elif position [i][j-1] == '.' and position [i][j+1] == '.' and position[i][j+2] == '.' and position[i][j+3] == '.' and score< 5:
                    score = 5
                    action = [i,j+1]
                elif position [i][j-1] == '.' and position [i][j-2] == '.' and position[i][j+1] == '.' and position[i][j+2] == '.' and score< 5:
                    score = 5
                    action = [i,j+1]
                elif position [i][j-1] == '.' and position [i][j-2] == '.' and position[i][j-3] == '.' and position[i][j+1] == '.' and score<5:
                    score = 5
                    action = [i,j-1]
                elif position [i][j-1] == '.' and position [i][j-2] == '.' and position[i][j-3] == '.' and position[i][j-4] == '.' and score<5:
                    score = 5
                    action = [i,j-1]
                    
                """ Verticale """   
                if position[i+1][j] == 'X' :
                    if position[i+2][j] == 'X' :
                        if position [i+3][j] == 'X' :
                            if position [i+4][j] == '.' :
                                return [i+4,j]
                            elif position [i-1][j] == '.' :
                                return [i-1,j]
                            """ 3 consécutifs """
                        elif position [i+3][j] == '.'  and position[i+4][j] == 'X':
                            return [i+3,j]
                        elif position [i-1][j] == '.'  and position[i-2][j] == 'X':
                            return [i-1,j]
                        elif position [i+3][j] == '.' and position [i-1][j] == '.' and position[i+4][j] == '.' and score < 50:
                            score = 50 
                            action = [i+3,j]
                        elif position [i+3][j] == '.' and position [i-1][j] == '.' and position[i-2][j] == '.' and score < 50:
                            score = 50 
                            action = [i-1,j]
                        elif position [i+3][j] == '.' and position [i+4][j] == '.' and score < 20:
                            score = 20 
                            action = [i+4,j] 
                        elif position [i-1][j] == '.' and position [i-2][j] == '.' and score < 20: 
                            score = 20
                            action = [i-2,j]
                        elif position [i+3][j] == '.' and position [i-1][j] == '.' and score < 20:
                            score = 20
                            action = [i+3,j]
                    """ 2 consécutifs """        
                    if position [i+2][j] == '.' and position [i+3][j] == 'X' and position[i+4][j] == 'X' :
                        return [i+2,j]
                    elif position [i+2][j] == '.' and position [i+3][j] == 'X' and position[i+4][j] == '.' and position [i-1][j] == '.' and score < 50: 
                        score = 50
                        action = [i+2,j]
                    elif position [i+2][j] == '.' and position [i-1][j] == '.' and position[i-2][j] == 'X' and position [i-3][j] == '.' and score < 50:
                        score = 50
                        action = [i-1,j]
                    elif position [i-1][j] == '.' and position [i-2][j] == 'X'  and position [i-3][j] == '.'and score < 20:
                        score = 20
                        action = [i-3,j]
                    elif position [i-1][j] == '.' and position [i-2][j] == '.'  and position [i-3][j] == 'X' and score < 20:
                        score = 20
                        action = [i-2,j]
                    elif position [i+2][j] == '.' and position [i+3][j] == '.' and position[i+4][j] == 'X' and score < 20:
                        score = 20
                        action = [i+3,j]
                    elif position [i-1][j] == '.' and position [i-2][j] == '.' and position[i-3][j] == 'X' and score < 20:
                        score = 20
                        action = [i-2,j]
                    elif position [i+2][j] == '.' and position [i-1][j] == '.' and position[i-2][j] == 'X' and score < 20:
                        score = 20
                        action = [i-1,j]
                    elif position [i+2][j] == '.' and position [i+3][j] == 'X' and position[i+4][j] == '.' and score < 20:
                        score = 20
                        action = [i+2,j]
                    elif position [i+2][j] == '.' and position [i+3][j] == '.' and position[i+4][j] == '.' and score<10:
                        score = 10
                        action = [i+3,j]
                    elif position [i-1][j] == '.' and position [i-2][j] == '.' and position[i-3][j] == '.' and score< 10:
                        score = 10
                        action = [i-2,j]
                    elif position [i-1][j] == '.' and position [i+1][j] == '.' and position[i+2][j] == '.' and score<10:
                        score = 10
                        action = [i+1,j]
                    elif position [i-1][j] == '.' and position [i-2][j] == '.' and position[i+1][j] == '.' and score<10:
                        score = 10
                        action = [i-1,j]
                """ 1 consécutif """
                if position [i+2][j] == 'X' and position [i+1][j] == '.' and position[i+3][j] == '.' and position[i+4][j] == 'X' and score < 15:
                    score = 15
                    action = [i+3,j]
                elif position [i+2][j] == 'X' and position [i+1][j] == '.' and position[i+3][j] == '.' and position[i+4][j] == '.' and score<10:
                    score = 10
                    action = [i+3,j]
                elif position [i+2][j] == '.' and position [i+1][j] == '.' and position[i+3][j] == 'X' and position[i+4][j] == '.' and score<10:
                    score = 10
                    action = [i+2,j]
                elif position [i-1][j] == '.' and position [i+1][j] == '.' and position[i+3][j] == '.' and position[i+2][j] == 'X' and score<10:
                    score = 10
                    action = [i+1,j]
                elif position [i-1][j] == '.' and position [i+1][j] == '.' and position[i+2][j] == '.' and position[i+3][j] == 'X' and score<10:
                    score = 10
                    action = [i+1,j]
                elif position [i-1][j] == '.' and position [i-2][j] == '.' and position[i+1][j] == '.' and position[i+2][j] == 'X' and score<10:
                    score = 10
                    action = [i+1,j]
                elif position [i+2][j] == '.' and position [i+1][j] == '.' and position[i+3][j] == '.' and position[i+4][j] == 'X' and score<7:
                    score = 7
                    action = [i+3,j]
                elif position [i+1][j] == '.' and position [i+2][j] == '.' and position[i+3][j] == '.' and position[i+4][j] == '.' and score<5:
                    score = 5
                    action = [i+2,j]
                elif position [i-1][j] == '.' and position [i+1][j] == '.' and position[i+2][j] == '.' and position[i+3][j] == '.' and score< 5:
                    score = 5
                    action = [i+1,j]
                elif position [i-1][j] == '.' and position [i-2][j] == '.' and position[i+1][j] == '.' and position[i+2][j] == '.' and score< 5:
                    score = 5
                    action = [i+1,j]
                elif position [i-1][j] == '.' and position [i-2][j] == '.' and position[i-3][j] == '.' and position[i+1][j] == '.' and score<5:
                    score = 5
                    action = [i-1,j]
                elif position [i-1][j] == '.' and position [i-2][j] == '.' and position[i-3][j] == '.' and position[i-4][j] == '.' and score<5:
                    score = 5
                    action = [i-1,j]
                
                """ Diagonale """
                if position[i+1][j+1] == 'X' :
                    if position[i+2][j+2] == 'X' :
                        if position [i+3][j+3] == 'X' :
                            if position [i+4][j+4] == '.' :
                                return [i+4,j+4]
                            elif position [i-1][j-1] == '.' :
                                return [i-1,j-1]
                            """ 3 consécutifs """
                        elif position [i+3][j+3] == '.'  and position[i+4][j+4] == 'X':
                            return [i+3,j+3]
                        elif position [i-1][j-1] == '.'  and position[i-2][j-2] == 'X':
                            return [i-1,j-1]
                        elif position [i+3][j+3] == '.' and position [i-1][j-1] == '.' and position[i+4][j+4] == '.' and score < 50:
                            score = 50 
                            action = [i+3,j+3]
                        elif position [i+3][j+3] == '.' and position [i-1][j-1] == '.' and position[i-2][j-2] == '.' and score < 50:
                            score = 50 
                            action = [i-1,j-1]
                        elif position [i+3][j+3] == '.' and position [i+4][j+4] == '.' and score <20:
                            score = 20 
                            action = [i+4,j+4] 
                        elif position [i-1][j-1] == '.' and position [i-2][j-2] == '.' and score <20: 
                            score = 20
                            action = [i-2,j-2]
                        elif position [i+3][j+3] == '.' and position [i-1][j-1] == '.' and score <20:
                            score = 20
                            action = [i+3,j+3]
                    """ 2 consécutifs """
                    if position [i+2][j+2] == '.' and position [i+3][j+3] == 'X' and position[i+4][j+4] == 'X' :
                        return [i+2,j+2]
                    elif position [i+2][j+2] == '.' and position [i+3][j+3] == 'X' and position[i+4][j+4] == '.' and position [i-1][j-1] == '.' and score < 50: 
                        score = 50
                        action = [i+2,j+2]
                    elif position [i+2][j+2] == '.' and position [i-1][j-1] == '.' and position[i-2][j-2] == 'X' and position [i-3][j-3] == '.' and score < 50:
                        score = 50
                        action = [i-1,j-1]
                    elif position [i-1][j-1] == '.' and position [i-2][j-2] == 'X'  and position [i-3][j-3] == '.'and score<20:
                        score = 20
                        action = [i-3,j-3]
                    elif position [i-1][j-1] == '.' and position [i-2][j-2] == '.'  and position [i-3][j-3] == 'X' and score< 20:
                        score = 20
                        action = [i-2,j-2]
                    elif position [i+2][j+2] == '.' and position [i+3][j+3] == '.' and position[i+4][j+4] == 'X' and score<20:
                        score = 20
                        action = [i+3,j+3]
                    elif position [i-1][j-1] == '.' and position [i-2][j-2] == '.' and position[i-3][j-3] == 'X' and score<20:
                        score = 20
                        action = [i-2,j-2]
                    elif position [i+2][j+2] == '.' and position [i-1][j-1] == '.' and position[i-2][j-2] == 'X' and score<20:
                        score = 20
                        action = [i-1,j-1]
                    elif position [i+2][j+2] == '.' and position [i+3][j+3] == 'X' and position[i+4][j+4] == '.' and score<20:
                        score = 20
                        action = [i+2,j+2]
                    elif position [i+2][j+2] == '.' and position [i+3][j+3] == '.' and position[i+4][j+4] == '.' and score<10:
                        score = 10
                        action = [i+3,j+3]
                    elif position [i-1][j-1] == '.' and position [i-2][j-2] == '.' and position[i-3][j-3] == '.' and score< 10:
                        score = 10
                        action = [i-2,j-2]
                    elif position [i-1][j-1] == '.' and position [i+1][j+1] == '.' and position[i+2][j+2] == '.' and score<10:
                        score = 10
                        action = [i+1,j+1]
                    elif position [i-1][j-1] == '.' and position [i-2][j-2] == '.' and position[i+1][j+1] == '.' and score<10:
                        score = 10
                        action = [i-1,j-1]
                """ 1 consécutif """
                if position [i+2][j+2] == 'X' and position [i+1][j+1] == '.' and position[i+3][j+3] == '.' and position[i+4][j+4] == 'X' and score<15:
                    score = 15
                    action = [i+3,j+3]
                elif position [i+2][j+2] == 'X' and position [i+1][j+1] == '.' and position[i+3][j+3] == '.' and position[i+4][j+4] == '.' and score<10:
                    score = 10
                    action = [i+3,j+3]
                elif position [i+2][j+2] == '.' and position [i+1][j+1] == '.' and position[i+3][j+3] == 'X' and position[i+4][j+4] == '.' and score<10: 
                    score = 10
                    action = [i+2,j+2]
                elif position [i-1][j-1] == '.' and position [i+1][j+1] == '.' and position[i+3][j+3] == '.' and position[i+2][j+2] == 'X' and score<10: 
                    score = 10
                    action = [i+1,j+1]
                elif position [i-1][j-1] == '.' and position [i+1][j+1] == '.' and position[i+2][j+2] == '.' and position[i+3][j+3] == 'X' and score<10: 
                    score = 10
                    action = [i+1,j+1]
                elif position [i-1][j-1] == '.' and position [i-2][j-2] == '.' and position[i+1][j+1] == '.' and position[i+2][j+2] == 'X' and score<10: 
                    score = 10
                    action = [i+1,j+1]
                elif position [i+2][j+2] == '.' and position [i+1][j+1] == '.' and position[i+3][j+3] == '.' and position[i+4][j+4] == 'X' and score<7:
                    score = 7
                    action = [i+3,j+3]
                elif position [i+1][j+1] == '.' and position [i+2][j+2] == '.' and position[i+3][j+3] == '.' and position[i+4][j+4] == '.' and score<5: 
                    score = 5
                    action = [i+2,j+2]
                elif position [i-1][j-1] == '.' and position [i+1][j+1] == '.' and position[i+2][j+2] == '.' and position[i+3][j+3] == '.' and score< 5:
                    score = 5
                    action = [i+1,j+1]
                elif position [i-1][j-1] == '.' and position [i-2][j-2] == '.' and position[i+1][j+1] == '.' and position[i+2][j+2] == '.' and score< 5:
                    score = 5
                    action = [i+1,j+1]
                elif position [i-1][j-1] == '.' and position [i-2][j-2] == '.' and position[i-3][j-3] == '.' and position[i+1][j+1] == '.' and score<5:
                    score = 5
                    action = [i-1,j-1]
                elif position [i-1][j-1] == '.' and position [i-2][j-2] == '.' and position[i-3][j-3] == '.' and position[i-4][j-4] == '.' and score<5:
                    score = 5
                    action = [i-1,j-1]
                
                """ Diagonale """            
                if position[i+1][j-1] == 'X' :
                    if position[i+2][j-2] == 'X' :
                        if position [i+3][j-3] == 'X' :
                            if position [i+4][j-4] == '.' :
                                return [i+4,j-4]
                            elif position [i-1][j+1] == '.' :
                                return [i-1,j+1]
                            """ 3 consécutifs """
                        elif position [i+3][j-3] == '.'  and position[i+4][j-4] == 'X':
                            return [i+3,j-3]
                        elif position [i-1][j+1] == '.'  and position[i-2][j+2] == 'X':
                            return [i-1,j+1]
                        elif position [i+3][j-3] == '.' and position [i-1][j+1] == '.' and position[i+4][j-4] == '.' and score < 50:
                            score = 50 
                            action = [i+3,j-3]
                        elif position [i+3][j-3] == '.' and position [i-1][j+1] == '.' and position[i-2][j+2] == '.' and score < 50:
                            score = 50 
                            action = [i-1,j+1]
                        elif position [i+3][j-3] == '.' and position [i+4][j-4] == '.' and score <20:
                            score = 20 
                            action = [i+4,j-4] 
                        elif position [i-1][j+1] == '.' and position [i-2][j+2] == '.' and score <20: 
                            score = 20
                            action = [i-2,j+2]
                        elif position [i+3][j-3] == '.' and position [i-1][j+1] == '.' and score <20:
                            score = 20
                            action = [i+3,j-3]
                    """ 2 consécutifs """
                    if position [i+2][j-2] == '.' and position [i+3][j-3] == 'X' and position[i+4][j-4] == 'X' :
                        return [i+2,j-2]
                    elif position [i+2][j-2] == '.' and position [i+3][j-3] == 'X' and position[i+4][j-4] == '.' and position [i-1][j+1] == '.' and score < 50: 
                        score = 50
                        action = [i+2,j-2]
                    elif position [i+2][j-2] == '.' and position [i-1][j+1] == '.' and position[i-2][j+2] == 'X' and position [i-3][j+3] == '.' and score < 50:
                        score = 50
                        action = [i-1,j+1]
                    elif position [i-1][j+1] == '.' and position [i-2][j+2] == 'X'  and position [i-3][j+3] == '.'and score<20:
                        score = 20
                        action = [i-3,j+3]
                    elif position [i-1][j+1] == '.' and position [i-2][j+2] == '.'  and position [i-3][j+3] == 'X' and score< 20:
                        score = 20
                        action = [i-2,j+2]
                    elif position [i+2][j-2] == '.' and position [i+3][j-3] == '.' and position[i+4][j-4] == 'X' and score<20:
                        score = 20
                        action = [i+3,j-3]
                    elif position [i-1][j+1] == '.' and position [i-2][j+2] == '.' and position[i-3][j+3] == 'X' and score<20:
                        score = 20
                        action = [i-2,j+2]
                    elif position [i+2][j-2] == '.' and position [i-1][j+1] == '.' and position[i-2][j+2] == 'X' and score<20:
                        score = 20
                        action = [i-1,j+1]
                    elif position [i+2][j-2] == '.' and position [i+3][j-3] == 'X' and position[i+4][j-4] == '.' and score<20:
                        score = 20
                        action = [i+2,j-2]
                    elif position [i+2][j-2] == '.' and position [i+3][j-3] == '.' and position[i+4][j-4] == '.' and score<10:
                        score = 10
                        action = [i+3,j-3]
                    elif position [i-1][j+1] == '.' and position [i-2][j+2] == '.' and position[i-3][j+3] == '.' and score< 10:
                        score = 10
                        action = [i-2,j+2]
                    elif position [i-1][j+1] == '.' and position [i+1][j-1] == '.' and position[i+2][j-2] == '.' and score<10:
                        score = 10
                        action = [i+1,j-1]
                    elif position [i-1][j+1] == '.' and position [i-2][j+2] == '.' and position[i+1][j-1] == '.' and score<10:
                        score = 10
                        action = [i-1,j+1]
                """ 1 consécutif """
                if position [i+2][j-2] == 'X' and position [i+1][j-1] == '.' and position[i+3][j-3] == '.' and position[i+4][j-4] == 'X' and score<15:
                    score = 15
                    action = [i+3,j-3]
                elif position [i+2][j-2] == 'X' and position [i+1][j-1] == '.' and position[i+3][j-3] == '.' and position[i+4][j-4] == '.' and score<10:
                    score = 10
                    action = [i+3,j-3]
                elif position [i+2][j-2] == '.' and position [i+1][j-1] == '.' and position[i+3][j-3] == 'X' and position[i+4][j-4] == '.' and score<10:
                    score = 10
                    action = [i+2,j-2]
                elif position [i-1][j+1] == '.' and position [i+1][j-1] == '.' and position[i+3][j-3] == '.' and position[i+2][j-2] == 'X' and score<10:
                    score = 10
                    action = [i+1,j-1]
                elif position [i-1][j+1] == '.' and position [i+1][j-1] == '.' and position[i+2][j-2] == '.' and position[i+3][j-3] == 'X' and score<10:
                    score = 10
                    action = [i+1,j-1]
                elif position [i-1][j+1] == '.' and position [i-2][j+2] == '.' and position[i+1][j-1] == '.' and position[i+2][j-2] == 'X' and score<10:
                    score = 10
                    action = [i+1,j-1]
                elif position [i+2][j-2] == '.' and position [i+1][j-1] == '.' and position[i+3][j-3] == '.' and position[i+4][j-4] == 'X' and score<7:
                    score = 7
                    action = [i+3,j-3]
                elif position [i+1][j-1] == '.' and position [i+2][j-2] == '.' and position[i+3][j-3] == '.' and position[i+4][j-4] == '.' and score<5:
                    score = 5
                    action = [i+2,j-2]
                elif position [i-1][j+1] == '.' and position [i+1][j-1] == '.' and position[i+2][j-2] == '.' and position[i+3][j-3] == '.' and score< 5:
                    score = 5
                    action = [i+1,j-1]
                elif position [i-1][j+1] == '.' and position [i-2][j+2] == '.' and position[i+1][j-1] == '.' and position[i+2][j-2] == '.' and score< 5:
                    score =5
                    action = [i+1,j-1]
                elif position [i-1][j+1] == '.' and position [i-2][j+2] == '.' and position[i-3][j+3] == '.' and position[i+1][j-1] == '.' and score<5:
                    score = 5
                    action = [i-1,j+1]
                elif position [i-1][j+1] == '.' and position [i-2][j+2] == '.' and position[i-3][j+3] == '.' and position[i-4][j+4] == '.' and score<5:
                    score = 5
                    action = [i-1,j+1]
            """ Coup de la ceinture """
            if position [i][j] == 'X' and position [i-1][j+1] == '.' and position [i+1][j+1] == '.' and position[i][j+2] == 'X' and position[i][j+1] == '.' and score < 25:
                score = 25
                action = [i-1,j+1]
            elif position [i][j] == 'X' and position [i-1][j+1] == 'X' and position [i+1][j+1] == '.' and position[i][j+2] == '.' and position[i][j+1] == '.' and score < 25:
                score = 25
                action = [i,j+2]
            elif position [i][j] == 'X' and position [i-1][j+1] == '.' and position [i+1][j+1] == 'X' and position[i][j+2] == '.' and position[i][j+1] == '.' and score < 25:
                score = 25
                action = [i,j+2]
            elif position [i][j] == 'X' and position [i-1][j+1] == 'X' and position [i+1][j+1] == 'X' and position[i][j+2] == '.' and position[i][j+1] == '.' and score < 30:
                score = 30
                action = [i,j+2]
            elif position [i][j] == 'X' and position [i-1][j+1] == '.' and position [i+1][j+1] == 'X' and position[i][j+2] == 'X' and position[i][j+1] == '.' and score < 30:
                score = 30
                action = [i-1,j+1]
            elif position [i][j] == 'X' and position [i-1][j+1] == 'X' and position [i+1][j+1] == '.' and position[i][j+2] == 'X' and position[i][j+1] == '.' and score < 30:
                score = 30
                action = [i+1,j+1]
            elif position [i][j] == 'X' and position [i-1][j+1] == 'X' and position [i+1][j+1] == 'X' and position[i][j+2] == 'X' and position[i][j+1] == '.' and score < 50:
                score = 50
                action = [i,j+1]
                
            """ Défense """
            
            if position[i][j] == 'O' :
                """ Horizontale """
                if position[i][j+1] == 'O' :
                    if position[i][j+2] == 'O' :
                        if position [i][j+3] == 'O' :
                            if position [i][j+4] == '.' and score < 100:
                                score = 100
                                action = [i,j+4]
                            elif position [i][j-1] == '.'and score < 100:
                                score = 100
                                action = [i,j-1]
                            """ 3 consécutifs """
                        elif position [i][j+3] == '.'  and position[i][j+4] == 'O' and score < 100:
                            score = 100
                            action = [i,j+3]
                        elif position [i][j-1] == '.'  and position[i][j-2] == 'O' and score < 100:
                            score = 100
                            action = [i,j-1]
                        elif position [i][j+3] == '.' and position [i][j-1] == '.' and position[i][j+4] == '.' and score < 49:
                            score = 50 
                            action = [i,j+3]
                        elif position [i][j+3] == '.' and position [i][j-1] == '.' and position[i][j-2] == '.' and score < 49:
                            score = 50 
                            action = [i,j-1]
                        elif position [i][j+3] == '.' and position [i][j+4] == '.' and score<19:
                            score = 20 
                            action = [i,j+4] 
                        elif position [i][j-1] == '.' and position [i][j-2] == '.' and score< 19: 
                            score = 20
                            action = [i,j-2]
                        elif position [i][j+3] == '.' and position [i][j-1] == '.' and score< 19:
                            score = 20
                            action = [i,j+3]
                    """ 2 consécutifs """
                    if position [i][j+2] == '.' and position [i][j+3] == 'O' and position[i][j+4] == 'O' and score < 100:
                        score = 100
                        action = [i,j+2]
                    elif position [i][j+2] == '.' and position [i][j+3] == 'O' and position[i][j+4] == '.' and position [i][j-1] == '.' and score< 49: 
                        score = 50
                        action = [i,j+2]
                    elif position [i][j+2] == '.' and position [i][j-1] == '.' and position[i][j-2] == 'O' and position [i][j-3] == '.' and score< 49:
                        score = 50
                        action = [i,j-1]
                    elif position [i][j-1] == '.' and position [i][j-2] == 'O'  and position [i][j-3] == '.'and score<19:
                        score = 20
                        action = [i,j-3]
                    elif position [i][j-1] == '.' and position [i][j-2] == '.'  and position [i][j-3] == 'O' and score< 19:
                        score = 20
                        action = [i,j-2]
                    elif position [i][j+2] == '.' and position [i][j+3] == '.' and position[i][j+4] == 'O' and score<19:
                        score = 20
                        action = [i,j+3]
                    elif position [i][j-1] == '.' and position [i][j-2] == '.' and position[i][j-3] == 'O' and score<19:
                        score = 20
                        action = [i,j-2]
                    elif position [i][j+2] == '.' and position [i][j-1] == '.' and position[i][j-2] == 'O' and score<19:
                        score = 20
                        action = [i,j-1]
                    elif position [i][j+2] == '.' and position [i][j+3] == 'O' and position[i][j+4] == '.' and score<19:
                        score = 20
                        action = [i,j+2]
                    elif position [i][j+2] == '.' and position [i][j+3] == '.' and position[i][j+4] == '.' and score<9:
                        score = 10
                        action = [i,j+3]
                    elif position [i][j-1] == '.' and position [i][j-2] == '.' and position[i][j-3] == '.' and score< 9:
                        score = 10
                        action = [i,j-2]
                    elif position [i][j-1] == '.' and position [i][j+1] == '.' and position[i][j+2] == '.' and score<9:
                        score = 10
                        action = [i,j+1]
                    elif position [i][j-1] == '.' and position [i][j-2] == '.' and position[i][j+1] == '.' and score<9:
                        score = 10
                        action = [i,j-1]
                """ 1 consécutif """
                if position [i][j+2] == 'O' and position [i][j+1] == '.' and position[i][j+3] == '.' and position[i][j+4] == 'O' and score<14:
                    score = 15
                    action = [i,j+3]
                elif position [i][j+2] == 'O' and position [i][j+1] == '.' and position[i][j+3] == '.' and position[i][j+4] == '.' and score<9:
                    score = 10
                    action = [i,j+3]
                elif position [i][j+2] == '.' and position [i][j+1] == '.' and position[i][j+3] == 'O' and position[i][j+4] == '.' and score<9:
                    score = 10
                    action = [i,j+2]
                elif position [i][j-1] == '.' and position [i][j+1] == '.' and position[i][j+3] == '.' and position[i][j+2] == 'O' and score<9:
                    score = 10
                    action = [i,j+1]
                elif position [i][j-1] == '.' and position [i][j+1] == '.' and position[i][j+2] == '.' and position[i][j+3] == 'O' and score<9:
                    score = 10
                    action = [i,j+1]
                elif position [i][j-1] == '.' and position [i][j-2] == '.' and position[i][j+1] == '.' and position[i][j+2] == 'O' and score<9:
                    score = 10
                    action = [i,j+1]
                elif position [i][j+2] == '.' and position [i][j+1] == '.' and position[i][j+3] == '.' and position[i][j+4] == 'O' and score<6:
                    score = 7
                    action = [i,j+3]
                elif position [i][j+1] == '.' and position [i][j+2] == '.' and position[i][j+3] == '.' and position[i][j+4] == '.' and score<4:
                    score = 5
                    action = [i,j+2]
                elif position [i][j-1] == '.' and position [i][j+1] == '.' and position[i][j+2] == '.' and position[i][j+3] == '.' and score< 4:
                    score = 5
                    action = [i,j+1]
                elif position [i][j-1] == '.' and position [i][j-2] == '.' and position[i][j+1] == '.' and position[i][j+2] == '.' and score< 4:
                    score = 5
                    action = [i,j+1]
                elif position [i][j-1] == '.' and position [i][j-2] == '.' and position[i][j-3] == '.' and position[i][j+1] == '.' and score<4:
                    score = 5
                    action = [i,j-1]
                elif position [i][j-1] == '.' and position [i][j-2] == '.' and position[i][j-3] == '.' and position[i][j-4] == '.' and score<4:
                    score = 5
                    action = [i,j-1]
                    
                """ Verticale """    
                if position[i+1][j] == 'O' :
                    if position[i+2][j] == 'O' :
                        if position [i+3][j] == 'O' :
                            if position [i+4][j] == '.' and score < 100:
                                score = 100
                                action = [i+4,j]
                            elif position [i-1][j] == '.' and score < 100:
                                score = 100
                                action = [i-1,j]
                            """ 3 consécutifs """
                        elif position [i+3][j] == '.'  and position[i+4][j] == 'O' and score < 100:
                            score = 100 
                            action = [i+3,j]
                        elif position [i-1][j] == '.'  and position[i-2][j] == 'O' and score < 100:
                            score = 100
                            action = [i-1,j]
                        elif position [i+3][j] == '.' and position [i-1][j] == '.' and position[i+4][j] == '.' and score < 49:
                            score = 50 
                            action = [i+3,j]
                        elif position [i+3][j] == '.' and position [i-1][j] == '.' and position[i-2][j] == '.' and score < 49:
                            score = 50 
                            action = [i-1,j]
                        elif position [i+3][j] == '.' and position [i+4][j] == '.' and score < 19:
                            score = 20 
                            action = [i+4,j] 
                        elif position [i-1][j] == '.' and position [i-2][j] == '.' and score < 19: 
                            score = 20
                            action = [i-2,j]
                        elif position [i+3][j] == '.' and position [i-1][j] == '.' and score < 19:
                            score = 20
                            action = [i+3,j]
                    """ 2 consécutifs """
                    if position [i+2][j] == '.' and position [i+3][j] == 'O' and position[i+4][j] == 'O' and score < 100:
                        score = 100
                        action = [i+2,j]
                    elif position [i+2][j] == '.' and position [i+3][j] == 'O' and position[i+4][j] == '.' and position [i-1][j] == '.' and score < 49 : 
                        score = 50
                        action = [i+2,j]
                    elif position [i+2][j] == '.' and position [i-1][j] == '.' and position[i-2][j] == 'O' and position [i-3][j] == '.' and score < 49:
                        score = 50
                        action = [i-1,j]
                    elif position [i-1][j] == '.' and position [i-2][j] == 'O'  and position [i-3][j] == '.'and score<19:
                        score = 20
                        action = [i-3,j]
                    elif position [i-1][j] == '.' and position [i-2][j] == '.'  and position [i-3][j] == 'O' and score< 19:
                        score = 20
                        action = [i-2,j]
                    elif position [i+2][j] == '.' and position [i+3][j] == '.' and position[i+4][j] == 'O' and score<19:
                        score = 20
                        action = [i+3,j]
                    elif position [i-1][j] == '.' and position [i-2][j] == '.' and position[i-3][j] == 'O' and score<19:
                        score = 20
                        action = [i-2,j]
                    elif position [i+2][j] == '.' and position [i-1][j] == '.' and position[i-2][j] == 'O' and score<19:
                        score = 20
                        action = [i-1,j]
                    elif position [i+2][j] == '.' and position [i+3][j] == 'O' and position[i+4][j] == '.' and score<19:
                        score = 20
                        action = [i+2,j]
                    elif position [i+2][j] == '.' and position [i+3][j] == '.' and position[i+4][j] == '.' and score<9:
                        score = 10
                        action = [i+3,j]
                    elif position [i-1][j] == '.' and position [i-2][j] == '.' and position[i-3][j] == '.' and score< 9:
                        score = 10
                        action = [i-2,j]
                    elif position [i-1][j] == '.' and position [i+1][j] == '.' and position[i+2][j] == '.' and score<9:
                        score = 10
                        action = [i+1,j]
                    elif position [i-1][j] == '.' and position [i-2][j] == '.' and position[i+1][j] == '.' and score<9:
                        score = 10
                        action = [i-1,j]
                """ 1 consécutif """
                if position [i+2][j] == 'O' and position [i+1][j] == '.' and position[i+3][j] == '.' and position[i+4][j] == 'O' and score<14:
                    score = 15
                    action = [i+3,j]
                elif position [i+2][j] == 'O' and position [i+1][j] == '.' and position[i+3][j] == '.' and position[i+4][j] == '.' and score<9:
                    score = 10
                    action = [i+3,j]
                elif position [i+2][j] == '.' and position [i+1][j] == '.' and position[i+3][j] == 'O' and position[i+4][j] == '.' and score<9:
                    score = 10
                    action = [i+2,j]
                elif position [i-1][j] == '.' and position [i+1][j] == '.' and position[i+3][j] == '.' and position[i+2][j] == 'O' and score<9:
                    score = 10
                    action = [i+1,j]
                elif position [i-1][j] == '.' and position [i+1][j] == '.' and position[i+2][j] == '.' and position[i+3][j] == 'O' and score<9:
                    score = 10
                    action = [i+1,j]
                elif position [i-1][j] == '.' and position [i-2][j] == '.' and position[i+1][j] == '.' and position[i+2][j] == 'O' and score<9:
                    score = 10
                    action = [i+1,j]
                elif position [i+2][j] == '.' and position [i+1][j] == '.' and position[i+3][j] == '.' and position[i+4][j] == 'O' and score<6:
                    score = 7
                    action = [i+3,j]
                elif position [i+1][j] == '.' and position [i+2][j] == '.' and position[i+3][j] == '.' and position[i+4][j] == '.' and score<4:
                    score = 5
                    action = [i+2,j]
                elif position [i-1][j] == '.' and position [i+1][j] == '.' and position[i+2][j] == '.' and position[i+3][j] == '.' and score< 4:
                    score =5
                    action = [i+1,j]
                elif position [i-1][j] == '.' and position [i-2][j] == '.' and position[i+1][j] == '.' and position[i+2][j] == '.' and score<4 :
                    score = 5
                    action = [i+1,j]
                elif position [i-1][j] == '.' and position [i-2][j] == '.' and position[i-3][j] == '.' and position[i+1][j] == '.' and score<4: 
                    score = 5
                    action = [i-1,j]
                elif position [i-1][j] == '.' and position [i-2][j] == '.' and position[i-3][j] == '.' and position[i-4][j] == '.' and score<4:
                    score = 5
                    action = [i-1,j]
                    
                """ Diagonale """            
                if position[i+1][j+1] == 'O' :
                    if position[i+2][j+2] == 'O' :
                        if position [i+3][j+3] == 'O' :
                            if position [i+4][j+4] == '.' and score < 100:
                                score = 100
                                action = [i+4,j+4]
                            elif position [i-1][j-1] == '.' and score < 100:
                                score = 100
                                action = [i-1,j-1]
                            """ 3 consécutifs """
                        elif position [i+3][j+3] == '.'  and position[i+4][j+4] == 'O' and score < 100:
                            score = 100
                            action = [i+3,j+3]
                        elif position [i-1][j-1] == '.'  and position[i-2][j-2] == 'O' and score < 100:
                            score = 100
                            action = [i-1,j-1]
                        elif position [i+3][j+3] == '.' and position [i-1][j-1] == '.' and position[i+4][j+4] == '.' and score < 49:
                            score = 50 
                            action = [i+3,j+3]
                        elif position [i+3][j+3] == '.' and position [i-1][j-1] == '.' and position[i-2][j-2] == '.' and score < 49:
                            score = 50 
                            action = [i-1,j-1]
                        elif position [i+3][j+3] == '.' and position [i+4][j+4] == '.' and score < 19:
                            score = 20 
                            action = [i+4,j+4] 
                        elif position [i-1][j-1] == '.' and position [i-2][j-2] == '.' and score < 19: 
                            score = 20
                            action = [i-2,j-2]
                        elif position [i+3][j+3] == '.' and position [i-1][j-1] == '.' and score < 19:
                            score = 20
                            action = [i+3,j+3]
                        """ 2 consécutifs """
                    if position [i+2][j+2] == '.' and position [i+3][j+3] == 'O' and position[i+4][j+4] == 'O' and score < 100:
                        score = 100
                        action = [i+2,j+2]
                    elif position [i+2][j+2] == '.' and position [i+3][j+3] == 'O' and position[i+4][j+4] == '.' and position [i-1][j-1] == '.' and score < 49 : 
                        score = 50
                        action = [i+2,j+2]
                    elif position [i+2][j+2] == '.' and position [i-1][j-1] == '.' and position[i-2][j-2] == 'O' and position [i-3][j-3] == '.' and score < 49:
                        score = 50
                        action = [i-1,j-1]
                    elif position [i-1][j-1] == '.' and position [i-2][j-2] == 'O'  and position [i-3][j-3] == '.'and score<19:
                        score = 20
                        action = [i-3,j-3]
                    elif position [i-1][j-1] == '.' and position [i-2][j-2] == '.'  and position [i-3][j-3] == 'O' and score< 19:
                        score = 20
                        action = [i-2,j-2]
                    elif position [i+2][j+2] == '.' and position [i+3][j+3] == '.' and position[i+4][j+4] == 'O' and score<19:
                        score = 20
                        action = [i+3,j+3]
                    elif position [i-1][j-1] == '.' and position [i-2][j-2] == '.' and position[i-3][j-3] == 'O' and score<19:
                        score = 20
                        action = [i-2,j-2]
                    elif position [i+2][j+2] == '.' and position [i-1][j-1] == '.' and position[i-2][j-2] == 'O' and score<19:
                        score = 20
                        action = [i-1,j-1]
                    elif position [i+2][j+2] == '.' and position [i+3][j+3] == 'O' and position[i+4][j+4] == '.' and score<19:
                        score = 20
                        action = [i+2,j+2]
                    elif position [i+2][j+2] == '.' and position [i+3][j+3] == '.' and position[i+4][j+4] == '.' and score<9:
                        score = 10
                        action = [i+3,j+3]
                    elif position [i-1][j-1] == '.' and position [i-2][j-2] == '.' and position[i-3][j-3] == '.' and score< 9:
                        score = 10
                        action = [i-2,j-2]
                    elif position [i-1][j-1] == '.' and position [i+1][j+1] == '.' and position[i+2][j+2] == '.' and score<9:
                        score = 10
                        action = [i+1,j+1]
                    elif position [i-1][j-1] == '.' and position [i-2][j-2] == '.' and position[i+1][j+1] == '.' and score<9:
                        score = 10
                        action = [i-1,j-1]
                    """ 1 consécutif """
                if position [i+2][j+2] == 'O' and position [i+1][j+1] == '.' and position[i+3][j+3] == '.' and position[i+4][j+4] == 'O' and score<14:
                    score = 15
                    action = [i+3,j+3]
                elif position [i+2][j+2] == 'O' and position [i+1][j+1] == '.' and position[i+3][j+3] == '.' and position[i+4][j+4] == '.' and score<9:
                    score = 10
                    action = [i+3,j+3]
                elif position [i+2][j+2] == '.' and position [i+1][j+1] == '.' and position[i+3][j+3] == 'O' and position[i+4][j+4] == '.' and score<9:
                    score = 10
                    action = [i+2,j+2]
                elif position [i-1][j-1] == '.' and position [i+1][j+1] == '.' and position[i+3][j+3] == '.' and position[i+2][j+2] == 'O' and score<9:
                    score = 10
                    action = [i+1,j+1]
                elif position [i-1][j-1] == '.' and position [i+1][j+1] == '.' and position[i+2][j+2] == '.' and position[i+3][j+3] == 'O' and score<9:
                    score = 10
                    action = [i+1,j+1]
                elif position [i-1][j-1] == '.' and position [i-2][j-2] == '.' and position[i+1][j+1] == '.' and position[i+2][j+2] == 'O' and score<9: 
                    score = 10
                    action = [i+1,j+1]
                elif position [i+2][j+2] == '.' and position [i+1][j+1] == '.' and position[i+3][j+3] == '.' and position[i+4][j+4] == 'O' and score<6:
                    score = 7
                    action = [i+3,j+3]
                elif position [i+1][j+1] == '.' and position [i+2][j+2] == '.' and position[i+3][j+3] == '.' and position[i+4][j+4] == '.' and score<4:
                    score = 5
                    action = [i+2,j+2]
                elif position [i-1][j-1] == '.' and position [i+1][j+1] == '.' and position[i+2][j+2] == '.' and position[i+3][j+3] == '.' and score< 4:
                    score = 5
                    action = [i+1,j+1]
                elif position [i-1][j-1] == '.' and position [i-2][j-2] == '.' and position[i+1][j+1] == '.' and position[i+2][j+2] == '.' and score< 4:
                    score = 5
                    action = [i+1,j+1]
                elif position [i-1][j-1] == '.' and position [i-2][j-2] == '.' and position[i-3][j-3] == '.' and position[i+1][j+1] == '.' and score<4:
                    score = 5
                    action = [i-1,j-1]
                elif position [i-1][j-1] == '.' and position [i-2][j-2] == '.' and position[i-3][j-3] == '.' and position[i-4][j-4] == '.' and score<4:
                    score = 5
                    action = [i-1,j-1]
                
                """ Diagonale """ 
                if position[i+1][j-1] == 'O' :
                    if position[i+2][j-2] == 'O' :
                        if position [i+3][j-3] == 'O' :
                            if position [i+4][j-4] == '.' and score < 100:
                                score = 100
                                action = [i+4,j-4]
                            elif position [i-1][j+1] == '.' and score < 100:
                                score = 100
                                action = [i-1,j+1]
                            """ 3 consécutifs """
                        elif position [i+3][j-3] == '.'  and position[i+4][j-4] == 'O' and score < 100:
                            score = 100
                            action = [i+3,j-3]
                        elif position [i-1][j+1] == '.'  and position[i-2][j+2] == 'O' and score < 100:
                            score = 100
                            action = [i-1,j+1]
                        elif position [i+3][j-3] == '.' and position [i-1][j+1] == '.' and position[i+4][j-4] == '.' and score < 49:
                            score = 50 
                            action = [i+3,j-3]
                        elif position [i+3][j-3] == '.' and position [i-1][j+1] == '.' and position[i-2][j+2] == '.' and score < 49:
                            score = 50 
                            action = [i-1,j+1]
                        elif position [i+3][j-3] == '.' and position [i+4][j-4] == '.' and score < 19:
                            score = 20 
                            action = [i+4,j-4] 
                        elif position [i-1][j+1] == '.' and position [i-2][j+2] == '.' and score < 19: 
                            score = 20
                            action = [i-2,j+2]
                        elif position [i+3][j-3] == '.' and position [i-1][j+1] == '.' and score < 19:
                            score = 20
                            action = [i+3,j-3]
                    """ 2 consécutifs """
                    if position [i+2][j-2] == '.' and position [i+3][j-3] == 'O' and position[i+4][j-4] == 'O' and score < 100:
                        score = 100
                        action = [i+2,j-2]
                    elif position [i+2][j-2] == '.' and position [i+3][j-3] == 'O' and position[i+4][j-4] == '.' and position [i-1][j+1] == '.' and score < 49: 
                        score = 50
                        action = [i+2,j-2]
                    elif position [i+2][j-2] == '.' and position [i-1][j+1] == '.' and position[i-2][j+2] == 'O' and position [i-3][j+3] == '.' and score < 49:
                        score = 50
                        action = [i-1,j+1]
                    elif position [i-1][j+1] == '.' and position [i-2][j+2] == 'O'  and position [i-3][j+3] == '.'and score<19:
                        score = 20
                        action = [i-3,j+3]
                    elif position [i-1][j+1] == '.' and position [i-2][j+2] == '.'  and position [i-3][j+3] == 'O' and score< 19:
                        score = 20
                        action = [i-2,j+2]
                    elif position [i+2][j-2] == '.' and position [i+3][j-3] == '.' and position[i+4][j-4] == 'O' and score<19:
                        score = 20
                        action = [i+3,j-3]
                    elif position [i-1][j+1] == '.' and position [i-2][j+2] == '.' and position[i-3][j+3] == 'O' and score<19:
                        score = 20
                        action = [i-2,j+2]
                    elif position [i+2][j-2] == '.' and position [i-1][j+1] == '.' and position[i-2][j+2] == 'O' and score<19:
                        score = 20
                        action = [i-1,j+1]
                    elif position [i+2][j-2] == '.' and position [i+3][j-3] == 'O' and position[i+4][j-4] == '.' and score<19:
                        score = 20
                        action = [i+2,j-2]
                    elif position [i+2][j-2] == '.' and position [i+3][j-3] == '.' and position[i+4][j-4] == '.' and score<9:
                        score = 10
                        action = [i+3,j-3]
                    elif position [i-1][j+1] == '.' and position [i-2][j+2] == '.' and position[i-3][j+3] == '.' and score< 9:
                        score = 10
                        action = [i-2,j+2]
                    elif position [i-1][j+1] == '.' and position [i+1][j-1] == '.' and position[i+2][j-2] == '.' and score<9:
                        score = 10
                        action = [i+1,j-1]
                    elif position [i-1][j+1] == '.' and position [i-2][j+2] == '.' and position[i+1][j-1] == '.' and score<9:
                        score = 10
                        action = [i-1,j+1]
                """ 1 consécutif """
                if position [i+2][j-2] == 'O' and position [i+1][j-1] == '.' and position[i+3][j-3] == '.' and position[i+4][j-4] == 'O' and score<14:
                    score = 15
                    action = [i+3,j-3]
                elif position [i+2][j-2] == 'O' and position [i+1][j-1] == '.' and position[i+3][j-3] == '.' and position[i+4][j-4] == '.' and score<9:
                    score = 10
                    action = [i+3,j-3]
                elif position [i+2][j-2] == '.' and position [i+1][j-1] == '.' and position[i+3][j-3] == 'O' and position[i+4][j-4] == '.' and score<9:
                    score = 10
                    action = [i+2,j-2]
                elif position [i-1][j+1] == '.' and position [i+1][j-1] == '.' and position[i+3][j-3] == '.' and position[i+2][j-2] == 'O' and score<9:
                    score = 10
                    action = [i+1,j-1]
                elif position [i-1][j+1] == '.' and position [i+1][j-1] == '.' and position[i+2][j-2] == '.' and position[i+3][j-3] == 'O' and score<9:
                    score = 10
                    action = [i+1,j-1]
                elif position [i-1][j+1] == '.' and position [i-2][j+2] == '.' and position[i+1][j-1] == '.' and position[i+2][j-2] == 'O' and score<9:
                    score = 10
                    action = [i+1,j-1]
                elif position [i+2][j-2] == '.' and position [i+1][j-1] == '.' and position[i+3][j-3] == '.' and position[i+4][j-4] == 'O' and score<6:
                    score = 7
                    action = [i+3,j-3]
                elif position [i+1][j-1] == '.' and position [i+2][j-2] == '.' and position[i+3][j-3] == '.' and position[i+4][j-4] == '.' and score<4:
                    score = 5
                    action = [i+2,j-2]
                elif position [i-1][j+1] == '.' and position [i+1][j-1] == '.' and position[i+2][j-2] == '.' and position[i+3][j-3] == '.' and score< 4:
                    score = 5
                    action = [i+1,j-1]
                elif position [i-1][j+1] == '.' and position [i-2][j+2] == '.' and position[i+1][j-1] == '.' and position[i+2][j-2] == '.' and score< 4:
                    score = 5
                    action = [i+1,j-1]
                elif position [i-1][j+1] == '.' and position [i-2][j+2] == '.' and position[i-3][j+3] == '.' and position[i+1][j-1] == '.' and score<4:
                    score = 5
                    action = [i-1,j+1]
                elif position [i-1][j+1] == '.' and position [i-2][j+2] == '.' and position[i-3][j+3] == '.' and position[i-4][j+4] == '.' and score<4:
                    score = 5
                    action = [i-1,j+1]
                """ Coup de la ceinture """
            if position [i][j] == 'O' and position [i-1][j+1] == 'O' and position [i+1][j+1] == 'O' and position[i][j+2] == 'O' and position[i][j+1] == '.' and score < 100:
                score = 100
                action = [i,j+1]
    return action
        
""" Utilisation de evaluateScore si le test manuel ne fonctionne pas """
def evaluateScore(consecutive, openEnds, maxplayer) :
        if (openEnds == 0 and consecutive < 5) :
            return -20
        if consecutive == 4 :
            if openEnds == 1:
                if maxplayer :
                    return 60
                return -50
            elif openEnds == 2 :
                if maxplayer:
                   return 100
                return -90
        elif consecutive == 3:
            if openEnds == 1:
                if maxplayer :
                    return 20
                return -10
            elif openEnds == 2:
                if maxplayer :
                    return 30
                return -20
        elif consecutive == 2 :
            if openEnds == 1:
                return 7
            elif openEnds == 2:
                return 9
        elif consecutive == 1 :
            if openEnds == 1 :
                return -2
            elif openEnds ==  2 :
                return 2
        elif consecutive == 0:
            if openEnds == 1 :
                return -5
            elif openEnds ==  2 :
                return 0
            elif openEnds ==  3 :
                return 1
            elif openEnds ==  4 :
                return 2
            elif openEnds ==  5 :
                return 2
            elif openEnds ==  6 :
                return 2
            elif openEnds ==  7 :
                return 2
            elif openEnds ==  8 :
                return 2

""" Méthode utile pour trier la liste des scores associés aux actions """
def takeFirst(elem):
    return elem[0]

""" Analyse du plateau pour le joueur X (max)  """
def AnalyseMax(maxplayer, position):
    score = 0
    countConsecutive = 0
    openEnds = 0
    """horizontale"""
    for i in range(len(position)):
        for j in range(len(position[i])) :
            if position[i][j] == 'X' :
                countConsecutive += 1
            elif position[i][j] == '.' and countConsecutive > 0 :
                openEnds+= 1
                score += evaluateScore(countConsecutive, openEnds, maxplayer)
                countConsecutive = 0
                openEnds= 1
            elif position[i][j] == '.' :
                openEnds = 1
            elif countConsecutive > 0 :
                score += evaluateScore(countConsecutive, openEnds, maxplayer)
                countConsecutive = 0
                openEnds= 0
            else :
                openEnds = 0
        if countConsecutive > 0 :
            score += evaluateScore(countConsecutive, openEnds, maxplayer);
        countConsecutive = 0
        openEnds = 0
    return score
    
    """verticale"""
    score = 0;
    countConsecutive = 0;
    openEnds = 0;
    for i in range(len(position)):
        for j in range(len(position[i])) :
            if position[j][i] == 'X' :
                countConsecutive += 1
            elif position[j][i] == '.' and countConsecutive > 0 :
                openEnds+= 1
                score += evaluateScore(countConsecutive, openEnds, maxplayer)
                countConsecutive = 0
                openEnds= 1
            elif position[j][i] == '.' :
                openEnds = 1
            elif countConsecutive > 0 :
                score += evaluateScore(countConsecutive, openEnds, maxplayer)
                countConsecutive = 0
                openEnds= 0
            else :
                openEnds = 0
        if countConsecutive > 0 :
            score += evaluateScore(countConsecutive, openEnds, maxplayer);
        countConsecutive = 0
        openEnds = 0
    return score
    """diagonale"""
    for i in range(len(position)):
        for j in range(len(position[i])) :
            
            """ Analyse diagonale """
            """ Diagonale droite haut """
            if(InPlateau([i-1,j-1]) and InPlateau([i+2,j+2]) and InPlateau([i+3,j+3]) and InPlateau([i+4,j+4])):    
                if position[i][j] == 'X' :
                    if position[i+1][j+1] == 'X':
                        if position[i+2][j+2] == 'X':
                            if position[i+3][j+3] == 'X':
                                countConsecutive += 1
                            elif position[i+3][j+3] == '.':
                                openEnds += 1
                            countConsecutive += 1
                        elif position[i+2][j+2] == '.' :
                            openEnds += 1
                            if evaluateScore(countConsecutive, openEnds, maxplayer) != None :
                                score += evaluateScore(countConsecutive, openEnds, maxplayer)
                        countConsecutive += 1
                    elif position[i+1][j+1] == '.':
                        openEnds += 1
                        if evaluateScore(countConsecutive, openEnds, maxplayer) != None :
                            score += evaluateScore(countConsecutive, openEnds, maxplayer)
                    countConsecutive += 1
                if position[i-1][j-1] == '.' :
                    openEnds += 1
                    if evaluateScore(countConsecutive, openEnds, maxplayer) != None :
                        score += evaluateScore(countConsecutive, openEnds, maxplayer)
                countConsecutive = 0
                openEnds= 0
                """ Diagonale gauche bas """
            elif(InPlateau([i+1,j+1]) and InPlateau([i-1,j-1]) and InPlateau([i-2,j-2]) and InPlateau([i-3,j-3]) and InPlateau([i-4,j-4])):
                if position[i][j] == 'X' :
                    if position[i-1][j-1] == 'X':
                        if position[i-2][j-2] == 'X':
                            if position[i-3][j-3] == 'X':
                                countConsecutive += 1
                            elif position[i-3][j-3] == '.':
                                openEnds += 1
                            countConsecutive += 1
                        elif position[i-2][j-2] == '.' :
                            openEnds += 1
                            if evaluateScore(countConsecutive, openEnds, maxplayer) != None :
                                score += evaluateScore(countConsecutive, openEnds, maxplayer)
                        countConsecutive += 1
                    elif position[i-1][j-1] == '.':
                        openEnds += 1
                        if evaluateScore(countConsecutive, openEnds, maxplayer) != None :
                            score += evaluateScore(countConsecutive, openEnds, maxplayer)
                    countConsecutive += 1
                if position[i+1][j+1] == '.' :
                    openEnds += 1
                    if evaluateScore(countConsecutive, openEnds, maxplayer) != None :
                        score += evaluateScore(countConsecutive, openEnds, maxplayer)
                countConsecutive = 0
                openEnds= 0
                """ Diagonale gauche haut """
            elif(InPlateau([i-1,j+1]) and InPlateau([i+1,j-1]) and InPlateau([i+2,j-2]) and InPlateau([i+3,j-3]) and InPlateau([i+4,j-4])):
                if position[i][j] == 'X' :
                    if position[i+1][j-1] == 'X':
                        if position[i+2][j-2] == 'X':
                            if position[i+3][j-3] == 'X':
                                countConsecutive += 1
                            elif position[i+3][j-3] == '.':
                                openEnds += 1
                            countConsecutive += 1
                        elif position[i+2][j-2] == '.' :
                            openEnds += 1
                            if evaluateScore(countConsecutive, openEnds, maxplayer) != None :
                                score += evaluateScore(countConsecutive, openEnds, maxplayer)
                        countConsecutive += 1
                    elif position[i+1][j-1] == '.':
                        openEnds += 1
                        if evaluateScore(countConsecutive, openEnds, maxplayer) != None :
                            score += evaluateScore(countConsecutive, openEnds, maxplayer)
                    countConsecutive += 1
                if position[i-1][j+1] == '.' :
                    openEnds += 1
                    if evaluateScore(countConsecutive, openEnds, maxplayer) != None :
                        score += evaluateScore(countConsecutive, openEnds, maxplayer)
                countConsecutive = 0
                openEnds= 0
                """ Diagonale droite bas """
            elif(InPlateau([i+1,j-1]) and InPlateau([i-1,j+1]) and InPlateau([i-2,j+2]) and InPlateau([i-3,j+3]) and InPlateau([i-4,j+4])):
                if position[i][j] == 'X' :
                    if position[i-1][j+1] == 'X':
                        if position[i-2][j+2] == 'X':
                            if position[i-3][j+3] == 'X':
                                countConsecutive += 1
                            elif position[i-3][j+3] == '.':
                                openEnds += 1
                            countConsecutive += 1
                        elif position[i-2][j+2] == '.' :
                            openEnds += 1
                            if evaluateScore(countConsecutive, openEnds, maxplayer) != None :
                                score += evaluateScore(countConsecutive, openEnds, maxplayer)
                        countConsecutive += 1
                    elif position[i-1][j+1] == '.':
                        openEnds += 1
                        if evaluateScore(countConsecutive, openEnds, maxplayer) != None :
                            score += evaluateScore(countConsecutive, openEnds, maxplayer)
                    countConsecutive += 1
                if position[i+1][j-1] == '.' :
                    openEnds += 1
                    if evaluateScore(countConsecutive, openEnds, maxplayer) != None :
                        score += evaluateScore(countConsecutive, openEnds, maxplayer)
                countConsecutive = 0
                openEnds= 0
            
            elif position[i][j] == '.' :
                if InPlateau([i+1,j+1]):
                    if position[i+1][j+1] == '.':
                        openEnds += 1
                if InPlateau([i-1,j-1]) :
                    if position[i-1][j-1] == '.':
                        openEnds += 1
                if InPlateau([i+1,j-1]):
                    if position[i+1][j-1] == '.':
                        openEnds += 1
                if InPlateau([i-1,j+1]) :
                    if position[i-1][j+1] == '.':
                        openEnds += 1
                if evaluateScore(countConsecutive, openEnds, maxplayer) != None :
                    score += evaluateScore(countConsecutive, openEnds, maxplayer)
    return score



""" Analyse du position pour le joueur O (min) """

""" Analyse horizontale """
def AnalyseMin(maxplayer, position) :
    score = 0
    countConsecutive = 0
    openEnds = 0
    """horizontale"""
    for i in range(len(position)):
        for j in range(len(position[i])) :
            if position[i][j] == 'O' :
                countConsecutive += 1
            elif position[i][j] == '.' and countConsecutive > 0 :
                openEnds+= 1
                score += evaluateScore(countConsecutive, openEnds, maxplayer)
                countConsecutive = 0
                openEnds= 1
            elif position[i][j] == '.' :
                openEnds = 1
            elif countConsecutive > 0 :
                score += evaluateScore(countConsecutive, openEnds, maxplayer)
                countConsecutive = 0
                openEnds= 0
            else :
                openEnds = 0
        if countConsecutive > 0 :
            score += evaluateScore(countConsecutive, openEnds, maxplayer);
        countConsecutive = 0
        openEnds = 0
    return score
    
    """verticale"""
    score = 0;
    countConsecutive = 0;
    openEnds = 0;
    for i in range(len(position)):
        for j in range(len(position[i])) :
            if position[j][i] == 'O' :
                countConsecutive += 1
            elif position[j][i] == '.' and countConsecutive > 0 :
                openEnds+= 1
                score += evaluateScore(countConsecutive, openEnds, maxplayer)
                countConsecutive = 0
                openEnds= 1
            elif position[j][i] == '.' :
                openEnds = 1
            elif countConsecutive > 0 :
                score += evaluateScore(countConsecutive, openEnds, maxplayer)
                countConsecutive = 0
                openEnds= 0
            else :
                openEnds = 0
        if countConsecutive > 0 :
            score += evaluateScore(countConsecutive, openEnds, maxplayer);
        countConsecutive = 0
        openEnds = 0
    return score
    """diagonale"""
    for i in range(len(position)):
        for j in range(len(position[i])) :
            
            """ Analyse diagonale """
            """ Diagonale droite haut """
            if(InPlateau([i-1,j-1]) and InPlateau([i+2,j+2]) and InPlateau([i+3,j+3]) and InPlateau([i+4,j+4])):    
                if position[i][j] == 'O' :
                    if position[i+1][j+1] == 'O':
                        if position[i+2][j+2] == 'O':
                            if position[i+3][j+3] == 'O':
                                countConsecutive += 1
                            elif position[i+3][j+3] == '.':
                                openEnds += 1
                            countConsecutive += 1
                        elif position[i+2][j+2] == '.' :
                            openEnds += 1
                            if evaluateScore(countConsecutive, openEnds, maxplayer) != None :
                                score += evaluateScore(countConsecutive, openEnds, maxplayer)
                        countConsecutive += 1
                    elif position[i+1][j+1] == '.':
                        openEnds += 1
                        if evaluateScore(countConsecutive, openEnds, maxplayer) != None :
                            score += evaluateScore(countConsecutive, openEnds, maxplayer)
                    countConsecutive += 1
                if position[i-1][j-1] == '.' :
                    openEnds += 1
                    if evaluateScore(countConsecutive, openEnds, maxplayer) != None :
                        score += evaluateScore(countConsecutive, openEnds, maxplayer)
                countConsecutive = 0
                openEnds= 0
                """ Diagonale gauche bas """
            elif(InPlateau([i+1,j+1]) and InPlateau([i-1,j-1]) and InPlateau([i-2,j-2]) and InPlateau([i-3,j-3]) and InPlateau([i-4,j-4])):
                if position[i][j] == 'O' :
                    if position[i-1][j-1] == 'O':
                        if position[i-2][j-2] == 'O':
                            if position[i-3][j-3] == 'O':
                                countConsecutive += 1
                            elif position[i-3][j-3] == '.':
                                openEnds += 1
                            countConsecutive += 1
                        elif position[i-2][j-2] == '.' :
                            openEnds += 1
                            if evaluateScore(countConsecutive, openEnds, maxplayer) != None :
                                score += evaluateScore(countConsecutive, openEnds, maxplayer)
                        countConsecutive += 1
                    elif position[i-1][j-1] == '.':
                        openEnds += 1
                        if evaluateScore(countConsecutive, openEnds, maxplayer) != None :
                            score += evaluateScore(countConsecutive, openEnds, maxplayer)
                    countConsecutive += 1
                if position[i+1][j+1] == '.' :
                    openEnds += 1
                    if evaluateScore(countConsecutive, openEnds, maxplayer) != None :
                        score += evaluateScore(countConsecutive, openEnds, maxplayer)
                countConsecutive = 0
                openEnds= 0
                """ Diagonale gauche haut """
            elif(InPlateau([i-1,j+1]) and InPlateau([i+1,j-1]) and InPlateau([i+2,j-2]) and InPlateau([i+3,j-3]) and InPlateau([i+4,j-4])):
                if position[i][j] == 'O' :
                    if position[i+1][j-1] == 'O':
                        if position[i+2][j-2] == 'O':
                            if position[i+3][j-3] == 'O':
                                countConsecutive += 1
                            elif position[i+3][j-3] == '.':
                                openEnds += 1
                            countConsecutive += 1
                        elif position[i+2][j-2] == '.' :
                            openEnds += 1
                            if evaluateScore(countConsecutive, openEnds, maxplayer) != None :
                                score += evaluateScore(countConsecutive, openEnds, maxplayer)
                        countConsecutive += 1
                    elif position[i+1][j-1] == '.':
                        openEnds += 1
                        if evaluateScore(countConsecutive, openEnds, maxplayer) != None :
                            score += evaluateScore(countConsecutive, openEnds, maxplayer)
                    countConsecutive += 1
                if position[i-1][j+1] == '.' :
                    openEnds += 1
                    if evaluateScore(countConsecutive, openEnds, maxplayer) != None :
                        score += evaluateScore(countConsecutive, openEnds, maxplayer)
                countConsecutive = 0
                openEnds= 0
                """ Diagonale droite bas """
            elif(InPlateau([i+1,j-1]) and InPlateau([i-1,j+1]) and InPlateau([i-2,j+2]) and InPlateau([i-3,j+3]) and InPlateau([i-4,j+4])):
                if position[i][j] == 'O' :
                    if position[i-1][j+1] == 'O':
                        if position[i-2][j+2] == 'O':
                            if position[i-3][j+3] == 'O':
                                countConsecutive += 1
                            elif position[i-3][j+3] == '.':
                                openEnds += 1
                            countConsecutive += 1
                        elif position[i-2][j+2] == '.' :
                            openEnds += 1
                            if evaluateScore(countConsecutive, openEnds, maxplayer) != None :
                                score += evaluateScore(countConsecutive, openEnds, maxplayer)
                        countConsecutive += 1
                    elif position[i-1][j+1] == '.':
                        openEnds += 1
                        if evaluateScore(countConsecutive, openEnds, maxplayer) != None :
                            score += evaluateScore(countConsecutive, openEnds, maxplayer)
                    countConsecutive += 1
                if position[i+1][j-1] == '.' :
                    openEnds += 1
                    if evaluateScore(countConsecutive, openEnds, maxplayer) != None :
                        score += evaluateScore(countConsecutive, openEnds, maxplayer)
                countConsecutive = 0
                openEnds= 0
            
            elif position[i][j] == '.' :
                if InPlateau([i+1,j+1]):
                    if position[i+1][j+1] == '.':
                        openEnds += 1
                if InPlateau([i-1,j-1]) :
                    if position[i-1][j-1] == '.':
                        openEnds += 1
                if InPlateau([i+1,j-1]):
                    if position[i+1][j-1] == '.':
                        openEnds += 1
                if InPlateau([i-1,j+1]) :
                    if position[i-1][j+1] == '.':
                        openEnds += 1
                if evaluateScore(countConsecutive, openEnds, maxplayer) != None :
                    score += evaluateScore(countConsecutive, openEnds, maxplayer)
    return score

def bestMove(L):
    bestscore = L[0][0]
    bestL = [L[0][1]]
    for i in range(len(L)):
        score = L[i][0]
        if score == bestscore :
            bestL.append(L[i][1])
    return bestL
    


#%% Algo loop
""" Lancement du jeu par algo loop """

def algo_loop_IA():
    Pions_J1 = 60
    Pions_J2 = 60
    Rest_Lettres = []
    Rest_Nbres = []
    ligne = 1
    colonne = 1
    reponseJeu=input("Qui commence ? (IA ou Joueur)")
    if(reponseJeu.lower() == "joueur"):
        while(is_end(position) == None and (Pions_J1>0 and Pions_J2>0)):
            exectime = 0.0
            if(Pions_J1==60):
                ligne = dict_alpha[input("Saisissez la ligne où vous souhaitez placer votre pion : ").upper()]
                colonne = int(input("Saisissez la colonne où vous souhaitez placer votre pion : "))
                while(ligne != 8 or colonne != 8):
                    print("Votre premier pion doit être en position H8")
                    ligne = dict_alpha[input("Saisissez la ligne où vous souhaitez placer votre pion : ").upper()]
                    colonne = int(input("Saisissez la colonne où vous souhaitez placer votre pion : "))
                position[ligne][colonne] = 'O'
                Liste1 = []
                Liste2 = []
                ligne = 8
                colonne = 8
                for k in range(-3,4):
                    if(InPlateau([ligne+k,colonne+k])):
                        Liste1.append(dict_num[colonne+k])
                        Liste2.append(colonne+k)
                Rest_Lettres.append(Liste1)
                Rest_Nbres.append(Liste2)
            else:
                ligne, colonne = Action()
            Pions_J1+=-1
            """ Choix de l'IA """
            start = time.time()
            if Heuristique(position)[1] == [0,0]:
                L = Minimax((position, [ligne, colonne]), 2, -math.inf, math.inf, True,[])[2]
                L.sort(reverse = True)
                bestL = bestMove(L)
                ligne, colonne = random.choice(bestL)
            else : 
                ligne, colonne = Heuristique(position)
            stop = time.time()
            exectime = stop - start
            ligne_IA, colonne_IA = ligne, colonne
            position[ligne][colonne] = "X"
            Pions_J2+=-1
            print("\n"+"||| J1 : "+str(Pions_J1)+" pions restants |||")
            print("||| J2 : "+str(Pions_J2)+" pions restants |||"+"\n")
            print(Affichage(position))
            print("Coup joué par l'IA : " + dict_num[ligne_IA],colonne_IA)
            print("Temps d'exécution : ", exectime)
        if(Pions_J1==0):
            print("Le joueur 1 n'a plus de jetons disponibles")
        if(Pions_J2==0):
            print("Le joueur 2 n'a plus de jetons disponibles")
        print("Le joueur " + is_end(position) + " a gagné !")
    if(reponseJeu.upper()=="IA"):
        while(is_end(position) == None and (Pions_J1>0 and Pions_J2>0)):
            exectime = 0.0
            if(Pions_J1==59):
                Liste1=[]
                Liste2=[]
                ligne = 8
                colonne = 8
                for k in range(-3,4):
                    if(InPlateau([ligne+k,colonne+k])):
                        Liste1.append(dict_num[colonne+k])
                        Liste2.append(colonne+k)
                Rest_Lettres.append(Liste1)
                Rest_Nbres.append(Liste2)
                """ Choix de l'IA hors du carré de 7"""
                start = time.time()
                if [4,4] in Liste_Positions_Possibles(position):
                    ligne, colonne = [4,4]
                else :
                    ligne, colonne = [4,12]
                stop = time.time()
                exectime = stop - start
                position[ligne][colonne] = "X"
                ligne_IA, colonne_IA = ligne, colonne
            if(Pions_J1<=60 and Pions_J1!=59):
                if(Pions_J1==60):
                    position[8][8] = "X"
                    ligne_IA, colonne_IA = (8, 8)
                else:
                    """ Choix de l'IA par minimax """
                    start = time.time()
                    if Heuristique(position)[1] == [0,0]:
                        L = Minimax((position, [ligne, colonne]), 2, -math.inf, math.inf, True,[])[2]
                        L.sort(reverse = True)
                        bestL = bestMove(L)
                        ligne, colonne = random.choice(bestL)
                    else : 
                        ligne, colonne = Heuristique(position)
                    stop = time.time()
                    exectime = stop - start
                    position[ligne][colonne] = "X"
                    ligne_IA, colonne_IA = ligne, colonne
            Pions_J1+=-1
            print(Affichage(position))
            print("Coup joué par l'IA : " + dict_num[ligne_IA],colonne_IA)
            print("Temps d'exécution : ", exectime)
            ligne, colonne = Action()
            Pions_J2+=-1
            print("\n"+"||| J1 : "+str(Pions_J1)+" pions restants |||")
            print("||| J2 : "+str(Pions_J2)+" pions restants |||"+"\n")
        if(Pions_J1==0):
            print("Le joueur 1 n'a plus de jetons disponibles")
        if(Pions_J2==0):
            print("Le joueur 2 n'a plus de jetons disponibles")
        print("Le joueur " + is_end(position) + " a gagné !")
#%% Main

if __name__ == '__main__' :
    algo_loop_IA()
