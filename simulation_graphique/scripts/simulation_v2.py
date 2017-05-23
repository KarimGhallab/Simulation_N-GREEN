#coding: utf8

##	@package simulation_v2
#	Ce script permet de réaliser une simulation d'un anneau en réseau dans le cadre du projet N-GREEN.

import tkMessageBox
import time
import random
import sys
import os

from Tkinter import Tk, Canvas, Button, Label, Entry, PhotoImage
from math import cos, sin, pi, exp
from threading import Thread
from PIL import Image, ImageTk
from collections import deque
# # # # # # # # # # # # # # # #		C O N S T A N T E	 # # # # # # # # # # # # # # # #

IMAGES = []

COULEURS_MESSAGE = ["yellowgreen", "orange", "turquoise", "royalblue", "purple", "teal", "tan", "snow", "mediumseagreen", "LightCoral", "Chartreuse", "CornflowerBlue", "DarkGray", "DarkOliveGreen", "DarkMagenta", "Lavender", "SandyBrown", "Black"]

COTE_CANVAS = 700	#Définit la hauteur/largeur de la toile sur laquelle seront déssinés les slots et les noeuds

global NOMBRE_SLOT
NOMBRE_SLOT = 25		#Le nombre de slot du système
COTE_SLOT = 15		#La hauteur/largeur d'un slot
DISTANCE_SLOT = COTE_CANVAS/3	#La distance d'un slot par rapport à l'axe central du canvas

global NOMBRE_NOEUD
NOMBRE_NOEUD = 10	#Le nombre de noeud du système
COTE_NOEUD = COTE_SLOT + 5		#La hauteur/largeur d'un noeud
DISTANCE_NOEUD = DISTANCE_SLOT + 50		#La distance d'un noeud par rapport à l'axe central du canvas

global VITESSE_LATENCE_MESSAGE
VITESSE_LATENCE_MESSAGE = 0.002		#Le temps d'attente en seconde entre chaque déplacement de message dans la canvas
COTE_MESSAGE = 4

LONGUEUR_BOUTON = COTE_CANVAS/60
LONGUEUR_ENTRY = COTE_CANVAS/60

NOMBRE_LIGNE_CANVAS = 50

CLE_ENTRY_SLOT = 1		#La clé de l'entry du slot pour le dictionnaire des entrys
CLE_ENTRY_NOEUD = 2		#La clé de l'entry du noeud pour le dictionnaire des entrys
CLE_ENTRY_LAMBDA = 3		#La clé de l'entry du lambda pour le dictionnaire des entrys
CLE_ENTRY_LAMBDA_BURST = 4		#La clé de l'entry du lambda burst pour le dictionnaire des entrys
CLE_ENTRY_LIMITE_MESSAGE = 5	#La clé de l'entry de la limite minimal du nombre de message

TIC = 600	#Temps d'attente entre chaque mouvement de l'anneau, envoi de message etc

global tache
tache = None

global LABEL_TIC
LABEL_TIC = None

global TEXTS_NOEUDS
TEXTS_NOEUDS = None

global DICT_TEXTES_NOEUDS
DICT_TEXTES_NOEUDS = {}

PERIODE_MESSAGE_ANTENNE = 100
STATHAM_MODE = False

""" Les variables pour l'hyper exponentielle """
PROBABILITE_BURST = 0.01
global LAMBDA
LAMBDA = 10

global LAMBDA_BURST
LAMBDA_BURST = 140

LIMITE_NOMBRE_MESSAGE_MAX = 80

global LIMITE_NOMBRE_MESSAGE_MIN
LIMITE_NOMBRE_MESSAGE_MIN = 60

# # # # # # # # # # # # # # # #		V U E	# # # # # # # # # # # # # # # #

##	Créer une fenetre Tkinter avec son titre.
#	@return La fenêtre Tkinter créée.
def creer_fenetre():
	fenetre = Tk()
	if STATHAM_MODE:
		titre = "Jason Statham : <3"
	else:
		titre = "Simulation N-GREEN"
	fenetre.title(titre)

	return fenetre

##	Créer un canvas avec une croix au centre et le place dans la fenetre.
#	@param fenetre : La fenetre Tkinter ou le canvas sera ajouté.
#	@return Le canvas créé.
def creer_canvas(fenetre):
	canvas = Canvas(fenetre, width=COTE_CANVAS, height=COTE_CANVAS, background='#909090')

	#Création de la croix au centre du canvas
	canvas.create_line(COTE_CANVAS/2, 0, COTE_CANVAS/2, COTE_CANVAS, fill="White")
	canvas.create_line(0, COTE_CANVAS/2, COTE_CANVAS, COTE_CANVAS/2, fill="White")

	canvas.grid(row=0, column=1, rowspan=NOMBRE_LIGNE_CANVAS, columnspan=4)

	return canvas

