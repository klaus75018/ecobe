#pour les sous lot en % par poste, cette fonction va me donner les poste proposables en fonctionn des correllation


#etape 1 faire la liste des sous poste dispo
#Ce sera une fonction qui recevra une liste des offres à analyser (car collant à ma recherche)
######################################"""
#"Je commence par faire une liste teste"
###########################
from polls.models import PrincingDBProjectSubPricingSubTradeCompanyOffer
import numpy as np


liste_test = []

for i in PrincingDBProjectSubPricingSubTradeCompanyOffer.objects.all():
    print(i)
    liste_test.append(i)

#Ma fonction qui donne la liste des postes

def lister_les_postes(ma_liste): 
    listeDePostes = []
    for i in ma_liste:
        for j in i.princingdbprojectsubpricingsubsubtradegroup_set.all():
            for k in j.princingdbprojectsubpricingsubsubtrade_set.all():
                listeDePostes.append(k.name)

    listeDePostes.append("Part du total")
    listeDePostes.append("Total avec les autres postes")
    listeDePostes.append("Surface")
    listeDePostes=list(dict.fromkeys(listeDePostes))
    return listeDePostes

#fonction pour faire la matrice d'ou sera tirée les coréllation
           
def matrice1(ma_liste, liste_de_postes):
    mat=[liste_de_postes]
    nb = len(liste_de_postes) #je compte le nombre de postes mais ya aussi 3 colones en plus : % prix tot et surface
    for i in ma_liste:
        entreprise = []
        for j in i.princingdbprojectsubpricingsubsubtradegroup_set.all():
            groupe = []
            for l in range(0,nb-3):
                groupe.append(0)
                for k in j.princingdbprojectsubpricingsubsubtrade_set.all():
                    if k.name == liste_de_postes[l]:
                        groupe[l] = 1
            groupe.append(j.group_price/i.company_offer_sub_trade_price)
            groupe.append(i.company_offer_sub_trade_price)
            groupe.append(i.sub_trade.trade.project.considered_surface)
            entreprise.append(groupe)
        mat.append(entreprise)
    return mat

#fonction qui calcule la somme la plus grande dans une matrice enn enlevant d'abord les entetes

def offre_la_plus_complete(myMatrix):
    mat = myMatrix
    lg = len(mat)
    somme_max = 0

    for i in range(1,lg):
        somme_inter = 0
        for j in mat[i]:
            for l in range(0,len(j)-3):
                somme_inter += j [l]
        if somme_inter > somme_max:
            somme_max = somme_inter
    return somme_max

#fonction qui extrait seulement les offres les plus completes

def offres_completes(myMatrix, nbDePostes):
    mat = myMatrix
    somme_max = nbDePostes
    lg = len(mat)
    mat2 = []
    for i in range(1,lg):
        somme_int = 0
        for j in mat[i]:
            for l in range(0,len(j)-3):
                somme_int += j [l]
                print(somme_int)
                print(type(somme_int))
        if somme_int == somme_max:
            mat2.append(mat[i])
        return mat2

#on decoude les groupes

def decoude(myMatrix2):
    mat2 = myMatrix2
    mat3 = []

    for i in mat2:
        for j in i:
            mat3.append(j)
    return mat3



#matrice de correlation


import numpy as np 
def correllMat(myMatrix3):
    mat3 = myMatrix3
    nbDeColones = len(mat3[0])
    nbDeLignes = len(mat3)


    corrmat = []
    for jj in range(0,nbDeColones-3):
        corrx = []
        for j in range(0,nbDeColones-3):
            x = []
            y = []
            for i in range(0,nbDeLignes):
                x.append(mat3[i][j])
                y.append(mat3[i][jj])
            print (f"x est egal à {x}")
            print(f"et y à {y}")
            c = np.corrcoef(x,y)
            print(c)
            print(f"c01 est egal à {c[0][1]}")
            print(corrx)
            corrx.append(c[0][1])
        
        corrmat.append(corrx)
    return corrmat



#matrice qui va regrouper les postes si nécessaire

def regroupepostes(corrmatrix,ListeDesPostes, myMatrix3):
    mat3 = myMatrix3

    corrmat = corrmatrix
    liste_de_postes = ListeDesPostes
mat4=[]
mat3inter = mat3.copy()
lg = len(corrmat)
nouveaux_postes = liste_de_postes.copy()
for i in range(0,lg):
    for j in range(0,lg):
        print(j)
        if j != i:
            if j > i :
                if corrmat[i][j] >0.99:
                    if nouveaux_postes[i] != "NA":
                        nouveaux_postes[i] =  f"{nouveaux_postes[i]} ET {liste_de_postes[j]}"
                        nouveaux_postes[j] = "NA"
                    for k in mat3inter:
                        k[j] = "NA"
mat4.append(nouveaux_postes)
for l in mat3inter:
    mat4.append(l)




def virerlesNA(mymatrix4):
mat4 = mymatrix4
mat5 = []
ligne = []
for i in mat4:
    ligne = []
    for j in i:
        if j!= "NA":
            ligne.append(j)
    mat5.append(ligne)


import csv

def creecvc(mymat5):
    mat5 = mymat5
with open('new_csv_file.csv','w') as new_file:
    csv_writer = csv.writer(new_file, delimiter = ',')
    for i in mat5:
        csv_writer.writerow(i)

######################regression##################
import pandas as pd
from sklearn import linear_model



df = pd.read_csv('new_csv_file.csv', encoding='unicode_escape')

x = df.drop(columns = ["Part du total","Total avec les autres postes","Surface"])
y = df["Part du total"]



