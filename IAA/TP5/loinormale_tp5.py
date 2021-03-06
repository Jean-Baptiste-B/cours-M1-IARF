    #!/usr/bin/env python
# -*- coding: utf-8 -*-
# prerequis : librairie pylab installée (regroupe scypy, matplotlib, numpy et ipython)
# codage de la méthode de classification par loi normale

from pylab import *
from turtle import * 

import random

#attend l'appuie d'une touche
def attente_touche():
	raw_input()


def affichage_lois_normales(liste_donnees_classes,liste_parametres_classes):
	assert type(liste_donnees_classes) is list
	assert type(liste_parametres_classes) is list
	assert len(liste_donnees_classes)==len(liste_parametres_classes)

# affichage_lois_normales affiche les données si elles sont de dimension 2 
#
# Entrée :
# - liste_donnees_classe : liste de classes (classe = listes de points (1 point = 1 vecteur de dimension 2)):
# - liste_parametres : liste des paramètres
#     element1 : centroïde (au format "array")
#     element2 : matrice de variance-covariance (au format "array")
	
	nb_classes = len(liste_donnees_classes)
	couleurs= [ 'b', 'g', 'r', 'c', 'm', 'y', 'k' ]
	formespoints = [ 'x', 'o', 'v', '^', '<', '>', '1', '2', '3', '4', 's', 'p', '*', 'h', 'H', '+', '.', 'D', 'd', ',' ]
	formescentres = ['D','D','D']
	
	hold(True)
	for classe in range(nb_classes):
		# Affichage des points de la classe 
		forme=formespoints[classe]
		couleur=couleurs[classe%len(couleurs)]
		stylepoint=forme+couleur
		for point in liste_donnees_classes[classe]:
			plot(point[0],point[1],stylepoint)
			
			
			
		# Affichage des centroïdes
		forme='D'
		stylecentre=forme+couleur
		vecteur_moyenne = liste_parametres_classes[classe][0]
		plot(vecteur_moyenne[0],vecteur_moyenne[1],stylecentre)


        show()

	
def apprentissage_loi_normale(liste_donnees_classe):
    assert type(liste_donnees_classe) is list
	# apprentissage_loi_normale renvoie la liste des paramètres de la loi
	# normale correspondant aux données récupérées
	#
	# Entrée :
	# - liste_donnees_classe : liste de points (1 point = 1 vecteur de dimension 2) d'une classe
	# Sortie :
	# - liste_parametres : liste des paramètres
	#     element1 : centroïde (au format "array")
	#     element2 : matrice de covariance (au format "array")
	

    tab_donnees=array(liste_donnees_classe)

	# calcul du vecteur moyenne
	#   utilisez la fonction mean() directement sur tab_donnees
	# ... a faire
    #on applique la moyenne sur l'axe 0 pour obtenir le vecteur moyenne de chaque coordonnée

    
    vect_moyenne=mean(liste_donnees_classe,0)

    #print("moyenne= " +str(vect_moyenne))
	# calcul de la patrice de covariance
	#   utilisez la fonction cov() directement sur tab_donnees, en utilisant transpose() si nécessaire
	#   cov calcule la matrice de covariance si l'on présente les données 
	# ... a faire


    mat_covariance = cov(tab_donnees.transpose())
    
    return [vect_moyenne, mat_covariance]

def calcul_vraisemblance_loi_normale(donnee,liste_parametres):
    assert type(donnee) is list
    assert type(liste_parametres) is list

    # calcul de la log vraisemblance
    #  (attention, restez sur le type array, si vous utilisez matrix vous ne pourrez pas transposer un vecteur)
    #   fonctions à utiliser :
    #       - dot(A,B) (produit matriciel de A par B)
    #       - inv(A)   (matrice inverse de A)
    #       - argmax : renvoi le numero de l'élément le plus grand
    #       - transpose(A) : transposee de A (qu'il soit un vecteur ou une matrice)
    # ... a faire
    score=[]
    for i in range(len(liste_parametres)) :
        #on recupère la moyenne de la classe i
        vect_moyenne = array(liste_parametres[i][0])

        #on recupère la matrice de covariance de la classe i
        mat_covariance = array(liste_parametres[i][1])

        #on recupère x sous forme d'array        
        x = array(donnee)   

        #on stocke le vecteur x-mu dans v_diff_mean
        v_diff_mean = x -  vect_moyenne 
        
        #on stocke l'inverse de la matrice de covariance dans inv_cov 
        inv_cov = inv(mat_covariance)   
        
        #on effectue le produit entre inv_cov et v_diff_mean
        
        prod=dot(inv_cov,v_diff_mean)

        #puis le produit de v_diff mean par le resultat trouvé
        
        prod2=dot(v_diff_mean,prod)
        
        #on ajoute log(det(cov)) au resultat pour obtenir le score
        res =  log(det(mat_covariance)) + prod2 

        #on ajoute le resultat à la liste des scores
        score.append(res)
    #on prend le argmin de la liste pour obtenir la bonne classe associé
    c=argmin(score)
    return [c,score] 