##	Place sur le canvas donnée en paramètre les slots et renvoie un tableau contenant :
#	En indice 0 les slots du modele
#	En indice 1 les slots de la vue.
#	@param fenetre : La fenetre sur laquelle se situe le canvas passé en paramètre.
#	@param canvas : Le canvas sur lequel on place les slots graphiques.
#	@return En indice 0 les slots du modèle, en indice 1 les slots de la vue.
def placer_slots(fenetre, canvas):
	slots_vue = [None] * NOMBRE_SLOT	#Tableau qui contiendra les rectangles représentant les slots du modèle
	slots_modele = [ None ] * NOMBRE_SLOT

	#Le point du milieu
	milieu_x = COTE_CANVAS/2
	milieu_y = COTE_CANVAS/2
	for i in range(1, NOMBRE_SLOT+1):
		val_cos = cos(2*i*pi/NOMBRE_SLOT)
		val_sin = sin(2*i*pi/NOMBRE_SLOT)
		nouveau_x = milieu_x + val_cos * DISTANCE_SLOT
		nouveau_y = milieu_y - val_sin * DISTANCE_SLOT

		slots_vue[i-1] = canvas.create_rectangle(nouveau_x - COTE_SLOT, nouveau_y - COTE_SLOT, nouveau_x + COTE_SLOT, nouveau_y + COTE_SLOT)
		slots_modele[i-1] = Slot(i, None, None, val_cos, val_sin)
		canvas.create_text(nouveau_x, nouveau_y)
	return slots_modele, slots_vue


##	Place sur la toile les noeuds et renvoie un tableau contenant :
#	En indice 0 les noeuds du modele.
#	En indice 1 les noeuds de la vue.
#	En indice 2 les slots du modèle.
#	@param fenetre : La fenetre sur laquelle se situe le canvas passé en paramètre.
#	@param canvas : Le canvas sur lequel on place les slots graphiques.
#	@param slots_modele : Les slots du modele
#	@param slots_vue : Les slots de la vue
#	@return En indice 0 les noeuds du modèle, en indice 1 les noeuds de la vue, en indice 2 les slots du modèle.
def placer_noeuds(fenetre, canvas, slots_modele, slots_vue):
	global TEXTS_NOEUDS
	global DICT_TEXTES_NOEUDS

	noeuds_vue = [None] * NOMBRE_NOEUD
	noeuds_modele = [None] * NOMBRE_NOEUD
	TEXTS_NOEUDS = [None] * NOMBRE_NOEUD

	pas = NOMBRE_SLOT // NOMBRE_NOEUD

	for j in range(NOMBRE_NOEUD):
		indice_slot_accessible = (( (j*pas) + ((j+1)*pas) ) / 2) - 1

		debut_periode = int(random.uniform(0, 99))	#Le décalage entre chaque récéption de message émis par les antennes

		if j == 0 or j == NOMBRE_NOEUD-1:	#L'anneau doit contenir deux noeuds n'étant liés avec aucunes antennes
			nb_antenne = 0
		else:
			nb_antenne = int(random.uniform(1, 5))	#Au maximum 5 antennes

		noeuds_modele[j] = Noeud(indice_slot_accessible, indice_slot_accessible-1, COULEURS_MESSAGE[j], nb_antenne, debut_periode)

		slots_modele[ indice_slot_accessible ].indice_noeud_lecture = j
		slots_modele[ indice_slot_accessible -1 ].indice_noeud_ecriture = j

		""" Modification des couleur des slots """
		couleur = noeuds_modele[j].couleur
		canvas.itemconfig(slots_vue[indice_slot_accessible], outline=couleur)
		canvas.itemconfig(slots_vue[indice_slot_accessible-1], outline=couleur)

		""" Calcule de la position du noeud """
		milieu_x = COTE_CANVAS/2
		milieu_y = COTE_CANVAS/2

		""" Calcule de l'abscisse du noeud en fonction de la position du slot """
		x1 = milieu_x + slots_modele [ indice_slot_accessible ].val_cos * DISTANCE_NOEUD
		x2 = milieu_x + slots_modele [ indice_slot_accessible -1 ].val_cos * DISTANCE_NOEUD
		x = (x1 + x2) / 2

		""" Calcule de l'ordonné du noeud en fonction de la position du slot """
		y1 = milieu_y - slots_modele [ indice_slot_accessible ].val_sin * DISTANCE_NOEUD
		y2 = milieu_y - slots_modele [ indice_slot_accessible -1 ].val_sin * DISTANCE_NOEUD
		y = (y1 + y2) / 2

		noeuds_vue[j] = canvas.create_rectangle( x - COTE_NOEUD, y - COTE_NOEUD, x + COTE_NOEUD, y + COTE_NOEUD, fill=COULEURS_MESSAGE[j] )
		canvas.tag_bind(noeuds_vue[j], "<Button-1>", callback_click_noeud)

		""" #le texte du rectangle """
		TEXTS_NOEUDS[j] = canvas.create_text(x, y, text="0")
		canvas.tag_bind(TEXTS_NOEUDS[j], "<Button-1>", callback_click_texte)

		DICT_TEXTES_NOEUDS[ TEXTS_NOEUDS[j] ] = noeuds_modele[j]

	return noeuds_modele, noeuds_vue, slots_modele


##	Place un message à un point de départ et le fait se déplacer jusqu'a un point d'arrivé.
#	@param fenetre : La fenetre sur laquelle se situe le canvas passé en paramètre.
#	@param canvas : Le canvas sur lequel on place le message.
#	@param depart : Les coordonnees de départ du message.
#	@param arrive : Les coordonnees d'arrivée du message.
#	@param couleur_message : La couleur du message.
#	@return L'id du message créé.

