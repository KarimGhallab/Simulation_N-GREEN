#coding: utf8

##	@package simulation_v2
#	Ce script permet de réaliser une simulation d'un anneau en réseau dans le cadre du projet N-GREEN.

from __future__ import print_function

import tkMessageBox, tkFileDialog, time, random, sys, os, csv

from Tkinter import Tk, Canvas, Button, Label, Entry, PhotoImage
from math import cos, sin, pi, exp
from threading import Thread
from PIL import Image, ImageTk
from collections import deque
# # # # # # # # # # # # # # # #		C O N S T A N T E	 # # # # # # # # # # # # # # # #

IMAGES = []
COULEURS_MESSAGE = []
COULEURS_MESSAGE.append( ["yellowgreen", "#b8dc6f", "#7ba428"] )
COULEURS_MESSAGE.append( ["orange", "#ffc14d", "#cc8500"] )
COULEURS_MESSAGE.append( ["turquoise", "#7beadf", "#20c5b5"] )
COULEURS_MESSAGE.append( ["royalblue", "#7b97ea", "#1f49c7"] )
COULEURS_MESSAGE.append( ["purple", "#cc00cc", "#660066"] )
COULEURS_MESSAGE.append( ["teal", "#00b3b3", "#006666"] )
COULEURS_MESSAGE.append( ["tan", "#e2cfb6", "#bf935a" ] )
COULEURS_MESSAGE.append( ["snow", "#ffffff", "#ffb3b3"] )
COULEURS_MESSAGE.append( ["mediumseagreen", "#33ffb1", "#00b36e"] )
COULEURS_MESSAGE.append( ["LightCoral", "#f7bbbb", "#ea4848"] )
COULEURS_MESSAGE.append( ["Chartreuse", "#a6ff4d", "#66cc00"] )
COULEURS_MESSAGE.append( ["CornflowerBlue", "#a4c0f4", "#3271e7"] )
COULEURS_MESSAGE.append( ["DarkGray", "#cccccc", "#8c8c8c"] )
COULEURS_MESSAGE.append( ["DarkOliveGreen", "#7fa046", "#38471f"] )
COULEURS_MESSAGE.append( ["DarkMagenta", "#cc00cc", "#660066"] )
COULEURS_MESSAGE.append( ["Lavender", "#eaeafb", "#aaaaee"] )
COULEURS_MESSAGE.append( ["SandyBrown", "#f8c9a0", "#f08628"] )
COULEURS_MESSAGE.append( ["Black", "#666666", "#262626"] )

COTE_SLOT = 7		#La hauteur/largeur d'un slot
COTE_NOEUD = COTE_SLOT + 20		#La hauteur/largeur d'un noeud

global VITESSE_LATENCE_MESSAGE
VITESSE_LATENCE_MESSAGE = 0.002		#Le temps d'attente en seconde entre chaque déplacement de message dans la canvas
COTE_MESSAGE = 5

NOMBRE_LIGNE_CANVAS = 50
NOMBRE_COLONNE_CANVAS = 3

CLE_ENTRY_SLOT = 1					#La clé de l'entry du slot pour le dictionnaire des entrys.
CLE_ENTRY_NOEUD = 2					#La clé de l'entry du noeud pour le dictionnaire des entrys.
CLE_ENTRY_LAMBDA = 3				#La clé de l'entry du lambda pour le dictionnaire des entrys.
CLE_ENTRY_LAMBDA_BURST = 4			#La clé de l'entry du lambda burst pour le dictionnaire des entrys.
CLE_ENTRY_LIMITE_MESSAGE = 5		#La clé de l'entry de la limite minimal du nombre de message.
CLE_ENTRY_NB_ANTENNE = 6			#La clé de l'entry du nombre d'antenne par noeud.
CLE_ENTRY_TAILLE_MESSAGE_BE = 7		#La clé de l'entry de la taille d'un message best effort.
CLE_ENTRY_NB_MESSAGE_REQUETE = 8	#La clé de l'entry du nombre de message par requete C-RAN.
CLE_ENTRY_PERIODE_REQUETE = 9		#La clé de l'entry indiquant la période de reception des requêtes.
CLE_ENTRY_NB_CARTE = 10				#La clé de l'entry indiquant le nombre de carte par noeud.

TIC = 600	#Temps d'attente entre chaque mouvement de l'anneau, envoi de message etc

global tache
tache = None

global LABEL_TIC
LABEL_TIC = None

global LABEL_HORLOGE
LABEL_HORLOGE = None

global LABEL_CHARGE
LABEL_CHARGE = None

global TEXTS_NOEUDS
TEXTS_NOEUDS = None

global DICT_TEXTES_NOEUDS
DICT_TEXTES_NOEUDS = {}

global PERIODE_MESSAGE_ANTENNE
PERIODE_MESSAGE_ANTENNE = 1000

global NB_ANTENNE
NB_ANTENNE = 10

global NB_CARTE
NB_CARTE = 2

global TAILLE_MESSAGE_BE
TAILLE_MESSAGE_BE = 5

global NB_MESSAGE_CRAN
NB_MESSAGE_CRAN = 500

""" Les variables pour l'hyper exponentielle """
PROBABILITE_BURST = 0.05
global LAMBDA_PETIT
LAMBDA_PETIT = 7

global LAMBDA_GRAND
LAMBDA_GRAND = 27

LIMITE_NOMBRE_MESSAGE_MAX = 1000

global LIMITE_NOMBRE_MESSAGE_MIN
LIMITE_NOMBRE_MESSAGE_MIN = LIMITE_NOMBRE_MESSAGE_MAX * 0.7

TAILLE_TABLEAU = 1000
global TABLEAU_POISSON

global TAILLE_UTILISEE_TABLEAU_POISSON

INDICE_DATA_CENTER = 0

POLITIQUE_SANS_PRIORITE = 0
POLITIQUE_PRIORITAIRE = 1
POLITIQUE_PRIORITE_ABSOLUE = 2

STATHAM_MODE = False
# # # # # # # # # # # # # # # #		V U E	# # # # # # # # # # # # # # # #

##	Représente graphiquement un paquet de message se déplaçant dans l'anneau.
class PaquetMessageGraphique:

	##	Constructeur
	#	@param self : L'objet en train d'être construit.
	#	@param depart_x : la coordonée x ou placer le paquet.
	#	@param depart_y : la coordonée y ou placer le paquet.
	#	@param couleur1 : la couleur des messages prioritaires.
	#	@param couleur2 : la couleur des messages best effort.
	#	@param proportion_message_prioritaire : la proportion des messages prioritaires dans le paquet.
	def __init__(self, depart_x, depart_y, couleur1, couleur2, proportion_message_prioritaire):
		self.couleur1 = couleur1
		self.couleur2 = couleur2
		self.proportion_message_prioritaire = proportion_message_prioritaire

		self.conteneur = controleur.canvas.create_rectangle(depart_x-COTE_MESSAGE, depart_y-COTE_MESSAGE, depart_x+COTE_MESSAGE, depart_y+COTE_MESSAGE)
		self.sous_rectangle1 = controleur.canvas.create_rectangle(depart_x-COTE_MESSAGE, depart_y-COTE_MESSAGE, (depart_x - COTE_MESSAGE) + ((2 * COTE_MESSAGE) * proportion_message_prioritaire), depart_y+COTE_MESSAGE, fill=couleur1)
		self.sous_rectangle2 = controleur.canvas.create_rectangle((depart_x - COTE_MESSAGE) + ((2 * COTE_MESSAGE) * proportion_message_prioritaire), depart_y-COTE_MESSAGE, depart_x+COTE_MESSAGE, depart_y+COTE_MESSAGE, fill=couleur2)


	##	Methode permettant de bouger un paquet de message
	#	@param self : Le paquet à bouger.
	#	@param ajout_x : la valeur de x à ajouter au paquet.
	#	@param ajout_y : la valeur de y à ajouter au paquet.
	def move_paquet(self, ajout_x, ajout_y):
		controleur.canvas.move(self.conteneur, ajout_x, ajout_y)
		controleur.canvas.move(self.sous_rectangle1, ajout_x, ajout_y)
		controleur.canvas.move(self.sous_rectangle2, ajout_x, ajout_y)

	##	Methode permettant de téléporter un paquet de message.
	#	@param self : Le paquet à téléporter.
	#	@param ajout_x : Le x d'arrivée.
	#	@param ajout_y : Le y d'arrivée.
	def teleporter_paquet(self, destination_x, destination_y):
		deplacement_x = (destination_x - controleur.canvas.coords(self.conteneur)[0]) - COTE_MESSAGE
		deplacement_y = (destination_y - controleur.canvas.coords(self.conteneur)[1]) - COTE_MESSAGE
		controleur.canvas.move(self.conteneur, deplacement_x, deplacement_y)
		controleur.canvas.move(self.sous_rectangle1, deplacement_x, deplacement_y)
		controleur.canvas.move(self.sous_rectangle2, deplacement_x, deplacement_y)




##	Créer une fenêtre Tkinter avec son titre.
#	@return La fenêtre Tkinter créée.
def creer_fenetre():
	fenetre = Tk()
	if STATHAM_MODE:
		titre = "Jason Statham : <3"
	else:
		titre = "Simulation réseau en anneau N-GREEN"
	fenetre.title(titre)

	return fenetre

##	Créer un canvas avec une croix au centre et le place dans la fenêtre.
#	@param fenetre : La fenêtre Tkinter ou le canvas sera ajouté.
#	@return Le canvas créé.
def creer_canvas(fenetre):
	canvas = Canvas(fenetre, width=LARGEUR_CANVAS, height=HAUTEUR_CANVAS, background='#ffffff')
	canvas.grid(row=0, column=1, rowspan=NOMBRE_LIGNE_CANVAS, columnspan=NOMBRE_COLONNE_CANVAS)

	return canvas

##	Met à jour les labels en haut à gauche du canvas affichant le TIC actuel de la simulation et la charge du réseau.
#	param tic_actuel : le TIC actuel de la simulation en cours.
def update_labels_globaux(tic_actuel):
	global LABEL_HORLOGE
	global LABEL_CHARGE

	""" Met à jour le TIC actuel """
	if LABEL_HORLOGE != None:
		controleur.canvas.delete(LABEL_HORLOGE)
	LABEL_HORLOGE = controleur.canvas.create_text(50, 10, text = "TIC actuel : "+str(tic_actuel)+".")

	""" Met à jour le label de la charge du réseau """
	slots_pris = 0
	for i in range(0, controleur.nb_slot_anneau):
		if controleur.slots_modele[i].paquet_message != None:
			slots_pris += 1
	charge = (slots_pris/float(controleur.nb_slot_anneau)) * 100

	if LABEL_CHARGE != None:
		controleur.canvas.delete(LABEL_CHARGE)
	LABEL_CHARGE = controleur.canvas.create_text(75, 30, text = "Charge actuelle : "+str(charge)+"%.")

##	Place sur le canvas donné en paramètre les slots et renvoie un tableau contenant :
#	En indice 0 les slots du modèle.
#	En indice 1 les slots de la vue.
#	@param fenetre : La fenêtre sur laquelle se situe le canvas passé en paramètre.
#	@param canvas : Le canvas sur lequel on place les slots graphiques.
#	@param nb_slot : Le nombre de slot à placer.
#	@return En indice 0 les slots du modèle, en indice 1 les slots de la vue.
def placer_slots(fenetre, canvas, nb_slot):
	slots_vue = [None] * nb_slot	#Tableau qui contiendra les rectangles représentant les slots du modèle
	slots_modele = [ None ] * nb_slot

	#Le point du milieu
	milieu_x = LARGEUR_CANVAS/2
	milieu_y = HAUTEUR_CANVAS/2
	for i in range(1, nb_slot+1):
		val_cos = cos(2*i*pi/nb_slot)
		val_sin = sin(2*i*pi/nb_slot)
		nouveau_x = milieu_x + val_cos * DISTANCE_SLOT
		nouveau_y = milieu_y - val_sin * DISTANCE_SLOT

		slots_vue[i-1] = canvas.create_rectangle(nouveau_x - COTE_SLOT, nouveau_y - COTE_SLOT, nouveau_x + COTE_SLOT, nouveau_y + COTE_SLOT)
		slots_modele[i-1] = Slot(i, None, None, val_cos, val_sin)
		canvas.create_text(nouveau_x, nouveau_y)
	return slots_modele, slots_vue