def calcul_vraisemblance_loi_normale_apriori(donnee,liste_parametres,probaclasses):
    assert type(donnee) is list
    assert type(liste_parametres) is list

    # fonction similaire à calcul_vraisemblance_loi_normale mais avec comme parametre supplémentaires
    #la liste des probabilités de chacune des classes

    score=[]
    for i in range(len(liste_parametres)) :
        #on recupère la moyenne de la classe i
        vect_moyenne = array(liste_parametres[i][0])

        #on recupère la matrice de covariance de la classe i
        mat_covariance = array(liste_parametres[i][1])

        #on recupère x sous forme d'array        
        x = array(donnee)   

        #on stocke le vecteur x-mu dans v_diff_mean
        v_diff_mean = x -  vect_moyenne 
        
        #on stocke l'inverse de la matrice de covariance dans inv_cov 
        inv_cov = inv(mat_covariance)   
        
        #on effectue le produit entre inv_cov et v_diff_mean
        
        prod=dot(inv_cov,v_diff_mean)

        #puis le produit de v_diff mean par le resultat trouvé
        
        prod2=dot(v_diff_mean,prod)
        
        #on ajoute log(det(cov)) au resultat
        res =  log(det(mat_covariance)) + prod2 

        #on enlève 2*log de la proba pour obtenir le score final
        res = res - (2*log(probaclasses[i]))
        
        
        score.append(res)
    c=argmin(score)
    return [c,score] 

def genere_donnee():
    #fonction servant à generer les donnees pour verifier la generalisation
    #on se met en dimension 3 avec 4 classes
    X1=[]    
    X2=[]
    X3=[]
    X4=[]
    
    #la fonction normal du module numpy.random sert à générerune liste de valeurs
    #suivant une loi normal
    d11=normal(0.,2.,100.)
    d12=normal(0.,2.,100.)
    d13=normal(0.,2.,100.)

    d21=normal(3.,2.,100.)
    d22=normal(3.,2.,100.)
    d23=normal(3.,2.,100.)
    
    d31=normal(0.,2.,100.)
    d32=normal(0.,2.,100.)
    d33=normal(3.,2.,100.)
    
    d41=normal(0.,2.,100.)
    d42=normal(3.,2.,100.)
    d43=normal(0.,2.,100.)




    for i in range(len(d1)):
        X1.append([d11[i],d12[i],d13[i]])
        X2.append([d21[i],d22[i],d23[i]])
        X3.append([d31[i],d32[i],d33[i]])
        X4.append([d41[i],d42[i],d43[i]])



    return (X1,X2,X3,X4)

def apprentissage_loi_normale_optimise(liste_donnees_classe):
    assert type(liste_donnees_classe) is list
        # fonction similaire à apprentissage_loi_normale mais en supposant que la matrice de
        #variance-covariance est diagonale

    tab_donnees=array(liste_donnees_classe)

        # calcul du vecteur moyenne
        #   utilisez la fonction mean() directement sur tab_donnees
        # ... a faire
    #on applique la moyenne sur l'axe 0 pour obtenir le vecteur moyenne de chaque coordonnée


    vect_moyenne=mean(liste_donnees_classe,0)


        # calcul du vecteur des variances à l'aide de la fonction var sur l'axe 0


    vect_variances = var(tab_donnees,0)

    return [vect_moyenne, vect_variances]

def calcul_vraisemblance_loi_normale_optimise(donnee,liste_parametres):
    assert type(donnee) is list
    assert type(liste_parametres) is list

    # fonction similaire à calcul_vraisemblance_loi_normale mais en supposant que la matrice de
    #variance-covariance est diagonale
    score=[]
    for i in range(len(liste_parametres)) :
        #on recupère la moyenne de la classe i
        vect_moyenne = array(liste_parametres[i][0])

        #on recupère le vecteur des covariances de la classe i
        vect_variances = array(liste_parametres[i][1])


        #on recupère x sous forme d'array
        x = array(donnee)

        #on stocke le vecteur x-mu dans v_diff_mean
        v_diff_mean = x -  vect_moyenne

        #on calcule log(det(vect_variances)), ie on multiplie tous ses membres et on prend le log

        prod=1.
        for j in range(len(vect_variances)):
            prod=prod*vect_variances[j]


        prod=log(prod)

        #on calcule la somme des (x-mu)²/var et on la stocke dans somme

        somme=0.

        for j in range(len(v_diff_mean)):
            somme=somme+pow(v_diff_mean[j],2)/vect_variances[j]


        #on ajoute log(det(cov)) au resultat pour obtenir le score
        res =  prod + somme



        score.append(res)
    c=argmin(score)
    return [c,score]