def placer_message_graphique(canvas, depart, arrive, couleur_message):
	coordonnees = canvas.coords(depart)

	depart_x = (coordonnees[0] + coordonnees[2])/2
	depart_y = (coordonnees[1] + coordonnees[3])/2

	coordonnees = canvas.coords(arrive)

	arrivee_x = (coordonnees[0] + coordonnees[2])/2
	arrivee_y = (coordonnees[1] + coordonnees[3])/2

	""" Le point est placé """
	if not STATHAM_MODE:
		objet = canvas.create_rectangle(depart_x-COTE_MESSAGE, depart_y-COTE_MESSAGE, depart_x+COTE_MESSAGE, depart_y+COTE_MESSAGE, fill=couleur_message)
	else:
		objet = canvas.create_image(depart_x-COTE_MESSAGE, depart_y-COTE_MESSAGE, image=IMAGE_JASON)
	""" On fait se déplacer le message """
	t = Thread(target=deplacer_vers, args=(canvas, objet, arrivee_x, arrivee_y))
	t.start()

	return objet

##	place le panel gauche de la fenetre contenant les boutons:
#	- Start.
#	- Stop.
#	- Restart.
#	- Augmenter vitesse.
#	- Diminuer vitesse.
#	@param fenetre : La fenetre sur laquelle on place le panel.
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
	bouton_reset = Button(fenetre, text ="Recommencer", command = reset, image = IMAGES[ len(IMAGES) -1 ], bg="White", activebackground="#E8E8E8")
	bouton_reset.grid(row=4)
	label_restart = Label(fenetre, text="Recommencer")
	label_restart.grid(row=5)

	replay = Image.open("../images/vitesse_up.png")
	IMAGES.append( ImageTk.PhotoImage(replay) )
	bouton_reset = Button(fenetre, text ="UP", command = augmenter_vitesse, image = IMAGES[ len(IMAGES) -1 ], bg="White", activebackground="#E8E8E8")
	bouton_reset.grid(row=7)
	label_restart = Label(fenetre, text="Modifier vitesse")
	label_restart.grid(row=8)

	vitesse_down = Image.open("../images/vitesse_down.png")
	IMAGES.append( ImageTk.PhotoImage(vitesse_down) )
	bouton_down = Button(fenetre, text ="DOWN", command = diminuer_vitesse, image = IMAGES[ len(IMAGES) -1 ], bg="White", activebackground="#E8E8E8")
	bouton_down.grid(row=9)


##	Place le panel bas affichant les informations courantes ainsi que moyens de modifier les valeurs suivantes:
#	- Le nombre de slot utilisé.
#	- Le nombre de Noeud présent.
#	- Le lambda actuellement utilisé.
#	- le lambda burst actuellement utilisé.
#	- Et la limite minimal des noeuds pour evoyer un message.
#	Le panel contient aussi un bouton de validation des données.
#	Si aucunes données n'est saisi pour un champs, la valeur de la configuration précèdente est consérvée.
#	@param fenetre : La fenetre sur laquelle on place le panel gauche.
def placer_panel_bas(fenetre):
	nombre_slot = len( controleur.slots_modele )
	nombre_noeud = len( controleur.noeuds_modele )

	""" Les labels présentant les nombres de slots, de noeuds, le lambda actuel ainsi que le TIC en milliseconde """
	label_slot_actuel = Label(fenetre, text = "Nombre de slot : "+str(nombre_slot) )
	label_noeud_actuel = Label(fenetre, text = "Nombre de noeud : "+str(nombre_noeud) )
	label_lambda_actuel = Label(fenetre, text = "Lambda actuel : "+str(LAMBDA) )
	label_lambda_burst_actuel = Label(fenetre, text = "Lambda Burst : "+str(LAMBDA_BURST) )
	label_limite_taille_message_min = Label(fenetre, text = "Nombre de message minimum : "+str(LIMITE_NOMBRE_MESSAGE_MIN) )

	label_slot_actuel.grid(row=NOMBRE_LIGNE_CANVAS+1, column=1, sticky='W')
	label_noeud_actuel.grid(row=NOMBRE_LIGNE_CANVAS+2, column=1, sticky='W')
	label_lambda_actuel.grid(row=NOMBRE_LIGNE_CANVAS+3, column=1, sticky='W')
	label_lambda_burst_actuel.grid(row=NOMBRE_LIGNE_CANVAS+4, column=1, sticky='W')
	label_limite_taille_message_min.grid(row=NOMBRE_LIGNE_CANVAS+5, column=1, sticky='W')
	update_label_TIC(fenetre, NOMBRE_LIGNE_CANVAS+6, 1)

	""" Les labels des entry pour un nouveau nombre de slot/noeud """
	label_nouveau_slot = Label(fenetre, text = "Nouveau nombre de slot : ")
	label_nouveau_noeud = Label(fenetre, text = "Nouveau nombre de noeud : ")
	label_nouveau_lambda = Label(fenetre, text = "Nouvelle valeur du lambda : ")
	label_nouveau_lambda_burst = Label(fenetre, text = "Nouvelle valeur du lambda Burst : ")
	label_nouvelle_limite = Label(fenetre, text = "Nouvelle valeur pour le nombre de message minimum : ")

	label_nouveau_slot.grid(row=NOMBRE_LIGNE_CANVAS+1, column=2, sticky='W')
	label_nouveau_noeud.grid(row=NOMBRE_LIGNE_CANVAS+2, column=2, sticky='W')
	label_nouveau_lambda.grid(row=NOMBRE_LIGNE_CANVAS+3, column=2, sticky='W')
	label_nouveau_lambda_burst.grid(row=NOMBRE_LIGNE_CANVAS+4, column=2, sticky='W')
	label_nouvelle_limite.grid(row=NOMBRE_LIGNE_CANVAS+5, column=2, sticky='W')

	""" Les entry """
	entry_slot = Entry(fenetre, width=LONGUEUR_ENTRY)
	entry_noeud = Entry(fenetre, width=LONGUEUR_ENTRY)
	entry_lambda = Entry(fenetre, width=LONGUEUR_ENTRY)
	entry_lambda_burst = Entry(fenetre, width=LONGUEUR_ENTRY)
	entry_limite_message = Entry(fenetre, width=LONGUEUR_ENTRY)

	""" Ajout d'un event """
	entry_slot.bind("<Key>", callback_validation_configuration)
	entry_noeud.bind("<Key>", callback_validation_configuration)
	entry_lambda.bind("<Key>", callback_validation_configuration)
	entry_lambda_burst.bind("<Key>", callback_validation_configuration)
	entry_limite_message.bind("<Key>", callback_validation_configuration)

	controleur.entrys[CLE_ENTRY_SLOT] = entry_slot
	controleur.entrys[CLE_ENTRY_NOEUD] = entry_noeud
	controleur.entrys[CLE_ENTRY_LAMBDA] = entry_lambda
	controleur.entrys[CLE_ENTRY_LAMBDA_BURST] = entry_lambda_burst
	controleur.entrys[CLE_ENTRY_LIMITE_MESSAGE] = entry_limite_message

	entry_slot.grid(row=NOMBRE_LIGNE_CANVAS+1, column=3, sticky='W')
	entry_noeud.grid(row=NOMBRE_LIGNE_CANVAS+2, column=3, sticky='W')
	entry_lambda.grid(row=NOMBRE_LIGNE_CANVAS+3, column=3, sticky='W')
	entry_lambda_burst.grid(row=NOMBRE_LIGNE_CANVAS+4, column=3, sticky='W')
	entry_limite_message.grid(row=NOMBRE_LIGNE_CANVAS+5, column=3, sticky='W')

	""" le bouton """
	bouton_reset = Button(fenetre, text ="Valider", command = modifier_configuration, bg="YellowGreen", fg="White", activebackground="#7ba428", activeforeground="White", width=LONGUEUR_BOUTON)
	bouton_reset.grid(row=NOMBRE_LIGNE_CANVAS+7, column=4, sticky='E')