##	Place sur la toile les noeuds et renvoie un tableau contenant :
#	En indice 0 les noeuds du modèle.
#	En indice 1 les noeuds de la vue.
#	En indice 2 les slots du modèle.
#	@param fenetre : La fenêtre sur laquelle se situe le canvas passé en paramètre.
#	@param canvas : Le canvas sur lequel on place les slots graphiques.
#	@param nb_noeud : Le nombre de noeud à placer.
#	@param nb_slot : Le nombre de slot déjà placé.
#	@param slots_modele : Les slots du modèle.
#	@param slots_vue : Les slots de la vue.
#	@return En indice 0 les noeuds du modèle, en indice 1 les noeuds de la vue, en indice 2 les slots du modèle.
def placer_noeuds(fenetre, canvas, nb_noeud, nb_slot, slots_modele, slots_vue, politique):
	global TEXTS_NOEUDS
	global DICT_TEXTES_NOEUDS

	noeuds_vue = [0] * nb_noeud
	noeuds_modele = [None] * nb_noeud
	TEXTS_NOEUDS = []

	pas = nb_slot // nb_noeud

	for j in range(nb_noeud):
		indice_slot_accessible = (( (j*pas) + ((j+1)*pas) ) / 2) - 1
		if j == INDICE_DATA_CENTER:
			noeuds_modele[j] = Noeud(indice_slot_accessible, indice_slot_accessible-1, COULEURS_MESSAGE[j][0], COULEURS_MESSAGE[j][1], COULEURS_MESSAGE[j][2], 0)
		else:
			noeuds_modele[j] = Noeud(indice_slot_accessible, indice_slot_accessible-1, COULEURS_MESSAGE[j][0], COULEURS_MESSAGE[j][1], COULEURS_MESSAGE[j][2], NB_ANTENNE)

		slots_modele[ indice_slot_accessible ].indice_noeud_lecture = j
		slots_modele[ indice_slot_accessible -1 ].indice_noeud_ecriture = j

		""" Modification des couleur des slots """
		couleur = noeuds_modele[j].couleur_noeud
		canvas.itemconfig(slots_vue[indice_slot_accessible], outline=couleur)
		canvas.itemconfig(slots_vue[indice_slot_accessible-1], outline=couleur)

		""" Calcule de la position du noeud """
		milieu_x = LARGEUR_CANVAS/2
		milieu_y = HAUTEUR_CANVAS/2

		""" Calcule de l'abscisse du noeud en fonction de la position du slot """
		x1 = milieu_x + slots_modele [ indice_slot_accessible ].val_cos * DISTANCE_NOEUD
		x2 = milieu_x + slots_modele [ indice_slot_accessible -1 ].val_cos * DISTANCE_NOEUD
		x = (x1 + x2) / 2

		""" Calcule de l'ordonné du noeud en fonction de la position du slot """
		y1 = milieu_y - slots_modele [ indice_slot_accessible ].val_sin * DISTANCE_NOEUD
		y2 = milieu_y - slots_modele [ indice_slot_accessible -1 ].val_sin * DISTANCE_NOEUD
		y = (y1 + y2) / 2

		if j == INDICE_DATA_CENTER:
			noeuds_vue[j] = canvas.create_rectangle( x - COTE_NOEUD, y - COTE_NOEUD, x + COTE_NOEUD, y + COTE_NOEUD, fill=COULEURS_MESSAGE[j][0], dash=(2,4))
		else:
			noeuds_vue[j] = canvas.create_rectangle( x - COTE_NOEUD, y - COTE_NOEUD, x + COTE_NOEUD, y + COTE_NOEUD, fill=COULEURS_MESSAGE[j][0] )
		canvas.tag_bind(noeuds_vue[j], "<Button-1>", callback_click_noeud)

		sous_tab = []
		""" le texte du rectangle """
		if politique == POLITIQUE_PRIORITAIRE or politique == POLITIQUE_PRIORITE_ABSOLUE:
			texte_messages_initaux = canvas.create_text(x-15, y, text="0")
			texte_messages_prioritaires = canvas.create_text(x+15, y, text="0")

			sous_tab.append(texte_messages_initaux)
			sous_tab.append(texte_messages_prioritaires)

			canvas.tag_bind(texte_messages_prioritaires, "<Button-1>", callback_click_texte)
			DICT_TEXTES_NOEUDS[ texte_messages_prioritaires ] = noeuds_modele[j]
		else:
			texte_messages_initaux = canvas.create_text(x, y, text="0")
			sous_tab.append(texte_messages_initaux)

		TEXTS_NOEUDS.append(sous_tab)
		canvas.tag_bind(texte_messages_initaux, "<Button-1>", callback_click_texte)
		DICT_TEXTES_NOEUDS[ texte_messages_initaux ] = noeuds_modele[j]

	return noeuds_modele, noeuds_vue, slots_modele


##	Place un message à un point de départ et le fait se déplacer jusqu'a un point d'arrivé.
#	@param fenetre : La fenêtre sur laquelle se situe le canvas passé en paramètre.
#	@param canvas : Le canvas sur lequel on place le message.
#	@param depart : Les coordonnees de départ du message.
#	@param arrive : Les coordonnees d'arrivées du message.
#	@param couleur_message : La couleur du message.
#	@return L'id du message créé.

def placer_message_graphique(canvas, depart, arrive, couleur_messages_prioritaires, couleur_messages_best_effort, proportion_message_prioritaire):
	coordonnees = canvas.coords(depart)

	depart_x = (coordonnees[0] + coordonnees[2])/2
	depart_y = (coordonnees[1] + coordonnees[3])/2

	coordonnees = canvas.coords(arrive)

	arrivee_x = (coordonnees[0] + coordonnees[2])/2
	arrivee_y = (coordonnees[1] + coordonnees[3])/2

	""" Le point est placé """
	if not STATHAM_MODE:
		#objet = canvas.create_rectangle(depart_x-COTE_MESSAGE, depart_y-COTE_MESSAGE, depart_x+COTE_MESSAGE, depart_y+COTE_MESSAGE, fill=couleur_message)
		objet = PaquetMessageGraphique(depart_x, depart_y, couleur_messages_prioritaires, couleur_messages_best_effort, proportion_message_prioritaire)
	else:
		objet = canvas.create_image(depart_x-COTE_MESSAGE, depart_y-COTE_MESSAGE, image=IMAGE_JASON)
	""" On fait se déplacer le message """
	t = Thread(target=deplacer_vers, args=(canvas, objet, arrivee_x, arrivee_y))
	t.start()

	return objet

##	Place le panel gauche de la fenêtre contenant les boutons :
#	- Start.
#	- Stop.
#	- Restart.
#	- Augmenter vitesse.
#	- Diminuer vitesse.
#	@param fenetre : La fenêtre sur laquelle on place le panel.
def placer_panel_gauche(fenetre):
	play = Image.open("../images/play.png")
	IMAGES.append( ImageTk.PhotoImage(play) )
	bouton_play = Button(fenetre, command = commencer_rotation, image = IMAGES[ len(IMAGES) -1 ], bg="White", activebackground="#E8E8E8")
	bouton_play.grid(row=0)
	label_play = Label(fenetre, text="Commencer/reprendre")
	label_play.grid(row=1)

	stop = Image.open("../images/stop.png")
	IMAGES.append( ImageTk.PhotoImage(stop) )
	bouton_stop = Button(fenetre, command = arreter_rotation, image = IMAGES[ len(IMAGES) -1 ], bg="White", activebackground="#E8E8E8")
	bouton_stop.grid(row=2)
	label_stop = Label(fenetre, text="Arrêter")
	label_stop.grid(row=3)

	replay = Image.open("../images/restart.png")
	IMAGES.append( ImageTk.PhotoImage(replay) )
	bouton_reset = Button(fenetre, text ="Recommencer", command= lambda: reset(), image = IMAGES[ len(IMAGES) -1 ], bg="White", activebackground="#E8E8E8")
	bouton_reset.grid(row=4)
	label_restart = Label(fenetre, text="Recommencer")
	label_restart.grid(row=5)

	replay = Image.open("../images/vitesse_up.png")
	IMAGES.append( ImageTk.PhotoImage(replay) )
	bouton_reset = Button(fenetre, text ="UP", command = augmenter_vitesse, image = IMAGES[ len(IMAGES) -1 ], bg="White", activebackground="#E8E8E8")
	bouton_reset.grid(row=6)
	label_restart = Label(fenetre, text="Modifier vitesse")
	label_restart.grid(row=7)

	vitesse_down = Image.open("../images/vitesse_down.png")
	IMAGES.append( ImageTk.PhotoImage(vitesse_down) )
	bouton_down = Button(fenetre, text ="DOWN", command = diminuer_vitesse, image = IMAGES[ len(IMAGES) -1 ], bg="White", activebackground="#E8E8E8")
	bouton_down.grid(row=8)

	aide = Image.open("../images/help.png")
	IMAGES.append( ImageTk.PhotoImage(aide) )
	bouton_aide = Button(fenetre, text ="Aide ?", command = afficher_aide, image = IMAGES[ len(IMAGES) -1 ])
	bouton_aide.grid(row=NOMBRE_LIGNE_CANVAS + 8, sticky="W")


