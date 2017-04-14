#coding: utf8

from Tkinter import *
from math import cos, sin, pi
import thread
import time

# # # # # # # # # # # # # # # #		C O N S T A N T E	 # # # # # # # # # # # # # # # #

COTE_CANVAS = 600	#Définit la hauteur/largeur de la toile sur laquelle seront déssinés les slots et les noeuds

NOMBRE_SLOT = 15	#Le nombre de slot du système
COTE_SLOT = 15		#La hauteur/largeur d'un slot
DISTANCE_SLOT = COTE_CANVAS/3	#La distance d'un slot par rapport à l'axe central du canvas

NOMBRE_NOEUD = 3	#Le nombre de noeud du système
COTE_NOEUD = COTE_SLOT + 5		#La hauteur/largeur d'un noeud
DISTANCE_NOEUD = DISTANCE_SLOT + 50		#La distance d'un noeud par rapport à l'axe central du canvas
COULEUR_NOEUD = "CadetBlue3"	#La couleur graphique d'un noeud

VITESSE_MESSAGE = 0.011		#La vitesse de déplacement des messages

global controleur
controleur = None

# # # # # # # # # # # # # # # #		V U E	# # # # # # # # # # # # # # # #
def callback(event):
	thread.start_new_thread(placer_message, (controleur, 0) )


def creer_fenetre():
	# On crée une fenêtre, racine de notre interface
	fenetre = Tk()
	fenetre.title("Jason Statham")
	
	return fenetre

def creer_canvas(fenetre):
	canvas = Canvas(fenetre, width=COTE_CANVAS, height=COTE_CANVAS, background='AntiqueWhite3')
	ligne1 = canvas.create_line(COTE_CANVAS/2, 0, COTE_CANVAS/2, COTE_CANVAS)
	ligne2 = canvas.create_line(0, COTE_CANVAS/2, COTE_CANVAS, COTE_CANVAS/2)
	
	#Ajout d'un click listernet pour les tests
	canvas.bind("<Button-1>", callback)
	
	return canvas

"""
	Place sur la toile les slots et renvoie un tableau contenant :
	En indice 0 les slots du modele
	En indice 1 les slots de la vue
"""
def placer_slots(fenetre, canvas):
	slots_vue = [None] * NOMBRE_SLOT	#Tableau qui contiendra les rectangles représentant les slots du modèle
	slots_modele = [0] * NOMBRE_SLOT
	
	#Le point du milieu
	milieu_x = COTE_CANVAS/2
	milieu_y = COTE_CANVAS/2
	
	for i in range(1, NOMBRE_SLOT+1):
		nouveau_x = milieu_x + cos(2*i*pi/NOMBRE_SLOT) * DISTANCE_SLOT
		nouveau_y = milieu_y - sin(2*i*pi/NOMBRE_SLOT) * DISTANCE_SLOT
		
		slots_vue[i-1] = canvas.create_rectangle(nouveau_x - COTE_SLOT, nouveau_y - COTE_SLOT, nouveau_x + COTE_SLOT, nouveau_y + COTE_SLOT)
		texte = canvas.create_text(nouveau_x, nouveau_y, text="S "+str(slots_vue[i-1]))
	canvas.pack()
	return slots_modele, slots_vue


"""
	Place sur la toile les noeuds et renvoie un tableau contenant :
	En indice 0 les noeuds du modele
	En indice 1 les noeuds de la vue
"""
def placer_noeuds(fenetre, canvas):
	noeuds_vue = [None] * NOMBRE_NOEUD
	noeuds_modele = [None] * NOMBRE_NOEUD
	
	milieu_x = COTE_CANVAS/2
	milieu_y = COTE_CANVAS/2
	
	pas = NOMBRE_SLOT // NOMBRE_NOEUD
	
	for j in range(NOMBRE_NOEUD):
		#Le rectangle
		x = milieu_x + cos(2*j*pas*pi/NOMBRE_SLOT) * DISTANCE_NOEUD
		y = milieu_y - sin(2*j*pas*pi/NOMBRE_SLOT) * DISTANCE_NOEUD
		noeuds_vue[j] = canvas.create_rectangle(x - COTE_NOEUD, y - COTE_NOEUD, x + COTE_NOEUD, y + COTE_NOEUD, fill=COULEUR_NOEUD)
		indice_slot_accessible = j*pas - 1
		noeuds_modele[j] = Noeud(indice_slot_accessible)
		
		#le texte du rectangle
		texte = canvas.create_text(x, y, text="N "+str(noeuds_vue[j]))
	canvas.pack()
	return noeuds_modele, noeuds_vue
			
	