##	Met a jour le label du panel bas affichant le TIC en millisecondes.
#	@param fenetre : La fenetre sur laquelle on se situe le label que l'on souhaite modifier.
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
	LABEL_TIC.grid(row=NOMBRE_LIGNE_CANVAS+6, column=1, sticky='W')


##	Déplace dans le canvas un objet vers un point d'arrivé définit par arrivee_x et arrivee_y.
#	@param canvas : Le canvas sur lequel se situe l'objet que l'on souhaite déplacer.
#	@param objet : L'objet que l'on souhaite déplacer.
#	@param arrivee_x : Le point d'arrivé x que l'on souhaite pour l'objet.
#	@param arrivee_y : Le point d'arrivé y que l'on souhaite pour l'objet.
def deplacer_vers(canvas, objet, arrivee_x, arrivee_y):
	""" Convertie les coordonnees en int afin de récupérer la partie entiere des nombres, ainsi les coordonnees coïncideront toujours """
	objet_x = int(canvas.coords(objet)[0])
	objet_y = int(canvas.coords(objet)[1])

	""" Calcule la taille de la forme de l'objet passé """

	if not STATHAM_MODE:
		canvas.coords(objet, objet_x - COTE_MESSAGE, objet_y - COTE_MESSAGE, objet_x + COTE_MESSAGE, objet_y + COTE_MESSAGE)
		arrivee_x = int(arrivee_x) - COTE_MESSAGE
		arrivee_y = int(arrivee_y) - COTE_MESSAGE
	else:
		canvas.coords(objet, objet_x, objet_y)
		arrivee_x = int(arrivee_x) + COTE_SLOT/8		#L'image ne se place pas de la meme manière qu'un rectangle
		arrivee_y = int(arrivee_y) + COTE_SLOT/8		#Il faut donc réajuster son point d'arrivé.

	while objet_x != arrivee_x or objet_y != arrivee_y:
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