##	Place le panel droit affichant les informations courantes ainsi des zones de saisie pour :
#	- Le nombre de Slot utilisé.
#	- Le nombre de Noeud présent.
#	- Le lambda actuellement utilisé.
#	- le lambda burst actuellement utilisé.
#	- Et la limite minimal des noeuds pour evoyer un message.
#	Le panel contient aussi un bouton de validation des données.
#	Si aucunes données n'est saisies pour un champs, la valeur de la configuration précèdente est consérvée.
#	@param fenetre : La fenêtre sur laquelle on place le panel gauche.
def placer_panel_droit(fenetre):
	nombre_slot = len( controleur.slots_modele )
	nombre_noeud = len( controleur.noeuds_modele )

	left_padding = 15
	right_padding = 15
	x_padding = (left_padding, right_padding)

	""" Les labels présentant les nombres de slots, de noeuds, le lambda actuel ainsi que le TIC en milliseconde """
	label_slot_actuel = Label(fenetre, text = "Nombre de slot : "+str(nombre_slot) )
	label_noeud_actuel = Label(fenetre, text = "Nombre de noeud : "+str(nombre_noeud) )
	label_lambda_actuel = Label(fenetre, text = "Lambda petit : "+str(LAMBDA_PETIT) )
	label_lambda_burst_actuel = Label(fenetre, text = "Lambda grand : "+str(LAMBDA_GRAND) )
	label_limite_taille_message_min = Label(fenetre, text = "Seul min de message : "+str(LIMITE_NOMBRE_MESSAGE_MIN) )
	label_nb_antenne = Label(fenetre, text = "Nombre d'antennes par noeud : "+str(NB_ANTENNE) )
	label_taille_message_BE = Label(fenetre, text = "Taille d'un message Best effort : "+str(TAILLE_MESSAGE_BE) )
	label_nb_message_requete = Label(fenetre, text = "Nombre de messages d'une requête : "+str(NB_MESSAGE_CRAN) )
	label_periode_requete = Label(fenetre, text = "Période avant l'envoi d'une requête : "+str(PERIODE_MESSAGE_ANTENNE) )
	label_nb_carte = Label(fenetre, text = "Nombre de carte par noeud : "+str(NB_CARTE) )

	""" Les labels des entry pour un nouveau nombre de slot/noeud """
	label_nouveau_slot = Label(fenetre, text = "Nouveau nombre de slot :")
	label_nouveau_noeud = Label(fenetre, text = "Nouveau nombre de noeud :")
	label_nouveau_lambda = Label(fenetre, text = "Nouveau lambda petit :")
	label_nouveau_lambda_burst = Label(fenetre, text = "Nouveau lambda grand :")
	label_nouvelle_limite = Label(fenetre, text = "Nouveau seuil min de message :")
	label_nouveau_nb_antenne = Label(fenetre, text = "Nouveau nombre d'antennes par noeud :")
	label_nouvelle_taille_message_BE = Label(fenetre, text = "Nouvelle taille d'un message Best effort :")
	label_nouveau_nb_message_requete = Label(fenetre, text = "Nouveau nombre de messages d'une requête :")
	label_nouvelle_periode_requete = Label(fenetre, text = "Nouvelle période avant l'envoi d'une requête :")
	label_nouveau_nb_carte = Label(fenetre, text = "Nouveau nombre de carte :")

	""" Les entry """
	entry_slot = Entry(fenetre, width=LONGUEUR_ENTRY)
	entry_noeud = Entry(fenetre, width=LONGUEUR_ENTRY)
	entry_lambda = Entry(fenetre, width=LONGUEUR_ENTRY)
	entry_lambda_burst = Entry(fenetre, width=LONGUEUR_ENTRY)
	entry_limite_message = Entry(fenetre, width=LONGUEUR_ENTRY)
	entry_nb_antenne = Entry(fenetre, width=LONGUEUR_ENTRY)
	entry_taille_message_BE = Entry(fenetre, width=LONGUEUR_ENTRY)
	entry_nb_message_requete = Entry(fenetre, width=LONGUEUR_ENTRY)
	entry_periode_requete = Entry(fenetre, width=LONGUEUR_ENTRY)
	entry_nb_carte = Entry(fenetre, width=LONGUEUR_ENTRY)

	""" Ajout d'un event """
	entry_slot.bind("<Key>", callback_validation_configuration)
	entry_noeud.bind("<Key>", callback_validation_configuration)
	entry_lambda.bind("<Key>", callback_validation_configuration)
	entry_lambda_burst.bind("<Key>", callback_validation_configuration)
	entry_limite_message.bind("<Key>", callback_validation_configuration)
	entry_nb_antenne.bind("<Key>", callback_validation_configuration)
	entry_taille_message_BE.bind("<Key>", callback_validation_configuration)
	entry_nb_message_requete.bind("<Key>", callback_validation_configuration)
	entry_periode_requete.bind("<Key>", callback_validation_configuration)
	entry_nb_carte.bind("<Key>", callback_validation_configuration)

	controleur.entrys[CLE_ENTRY_SLOT] = entry_slot
	controleur.entrys[CLE_ENTRY_NOEUD] = entry_noeud
	controleur.entrys[CLE_ENTRY_LAMBDA] = entry_lambda
	controleur.entrys[CLE_ENTRY_LAMBDA_BURST] = entry_lambda_burst
	controleur.entrys[CLE_ENTRY_LIMITE_MESSAGE] = entry_limite_message
	controleur.entrys[CLE_ENTRY_NB_ANTENNE] = entry_nb_antenne
	controleur.entrys[CLE_ENTRY_TAILLE_MESSAGE_BE] = entry_taille_message_BE
	controleur.entrys[CLE_ENTRY_NB_MESSAGE_REQUETE] = entry_nb_message_requete
	controleur.entrys[CLE_ENTRY_PERIODE_REQUETE] = entry_periode_requete
	controleur.entrys[CLE_ENTRY_NB_CARTE] = entry_nb_carte


	label_slot_actuel.grid(row=0, column=NOMBRE_COLONNE_CANVAS+1, sticky='W', padx=(left_padding, 0))
	label_nouveau_slot.grid(row=1, column=NOMBRE_COLONNE_CANVAS+1, sticky='W', padx=(left_padding, 0))
	entry_slot.grid(row=1, column=NOMBRE_COLONNE_CANVAS+2, sticky="E"+"W", padx=(0, right_padding))

	label_noeud_actuel.grid(row=2, column=NOMBRE_COLONNE_CANVAS+1, sticky='W', padx=(left_padding, 0))
	label_nouveau_noeud.grid(row=3, column=NOMBRE_COLONNE_CANVAS+1, sticky='W', padx=(left_padding, 0))
	entry_noeud.grid(row=3, column=NOMBRE_COLONNE_CANVAS+2, sticky="E"+"W", padx=(0, right_padding))

	label_lambda_actuel.grid(row=4, column=NOMBRE_COLONNE_CANVAS+1, sticky='W', padx=(left_padding, 0))
	label_nouveau_lambda.grid(row=5, column=NOMBRE_COLONNE_CANVAS+1, sticky='W', padx=(left_padding, 0))
	entry_lambda.grid(row=5, column=NOMBRE_COLONNE_CANVAS+2, sticky="E"+"W", padx=(0, right_padding))

	label_lambda_burst_actuel.grid(row=6, column=NOMBRE_COLONNE_CANVAS+1, sticky='W', padx=(left_padding, 0))
	label_nouveau_lambda_burst.grid(row=7, column=NOMBRE_COLONNE_CANVAS+1, sticky='W', padx=(left_padding, 0))
	entry_lambda_burst.grid(row=7, column=NOMBRE_COLONNE_CANVAS+2, sticky="E"+"W", padx=(0, right_padding))

	label_limite_taille_message_min.grid(row=8, column=NOMBRE_COLONNE_CANVAS+1, sticky='W', padx=(left_padding, 0))
	label_nouvelle_limite.grid(row=9, column=NOMBRE_COLONNE_CANVAS+1, sticky='W', padx=(left_padding, 0))
	entry_limite_message.grid(row=9, column=NOMBRE_COLONNE_CANVAS+2, sticky="E"+"W", padx=(0, right_padding))
	###
	label_nb_antenne.grid(row=10, column=NOMBRE_COLONNE_CANVAS+1, sticky='W', padx=(left_padding, 0))
	label_nouveau_nb_antenne.grid(row=12, column=NOMBRE_COLONNE_CANVAS+1, sticky='W', padx=(left_padding, 0))
	entry_nb_antenne.grid(row=12, column=NOMBRE_COLONNE_CANVAS+2, sticky="E"+"W", padx=(0, right_padding))

	label_taille_message_BE.grid(row=14, column=NOMBRE_COLONNE_CANVAS+1, sticky='W', padx=(left_padding, 0))
	label_nouvelle_taille_message_BE.grid(row=16, column=NOMBRE_COLONNE_CANVAS+1, sticky='W', padx=(left_padding, 0))
	entry_taille_message_BE.grid(row=16, column=NOMBRE_COLONNE_CANVAS+2, sticky="E"+"W", padx=(0, right_padding))

	label_nb_message_requete.grid(row=18, column=NOMBRE_COLONNE_CANVAS+1, sticky='W', padx=(left_padding, 0))
	label_nouveau_nb_message_requete.grid(row=20, column=NOMBRE_COLONNE_CANVAS+1, sticky='W', padx=(left_padding, 0))
	entry_nb_message_requete.grid(row=20, column=NOMBRE_COLONNE_CANVAS+2, sticky="E"+"W", padx=(0, right_padding))

	label_periode_requete.grid(row=22, column=NOMBRE_COLONNE_CANVAS+1, sticky='W', padx=(left_padding, 0))
	label_nouvelle_periode_requete.grid(row=24, column=NOMBRE_COLONNE_CANVAS+1, sticky='W', padx=(left_padding, 0))
	entry_periode_requete.grid(row=24, column=NOMBRE_COLONNE_CANVAS+2, sticky="E"+"W", padx=(0, right_padding))

	label_nb_carte.grid(row=26, column=NOMBRE_COLONNE_CANVAS+1, sticky='W', padx=(left_padding, 0))
	label_nouveau_nb_carte.grid(row=28, column=NOMBRE_COLONNE_CANVAS+1, sticky='W', padx=(left_padding, 0))
	entry_nb_carte.grid(row=28, column=NOMBRE_COLONNE_CANVAS+2, sticky="E"+"W", padx=(0, right_padding))

	update_label_TIC(fenetre, 30, NOMBRE_COLONNE_CANVAS+1)

	if controleur.politique == POLITIQUE_PRIORITAIRE:
		resultat = "Priorité aux C-RAN"
	elif controleur.politique == POLITIQUE_PRIORITE_ABSOLUE:
		resultat = "Priorité absolue aux C-RAN"
	else:
		resultat = "Aucune priorité"
	label_politique_actuel = Label(fenetre, text = "Politique actuelle : "+str(resultat) )
	label_politique_actuel.grid(row=32, column=NOMBRE_COLONNE_CANVAS+1, sticky='W', padx=x_padding )

	""" les boutons """
	bouton_politique = Button(fenetre, text ="Changer de politique", command = changer_politique, bg="#ff9900", fg="White", activebackground="#e68a00", activeforeground="White")
	bouton_politique.grid(row=34, column=NOMBRE_COLONNE_CANVAS+1, sticky='W', padx=x_padding)

	bouton_explorer = Button(fenetre, text ="Ouvrir un fichier de simulation", command = ouvrir_fichier, bg="#0099ff", fg="White", activebackground="#007acc", activeforeground="White")
	bouton_explorer.grid(row=34, column=NOMBRE_COLONNE_CANVAS+2, sticky='E', padx=x_padding)

	bouton_reset = Button(fenetre, text ="Valider nouvelle configuration", command = modifier_configuration, bg="YellowGreen", fg="White", activebackground="#7ba428", activeforeground="White", width=LONGUEUR_BOUTON*2)
	bouton_reset.grid(row=35, column=NOMBRE_COLONNE_CANVAS+1, sticky="N"+"S"+"E"+"W",columnspan=2, padx=x_padding)

##	Alterne le couleur de fond d'un noeud avec sa couleur de message prioritaire
#	@param iteration : Le nombre de fois ou l'on souhaite effectuer l'alternance de couleur.
#	@param noeud_graphique : L'objet graphique sur lequelle nous effecturons les changements de couleurs.
#	@param noeud_modele : Le noeud dans notre modèle.
def changer_couleur(iteration, noeud_graphique, noeud_modele):
	nb_interation =  3	#Le nombre de changement de couleur que l'on effectue
	for i in range(0, nb_interation):
		couleur_actuelle = controleur.canvas.itemcget(noeud_graphique, "fill")
		if couleur_actuelle == noeud_modele.couleur_noeud:
			nouvelle_couleur = noeud_modele.couleur_noeud_claire
		else:
			nouvelle_couleur = noeud_modele.couleur_noeud
		controleur.canvas.itemconfigure(noeud_graphique, fill=nouvelle_couleur)
		time.sleep(0.2)		#On fait une pause le temps que l'utilisateur puisse apercevoir le changement de couleur.

	controleur.canvas.itemconfigure(noeud_graphique, fill=noeud_modele.couleur_noeud)


##	Fonction callback ouvrant un fichier selectionné depuis un explorateur.
#	Le fichier ouvert doit être un fichier de configuration au format csv.
def ouvrir_fichier():
	global controleur

	chemin_fichier = tkFileDialog.askopenfilename(initialdir="../../fichiers_simulations/")
	if type(chemin_fichier) is not tuple:	#Si la variable est de type tuple, la fonction "askopenfilename" à renvoyé un champ vide
		controleur.chemin_fichier = chemin_fichier
		controleur.lire_fichier = True
		reset()
		tkMessageBox.showinfo("Chargement", "La simulation va désormais exécuter le scénario du fichier fournis !;)")
		commencer_rotation()


