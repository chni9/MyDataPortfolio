# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 18:17:28 2022

@author: yassi
"""
import random
from math import sin, sqrt
import time
from operator import itemgetter
import numpy as np
import matplotlib.pyplot as plt

#Chargement des données de "position_sample.csv"
def position_sample(file):
    f = open(file)
    X = []
    Y = []
    T = []
    
    """ Traitement des données du fichier """
    data1 = []
    data2 = []
    data = f.read()
    data = data.split("\n")
    for line in data:
        data1.append(line.split(";"))
    del data1[0]
    
    """Transformation des tous les éléments en float"""
    for k in data1:
        data2.append((float(k[0]),float(k[1]),float(k[2])))
        
    """ Tri des éléments selon t """
    data3 = sorted(data2, key = itemgetter(0))
    
    """ Remplissage de trois tableaux contenants les données de x(t), y(t) et t """
    for i in range(1,len(data3)):
        T.append(float(data3[i][0]))
        X.append(float(data3[i][1]))
        Y.append(float(data3[i][2]))
        
    """ Affichage des courbes de X et Y pour mieux comprendre le problème
    plt.plot(T,X)
    plt.plot(T,Y,"red")
    plt.grid()
    plt.show()
    """
    
    return X, Y, T
        
        
    #random.sample([float(i) for i in range(-100,101)], 6)
    

class individu:
    
    
    #Constructeur
    def __init__(self, val = None):
        if val == None:
            self.val = []
            for i in range(6):
                self.val.append(round(random.uniform(-100.00,100.00),3))
        else :
            self.val = val
        self.avg_dist = self.fitness(X, Y, T)
        
    #Affichage
    def __str__(self):
        return f"Les paramètres de la trajectoire du satellite sont {self.val}"
    
    #Fitness
    def fitness(self, X, Y, T):
        distx = []
        disty = []
        avg_distx = 0
        avg_disty = 0
        self.avg_dist = 0
        """ Calcul de la distance Euclidienne entre les trajectoires mesurées et calculées """
        for i in range(len(T)) :
            xt = self.val[0] * sin(self.val[1] * T[i] + self.val[2])
            yt = self.val[3] * sin(self.val[4] * T[i] + self.val[5])
            distx.append(sqrt((X[i] - xt)**2))
            disty.append(sqrt((Y[i] - yt)**2))
        for dx in distx:
            avg_distx += dx
        for dy in disty:
            avg_disty += dy
        avg_distx =  avg_distx / len(distx)
        avg_disty =  avg_disty / len(disty)
        self.avg_dist = [avg_distx, avg_disty]
        return  self.avg_dist
    
    #Population
    def create_rand_pop(n):
        """ Création aléatoire d'une population de taille n """
        pop = []
        for i in range(n):
            pop.append(individu())
        return pop
    
    #Evaluation
    def evaluate(pop):
        """ Tri de pop en fonction de 'avg_dist' de chaque individu """
        return sorted(pop, key = lambda individu : individu.avg_dist)
    
    #Sélection
    def selection(pop, hcount, lcount):
        """ On séléctionne les hcount meilleurs individu et les lcount pires """
        sub_pop = []
        for i in range(hcount):
            sub_pop.append(pop[i])
        for j in range(1, lcount + 1):
            sub_pop.append(pop[-j])
        return sub_pop
     
    #Croisement
    def croisement(ind1,ind2):
        """ Création de deux individu issus du croisement des 3 premiers et 3 derniers élements de chacun """
        new_ind1 = individu(ind1.val[:3] + ind2.val[3:])
        new_ind2 = individu(ind2.val[:3] + ind1.val[3:])
        return new_ind1, new_ind2
    
    #Mutation
    def mutation(ind):
        """ Modification aléatoire d'un élement de l'individu ind """
        index = random.randint(0,5)
        ind.val[index] = round(random.uniform(-100,100),3)
        return ind
    
    #Boucle finale
    def algoloop():
        start = time.time()
        pop = individu.create_rand_pop(250)
        solutiontrouvee = False
        nbiteration = 0
        while not solutiontrouvee :
            print("Itération numéro : ", nbiteration)
            nbiteration += 1
            evaluation = individu.evaluate(pop)
            if evaluation[0].fitness(X, Y, T)[0] == 0.0 and evaluation[0].fitness(X, Y, T)[1] == 0.0 :
                print(evaluation[0].fitness(X, Y, T))
                solutiontrouvee = True
            else :
                select = individu.selection(evaluation, 150, 0)
                print(evaluation[0].fitness(X, Y, T))
                croises = []
                for i in range (0, len(select), 2) :
                    croises += individu.croisement(select[i], select[i+1])
                mutes = []
                for i in select :
                    mutes.append(individu.mutation(i))
                newalea = individu.create_rand_pop(50)
                pop = select[:] + croises[:] + mutes[:] + newalea[:]
            #time.sleep(0.25)
        end = time.time()
        print(evaluation[0])
        print("Temps d'exécution :", end - start,"s")
        
#%% Main

if __name__ == '__main__' :
    #Tableaux des données de positions du staellite
    X, Y, T = position_sample("C:\\Users\\yassi\\OneDrive - De Vinci\\ESILV\\Semestre 06\\Datascience & IA\\Projet\\position_sample.csv")
    
    #Lancement du programe
    individu.algoloop()
    
        