##	Fait sortir graphiquement un mssage du canvas.
#	@param canvas : Le canvas sur lequel se situe le message que l'on souhaite sortir.
#	@param message : Le message que l'on souhaite sortir.
def sortir_message_graphique(canvas, message):
	""" L'appelle à la méthode sleep permet de laisser le temps à Tkinter de mettre à jour le canvas """
	time.sleep( float(TIC) / float(1000) )

	x = int(canvas.coords(message)[0])
	y = int(canvas.coords(message)[1])

	""" Mise en place des directions pour les abscisses et les ordonnées """
	if x > COTE_CANVAS/2:
		direction_x = 1
		objectif_x = COTE_CANVAS
	elif x < COTE_CANVAS/2:
		direction_x = -1
		objectif_x = 0
	else:
		direction_x = 0
		objectif_x = x

	if y > COTE_CANVAS/2 :
		direction_y = 1
		objectif_y = COTE_CANVAS
	elif y < COTE_CANVAS/2:
		direction_y = -1
		objectif_y = 0
	else:
		direction_y = 0
		objectif_y = y

	while x != objectif_x or y != objectif_y:
		canvas.move(message, direction_x, direction_y)
		x = int(canvas.coords(message)[0])
		y = int(canvas.coords(message)[1])

		time.sleep(VITESSE_LATENCE_MESSAGE)

		""" Si un bord du canvas est atteint on supprime le message du canvas """
		if x == 0 or x == COTE_CANVAS or y == 0 or y == COTE_CANVAS:
			canvas.delete(message)
			break


# # # # # # # # # # # # # # # #		M O D E L E		# # # # # # # # # # # # # # # #

##	Représente un noeud dans le système, un noeuds peux stocker des messages.
class Noeud:


	##	Constructeur d'un noeud.
	#	@param self : L'objet de la classe.
	#	@param indice_slot_lecture : L'indice du slot en lecture.
	#	@param indice_slot_ecriture : L'indice du slot en ecriture.
	#	@param couleur : La couleur graphique du noeud.
	#	@param nb_antenne : Le nombre d'antenne du noeud.
	#	@param debut_periode : Le début de la période du noeud pour recevoir des messages des antennes.
	def __init__(self, indice_slot_lecture, indice_slot_ecriture, couleur, nb_antenne, debut_periode):
		self.nb_message = 0
		self.indice_slot_lecture = indice_slot_lecture
		self.indice_slot_ecriture = indice_slot_ecriture
		self.couleur = couleur
		self.nb_antenne = nb_antenne	#Indique le nombre d'antenne auquel est lié le noeud
		self.debut_periode = debut_periode		#Le décalage selon lequel le noeud recoit des messages des antennes
		self.messages = deque()		#File FIFO contenant les TIC d'arrivé des messages
		self.attente_max = 0		#Le temps d'attente maximal dans le noeud
		self.nb_message_total = 0
		self.attente_totale = 0


	##	renvoie l'équalité entres deux noeuds.
	#	@param self : Le premier noeud.
	#	@param autre_noeud : Le second noeud.
	#	@return True si les noeuds sont les mêmes, False sinon.
	def equals(self, autre_noeud):
		return self.couleur == autre_noeud.couleur


	##	Ajoute un message au noeud.
	#	@param self : Le noeud.
	#	@param message : Le message à ajouter au noeud.
	def ajouter_message(self, message):
		self.messages.append(message)
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

		controleur.canvas.delete(TEXTS_NOEUDS[indice_noeud])

		TEXTS_NOEUDS[indice_noeud] = controleur.canvas.create_text(x, y, text= str(noeud_modele.nb_message) )
		controleur.canvas.tag_bind(TEXTS_NOEUDS [indice_noeud], "<Button-1>", callback_click_texte)

		DICT_TEXTES_NOEUDS[ TEXTS_NOEUDS[indice_noeud] ] = controleur.noeuds_modele [indice_noeud]


	##	Renvoie le noeud sous forme de chaine de caractères.
	#	@param self : Le noeud.
	#	@return Le noeud sous forme de chaine de caractères.
	def __str__(self):
		return str(self.couleur)

	##	Met à jour le temps d'attente des messages du noeud.
	#	@param self : Le noeud.
	def update_attente(self):
		for message in self.messages:
			self.attente_totale += 1


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


##	Représente un paquet de message curculant dans l'anneau : contient à la fois les coordonnées graphiques du messages, l'indice du noeud auquel il appartient,
#	l'id du paquet le représentant graphiquement ainsi que la taille du paquet.
#	Il contient aussi un tableau contenant les messages du paquet.
class PaquetMessage:

	##	Le constructeur d'un paquet de message.
	#	@param self : le PaquetMessage.
	#	@param id_message : L'id du message.
	#	@param indice_noeud_emetteur : L'indice du noeud emetteur du paquet.
	#	@param taille : La taille du paquet.
	#	@param messages : Les messages du paquet.
	def __init__(self, id_message, indice_noeud_emetteur, taille, messages):
		self.id_message_graphique = id_message
		self.indice_noeud_emetteur = indice_noeud_emetteur
		self.x = None
		self.y = None
		self.taille = None	#La taille du paquet
		self.messages = messages


	##	Met a jour la position graphique du message.
	#	@param self : le PaquetMessage.
	#	@param nouveau_x : La nouvelle coordonnée X du message.
	#	@param nouveau_y : La nouvelle coordonnée Y du message.
	def update_position(self, nouveau_x, nouveau_y):
		self.x = nouveau_x
		self.y = nouveau_y

	##	Renvoie le paquet sous forme de chaine de caractères.
	#	@param self : le PaquetMessage.
	#	@return Le paquet sous forme de chaine de caractères.
	def __str__(self):
		global controleur
		return "Message envoyé par le noeud  : "+str(controleur.noeuds_modele[self.indice_noeud_emetteur].couleur)


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
	if effectuer_tirage(PROBABILITE_BURST) == True:		#Le tirage est tombé sur la faible proba
		return LAMBDA_BURST
	else:
		u = random.uniform(0, 1)
		return loi_de_poisson_naif(u)

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