##	Fonction callback changant la politique d'envoi de message de l'anneau
def changer_politique():
	global controleur

	arreter_rotation()
	#On change de politique
	if controleur.politique == POLITIQUE_PRIORITE_ABSOLUE:
		controleur.politique = POLITIQUE_SANS_PRIORITE
	else:
		controleur.politique = controleur.politique + 1
	controleur.lire_fichier = False
	reset()
	if controleur.politique == POLITIQUE_PRIORITAIRE:
		message = "La simulation va désormais prendre en compte la priorité des messages provenants des antennes en leur fixant un seuil prenant aussi en compte le nombre de messages Best effort."
	elif controleur.politique == POLITIQUE_PRIORITE_ABSOLUE:
		message = "La simulation va désormais prendre en compte la priorité des messages C-RAN et cherchera à les envoyer des que possible"
	else:
		message = "Les messages prioritaires seront désormais traités de la même manière que les Best effort."
	tkMessageBox.showinfo("Changement de politique", message)


##	Met a jour le label du panel bas affichant le TIC en millisecondes.
#	@param fenetre : La fenêtre sur laquelle on se situe le label que l'on souhaite modifier.
#	@param ligne : La ligne ou se situe le label par rapport au panel bas.
#	@param colonne : La colonne ou se situe le label par rapport au panel bas.
def update_label_TIC(fenetre, ligne, colonne):
	global LABEL_TIC

	if LABEL_TIC != None:
		LABEL_TIC.destroy()

	if TIC <= 600:
		message = "TIC : "+str(TIC)+" millisecondes, on est au max !"
	else:
		message = "TIC : "+str(TIC)+" millisecondes"
	LABEL_TIC = Label(fenetre, text = message)
	LABEL_TIC.grid(row=ligne, column=colonne, sticky='W', padx=(15, 15))

##	Affiche un message d'aide sur la simulation.
def afficher_aide():
	message = "Cette fenêtre a pour but de fournir une petite explication des points pouvant parraitre peu claire sur l'interface graphique de la simulation."
	message += "\n\nLors d'une politique d'envoi prioritaire des messages, chaque noeud dispose de deux labels différents. "
	message += "Le label situé à droite du noeud indique le nombre de messages best effort du noeud, alors que le label à gauche indique le nombre de messages prioritaires."
	message += "\nLors d'un envoi de messages, un paquet de message contient deux couleurs. La couleur la plus claire représente la proportion de messages prioritaires du paquet, alors que la couleur la plus foncée représente la proportion de message best effort."
	message += "\n\nDans le cas ou est appliquée une politique ne prenant pas en charge l'aspect prioritaire de certains messages, un seul label par noeud indique le nombre de messages contenus dans le noeud, et une seule couleur est utilisée pour un paquet de message."
	tkMessageBox.showinfo("Aide", message)


##	Déplace dans le canvas un objet vers un point d'arrivé définit par arrivee_x et arrivee_y.
#	@param canvas : Le canvas sur lequel se situe l'objet que l'on souhaite déplacer.
#	@param objet : L'objet que l'on souhaite déplacer.
#	@param arrivee_x : Le point d'arrivé x que l'on souhaite pour l'objet.
#	@param arrivee_y : Le point d'arrivé y que l'on souhaite pour l'objet.
def deplacer_vers(canvas, objet, arrivee_x, arrivee_y):
	if not STATHAM_MODE:
		paquet = objet
		objet = paquet.conteneur

	""" Convertie les coordonnees en int afin de récupérer la partie entiere des nombres, ainsi les coordonnees coïncideront toujours """
	objet_x = int(canvas.coords(objet)[0])
	objet_y = int(canvas.coords(objet)[1])

	""" Calcule la taille de la forme de l'objet passé """

	if not STATHAM_MODE:
		canvas.coords(objet, objet_x - COTE_MESSAGE, objet_y - COTE_MESSAGE, objet_x + COTE_MESSAGE, objet_y + COTE_MESSAGE)
		canvas.coords(paquet.sous_rectangle1, objet_x - COTE_MESSAGE, objet_y - COTE_MESSAGE, (objet_x - COTE_MESSAGE) + ((2 * COTE_MESSAGE) * paquet.proportion_message_prioritaire), objet_y + COTE_MESSAGE)
		canvas.coords(paquet.sous_rectangle2, (objet_x - COTE_MESSAGE) + ((2 * COTE_MESSAGE) * paquet.proportion_message_prioritaire), objet_y - COTE_MESSAGE, objet_x + COTE_MESSAGE, objet_y + COTE_MESSAGE)
		arrivee_x = int(arrivee_x) - COTE_MESSAGE
		arrivee_y = int(arrivee_y) - COTE_MESSAGE
	else:
		canvas.coords(objet, objet_x, objet_y)
		arrivee_x = int(arrivee_x) + COTE_SLOT/8		#L'image ne se place pas de la meme manière qu'un rectangle
		arrivee_y = int(arrivee_y) + COTE_SLOT/8		#Il faut donc réajuster son point d'arrivé.

	while objet_x != arrivee_x or objet_y != arrivee_y:
		if not STATHAM_MODE:
			if objet_x < arrivee_x:
				paquet.move_paquet(1, 0)
			elif objet_x > arrivee_x:
				paquet.move_paquet(-1, 0)
			if objet_y < arrivee_y:
				paquet.move_paquet(0, 1)
			elif objet_y > arrivee_y:
				paquet.move_paquet(0, -1)
			objet = paquet.conteneur
		else:
			if objet_x < arrivee_x:
				canvas.move(objet, 1, 0)
			elif objet_x > arrivee_x:
				canvas.move(objet, -1, 0)
			if objet_y < arrivee_y:
				canvas.move(objet, 0, 1)
			elif objet_y > arrivee_y:
				canvas.move(objet, 0, -1)
		objet_x = canvas.coords(objet)[0]
		objet_y = canvas.coords(objet)[1]

		time.sleep(VITESSE_LATENCE_MESSAGE)


##	Fait sortir graphiquement un message du canvas.
#	@param canvas : Le canvas sur lequel se situe le message que l'on souhaite sortir.
#	@param message : Le message que l'on souhaite sortir.
def sortir_message_graphique(canvas, message):

	""" L'appelle à la méthode sleep permet de laisser le temps à Tkinter de mettre à jour le canvas """
	time.sleep( float(TIC) / float(1000) )

	if not STATHAM_MODE:
		paquet = message
		message = paquet.conteneur
	x = int(canvas.coords(message)[0])
	y = int(canvas.coords(message)[1])

	""" Mise en place des directions pour les abscisses et les ordonnées """
	if x > HAUTEUR_CANVAS/2:
		direction_x = 1
		objectif_x = HAUTEUR_CANVAS
	elif x < HAUTEUR_CANVAS/2:
		direction_x = -1
		objectif_x = 0
	else:
		direction_x = 0
		objectif_x = x

	if y > HAUTEUR_CANVAS/2 :
		direction_y = 1
		objectif_y = HAUTEUR_CANVAS
	elif y < HAUTEUR_CANVAS/2:
		direction_y = -1
		objectif_y = 0
	else:
		direction_y = 0
		objectif_y = y

	while x != objectif_x or y != objectif_y:
		if STATHAM_MODE:
			paquet.move_paquet(direction_x, direction_y)
			message = paquet.conteneur
		else:
			paquet.move_paquet(direction_x, direction_y)
			message = paquet.conteneur
		x = int(canvas.coords(message)[0])
		y = int(canvas.coords(message)[1])

		time.sleep(VITESSE_LATENCE_MESSAGE)

		""" Si un bord du canvas est atteint on supprime le message du canvas """
		if x == 0 or x == HAUTEUR_CANVAS or y == 0 or y == HAUTEUR_CANVAS:
			canvas.delete(paquet.sous_rectangle1)
			canvas.delete(paquet.sous_rectangle2)
			canvas.delete(message)
			break


# # # # # # # # # # # # # # # #		M O D E L E		# # # # # # # # # # # # # # # #

##	Représente un noeud dans le système, un noeud peut stocker des messages.
class Noeud:

	##	Constructeur d'un noeud.
	#	@param self : L'objet de la classe.
	#	@param indice_slot_lecture : L'indice du slot en lecture.
	#	@param indice_slot_ecriture : L'indice du slot en écriture.
	#	@param couleur_noeud : La couleur graphique du noeud.
	#	@param couleur_noeud_claire : Une couleur plus claire pour les messages prioritaires
	#	@param couleur_noeud_foncee : Une couleur plus foncée pour les messages prioritaires
	#	@param nb_antenne : Le nombre d'antenne du noeud.
	#	@param debut_periode : Le début de la période du noeud pour recevoir des messages des antennes.
	def __init__(self, indice_slot_lecture, indice_slot_ecriture, couleur_noeud, couleur_noeud_claire, couleur_noeud_foncee, nb_antenne):
		self.nb_messages_initaux = 0
		self.nb_messages_prioritaires = 0
		self.indice_slot_lecture = indice_slot_lecture
		self.indice_slot_ecriture = indice_slot_ecriture
		self.couleur_noeud = couleur_noeud
		self.couleur_noeud_claire = couleur_noeud_claire
		self.couleur_noeud_foncee = couleur_noeud_foncee
		self.nb_antenne = nb_antenne	#Indique le nombre d'antenne auquel est lié le noeud
		self.debuts_periodes = [0] * nb_antenne
		self.messages_initiaux = deque()		#File FIFO contenant les TIC d'arrivé des messages
		self.messages_prioritaires = deque()
		self.attente_max = 0		#Le temps d'attente maximal dans le noeud
		self.nb_message_total = 0
		self.attente_totale = 0
		self.tics_sorties = []
		self.cartes = [0] * NB_CARTE


	##	Renvoie l'équalité entres deux noeuds.
	#	@param self : Le premier noeud.
	#	@param autre_noeud : Le second noeud.
	#	@return True si les noeuds sont les mêmes, False sinon.
	def equals(self, autre_noeud):
		return self.couleur_noeud == autre_noeud.couleur_noeud


	##	Ajoute un message au noeud.
	#	@param self : Le noeud.
	#	@param message : Le message à ajouter au noeud.
	def ajouter_messages_initiaux(self, message):
		self.messages_initiaux.append(message)
		self.nb_message_total += 1
		self.nb_messages_initaux += 1


	def ajouter_messages_prioritaires(self, message):
		if controleur.politique == POLITIQUE_PRIORITAIRE or controleur.politique == POLITIQUE_PRIORITE_ABSOLUE:
			self.messages_prioritaires.append(message)
			self.nb_messages_prioritaires += 1
		else:
			self.messages_initiaux.append(message)
			self.nb_messages_initaux += 1
		self.nb_message_total += 1


	##	Met a jour le texte affichant le nombre de message en attente dans le noeud.
	#	@param self : Le noeud.
	def update_file_noeud_graphique(self):
		global controleur
		global TEXTS_NOEUDS
		global DICT_TEXTES_NOEUDS

		for i in range (len (controleur.noeuds_modele) ):
			if self.equals(controleur.noeuds_modele[i] ):
				break

		indice_noeud = i

		noeud_graphique = controleur.noeuds_vue[indice_noeud]
		noeud_modele = controleur.noeuds_modele[indice_noeud]

		x = controleur.canvas.coords(noeud_graphique)[0] + COTE_NOEUD
		y = controleur.canvas.coords(noeud_graphique)[1] + COTE_NOEUD

		controleur.canvas.delete(TEXTS_NOEUDS[indice_noeud][0])

		if controleur.politique == POLITIQUE_PRIORITAIRE or controleur.politique == POLITIQUE_PRIORITE_ABSOLUE:
			controleur.canvas.delete(TEXTS_NOEUDS[indice_noeud][1])
			TEXTS_NOEUDS[indice_noeud][1] = controleur.canvas.create_text(x-15, y, text= str(noeud_modele.nb_messages_prioritaires) )
			DICT_TEXTES_NOEUDS[ TEXTS_NOEUDS[indice_noeud][1] ] = controleur.noeuds_modele [indice_noeud]
			controleur.canvas.tag_bind(TEXTS_NOEUDS [indice_noeud][1], "<Button-1>", callback_click_texte)
			TEXTS_NOEUDS[indice_noeud][0] = controleur.canvas.create_text(x+15, y, text= str(noeud_modele.nb_messages_initaux) )
		else:
			TEXTS_NOEUDS[indice_noeud][0] = controleur.canvas.create_text(x, y, text= str(noeud_modele.nb_messages_initaux) )

		controleur.canvas.tag_bind(TEXTS_NOEUDS [indice_noeud][0], "<Button-1>", callback_click_texte)

		DICT_TEXTES_NOEUDS[ TEXTS_NOEUDS[indice_noeud][0] ] = controleur.noeuds_modele [indice_noeud]


	##	Renvoie le noeud sous forme de chaine de caractères.
	#	@param self : Le noeud.
	#	@return Le noeud sous forme de chaine de caractères.
	def __str__(self):
		return str(self.couleur_noeud)

	##	Met à jour le temps d'attente des messages du noeud.
	#	@param self : Le noeud.
	def update_attente(self):
		if controleur.politique == POLITIQUE_PRIORITAIRE or controleur.politique == POLITIQUE_PRIORITE_ABSOLUE:
			for message in self.messages_prioritaires:
				self.attente_totale += 1
		for message in self.messages_initiaux:
			self.attente_totale += 1

