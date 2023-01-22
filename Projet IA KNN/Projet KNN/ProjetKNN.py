# -*- coding: utf-8 -*-
"""
Created on Mon May  9 12:59:17 2022

@author: yassi
"""
from math import sqrt
import collections

def KNN(k, file, individu):
    """ Chargement des données """
    f = open(file, 'r')
    data = f.read()
    data1 = data.split('\n')
    dataset = []
    for line in data1 :
        dataset.append(line.split(';'))
    del dataset[-1]
    
    """ Calcul des distances et traitement des données """

    categorie = []
    for i in range(len(dataset)):
        categorie.append(dataset[i][10])
    average_dist = DistanceEuclidienne(dataset, individu)
    distance = dict(zip(average_dist, categorie))

    """ Sélection des k voisins les plus proches """

    selected = []
    ordered_distance = collections.OrderedDict(sorted(distance.items()))
    n = 0
    for key, value in ordered_distance.items():
        if n <= k :
            selected.append((key, value))
        n+=1

    
    """ Détermination de la catégorie """
    del selected[0]
    classe0 = 0
    classe1 = 0
    for individu in selected :
        if individu[1] == '0' :
            classe0 += 1
        elif individu[1] == '1' :
            classe1 += 1

            
    if classe0 > classe1 :
        classe_individu = '0'
    elif classe1 > classe0 :
        classe_individu = '1'
    elif classe1 == classe0 :
        classe_individu = 'Not found'

    f.close()
    
    return classe_individu

    
    
    
def DistanceEuclidienne(L1, L2):
    result1 = []
    result2 = []
    result3 = []
    result4 = []
    result5 = []
    result6 = []
    result7 = []
    result8 = []
    result9 = []
    result10 = []
    average_dist = []
    """ Calcul distance pour chaque attribut """
    for i in range(len(L2)):
        for j in range(len(L1)):
            if i == 0 :
                result1.append(sqrt((float(L2[i])- float(L1[j][i]))**2))
            elif i == 1:
                result2.append(sqrt((float(L2[i])- float(L1[j][i]))**2))
            elif i == 2:
                result3.append(sqrt((float(L2[i])- float(L1[j][i]))**2))
            elif i == 3:
                result4.append(sqrt((float(L2[i])- float(L1[j][i]))**2))
            elif i == 4:
                result5.append(sqrt((float(L2[i])- float(L1[j][i]))**2))
            elif i == 5:
                result6.append(sqrt((float(L2[i])- float(L1[j][i]))**2))
            elif i == 6:
                result7.append(sqrt((float(L2[i])- float(L1[j][i]))**2))
            elif i == 7:
                result8.append(sqrt((float(L2[i])- float(L1[j][i]))**2))
            elif i == 8:
                result9.append(sqrt((float(L2[i])- float(L1[j][i]))**2))
            elif i == 9:
                result10.append(sqrt((float(L2[i])- float(L1[j][i]))**2))
    """ Calcul de la distance moyenne des 10 attributs """
    for l in range(len(result1)):
        sum = result1[l] + result2[l] + result3[l] + result4[l] + result5[l] + result6[l] + result7[l] + result8[l] + result9[l] + result10[l]
        average_dist.append(sum / 10)
    return average_dist


     
def tauxReussite():
    f = open("C:\\Users\\yassi\\OneDrive - De Vinci\\ESILV\\Semestre 06\\Datascience & IA\\Projet KNN\\resultat.txt", 'r')
    doc = f.read()
    doc = doc.split('\n')
    del doc[0]
    reussite = 0
    for x in doc:
        y = x.split(";")
        if y[0] == y[1]:
            reussite += 1
    return reussite / len(doc)    
                    
       

#%% Main
if __name__ == '__main__' :
    # for k in range(3, 51, 2):
    #     f = open("C:\\Users\\yassi\\OneDrive - De Vinci\\ESILV\\Semestre 06\\Datascience & IA\\Projet KNN\\preTest.txt", 'r')
    #     data = f.read()
    #     data1 = data.split('\n')
    #     dataset = []
    #     for line in data1 :
    #         dataset.append(line.split(';'))
    #     del dataset[-1]
    #     fichier = open("C:\\Users\\yassi\\OneDrive - De Vinci\\ESILV\\Semestre 06\\Datascience & IA\\Projet KNN\\resultat.txt", 'w')
    #     for individu in dataset :
    #         result = KNN(k,"C:\\Users\\yassi\\OneDrive - De Vinci\\ESILV\\Semestre 06\\Datascience & IA\\Projet KNN\\data.txt", individu)
    #         str_result = individu[10] + ";" + result 
    #         fichier.write("\n" + str_result)
    #     fichier.close()
    #     taux = tauxReussite()
    #     print("Pour k = ", k," --> taux de réussite =", taux)
    
    
    k = 45
    f = open("C:\\Users\\yassi\\OneDrive - De Vinci\\ESILV\\Semestre 06\\Datascience & IA\\Projet KNN\\preTest.txt", 'r')
    data = f.read()
    data1 = data.split('\n')
    dataset = []
    for line in data1 :
        dataset.append(line.split(';'))
    del dataset[-1]
    fichier = open("C:\\Users\\yassi\\OneDrive - De Vinci\\ESILV\\Semestre 06\\Datascience & IA\\Projet KNN\\CHENIK_BOUCHIBA_groupeL.txt", 'w')
    for individu in dataset :
        result = KNN(k,"C:\\Users\\yassi\\OneDrive - De Vinci\\ESILV\\Semestre 06\\Datascience & IA\\Projet KNN\\data.txt", individu) 
        fichier.write(result + "\n")
    fichier.close()
    print("Fichier prédicition créé !")
    