# # # # # # # # # # # # # # # #		C O N T R O L E U R		# # # # # # # # # # # # # # # #

##	Classe représentant le système que l'on souhaite modéliser dans sa globalité
#	Elle fait l'intermédiaire entre le modèle et la vue.
class Controleur:

	##	Le constructeur d'un Controleur.
	#	@param self : L'objet Controleur.
	#	@param fenetre : La fenêtre Tkinter de la simulation.
	#	@param canvas : Le canvas de la simulation.
	#	@param slots_vue : Les slots de la vue de la simulation.
	#	@param slots_modele : Les slost du modèle de la simulation.
	#	@param noeuds_vue : Les noeuds de la vue de la simulation.
	#	@param noeuds_modele : Les noeuds du modèle de la simulation.
	def __init__(self, fenetre, canvas, slots_vue, slots_modele, noeuds_vue, noeuds_modele):
		self.fenetre = fenetre
		self.canvas = canvas
		self.slots_vue = slots_vue
		self.slots_modele = slots_modele
		self.noeuds_vue = noeuds_vue
		self.noeuds_modele = noeuds_modele
		self.continuer = False		#Booléen indiquant s'il faut effectuer d'autres tics ou non
		self.entrys = {}	#Un dictionnaire des entry de l'interface
		self.nb_tic = 0


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
	while i < NOMBRE_NOEUD -1 and controleur.noeuds_vue[i] != id_objet:
		controleur.noeuds_vue[i]
		i += 1

	if controleur.noeuds_vue[i] == id_objet:	#On a trouvé le noeud !
		afficher_dialogue_noeud( controleur.noeuds_modele[i], etat_continuer )


##	Fonction callback d'un clique sur le texte d'un noeud.
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
			message = "Nombre de message : "+str( noeud.nb_message )
			message += "\nAttente moyenne des messages : "+str(attente_moyenne_arrondie)
			message += "\nAttente maximale des messages : "+str(attente_max)+"."
		else:
			message = "Le noeud n'a pas encore envoyé de message dans l'anneau."

	else:
		message = "Ce noeud n'a encore reçu aucun message."
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
#	Ici on supprime le canvas et on en crée un nouveau. Les paramètres sont ceux utilisé pour la précédente configuration.
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
	controleur.fenetre.after(TIC, initialisation, (fenetre) )


##	Commence la rotaion. Méthode appeler lors d'un clique sur le bouton de commencement.
def commencer_rotation():
	global controleur
	global tache

	if not controleur.continuer:
		controleur.continuer = True


## Arrête la rotaion. Méthode appeler lors d'un clique sur le bouton de fin.
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
	global NOMBRE_NOEUD
	global NOMBRE_SLOT
	global LAMBDA
	global LAMBDA_BURST
	global LIMITE_NOMBRE_MESSAGE_MIN

	tmp_noeud = NOMBRE_NOEUD
	tmp_slot = NOMBRE_SLOT
	tmp_lambda = LAMBDA
	tmp_limite_message = LIMITE_NOMBRE_MESSAGE_MIN
	nb_champ_vide = 0

	erreur = False

	valeur_noeud = controleur.entrys[ CLE_ENTRY_NOEUD ].get()
	valeur_slot = controleur.entrys[ CLE_ENTRY_SLOT ].get()
	valeur_lambda = controleur.entrys[ CLE_ENTRY_LAMBDA ].get()
	valeur_lambda_burst = controleur.entrys[ CLE_ENTRY_LAMBDA_BURST ].get()
	valeur_limite_message = controleur.entrys[ CLE_ENTRY_LIMITE_MESSAGE ].get()

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
			NOMBRE_NOEUD = int_valeur_noeud
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
			NOMBRE_SLOT = int_valeur_slot
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
			LAMBDA = valeur_lambda
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
			LAMBDA_BURST = valeur_lambda_burst
	else:
		nb_champ_vide += 1

	if valeur_limite_message != "":
		valeur_limite_message = int(valeur_limite_message)
		if valeur_lambda_burst <= 0 or valeur_limite_message > LIMITE_NOMBRE_MESSAGE_MAX:
			message = "Le nombre de message minimum doit être positif est inférieur à la limite maximum (ici 80)."
			tkMessageBox.showerror("Erreur Limite di nombre de message minimum !", message)
			erreur = True
		else:
			LIMITE_NOMBRE_MESSAGE_MIN = valeur_limite_message
	else:
		nb_champ_vide += 1

	if erreur or nb_champ_vide == len(controleur.entrys):
		NOMBRE_NOEUD = tmp_noeud
		NOMBRE_SLOT = tmp_slot
		LAMBDA = tmp_lambda
		LIMITE_NOMBRE_MESSAGE_MIN = tmp_limite_message
	else:	#Il n'y a aucune erreur, on redéfinit la nouvelle configuration
		reset()
		tkMessageBox.showinfo("Chargement", "Votre nouvelle configuration est en cours de chargement !;)")


##	Stop l'appli en faisant attention aux thread restants.
def arreter_appli():
	arreter_rotation()
	afficher_stat_noeud()
	fenetre.destroy()