##	Applique une période d'envoi de requête pour chaque antenne présente dans l'anneau
def initialiser_periode_antennes():
	global controleur

	for i in range(0, controleur.nb_noeud_anneau):
		for j in range(0, controleur.noeuds_modele[i].nb_antenne):
			controleur.noeuds_modele[i].debuts_periodes[j] = int(random.uniform(1, PERIODE_MESSAGE_ANTENNE))		#Le décalage selon lequel l'antenne envoi une requête au noeud
		print("Debuts periode du noeud ", controleur.noeuds_modele[i].couleur_noeud, " : ", controleur.noeuds_modele[i].debuts_periodes)

##	Repprésente un slot dans l'anneau, il a un id qui lui est propres ainsi qu'un paquet de message et un indice vers le noeud qui lui accède.
class Slot:

	##	Le constructeur d'un slot
	#	@param self : Le slot.
	#	@param id : L'id du slot.
	#	@param indice_noeud_lecture : L'indice du noeud en lecture.
	#	@param indice_noeud_ecriture : L'indice du noeud en écriture.
	#	@param val_cos : La valeur du cosinus de la position du noeud.
	#	@param val_sin : La valeur du sinus de la position du noeud.
	def __init__(self, id, indice_noeud_lecture, indice_noeud_ecriture, val_cos, val_sin):
		self.id = id
		self.paquet_message = None	#Indique si le slot possede un paquet de message
		self.indice_noeud_lecture = indice_noeud_lecture		#Si le slot ne peut accèder a aucun noeud, ce champs vaut None
		self.indice_noeud_ecriture = indice_noeud_ecriture
		self.val_cos = val_cos
		self.val_sin = val_sin

	##	Renvoie le slot sous la forme d'une chaine de caractères.
	#	@return Le slot sous la forme d'une chaine de caractères.
	def __str__(self):
		if self.paquet_message == None:
			return "Je peux accèder au noeud : "+str(self.indice_noeud_accessible)+" Je ne possede pas de message"
		else:
			return "Je peux accèder au noeud : "+str(self.indice_noeud_accessible)+" Je possede un message"


##	Représente un paquet de message circulant dans l'anneau : contient à la fois les coordonnées graphiques du messages, l'indice du noeud auquel il appartient,
#	l'id du paquet le représentant graphiquement ainsi que la taille du paquet.
#	Il contient aussi un tableau contenant les messages du paquet.
class PaquetMessage:

	##	Le constructeur d'un paquet de message.
	#	@param self : le PaquetMessage.
	#	@param id_message : L'id du message.
	#	@param indice_noeud_emetteur : L'indice du noeud emetteur du paquet.
	#	@param taille : La taille du paquet.
	#	@param messages : Les messages du paquet.
	def __init__(self, id_message, indice_noeud_emetteur, taille, proportion_message_prioritaire, messages):
		self.id_message_graphique = id_message
		self.indice_noeud_emetteur = indice_noeud_emetteur
		self.x = None
		self.y = None
		self.taille = taille	#La taille du paquet
		self.proportion_message_prioritaire = proportion_message_prioritaire
		self.messages = messages

	##	Renvoie le paquet sous forme de chaine de caractères.
	#	@param self : le PaquetMessage.
	#	@return Le paquet sous forme de chaine de caractères.
	def __str__(self):
		global controleur
		return "Paquet envoyé par le noeud  : "+str(controleur.noeuds_modele[self.indice_noeud_emetteur].couleur_noeud)+"\nLa taille du paquet est de "+str(self.taille)+" et sa proportion de message prioritaire est de "+str(self.proportion_message_prioritaire)


	##	Retourne l'equalité entre deux messages.
	#	@param self : le premier PaquetMessage.
	#	@param autre_message : le second PaquetMessage.
	#	@return True si les PaquetMessages sont les mêmes, False sinon.
	def equals(self, autre_message):
		return self.id_message_graphique == autre_message.id_message_graphique

##	Classe représentant un message dans l'anneau.
class MessageN:

	##	Constructeur d'un message.
	#	@param self : Le MessageN
	#	@param TIC_arrive : Le TIC d'arrivé du message.
	def __init__(self, TIC_arrive):
		self.TIC_arrive = TIC_arrive


###########################################################
############ Partie tirage/hyper exponentielle ############
###########################################################

##	Effectue un tirage et renvoie True ou False si la variable tirée est contenu dans la probabilité passée en paramètre.
#	@param La probabilité selon laquel le tirage à tiré un événement ou non.
#	@return True si le tirage est inférieur ou égal à la probabilité, False sinon.
def effectuer_tirage(probabilite):
	tirage = random.uniform(0, 1)
	return tirage <= probabilite

##	Réalise le tirage selon l'hyper exponentielle.
def hyper_expo():
	u = random.uniform(0, 1)
	if effectuer_tirage(PROBABILITE_BURST) == True:		#Le tirage est tombé sur la faible proba
		return loi_de_poisson_opti(u, LAMBDA_GRAND) * TAILLE_MESSAGE_BE
	else:
		return loi_de_poisson_opti(u, LAMBDA_PETIT) * TAILLE_MESSAGE_BE

##	Calcule le nombre de message Best Effort transmis par un noeud selon l'algorithme naif de la loi de poisson.
#	@param u : Le paramètre u de la loi de poisson.
#	@param lamb : Le parametre lambda de la loi de poisson.
def loi_de_poisson_naif(u, lamb):
	p = exp (- lamb)
	x = 0
	f = p
	while (u > f):
		x += 1
		p = p*lamb/x
		f += p
	return x

##	Calcule le nombre de message Best Effort transmis par un noeud selon l'algorithme optimisé de la loi de poisson.
#	@param u : Le paramètre u de la loi de poisson.
#	@param lamb : Le parametre lambda de la loi de poisson.
def loi_de_poisson_opti(u, lamb):

	""" Initialisation des variables """
	maxi = TAILLE_UTILISEE_TABLEAU_POISSON
	maxF = TABLEAU_POISSON[ maxi -1]
	maxP = maxF

	if u <= maxF:		#On peut trouver la valeur à l'aide du tableau
		x = 1
		while u > TABLEAU_POISSON[x]:
			x += 1
	else:
		x = maxi
		f = maxF
		p = maxP

		while u > f:
			x += 1
			p = p*lamb/x
			f = f + p
	return x

##	Initialise le tableau avec les résultats de le loi de poisson.
#	Cette fonction est utilisé dans le cadre de l'algorithme optimisé.
def initialiser_tableau():
	global TABLEAU_POISSON
	global TAILLE_UTILISEE_TABLEAU_POISSON

	TABLEAU_POISSON = [0] * TAILLE_TABLEAU

	TABLEAU_POISSON[0] = exp(-LAMBDA_PETIT)
	p = TABLEAU_POISSON[0]

	i = 1
	seuil = 0.99999
	while TABLEAU_POISSON[i-1] < seuil:
		p = p*LAMBDA_PETIT/i
		TABLEAU_POISSON[i] = TABLEAU_POISSON[i-1]+p
		i+=1
	TAILLE_UTILISEE_TABLEAU_POISSON = i


# # # # # # # # # # # # # # # #		C O N T R O L E U R		# # # # # # # # # # # # # # # #

##	Classe représentant le système que l'on souhaite modéliser dans sa globalité
#	Elle fait l'intermédiaire entre le modèle et la vue.
class Controleur:

	##	Le constructeur d'un Controleur.
	#	@param self : L'objet Controleur.
	#	@param fenetre : La fenêtre Tkinter de la simulation.
	#	@param canvas : Le canvas de la simulation.
	#	@param slots_vue : Les slots de la vue de la simulation.
	#	@param slots_modele : Les slots du modèle de la simulation.
	#	@param noeuds_vue : Les noeuds de la vue de la simulation.
	#	@param noeuds_modele : Les noeuds du modèle de la simulation.
	#	@param nb_noeud : Le nombre de noeud de la simulation.
	#	@param nb_slot : Le nombre de slot de la simulation.
	#	@param lire_fichier : Un booléen indiquant s'il la simulation se fait de manière probabiliste ou via une lecture de fichier.
	#	@param politique : Un entier indiquant le type de politique d'envoi.
	def __init__(self, fenetre, canvas, slots_vue, slots_modele, noeuds_vue, noeuds_modele, nb_noeud, nb_slot, lire_fichier, politique):
		self.fenetre = fenetre
		self.canvas = canvas
		self.slots_vue = slots_vue
		self.slots_modele = slots_modele
		self.noeuds_vue = noeuds_vue
		self.noeuds_modele = noeuds_modele
		self.continuer = False		#Booléen indiquant s'il faut effectuer d'autres tics ou non
		self.entrys = {}	#Un dictionnaire des entry de l'interface
		self.nb_tic = 0
		self.nb_noeud_anneau = nb_noeud
		self.nb_slot_anneau = nb_slot
		self.lire_fichier = lire_fichier
		self.chemin_fichier = None
		self.tics_restants = -1
		self.politique = politique


###########################################################
################ Les listeners des boutons ################
###########################################################

##	Fonction callback du click sur un noeud.
#	@param event : L'événement qui déclenche le callback.
def callback_click_noeud(event):
	etat_continuer = controleur.continuer	#L'état de l'anneau

	id_objet = event.widget.find_closest(event.x, event.y)
	id_objet = int( id_objet[0] )

	""" On récupére le noeud sur lequel l'utilisateur à cliqué """
	i = 0
	while i < controleur.nb_noeud_anneau -1 and controleur.noeuds_vue[i] != id_objet:
		controleur.noeuds_vue[i]
		i += 1

	if controleur.noeuds_vue[i] == id_objet:	#On a trouvé le noeud !
		afficher_dialogue_noeud( controleur.noeuds_modele[i], etat_continuer )


##	Fonction callback d'un click sur le texte d'un noeud.
#	@param event : L'événement qui déclenche le callback.
def callback_click_texte(event):
	etat_continuer = controleur.continuer	#L'état de l'anneau

	id_objet = event.widget.find_closest(event.x, event.y)
	id_objet = int( id_objet[0] )

	""" On récupére le noeud sur lequel est situé le texte """
	noeud = DICT_TEXTES_NOEUDS [id_objet]

	if noeud != None:
		afficher_dialogue_noeud( noeud, etat_continuer )


