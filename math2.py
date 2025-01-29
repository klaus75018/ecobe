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
    listeDePostes=list(dict.fromkeys(listeDePostes))
    return listeDePostes

#fonction pour faire la matrice d'ou sera tirée les coréllation
           
def matrice1(ma_liste, liste_de_postes):
    mat = []
    mat.append(liste_de_postes)
    nb = len(liste_de_postes) #je compte le nombre de postes
    for i in ma_liste:
        entreprise = []
        for j in i.princingdbprojectsubpricingsubsubtradegroup_set.all():
            groupe = []
            for l in range(0,nb-2):
                groupe.append(0)
                for k in j.princingdbprojectsubpricingsubsubtrade_set.all():
                    if k.name == liste_de_postes[l]:
                        groupe[l] = 1
            groupe.append(j.group_price/i.company_offer_sub_trade_price)
            groupe.append(i.company_offer_sub_trade_price)
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
            for l in range(0,len(j)-2):
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
            for l in range(0,len(j)-2):
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



def correllMat(myMatrix3):
    mat3 = myMatrix3
    nbDeColones = len(mat3[0])
    nbDeLignes = len(mat3)


    corrmat = []
    for jj in range(0,nbDeColones-2):
        corrx = []
        for j in range(0,nbDeColones-2):
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
    nouveaux_postes = liste_de_postes.copy()
    for i in range(0,len(corrmat)):
        for j in range(0,len(corrmat[0])):
            print(j)
            if j != i:
                if j > i :
                    if corrmat[i][j] >0.99:
                        nouveaux_postes[i] =  f"{nouveaux_postes[i]} ET {nouveaux_postes[j]}"
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

def creecvc(mymat5):
    mat5 = mymat5
    with open('mynewcsvfile.csv','w') as new_file:
        csv_writer = csv.writer(new_file, delimiter = ',')
        for i in mat5:
            csv_writer.writerow(i)

def ouvrireetregression():
    df = pd.read_csv(".\mynewcsvfile.csv",encoding='unicode_escape')

    reg = linear_model.LinearRegression(fit_intercept=False)#fit intercept False force b = 0

    x = df.drop(columns = ["Total avec les autres postes","Part du total"])

    y = df["Part du total"]

    reg.fit(x,y)

    coefs = reg.coef_


def valeurscherchees(choix, coeficient, mymatrix5):
    


         
    




 










               
                 



