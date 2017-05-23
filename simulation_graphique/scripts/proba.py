#coding: utf8

##	@package proba
#	Script Python permettant d'effectuer une série de tirage sur des événements et affiche des statistiques sur ces événements.

from __future__ import division
import random
from math import factorial, exp

##	Classe représentant un événement.
class Evenement:

	##	Constructeur d'un événement.
	#	@param self : L'objet.
	#	@param probabilite : La probabilitede l'événement.
	def __init__(self, nom, probabilite):
		self.nom = nom		#Le nom de l'événement
		self.probabilite = probabilite		#La probabilité qu'a l'evt de se réaliser
		self.compteur = 0		#Le nombre de fois que l'événement s'est réalisé
		self.pourcentage_realisation = 0

	##	Renvoie l'événement sous forme d'une chaine de caractère.
	#	@return Renvoie l'événement sous forme d'une chaine de caractère.
	def __str__(self):
		return "Nom de l'événement : "+self.nom+".\nProbabilité de l'événement : "+str(self.probabilite)+".\nNombre de réalisation de l'événement : "+str(self.compteur)+"\nTaux de réalisation de l'événement : "+str(self.pourcentage_realisation)+"\n\n"


##	Effectue une serie de k tirages sur un tableau d'événement.
#	@param k : Le nombre de tirage à effectuer.
#	@param evenements : Les évenemts dont dépendent les tirages.
def effectuer_tirages(k, evenements):
	i = 0
	#On effectue k tirages
	for i in range(k):
		tirage = random.uniform(0, 1)
		print "Variable aléatoire : ", tirage
		somme_proba = 0
		j = 0

		#Tant que la somme des proba est inférieure à la proba du tirage
		while somme_proba < tirage:
			somme_proba += evenements[j].probabilite
			j += 1
		evenements[j-1].compteur += 1

	#Affichage des résultas
	for evt in evenements:
		evt.pourcentage_realisation = (evt.compteur / nombre_tirage)
		print str(evt)

##	Génére n événement un renvoie un tableau contenant ces événement.
#	@param n : Le nombre d'évenement à génerer.
def generer_evenements(n):
	evenements = [0] * n
	reste_proba = 1
	for i in range(n):
		nom = "P"+str(i+1)
		if i == n - 1:
			evenements[i] = Evenement(nom, reste_proba)
		else:
			proba = random.uniform(0, reste_proba)
			reste_proba = reste_proba - proba
			evenements[i] = Evenement(nom, proba)
	return evenements

##	Effectue une loi de poisson en fonction des paramètres lamb (Lambda) et k.
#	@param lamb : Le paramètre lambda de la loi de poisson.
#	@param k : Le paramètre k de la loi de poisson.
def loi_de_poisson(lamb, k):
	nb_occurence = ( lamb**k / factorial(k) )*exp(-lamb)
	print "La probabilite qu'un événement avec une moyenne de réalisation de "+str(lamb)+" se déroule "+str(k)+" fois est de "+str(nb_occurence)


###############################################################################
# # # # # # # # # # # # # # # #		M A I N 	# # # # # # # # # # # # # # # #
###############################################################################

# Mon ensemble d'événement
p1 = Evenement("P1", 0.35)
p2 = Evenement("P2", 0.25)
p3 = Evenement("P2", 0.1)
p4 = Evenement("P2", 0.3)

nombre_tirage = input("Combien de tirage voulez-vous ?\n")

if nombre_tirage == 0:
	print "0 tirage ? Très bien c'est fini alors ! ^^"
elif nombre_tirage < 0:
	print "Moins de zero tirage ? C'est bizarre ça..."
else:		#Tout va bien
	n = input("Combien d'événement voulez-vous ?\n")
	evts = generer_evenements(n)
	effectuer_tirages(nombre_tirage, evts)
	moyenne = evts[0].compteur/nombre_tirage
	loi_de_poisson(moyenne, 2)