##	Action de faire entrer un paquet de message d'un noeud jusqu'à son slot.
def placer_message(indice_noeud, messages):
	global controleur

	noeud_modele = controleur.noeuds_modele[ indice_noeud ]
	indice_slot = controleur.noeuds_modele[ indice_noeud ].indice_slot_ecriture
	slot_modele = controleur.slots_modele[ indice_slot ]
	message = ""
	erreur = False
	if slot_modele == 1:
		erreur = True
		message = "Le slot est déjà remplis, "
	if noeud_modele == 0:
		erreur = True
		message += "Le noeud est vide"
	if not erreur:
		""" Récupération des valeurs """
		canvas = controleur.canvas
		noeud_graphique = controleur.noeuds_vue[ indice_noeud ]
		slot_graphique = controleur.slots_vue[indice_slot]
		couleur_message = controleur.noeuds_modele[ indice_noeud ].couleur

		""" Création du message """
		id_message_graphique = placer_message_graphique(canvas, noeud_graphique, slot_graphique, couleur_message)
		controleur.slots_modele[indice_slot].paquet_message = PaquetMessage( id_message_graphique, indice_noeud, len(messages), messages)

		""" Mise à jour de la distance """
		message_x = canvas.coords(id_message_graphique)[0]
		message_y = canvas.coords(id_message_graphique)[1]
		controleur.slots_modele[indice_slot].paquet_message.update_position(message_x, message_y)

		""" Met à jour les temps d'attentes du noeud qui envoi le message """
		for message in messages:
			if message != None:
				temps_attente_message = (controleur.nb_tic - message.TIC_arrive)
				if temps_attente_message > noeud_modele.attente_max:
					noeud_modele.attente_max = temps_attente_message
				noeud_modele.attente_totale += temps_attente_message

	else:	#Une erreur est survenue, on affiche un message
		print message


##	Exécute une rotation des messages dans l'anneau.
def rotation_message():
	global controleur

	decaler_messages()
	sortir_message()
	entrer_message()


##	Fait entrer dans l'anneau des messages.
#	Ici les arrivées de messages sont gérées par l'hyper exponentielle et des files d'attentes.
def entrer_message():
	global controleur

	for i in range (NOMBRE_SLOT):		#Parcours des slots de l'anneau
		slot = controleur.slots_modele[i]
		if slot.indice_noeud_ecriture != None:	#Le slot est un slot d'ecriture
			noeud = controleur.noeuds_modele[ slot.indice_noeud_ecriture ]

			""" Le slot affiche si c'est sa période de réception de message provenant des antennes """
			if controleur.nb_tic % PERIODE_MESSAGE_ANTENNE == noeud.debut_periode:		#C'est la periode du noeud, il reçoit un message de ses antennes
				print "C'est le moment ! Periode du noeud : ", noeud.debut_periode, ". Je recois un message provenant de mes ", noeud.nb_antenne, " antennes."

			nb_message = hyper_expo()	#Le nombre de message Best Effort reçu est géré par l'hyper exponentielle

			""" On ajoute au noeud le tic d'arrivé des messages """
			for i in range(nb_message):
					noeud.ajouter_message( MessageN(controleur.nb_tic) )

			noeud.nb_message += nb_message
			if slot.paquet_message == None and noeud.nb_message >= LIMITE_NOMBRE_MESSAGE_MIN:		#Le slot peut recevoir un message et le noeud peut enenvoyer un
				if noeud.nb_message >= LIMITE_NOMBRE_MESSAGE_MAX:
					""" On enleve les messages du noeud """
					messages = [None] * LIMITE_NOMBRE_MESSAGE_MAX
					for i in range(LIMITE_NOMBRE_MESSAGE_MAX):
						messages.append( noeud.messages.popleft() )

					noeud.nb_message -= LIMITE_NOMBRE_MESSAGE_MAX
				else:		#Le nombre de message est compris entre le minimum est le maximum, on vide donc le noeud
					""" On enleve les messages du noeud """
					messages = [None] * noeud.nb_message
					for i in range(noeud.nb_message):
							messages.append( noeud.messages.popleft() )
					noeud.nb_message = 0
				placer_message( slot.indice_noeud_ecriture, messages )
			noeud.update_file_noeud_graphique()


##	Fait sortir du système un mesage.
def sortir_message():
	global controleur

	""" Fais sortir les messages qui repassent devant leur Noeud emetteur """
	for slot in controleur.slots_modele:
		paquet_message = slot.paquet_message

		if paquet_message and slot.indice_noeud_lecture != None and paquet_message.indice_noeud_emetteur == slot.indice_noeud_lecture:
			t = Thread(target=sortir_message_graphique, args=(controleur.canvas, slot.paquet_message.id_message_graphique) )
			t.start()
			slot.paquet_message = None


##	Methode appelant une methode récursive qui décale d'un slot les message du système.
def decaler_messages():
	global controleur

	tempon = controleur.slots_modele[1].paquet_message

	decaler_messages2(0, 0, tempon, True)


##	Méthode récursive qui décale les messages de l'anneau.
def decaler_messages2(premier_indice, indice_slot, paquet_message, premier_appel):
	global controleur

	milieu_x = COTE_CANVAS/2
	milieu_y = COTE_CANVAS/2

	destination_x = milieu_x + cos(2*indice_slot*pi/NOMBRE_SLOT) * DISTANCE_SLOT
	destination_y = milieu_y - sin(2*indice_slot*pi/NOMBRE_SLOT) * DISTANCE_SLOT

	msg = controleur.slots_modele[indice_slot].paquet_message
	if msg != None:
		""" On déplace le message """
		t = Thread(target=deplacer_vers, args=( controleur.canvas, msg.id_message_graphique, destination_x, destination_y ))
		t.start()

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


