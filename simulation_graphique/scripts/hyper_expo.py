#coding: utf8

##	@package hyper_expo
#	Script Python simulant le comportement de l'hyper exponentielle.

from math import exp
import random

PROBABILITE_BURST = 0.01
NOMBRE_MESSAGE_BURST = 140
LAMBDA = 1
TAILLE_TABLEAU = 10
global TABLEAU_POISSON


##	Effectue un tirage et renvoie True ou False si la variable tirée est contenu dans la probabilité passée en paramètre.
#	@param La probabilité selon laquel le tirage à tiré un événement ou non.
#	@return True si le tirage est inférieur ou égal à la probabilité, False sinon.
def effectuer_tirage(probabilite):
	tirage = random.uniform(0, 1)
	print "Tirage : " ,tirage
	return tirage <= probabilite

##	Réalise le tirage selon l'hyper exponentielle.
def hyper_expo():
	if effectuer_tirage(PROBABILITE_BURST) == True:		#Le tirage est tombé sur la faible proba
		print "Burst !\nOn envoie : ", NOMBRE_MESSAGE_BURST, " messages."
	else:
		u = random.uniform(0, 1)
		print "Resultat loi de poisson via l'algo naif : ", loi_de_poisson_naif(u)
		print "Resultat loi de poisson via l'algo optimisé : ", loi_de_poisson_opti(u)

##	Calcule le nombre de message Best Effort transmis par un noeud selon l'algorithme naif de la loi de poisson.
#	@param u : Le paramètre u de la loi de poisson.
def loi_de_poisson_naif(u):
	p = exp (- LAMBDA)
	x = 0
	f = p
	while (u > f):
		x += 1
		p = p*LAMBDA/x
		f += p
	return x

##	Calcule le nombre de message Best Effort transmis par un noeud selon l'algorithme optimisé de la loi de poisson.
#	@param u : Le paramètre u de la loi de poisson.
def loi_de_poisson_opti(u):
	""" Initialisation des variables """
	initialiser_tableau()

	maxi = TAILLE_TABLEAU
	maxF = TABLEAU_POISSON[ TAILLE_TABLEAU -1]
	maxP = maxF

	f = TABLEAU_POISSON

	if u <= maxF:		#On peut trouver la valeur à l'aide du tableau
		x = 0
		while u > f[x]:
			x += 1
	else:
		x = maxi
		f = maxF
		p = maxP

		while u > f:
			x += 1
			p = p*LAMBDA/x
			f = f + p
	return x

##	Initialise le tableau avec les résultats de le loi de poisson.
#	Cette fonction est utilisé dans le cadre de l'algorithme optimisé.
def initialiser_tableau():
	global TABLEAU_POISSON

	TABLEAU_POISSON = [0] * TAILLE_TABLEAU

	TABLEAU_POISSON[0] = exp(-LAMBDA)
	p = TABLEAU_POISSON[0]

	for i in range(1, TAILLE_TABLEAU):
		p = p*LAMBDA/i
		TABLEAU_POISSON[i] = TABLEAU_POISSON[i-1]+p


##	Affiche un tableau sous la forme :
#		Indice :
#		Valeur :
def afficher_tableau():
	for i in range(TAILLE_TABLEAU):
		print "Indice : ", i
		print "valeur : ", TABLEAU_POISSON[i], "\n"


#####################     M A I N     #######################

hyper_expo()