##	Affiche une boîte de dialogue avec les informations du noeud.
#	@param noeud : le noeud pour lequel on souhaite afficher les informations.
#	@param etat_mouvement_anneau : Booléen inquiant si l'anneau est en marche.
def afficher_dialogue_noeud(noeud, etat_mouvement_anneau):
	if etat_mouvement_anneau == True:
		arreter_rotation()

	if noeud.nb_message_total > 0:
		""" Récupération des valeurs """
		attente_moyenne = float(noeud.attente_totale) / float(noeud.nb_message_total)
		attente_moyenne_arrondie = format(attente_moyenne, '.2f')
		attente_max = noeud.attente_max

		if attente_moyenne_arrondie > 0 and attente_max > 0:
			message = "Nombre de message : "+str( noeud.nb_messages_initaux + noeud.nb_messages_prioritaires )+"."
			message += "\nAttente moyenne des messages : "+str(attente_moyenne_arrondie)+"."
			message += "\nAttente maximale des messages : "+str(attente_max)+"."
		else:
			message = "Le noeud n'a pas encore envoyé de message dans l'anneau."
	else:
		message = "\nCe noeud n'a encore reçu aucun message."

	""" Affichage des periodes des antennes """
	if noeud.nb_antenne == 0:
		message += "\nCe noeud est relié à des BBU."
	else:
		message += "\nTICs de réception de requête C-RAN : ["
		for k in range(0, noeud.nb_antenne):
			if k == noeud.nb_antenne-1:
				message += str(noeud.debuts_periodes[k])+"]."
			else:
				message += str(noeud.debuts_periodes[k])+", "

	""" Affichage des buffer des cartes """
	message += "\nBuffer du/des carte(s) du noeud : "
	for k in range(0, NB_CARTE):
		message += "\nCarte numéro "+str(k+1)+" : "+str(noeud.cartes[k])+"."

	titre = str(noeud)

	""" Si l'anneau était en marche, on reprend le mouvement une fois que l'utilisateur a cliqué sur le bouton de la boite de dîalogue """
	if tkMessageBox.showinfo(titre, message) and etat_mouvement_anneau == True:
		commencer_rotation()


##	Gére les inputs au clavier d'un utilisteur lorsqu'il saisie une nouvelle configuration pour l'anneau.
#	@param event : L'évenement qui déclenche la fonction.
def callback_validation_configuration(event):
	if event.char == '\r':		#Le bouton entrée
		modifier_configuration()


##	Callback au bouton demandant un reset de l'application.
#	Ici, on supprime le canvas et on en crée un nouveau. Les paramètres sont ceux utilisés pour la précédente configuration.
def reset():
	global controleur
	global tache

	controleur.continuer = False
	controleur.nb_tic = 0

	""" Clear la console python (Pour Linux uniquement) """
	os.system("clear")

	""" supprime le prochain tic s'il y a afin de ne pas faire planté les threads et l'interface """
	if tache != None:
		controleur.fenetre.after_cancel(tache)

	""" La méthode after permet ici de faire s'executer les threads en cours """
	controleur.fenetre.after(TIC, initialisation(fenetre, controleur.nb_noeud_anneau, controleur.nb_slot_anneau, controleur.lire_fichier, controleur.politique) )


##	Commence la rotation. Méthode appelée lors d'un click sur le bouton de commencement.
def commencer_rotation():
	global controleur
	global tache

	if not controleur.continuer:
		controleur.continuer = True


## Arrête la rotation. Méthode appelée lors d'un click sur le bouton de fin.
def arreter_rotation():

	global controleur

	afficher_stat_noeud()
	""" supprime le prochain tic s'il y a afin de ne pas faire planté les threads et l'interface """
	controleur.continuer = False


##	Augmente la vitesse de rotation.
def augmenter_vitesse():
	global TIC
	global LABEL_TIC

	if TIC - 100 >= 600:
		TIC -= 100
		if controleur.continuer == True:
			arreter_rotation()
			calculer_vitesse()
			commencer_rotation()
		else:
			calculer_vitesse()
		update_label_TIC(controleur.fenetre, NOMBRE_LIGNE_CANVAS+4, 1)


##	Diminue la vitesse de rotation.
def diminuer_vitesse():
	global TIC

	TIC += 100
	if controleur.continuer == True:
		arreter_rotation()
		calculer_vitesse()
		commencer_rotation()
	else:
		calculer_vitesse()

	update_label_TIC(controleur.fenetre, NOMBRE_LIGNE_CANVAS+4, 1)


##	Modifie la configuration de l'anneau en fonction des données saisies dans le panel bas.
def modifier_configuration():
	global controleur
	global LAMBDA_PETIT
	global LAMBDA_GRAND
	global LIMITE_NOMBRE_MESSAGE_MIN
	global NB_ANTENNE
	global TAILLE_MESSAGE_BE
	global NB_MESSAGE_CRAN
	global PERIODE_MESSAGE_ANTENNE
	global NB_CARTE

	tmp_noeud = controleur.nb_noeud_anneau
	tmp_slot = controleur.nb_slot_anneau
	tmp_lambda = LAMBDA_PETIT
	tmp_limite_message = LIMITE_NOMBRE_MESSAGE_MIN
	tmp_nb_antenne = NB_ANTENNE
	tmp_taille_BE = TAILLE_MESSAGE_BE
	tmp_nb_cran = NB_MESSAGE_CRAN
	tmp_periode_requete = PERIODE_MESSAGE_ANTENNE
	tmp_nb_carte = NB_CARTE
	nb_champ_vide = 0

	erreur = False

	valeur_noeud = controleur.entrys[ CLE_ENTRY_NOEUD ].get()
	valeur_slot = controleur.entrys[ CLE_ENTRY_SLOT ].get()
	valeur_lambda = controleur.entrys[ CLE_ENTRY_LAMBDA ].get()
	valeur_lambda_burst = controleur.entrys[ CLE_ENTRY_LAMBDA_BURST ].get()
	valeur_limite_message = controleur.entrys[ CLE_ENTRY_LIMITE_MESSAGE ].get()
	valeur_nb_antenne = controleur.entrys[ CLE_ENTRY_NB_ANTENNE ].get()
	valeur_taille_message_BE = controleur.entrys[ CLE_ENTRY_TAILLE_MESSAGE_BE ].get()
	valeur_nb_message_requete = controleur.entrys[ CLE_ENTRY_NB_MESSAGE_REQUETE ].get()
	valeur_periode_requete = controleur.entrys[ CLE_ENTRY_PERIODE_REQUETE ].get()
	valeur_nb_carte = controleur.entrys[ CLE_ENTRY_NB_CARTE ].get()

	""" Recupération de la valeur du noeud """
	if valeur_noeud != "":
		int_valeur_noeud = int(valeur_noeud)
		if int_valeur_noeud > len(COULEURS_MESSAGE):
			message = "Désolé mais nous ne pouvons produire plus de "+str( len(COULEURS_MESSAGE) )+" noeuds.\nAfin de pouvoir produire plus de noeud, demander à l'esclave d'ajouter des couleurs dans le tableau de couleur."
			tkMessageBox.showerror("Erreur nombre de noeud !", message)
			erreur = True
		elif int_valeur_noeud <= 0:
			message = "Le nombre de noeud doit etre supérieur à 0."
			tkMessageBox.showerror("Erreur nombre de noeud !", message)
			erreur = True
		else:
			controleur.nb_noeud_anneau = int_valeur_noeud
	else:
		nb_champ_vide += 1

	""" Recupération de la valeur du slot """
	if valeur_slot != "":
		int_valeur_slot = int(valeur_slot)
		if int_valeur_slot <= 0:
			message = "Le nombre de slot doit etre supérieur à 0."
			tkMessageBox.showerror("Erreur nombre de noeud !", message)
			erreur = True
		else:
			controleur.nb_slot_anneau = int_valeur_slot
	else:
		nb_champ_vide += 1

	if valeur_noeud != "" and valeur_slot != "" and float(valeur_noeud) / float(valeur_slot) > 0.5:
		message = "Il doit y avoir au minimum deux slots par noeud."
		tkMessageBox.showerror("Erreur nombre de noeud et nombre de slot!", message)
		erreur = True

	""" Recupération de la valeur du lambda """
	if valeur_lambda != "":
		valeur_lambda = int(valeur_lambda)
		if valeur_lambda <= 0:
			message = "Le paramètre lambda doit être supérieur à zéro."
			tkMessageBox.showerror("Erreur valeur lambda !", message)
			erreur = True
		else:
			LAMBDA_PETIT = valeur_lambda
	else:
		nb_champ_vide += 1

	""" Recupération de la valeur du lambda burst """
	if valeur_lambda_burst != "":
		valeur_lambda_burst = int(valeur_lambda_burst)
		if valeur_lambda_burst <= 0:
			message = "Le paramètre lambda burst doit être supérieur à zéro."
			tkMessageBox.showerror("Erreur valeur lambda burst !", message)
			erreur = True
		else:
			LAMBDA_GRAND = valeur_lambda_burst
	else:
		nb_champ_vide += 1

	""" Récupération du nouveau seuil de message """
	if valeur_limite_message != "":
		valeur_limite_message = int(valeur_limite_message)
		if valeur_limite_message <= 0 or valeur_limite_message > LIMITE_NOMBRE_MESSAGE_MAX:
			message = "Le nombre de message minimum doit être positif est inférieur à la limite maximum (ici "+str(LIMITE_NOMBRE_MESSAGE_MAX)+")."
			tkMessageBox.showerror("Erreur limite du nombre de message minimum !", message)
			erreur = True
		else:
			LIMITE_NOMBRE_MESSAGE_MIN = valeur_limite_message
	else:
		nb_champ_vide += 1

	""" Récupération du nombre d'antenne par noeud """
	if valeur_nb_antenne != "":
		valeur_nb_antenne = int(valeur_nb_antenne)
		if valeur_nb_antenne < 0:
			message = "Le nombre de message minimum doit être positif"
			tkMessageBox.showerror("Erreur nombre d'antenne par noeud !", message)
			erreur = True
		else:
			NB_ANTENNE = valeur_nb_antenne
	else:
		nb_champ_vide += 1

	""" Récupération de la taille d'un message best effort """
	if valeur_taille_message_BE != "":
		valeur_taille_message_BE = int(valeur_taille_message_BE)
		if valeur_taille_message_BE <= 0:
			message = "La taille d'un message best effort doit etre supérieur à zéro."
			tkMessageBox.showerror("Erreur taille d'un message best effort !", message)
			erreur = True
		else:
			TAILLE_MESSAGE_BE = valeur_taille_message_BE
	else:
		nb_champ_vide += 1

	""" Récupération du nombre de message par requête """
	if valeur_nb_message_requete != "":
		valeur_nb_message_requete = int(valeur_nb_message_requete)
		if valeur_nb_message_requete < 0:
			message = "Une requête ne peut contenir un nombre négatif de messages."
			tkMessageBox.showerror("Erreur nombre de message par requête !", message)
			erreur = True
		else:
			NB_MESSAGE_CRAN = valeur_nb_message_requete
	else:
		nb_champ_vide += 1

	""" Récupération de la période avant l'envoi de requête """
	if valeur_periode_requete != "":
		valeur_periode_requete = int(valeur_periode_requete)
		if valeur_periode_requete <= 0:
			message = "La période doit etre positive."
			tkMessageBox.showerror("Erreur nombre de message par requête !", message)
			erreur = True
		else:
			PERIODE_MESSAGE_ANTENNE = valeur_periode_requete
	else:
		nb_champ_vide += 1

	""" Récupération du nombre d ecarte par noeud """
	if valeur_nb_carte != "":
		valeur_nb_carte = int(valeur_nb_carte)
		if valeur_nb_carte <= 0:
			message = "Le nombre de carte doit etre positif."
			tkMessageBox.showerror("Erreur nombre de carte !", message)
			erreur = True
		else:
			NB_CARTE = valeur_nb_carte
	else:
		nb_champ_vide += 1

	if erreur or nb_champ_vide == len(controleur.entrys):
		controleur.nb_noeud_anneau = tmp_noeud
		controleur.nb_slot_anneau = tmp_slot
		LAMBDA_PETIT = tmp_lambda
		LIMITE_NOMBRE_MESSAGE_MIN = tmp_limite_message
		NB_ANTENNE = tmp_nb_antenne
		PERIODE_MESSAGE_ANTENNE = tmp_periode_requete
		TAILLE_MESSAGE_BE = tmp_taille_BE
		NB_MESSAGE_CRAN = tmp_nb_cran
		NB_CARTE = tmp_nb_carte
	else:	#Il n'y a aucune erreur, on redéfinit la nouvelle configuration
		controleur.lire_fichier = False
		reset()
		tkMessageBox.showinfo("Chargement", "Votre nouvelle configuration a été chargé avec succès !;)")