cor = linear_model.LinearRegression(fit_intercept=False)#"False pour que b soit egal à 0"

cor.fit(x,y)

coeficients = cor.coef_
#############################################################   

def nouvellescolones(choix, liste_de_postes, coefficients, matrix5):#coix ,DOIT etre une liste, meme si un seul choix !!

    mat5 = matrix5
    mat_finale = []
    nb_de_choix = len(choix)
    nbmax = len(liste_de_postes)-3
    dic ={}
    l=0
        #je fais un dictionnaire avec mes coefficients
    for m in range(0,nbmax):
        dic[liste_de_postes[m]] = coefficients[l]
        l+=1


    for i in range(1,len(mat5)):
        x = mat5[i][11]
        y = 0
        nbdeparam = 0
        nbdechoixpresent = 0
        for j in range(0,nbmax):
            nbdeparam += mat5[i][j]
            for k in choix:
                if mat5[0][j]==k:
                    nbdechoixpresent += mat5[i][j]
                
            if nbdechoixpresent ==0:#cas 1
                y = mat5[i][9]
                for choice in choix:
                    y += dic[choice]

                for nn in range(0,nbmax):
                    y-=mat5[i][nn]*dic[mat5[0][nn]]
        #----------------------------------------------------------------

            elif nbdechoixpresent ==  nb_de_choix:
                if nbdechoixpresent == nbdeparam: #cas 2
                    y = mat5[i][9]
        #----------------------------------------------------------------
                
                elif nbdechoixpresent < nbdeparam: #cas 3
                    y = mat5[i][9]
                    for n in range(0,nbmax):
                        var = 0
                        for choice in choix:
                            if mat5[0][n] == choice:
                                var = 1
                        if var == 0:
                            y-=mat5[i][n]*dic[mat5[0][n]]
        #----------------------------------------------------------------

            elif nbdechoixpresent < nb_de_choix:
                if nbdechoixpresent == nbdeparam: #cas 4
                    y = mat5[i][9]
                    missing_choices = choix.copy()
                    for n in range(0,nbmax):
                        if mat5[i][n] == 1:
                            missing_choices.remove(mat5[0][n])
                    for choice in missing_choices:
                        y+=dic[choice]

        #_________________________________________________________________



                elif nbdechoixpresent < nbdeparam:#cas 5
                    y = mat5[i][9]
                    missing_choices = choix.copy()    
                    for n in range(0,nbmax):
                            if mat5[i][n] == 1:
                                var=0
                                for choice in choix:
                                    if mat5[i][n] == choice:
                                        var = 1
                                if var == 1:
                                    missing_choices.remove(mat5[0][n])
                                else:
                                    y-=mat5[i][n]*dic[mat5[0][n]]
                    for choice in missing_choices:
                        y+=dic[choice]
                            
        y = y * mat5[i][10]
        mat_finale.append([x,y])
    return mat_finale


def nouvelles_colonnes_GPT(choix, liste_de_postes, coefficients, matrix5):
    """
    Compute new columns based on choices, positions, coefficients, and an input matrix.
    
    Parameters:
    - choix: List of selected choices (must be a list even if only one choice).
    - liste_de_postes: List of job positions.
    - coefficients: List of coefficients corresponding to job positions.
    - matrix5: Input matrix (2D list).

    Returns:
    - mat_finale: A list of computed [x, y] values for each row in matrix5.
    """
    mat5 = matrix5
    mat_finale = []
    nb_de_choix = len(choix)
    nbmax = len(mat5[0]) - 3


    # Create a dictionary of coefficients
    dic = {mat5[0][m]: coefficients[m] for m in range(nbmax)}

    for i in range(1, len(mat5)):  # Skip the header row
        x = mat5[i][nbmax+2]
        y = 0
        nbdeparam = sum(mat5[i][j] for j in range(nbmax))
        nbdechoixpresent = sum(mat5[i][j] for j in range(nbmax) if mat5[0][j] in choix)
        
        if nbdechoixpresent == 0:  # Case 1
            y = mat5[i][nbmax] + sum(dic[choice] for choice in choix)
            y -= sum(mat5[i][nn] * dic[mat5[0][nn]] for nn in range(nbmax))
        
        elif nbdechoixpresent == nb_de_choix:
            if nbdechoixpresent == nbdeparam:  # Case 2
                y = mat5[i][nbmax]
            elif nbdechoixpresent < nbdeparam:  # Case 3
                y = mat5[i][nbmax]
                y -= sum(mat5[i][n] * dic[mat5[0][n]] for n in range(nbmax) if mat5[0][n] not in choix)
        
        elif nbdechoixpresent < nb_de_choix:
            if nbdechoixpresent == nbdeparam:  # Case 4
                y = mat5[i][nbmax]
                missing_choices = choix.copy()
                for n in range(nbmax):
                    if mat5[i][n] == 1:
                        if mat5[0][n] in choix:
                            missing_choices.remove(mat5[0][n])
                y += sum(dic[choice] for choice in missing_choices)
            elif nbdechoixpresent < nbdeparam:  # Case 5
                y = mat5[i][nbmax]
                missing_choices = choix.copy()
                for n in range(nbmax):
                    if mat5[i][n] == 1:
                        if mat5[0][n] in choix:
                            missing_choices.remove(mat5[0][n])
                        else:
                            y -= mat5[i][n] * dic[mat5[0][n]]
                y += sum(dic[choice] for choice in missing_choices)
        
        y *= mat5[i][nbmax+1]
        y /= mat5[i][nbmax+2]
        z = y**2
        y = z**0.5
        mat_finale.append([x, y])

return mat_finale










               
                 