def placer_message_graphique(canvas, noeud_depart, slot_arrive):
	
	coordonnees = canvas.coords(noeud_depart)
	
	depart_x = (coordonnees[0] + coordonnees[2])/2
	depart_y = (coordonnees[1] + coordonnees[3])/2
	
	coordonnees = canvas.coords(slot_arrive)
	
	arrivee_x = (coordonnees[0] + coordonnees[2])/2
	arrivee_y = (coordonnees[1] + coordonnees[3])/2
	
	#Le point est placé
	message = canvas.create_rectangle(depart_x-2, depart_y-2, depart_x+2, depart_y+2, fill="deeppink")
	canvas.pack()
	
	deplacer_vers(canvas, message, arrivee_x, arrivee_y)


""" Déplace dans le canvas un objet vers un point d'arrivé définit par arrivee_x et arrivee_y """
def deplacer_vers(canvas, objet, arrivee_x, arrivee_y):
	objet_x = canvas.coords(objet)[0]
	objet_y = canvas.coords(objet)[1]
	
	while objet_x != arrivee_x and objet_y != arrivee_y:
		if objet_x < arrivee_x:
			canvas.move(objet, 1, 0)
		elif objet_x > arrivee_x:
			canvas.move(objet, -1, 0)
		if objet_y < arrivee_y:
			canvas.move(objet, 0, 1)
		elif objet_y > arrivee_y:
			canvas.move(objet, 0, -1)
		canvas.pack()
			
		objet_x = canvas.coords(objet)[0]
		objet_y = canvas.coords(objet)[1]
		canvas.pack()
		time.sleep(VITESSE_MESSAGE)

# # # # # # # # # # # # # # # #		M O D E L E		# # # # # # # # # # # # # # # #

""" Représente un noeud dans le système, un noeuds peux stocker des messages """
class Noeud:
	def __init__(self, indice_slot_accessible):
		self.nb_message = 0
		self.indice_slot_accessible = indice_slot_accessible


# # # # # # # # # # # # # # # #		C O N T R O L E U R		# # # # # # # # # # # # # # # #

"""
	Classe représentant le système que l'on souhaite modéliser dans sa globalité 
	Elle fera l'intermédiaire entre le modèle et la vue
"""
class Controleur:
	def __init__(self, fenetre, canvas, slots_vue, slots_modele, noeuds_vue, noeuds_modele):
		self.fenetre = fenetre
		self.canvas = canvas
		self.slots_vue = slots_vue		#La représentation des slots dans le canvas (un tableau de rectangle)
		self.slots_modele = slots_modele		#Un tableau représentant les slots, chaque case dispose de deux etats si elle dispose ou non d'un message
		self.noeuds_vue = noeuds_vue		#La représentation des noeuds dans le canvas
		self.noeuds_modele = noeuds_modele	#Un tableau de Noeud
		

def placer_message(controleur, indice_noeud):
	noeud_modele = controleur.noeuds_modele[ indice_noeud ]
	slot_modele = controleur.noeuds_modele[ indice_noeud ].indice_slot_accessible
	erreur = False
	if slot_modele == 1:
		erreur = True
		message = "Le slot est déjà remplis, "
	if noeud_modele == 0:
		erreur = True
		message += "Le  est déjà remplis"
	if not erreur:
		#Partie graphique
		canvas = controleur.canvas
		noeud_graphique = controleur.noeuds_vue[ indice_noeud ]
		indice_slot = controleur.noeuds_modele[ indice_noeud ].indice_slot_accessible
		slot_graphique = controleur.slots_vue[indice_slot]
		
		placer_message_graphique(canvas, noeud_graphique, slot_graphique)
		
		noeud_vue = controleur.noeuds_vue[ indice_noeud ]
		slot_vue = controleur.slots_vue[indice_slot]
	else:
		print message

###############################################################################
# # # # # # # # # # # # # # # #		M A I N 	# # # # # # # # # # # # # # # #
###############################################################################

fenetre = creer_fenetre()
canvas = creer_canvas(fenetre)

slots = placer_slots(fenetre, canvas)
slots_modele = slots[0]
slots_vue = slots[1]

noeuds = placer_noeuds(fenetre, canvas)

noeuds_modele = noeuds[0]
noeuds_vue = noeuds[1]

controleur = Controleur(fenetre, canvas, slots_vue, slots_modele, noeuds_vue, noeuds_modele)

""" Affichage des noeuds et de leurs slots respectifs """
couleurs = ["", "", ""]
for i in range( len( noeuds_modele ) ):
	indice = controleur.noeuds_modele[i].indice_slot_accessible
	noeud_vue = controleur.noeuds_vue[i]
	slot_vue = controleur.slots_vue[indice]
	print "Le noeud numéro : ", noeud_vue, " a accès au slot : ", slot_vue

# On démarre la boucle Tkinter qui s'interompt quand on ferme la fenêtre
fenetre.mainloop()