##	calculer le temps de latence entre chaque mouvement de pixel lors d'un déplacement de message
#	Le calcul prend en compte la distance à parcourir entre chaque déplacement.
def calculer_vitesse():
	""" Coefficent multiplant le nombre maximum de pixel afin de s'assurer que les threads ont
		suffisament de temps pour finir de bouger les messages """
	matela_securite = 100

	milieu_x = COTE_CANVAS/2
	milieu_y = COTE_CANVAS/2

	""" Ici on choisi deux slots voisins et on calcul la distance entre ces deux slots """
	x1 = milieu_x + cos(0/NOMBRE_SLOT) * DISTANCE_SLOT
	y1 = milieu_y - sin(0/NOMBRE_SLOT) * DISTANCE_SLOT

	x2 = milieu_x + cos(2*pi/NOMBRE_SLOT) * DISTANCE_SLOT
	y2 = milieu_y - sin(2*pi/NOMBRE_SLOT) * DISTANCE_SLOT

	distance_max = max( abs(x1 - x2), abs(y1 - y2) ) #* matela_securite

	global VITESSE_LATENCE_MESSAGE

	""" Le résultat est en milliseconde, il faut donc le diviser par 1000 pour l'obtenir en seconde """
	pixel_par_seconde = (TIC/distance_max) / (1000 * matela_securite)

	arrondi = format(pixel_par_seconde, '.5f')

	VITESSE_LATENCE_MESSAGE = float(arrondi)

# # # # # # # # # #		M E T H O D E S		M A I N		# # # # # # # # # # # #


##	Met en place le canvas.
#	@param fenetre : La fenetre sur laquelle on place le canvas.
def initialisation(fenetre):
	global controleur
	global IMAGE_JASON

	""" On détruit tout les widgets de la fenêtre afin que celle-ci soit toute belle """
	for widget in fenetre.winfo_children():
	    widget.destroy()

	""" Mise en place du canvas et des données du controleur """
	canvas = creer_canvas(fenetre)
	IMAGE_JASON = PhotoImage(file="../images/jason_statham.png")

	slots = placer_slots(fenetre, canvas)
	slots_modele = slots[0]
	slots_vue = slots[1]

	noeuds = placer_noeuds(fenetre, canvas, slots_modele, slots_vue)

	noeuds_modele = noeuds[0]
	noeuds_vue = noeuds[1]
	slots_modele = noeuds[2]

	controleur = Controleur(fenetre, canvas, slots_vue, slots_modele, noeuds_vue, noeuds_modele)

	calculer_vitesse()

	placer_panel_gauche(fenetre)
	placer_panel_bas(fenetre)

	effectuer_tic()

##	Attend un TIC et effectue une rotation des messages.
def effectuer_tic():
	global controleur
	global tache

	if controleur.continuer == True:
		controleur.nb_tic += 1
		print "Nombre de TIC : ", controleur.nb_tic

		rotation_message()

		for noeud in controleur.noeuds_modele:
			noeud.update_attente()

	tache = controleur.fenetre.after(TIC, effectuer_tic )


##	Affiche l'état des slots de l'anneau.
def afficher_message_anneau():
	global controleur
	for i in range (NOMBRE_SLOT):
		if controleur.slots_modele[i].paquet_message == None:
			print "Le slot ", controleur.slots_vue[i], " ne contient pas de message"
		else:
			print "Le slot ", controleur.slots_vue[i], " contient un message mis par le noeud ", controleur.noeuds_modele[ controleur.slots_modele[i].paquet_message.indice_noeud_emetteur ]


##	Affiche les statistiques liés aux temps d'attente des noeuds.
def afficher_stat_noeud():
	global controleur

	print "\n######### STATS #######"
	for noeud in controleur.noeuds_modele:
		if noeud.nb_message_total != 0:
			attente_moyenne = float(noeud.attente_totale) / float(noeud.nb_message_total)
			attente_moyenne_arrondie = format(attente_moyenne, '.2f')
			print "Noeud "+str(noeud)+" Attente moyenne : "+str( attente_moyenne_arrondie )+" Attente max : "+str(noeud.attente_max)
	print ""


# # # # # # # # # # # # # # # #		M A I N 	# # # # # # # # # # # # # # # #

if len(sys.argv) == 2:	#Un argument à été donnée
	valeur_pour_statham = ["jason_statham", "Jason", "Statham", "Jason_Statham", "JASON", "STATHAM", "JASON_STATHAM", "STATHAM_MODE", "True", "true", "TRUE"]

	if str(sys.argv[1]) in valeur_pour_statham:		#On active le STATHAM MDOE !!!
		print "On active le STATHAM MDOE !!!"
		STATHAM_MODE = True

global controleur
controleur = None

fenetre = creer_fenetre()
fenetre.protocol("WM_DELETE_WINDOW", arreter_appli)		#Réagie à la demande d'un utilisateur de quitter l'application via la croix graphique

initialisation(fenetre)
fenetre.mainloop()