##	Stop l'appli en faisant attention aux thread restants.
def arreter_appli():
	arreter_rotation()
	fenetre.destroy()


##	Action de faire entrer un paquet de message d'un noeud jusqu'à son slot.
def placer_message(indice_noeud, messages, proportion_message_prioritaire):
	global controleur

	noeud_modele = controleur.noeuds_modele[ indice_noeud ]
	indice_slot = controleur.noeuds_modele[ indice_noeud ].indice_slot_ecriture

	""" Récupération des valeurs """
	canvas = controleur.canvas
	noeud_graphique = controleur.noeuds_vue[ indice_noeud ]
	slot_graphique = controleur.slots_vue[indice_slot]
	couleur_messages_prioritaires = controleur.noeuds_modele[ indice_noeud ].couleur_noeud_claire
	couleur_messages_best_effort = controleur.noeuds_modele[ indice_noeud ].couleur_noeud_foncee

	""" Création du message """
	id_message_graphique = placer_message_graphique(canvas, noeud_graphique, slot_graphique, couleur_messages_prioritaires, couleur_messages_best_effort, proportion_message_prioritaire)
	if controleur.politique == POLITIQUE_PRIORITAIRE or controleur.politique == POLITIQUE_PRIORITE_ABSOLUE:
		controleur.slots_modele[indice_slot].paquet_message = PaquetMessage( id_message_graphique, indice_noeud, len(messages), proportion_message_prioritaire, messages)
	else:
		controleur.slots_modele[indice_slot].paquet_message = PaquetMessage( id_message_graphique, indice_noeud, len(messages), 0, messages)

	""" Met à jour les temps d'attentes du noeud qui envoi le message """
	if controleur.lire_fichier == False:
		for message in messages:
			if message != None:
				temps_attente_message = (controleur.nb_tic - message.TIC_arrive)
				if temps_attente_message > noeud_modele.attente_max:
					noeud_modele.attente_max = temps_attente_message
				noeud_modele.attente_totale += temps_attente_message


##	Exécute une rotation des messages dans l'anneau.
def rotation_message():
	global controleur

	decaler_messages()
	sortir_message()
	if controleur.lire_fichier == False:
		entrer_message()
	else:
		if controleur.tics_restants == -1:
			controleur.tics_restants = entrer_message_via_fichier()
		elif controleur.tics_restants == 0:
			arreter_rotation()
		else:
			controleur.tics_restants -= 1



##	Fait entrer dans l'anneau des messages.
#	Ici, les arrivées de messages sont gérées par l'hyper exponentielle et des files d'attentes.
def entrer_message():
	global controleur
	Q = 100
	for i in range (0, controleur.nb_slot_anneau):		#Parcours des slots de l'anneau
		slot = controleur.slots_modele[i]
		if slot.indice_noeud_ecriture != None:	#Le slot est un slot d'ecriture
			noeud = controleur.noeuds_modele[ slot.indice_noeud_ecriture ]
			# # # # # # # # # # # # #
			# RECEPTION DES MESSAGES PAR LE NOEUD
			# # # # # # # # # # # # #
			""" Envoi de message par une antenne """
			if slot.indice_noeud_ecriture != INDICE_DATA_CENTER:
				for j in range (0, NB_ANTENNE):
					if controleur.nb_tic % PERIODE_MESSAGE_ANTENNE == noeud.debuts_periodes[j]:		#C'est la periode du noeud, il reçoit un message de ses antennes
						for k in range(0, NB_MESSAGE_CRAN):
							noeud.ajouter_messages_prioritaires( MessageN(controleur.nb_tic) )
			""" Génération des messages pour chaque carte du noeud """
			for j in range (0, NB_CARTE):
				nb_messages_best_effort = hyper_expo()	#Le nombre de message Best Effort reçu est géré par l'hyper exponentielle
				if nb_messages_best_effort + noeud.cartes[j] < Q:	#La carte peut envoyer tous ses messages
					for k in range(0, nb_messages_best_effort + noeud.cartes[j]):
						noeud.ajouter_messages_initiaux( MessageN(controleur.nb_tic) )
				else:
					for k in range(0, Q):
						noeud.ajouter_messages_initiaux( MessageN(controleur.nb_tic) )
					noeud.cartes[j] = (nb_messages_best_effort + noeud.cartes[j]) - Q

			if controleur.politique == POLITIQUE_PRIORITAIRE or controleur.politique == POLITIQUE_PRIORITE_ABSOLUE:
				nb_message_noeud = noeud.nb_messages_prioritaires + noeud.nb_messages_initaux
			else:
				nb_message_noeud = noeud.nb_messages_initaux
			# # # # # # # # # # # # #
			# ENVOI DES MESSAGES PAR LE NOEUD
			# # # # # # # # # # # # #

			if slot.paquet_message == None: 		#Le slot est disponible en ecriture

				# # # # # # # # # # # # #
				# POLITIQUE DE PRIORITE ABSOLUE
				# # # # # # # # # # # # #
				if controleur.politique == POLITIQUE_PRIORITE_ABSOLUE:	#Politique de priorité absolue
					if noeud.nb_messages_prioritaires > 0:
						messages = []
						nb_messages_prioritaire_noeud = noeud.nb_messages_prioritaires
						if noeud.nb_messages_prioritaires >= LIMITE_NOMBRE_MESSAGE_MAX:		#On place uniquement des C-RAN
							proportion_message_prioritaire = 1
							for k in range(0, LIMITE_NOMBRE_MESSAGE_MAX):
								messages.append( noeud.messages_prioritaires.popleft() )
							noeud.nb_messages_prioritaires -= LIMITE_NOMBRE_MESSAGE_MAX
						else:	#On place des C-RAN et le reste de Best effort
							nb_messages_best_effort_noeud = noeud.nb_messages_initaux
							for k in range(0, nb_messages_prioritaire_noeud):
								messages.append( noeud.messages_prioritaires.popleft() )
							noeud.nb_messages_prioritaires = 0

							if nb_messages_prioritaire_noeud + nb_messages_best_effort_noeud >= LIMITE_NOMBRE_MESSAGE_MAX:	#On a plus de BE que necessaire
								nb_BE_a_envoyer = LIMITE_NOMBRE_MESSAGE_MAX - nb_messages_prioritaire_noeud
								for k in range(0, nb_BE_a_envoyer):
									messages.append( noeud.messages_initiaux.popleft() )
								noeud.nb_messages_initaux -= LIMITE_NOMBRE_MESSAGE_MAX - nb_messages_prioritaire_noeud

							else:	#On place tous nos BE
								nb_BE_a_envoyer = nb_messages_best_effort_noeud
								for k in range(0, nb_BE_a_envoyer):
									messages.append( noeud.messages_initiaux.popleft() )
								noeud.nb_messages_initaux = 0
							proportion_message_prioritaire = nb_messages_prioritaire_noeud / float(nb_BE_a_envoyer + nb_messages_prioritaire_noeud)
						placer_message( slot.indice_noeud_ecriture, messages, proportion_message_prioritaire )

					#Ici on a pas de prioritaire, mais les BE on attenit le seuil
					elif noeud.nb_messages_initaux >= LIMITE_NOMBRE_MESSAGE_MIN:
						messages = []
						nb_messages_best_effort_noeud = noeud.nb_messages_initaux
						proportion_message_prioritaire = 0
						if noeud.nb_messages_initaux >= LIMITE_NOMBRE_MESSAGE_MAX:		#On envoie autant de BE que possible
							for k in range(0, LIMITE_NOMBRE_MESSAGE_MAX):
								messages.append( noeud.messages_initiaux.popleft() )
							noeud.nb_messages_initaux -= LIMITE_NOMBRE_MESSAGE_MAX
						else:	#On vide les be
							for k in range(0, nb_messages_best_effort_noeud):
								messages.append( noeud.messages_initiaux.popleft() )
							noeud.nb_messages_initaux = 0
						placer_message( slot.indice_noeud_ecriture, messages, proportion_message_prioritaire )

				# # # # # # # # # # # # #
				# POLITIQUE PRIORITAIRE
				# # # # # # # # # # # # #
				elif controleur.politique == POLITIQUE_PRIORITAIRE:
					if nb_message_noeud >= LIMITE_NOMBRE_MESSAGE_MIN:		#Le noeud peut emettre un message
						if nb_message_noeud >= LIMITE_NOMBRE_MESSAGE_MAX:	#On envoi un max de message
							nb_message_a_envoyer = LIMITE_NOMBRE_MESSAGE_MAX
						else:												#on vide le noeud
							nb_message_a_envoyer = nb_message_noeud
						messages = []
						nb_messages_prioritaire_noeud = noeud.nb_messages_prioritaires
						if nb_messages_prioritaire_noeud >= nb_message_a_envoyer:	 #On envoie uniquement des prioritaires
							for k in range(0, nb_message_a_envoyer):
								messages.append( noeud.messages_prioritaires.popleft() )
							noeud.nb_messages_prioritaires -= nb_message_a_envoyer
							proportion_message_prioritaire = 1
						else:		#On envoie tous les prioritaires et le reste en best effort
							for k in range(0, nb_messages_prioritaire_noeud):
								messages.append( noeud.messages_prioritaires.popleft() )
							for k in range(0, nb_message_a_envoyer - nb_messages_prioritaire_noeud):
								messages.append( noeud.messages_initiaux.popleft() )
							noeud.nb_messages_prioritaires -= nb_messages_prioritaire_noeud
							noeud.nb_messages_initaux -= (nb_message_a_envoyer - nb_messages_prioritaire_noeud)
							if nb_messages_prioritaire_noeud == 0:
								proportion_message_prioritaire = 0
							else:
								proportion_message_prioritaire = nb_messages_prioritaire_noeud / float(nb_message_a_envoyer)
						placer_message( slot.indice_noeud_ecriture, messages, proportion_message_prioritaire )

				# # # # # # # # # # # # #
				# POLITIQUE SANS PRIORITE
				# # # # # # # # # # # # #
				else:
					if nb_message_noeud >= LIMITE_NOMBRE_MESSAGE_MIN:		#Le noeud peut emettre un message
						proportion_message_prioritaire = 0
						if nb_message_noeud >= LIMITE_NOMBRE_MESSAGE_MAX:	#On envoi un max de message
							nb_message_a_envoyer = LIMITE_NOMBRE_MESSAGE_MAX
						else:												#on vide le noeud
							nb_message_a_envoyer = noeud.nb_messages_initaux
						""" On enleve les messages du noeud """
						messages = []
						for k in range(0, nb_message_a_envoyer):
							messages.append( noeud.messages_initiaux.popleft() )
						noeud.nb_messages_initaux -= nb_message_a_envoyer
						placer_message( slot.indice_noeud_ecriture, messages, proportion_message_prioritaire )

			noeud.update_file_noeud_graphique()


##	Envoie les messages dans l'anneau à partir d'un scénario de fichier.
#	@return Le nombre de tic à attendre avant de finir la rotation, -1 si ce temps d'attente n'est pas encore déterminé.
def entrer_message_via_fichier():
	global controleur

	tic_actuel = controleur.nb_tic
	for i in range( len(controleur.noeuds_modele) ):
		noeud = controleur.noeuds_modele[i]
		if len(noeud.tics_sorties) > 0:
			if tic_actuel == int(noeud.tics_sorties[0]):
				noeud.tics_sorties.pop(0)
				message = [0] * LIMITE_NOMBRE_MESSAGE_MAX
				placer_message(i, message, 0)

	for noeud in controleur.noeuds_modele:
		if len(noeud.tics_sorties) > 0:
			return -1
	return len(controleur.slots_modele)


##	Fait sortir du système un message.
def sortir_message():
	global controleur

	""" Fais sortir les messages qui repassent devant leur Noeud emetteur """
	for slot in controleur.slots_modele:
		paquet_message = slot.paquet_message

		#Il y a un message sur le slot de lecture du noeud emetteur
		if paquet_message and slot.indice_noeud_lecture != None and paquet_message.indice_noeud_emetteur == slot.indice_noeud_lecture:
			t = Thread(target=sortir_message_graphique, args=(controleur.canvas, slot.paquet_message.id_message_graphique) )
			t.start()
			slot.paquet_message = None
		#Ici on gére le cas ou des messages prioritaires passent devant le BBU
		elif (controleur.politique == POLITIQUE_PRIORITAIRE or controleur.politique == POLITIQUE_PRIORITE_ABSOLUE) and (paquet_message and slot.indice_noeud_lecture != None and slot.indice_noeud_lecture == INDICE_DATA_CENTER):
			nb_messages_prioritaires = int(paquet_message.taille * paquet_message.proportion_message_prioritaire)
			if nb_messages_prioritaires > 0:
				for k in range(0, nb_messages_prioritaires):
					controleur.noeuds_modele[INDICE_DATA_CENTER].ajouter_messages_prioritaires( MessageN(controleur.nb_tic) )
				t = Thread(target=changer_couleur, args=(0, controleur.noeuds_vue[INDICE_DATA_CENTER], controleur.noeuds_modele[INDICE_DATA_CENTER]))
				t.start()
				controleur.noeuds_modele[INDICE_DATA_CENTER].update_file_noeud_graphique()


##	Methode appelant une methode récursive qui décale d'un slot les message du système.
def decaler_messages():
	global controleur

	tempon = controleur.slots_modele[1].paquet_message

	decaler_messages2(0, 0, tempon, True)


##	Méthode récursive qui décale les messages de l'anneau.
def decaler_messages2(premier_indice, indice_slot, paquet_message, premier_appel):
	global controleur

	milieu_x = HAUTEUR_CANVAS/2
	milieu_y = HAUTEUR_CANVAS/2

	destination_x = milieu_x + cos(2*indice_slot*pi/controleur.nb_slot_anneau) * DISTANCE_SLOT
	destination_y = milieu_y - sin(2*indice_slot*pi/controleur.nb_slot_anneau) * DISTANCE_SLOT

	msg = controleur.slots_modele[indice_slot].paquet_message
	if msg != None:
		""" On déplace le message """
		if STATHAM_MODE:
			t = Thread(target=deplacer_vers, args=( controleur.canvas, msg.id_message_graphique, destination_x, destination_y ))
			t.start()
		else:
			paquet = msg.id_message_graphique
			paquet.teleporter_paquet(destination_x, destination_y)


	if indice_slot-1 < 0:
		nouvelle_indice = len(controleur.slots_modele) - 1
	else:
		nouvelle_indice = indice_slot-1

	if indice_slot != premier_indice or premier_appel:
		tempon = controleur.slots_modele[indice_slot].paquet_message

		decaler_messages2(premier_indice, nouvelle_indice, tempon, False)
		controleur.slots_modele[indice_slot].paquet_message = paquet_message
	else:
		controleur.slots_modele[indice_slot].paquet_message = paquet_message


##	Calculer le temps de latence entre chaque mouvement de pixel lors d'un déplacement de message.
#	Le calcul prend en compte la distance à parcourir entre chaque déplacement.
def calculer_vitesse():
	matela_securite = 100

	milieu_x = HAUTEUR_CANVAS/2
	milieu_y = HAUTEUR_CANVAS/2

	""" Ici on choisi deux slots voisins et on calcul la distance entre ces deux slots """
	x1 = milieu_x + cos(0/controleur.nb_slot_anneau) * DISTANCE_SLOT
	y1 = milieu_y - sin(0/controleur.nb_slot_anneau) * DISTANCE_SLOT

	x2 = milieu_x + cos(2*pi/controleur.nb_slot_anneau) * DISTANCE_SLOT
	y2 = milieu_y - sin(2*pi/controleur.nb_slot_anneau) * DISTANCE_SLOT

	distance_max = max( abs(x1 - x2), abs(y1 - y2) ) #* matela_securite

	global VITESSE_LATENCE_MESSAGE

	""" Le résultat est en milliseconde, il faut donc le diviser par 1000 pour l'obtenir en seconde """
	pixel_par_seconde = (TIC/distance_max) / (1000 * matela_securite)

	arrondi = format(pixel_par_seconde, '.5f')

	VITESSE_LATENCE_MESSAGE = float(arrondi)

# # # # # # # # # #		M E T H O D E S		M A I N		# # # # # # # # # # # #


##	Met en place le canvas.
#	@param fenetre : La fenêtre sur laquelle on place le canvas.
#	@param nb_noeud : Le nombre de noeud à initialiser.
#	@param lire_fichier : Un booléen indiquant si la simulation se fait via une lecture de fichier ou non.
def initialisation(fenetre, nb_noeud, nb_slot, lire_fichier, politique):
	global controleur
	global IMAGE_JASON

	if lire_fichier:
		chemin_fichier = controleur.chemin_fichier
		fichier =   open(chemin_fichier, 'r')
		reader = csv.reader(fichier)
		i = 0
		for ligne in reader:	#On ne parcours que les deux premieres lignes afin de recuperer les nombres de noeud et de slot
			if i == 0:		#Le nombre de noeud de l'anneau
				nb_noeud = int(ligne[0])
			elif i == 1:	#le nombre de slot de l'anneau
				nb_slot = int(ligne[0])
			else:
				break
			i += 1
	""" On détruit tout les widgets de la fenêtre afin que celle-ci soit toute belle """
	for widget in fenetre.winfo_children():
	    widget.destroy()

	""" Mise en place du canvas et des données du controleur """
	canvas = creer_canvas(fenetre)
	IMAGE_JASON = PhotoImage(file="../images/jason_statham.png")

	slots = placer_slots(fenetre, canvas, nb_slot)
	slots_modele = slots[0]
	slots_vue = slots[1]

	noeuds = placer_noeuds(fenetre, canvas, nb_noeud, nb_slot, slots_modele, slots_vue, politique)
	noeuds_modele = noeuds[0]
	noeuds_vue = noeuds[1]
	slots_modele = noeuds[2]

	controleur = Controleur(fenetre, canvas, slots_vue, slots_modele, noeuds_vue, noeuds_modele, nb_noeud, nb_slot, lire_fichier, politique)
	initialiser_periode_antennes()
	update_labels_globaux(0)

	if lire_fichier:
		fichier = open(chemin_fichier, 'r')
		reader = csv.reader(fichier)
		i = 0
		for ligne in reader:
			if i >= 2:			#Les tics d'envoi de message d'un noeud
				indice_noeud = int(ligne[0])
				for j in range(1, len(ligne)):
					controleur.noeuds_modele[indice_noeud].tics_sorties.append(ligne[j])
			i += 1
		controleur.chemin_fichier = chemin_fichier

	calculer_vitesse()

	placer_panel_gauche(fenetre)
	placer_panel_droit(fenetre)

	initialiser_tableau()

	effectuer_tic()

##	Attend un TIC et effectue une rotation des messages.
def effectuer_tic():
	global controleur
	global tache

	if controleur.continuer == True:
		controleur.nb_tic += 1
		update_labels_globaux(controleur.nb_tic)

		rotation_message()

		for noeud in controleur.noeuds_modele:
			noeud.update_attente()

	tache = controleur.fenetre.after(TIC, effectuer_tic )


##	Affiche l'état des slots de l'anneau.
def afficher_message_anneau():
	global controleur
	for i in range (controleur.nb_slot_anneau):
		if controleur.slots_modele[i].paquet_message == None:
			print ("Le slot ", controleur.slots_vue[i], " ne contient pas de message")
		else:
			print ("Le slot ", controleur.slots_vue[i], " contient un message mis par le noeud ", controleur.noeuds_modele[ controleur.slots_modele[i].paquet_message.indice_noeud_emetteur ])


##	Affiche les statistiques liés aux temps d'attente des noeuds.
def afficher_stat_noeud():
	global controleur

	print ("\n######### STATS #######")
	for noeud in controleur.noeuds_modele:
		if noeud.nb_message_total != 0:
			attente_moyenne = float(noeud.attente_totale) / float(noeud.nb_message_total)
			attente_moyenne_arrondie = format(attente_moyenne, '.2f')
			print ("Noeud "+str(noeud)+" Nombre de message : "+str(noeud.nb_messages_prioritaires + noeud.nb_messages_initaux)+" Attente moyenne : "+str( attente_moyenne_arrondie )+" Attente max : "+str(noeud.attente_max))
	print ("\n")


# # # # # # # # # # # # # # # #		M A I N 	# # # # # # # # # # # # # # # #

lire_fichier = False

if len(sys.argv) > 1:	#Un argument à été donnée
	valeur_pour_statham = ["-jason_statham", "-Jason", "-Statham", "-Jason_Statham", "-JASON", "-STATHAM", "-JASON_STATHAM", "-STATHAM_MODE", "-True", "-true", "-TRUE"]
	for i in range( len(sys.argv) ):
		argument = str( sys.argv[i] )
		if argument in valeur_pour_statham:		#On active le STATHAM MDOE !!!
			print ("On active le STATHAM MDOE !!!")
			STATHAM_MODE = True

		elif argument == "-f":
			if len(sys.argv) > i+1:
				chemin_fichier = str(sys.argv[i+1])
				lire_fichier = True
				print ("Lecture du fichier : \""+chemin_fichier+"\"")
			else:
				print ("Aucun chemin de fichier spécifié")

global controleur
controleur = None

fenetre = creer_fenetre()

# # # # # # # # # # # # 	VALEUR POUR LA TAILLE DU CANVAS 	# # # # # # # # # # # #
hauteur_ecran = fenetre.winfo_screenheight()
print ("Hauteur écran : ", hauteur_ecran)
if hauteur_ecran > 800:
	print("Supérieur à 800, on fixe le max")
	LARGEUR_CANVAS = 800
	HAUTEUR_CANVAS = 800
else:
	print("Inferieur à 800, on prend la hauteur totale")
	HAUTEUR_CANVAS = hauteur_ecran - 150
	LARGEUR_CANVAS = hauteur_ecran - 50

DISTANCE_SLOT = HAUTEUR_CANVAS/2.5			#La distance d'un slot par rapport à l'axe central du canvas
DISTANCE_NOEUD = DISTANCE_SLOT + 40		#La distance d'un noeud par rapport à l'axe central du canvas

LONGUEUR_BOUTON = HAUTEUR_CANVAS/31
LONGUEUR_ENTRY = HAUTEUR_CANVAS/60

fenetre.protocol("WM_DELETE_WINDOW", arreter_appli)		#Réagie à la demande d'un utilisateur de quitter l'application via la croix graphique

nb_noeud = 5
nb_slot = 100

initialisation(fenetre, nb_noeud, nb_slot, lire_fichier, POLITIQUE_PRIORITE_ABSOLUE)
fenetre.mainloop()
