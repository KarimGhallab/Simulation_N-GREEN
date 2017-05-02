#coding: utf8

"""
	Ce script permet de réaliser une simulation d'un anneau en réseau dans le cadre du projet N-GREEN.
	Auteur : Ghallab Karim.
"""

import tkMessageBox
import time
import random
import sys

from Tkinter import Tk, Canvas, Button, Label, Entry, PhotoImage
from math import cos, sin, pi, exp
from threading import Thread
from PIL import Image, ImageTk
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
COULEUR_NOEUD = "CadetBlue3"	#La couleur graphique d'un noeud

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

PERIODE_MESSAGE_ANTENNE = 100
STATHAM_MODE = False

#Les variables pour l'hyper exponentielle
PROBABILITE_BURST = 0.01
global LAMBDA
LAMBDA = 1

global LAMBDA_BURST
LAMBDA_BURST = 140

LIMITE_NOMBRE_MESSAGE_MAX = 80

global LIMITE_NOMBRE_MESSAGE_MIN
LIMITE_NOMBRE_MESSAGE_MIN = 60

# # # # # # # # # # # # # # # #		V U E	# # # # # # # # # # # # # # # #

def creer_fenetre():
	"""
		Créer une fenetre Tkinter avec son titre.
	"""

	# On crée une fenêtre, racine de notre interface
	fenetre = Tk()
	if STATHAM_MODE:
		titre = "Jason Statham : <3"
	else:
		titre = "Simulation N-GREEN"
	fenetre.title(titre)

	return fenetre


def creer_canvas(fenetre):
	"""
		Créer un canvas avec une croix au centre et le place dans la fenetre.
		fenetre est la fenetre Tkinter ou le canvas sera ajouté.
	"""

	canvas = Canvas(fenetre, width=COTE_CANVAS, height=COTE_CANVAS, background='#909090')

	#Création de la croix au centre du canvas
	canvas.create_line(COTE_CANVAS/2, 0, COTE_CANVAS/2, COTE_CANVAS, fill="White")
	canvas.create_line(0, COTE_CANVAS/2, COTE_CANVAS, COTE_CANVAS/2, fill="White")

	canvas.grid(row=0, column=1, rowspan=NOMBRE_LIGNE_CANVAS, columnspan=4)

	return canvas


def placer_slots(fenetre, canvas):
	"""
		Place sur le canvas donnée en paramètre les slots et renvoie un tableau contenant :
		En indice 0 les slots du modele
		En indice 1 les slots de la vue.
	"""

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


def placer_noeuds(fenetre, canvas, slots_modele, slots_vue):
	"""
		Place sur la toile les noeuds et renvoie un tableau contenant :
		En indice 0 les noeuds du modele.
		En indice 1 les noeuds de la vue.
		En indice 2 les slots du modèle.
	"""

	global TEXTS_NOEUDS

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

		#Modification des couleur des slots
		couleur = noeuds_modele[j].couleur
		canvas.itemconfig(slots_vue[indice_slot_accessible], outline=couleur)
		canvas.itemconfig(slots_vue[indice_slot_accessible-1], outline=couleur)

		#Calcule de la position du noeud
		milieu_x = COTE_CANVAS/2
		milieu_y = COTE_CANVAS/2

		#Calcule de l'abscisse du noeud en fonction de la position du slot
		x1 = milieu_x + slots_modele [ indice_slot_accessible ].val_cos * DISTANCE_NOEUD
		x2 = milieu_x + slots_modele [ indice_slot_accessible -1 ].val_cos * DISTANCE_NOEUD
		x = (x1 + x2) / 2

		#Calcule de l'ordonné du noeud en fonction de la position du slot
		y1 = milieu_y - slots_modele [ indice_slot_accessible ].val_sin * DISTANCE_NOEUD
		y2 = milieu_y - slots_modele [ indice_slot_accessible -1 ].val_sin * DISTANCE_NOEUD
		y = (y1 + y2) / 2

		noeuds_vue[j] = canvas.create_rectangle( x - COTE_NOEUD, y - COTE_NOEUD, x + COTE_NOEUD, y + COTE_NOEUD, fill=COULEURS_MESSAGE[j] )

		#le texte du rectangle
		TEXTS_NOEUDS[j] = canvas.create_text(x, y, text="0")
	return noeuds_modele, noeuds_vue, slots_modele


def placer_message_graphique(canvas, depart, arrive, couleur_message):
	"""
		Place un message à un point de départ et le fait se déplacer jusqu'a un point d'arrivé.
	"""

	coordonnees = canvas.coords(depart)

	depart_x = (coordonnees[0] + coordonnees[2])/2
	depart_y = (coordonnees[1] + coordonnees[3])/2

	coordonnees = canvas.coords(arrive)

	arrivee_x = (coordonnees[0] + coordonnees[2])/2
	arrivee_y = (coordonnees[1] + coordonnees[3])/2

	#Le point est placé
	if not STATHAM_MODE:
		objet = canvas.create_rectangle(depart_x-COTE_MESSAGE, depart_y-COTE_MESSAGE, depart_x+COTE_MESSAGE, depart_y+COTE_MESSAGE, fill=couleur_message)
	else:
		objet = canvas.create_image(depart_x-COTE_MESSAGE, depart_y-COTE_MESSAGE, image=IMAGE_JASON)
	#On fait se déplacer le message
	t = Thread(target=deplacer_vers, args=(canvas, objet, arrivee_x, arrivee_y))
	t.start()

	return objet


def placer_panel_gauche(fenetre):
	"""
		place le panel gauche de la fenetre contenant les boutons:
			- Start.
			- Stop.
			- Restart.
			- Augmenter vitesse.
			- Diminuer vitesse.
	"""

	play = Image.open("./images/play.png")
	IMAGES.append( ImageTk.PhotoImage(play) )
	bouton_play = Button(fenetre, command = commencer_rotation, image = IMAGES[ len(IMAGES) -1 ], bg="White", activebackground="#E8E8E8")
	bouton_play.grid(row=0)
	label_play = Label(fenetre, text="Commencer/reprendre")
	label_play.grid(row=1)

	stop = Image.open("./images/stop.png")
	IMAGES.append( ImageTk.PhotoImage(stop) )
	bouton_stop = Button(fenetre, command = arreter_rotation, image = IMAGES[ len(IMAGES) -1 ], bg="White", activebackground="#E8E8E8")
	bouton_stop.grid(row=2)
	label_stop = Label(fenetre, text="Arrêter")
	label_stop.grid(row=3)

	replay = Image.open("./images/restart.png")
	IMAGES.append( ImageTk.PhotoImage(replay) )
	bouton_reset = Button(fenetre, text ="Recommencer", command = reset, image = IMAGES[ len(IMAGES) -1 ], bg="White", activebackground="#E8E8E8")
	bouton_reset.grid(row=4)
	label_restart = Label(fenetre, text="Recommencer")
	label_restart.grid(row=5)

	replay = Image.open("./images/vitesse_up.png")
	IMAGES.append( ImageTk.PhotoImage(replay) )
	bouton_reset = Button(fenetre, text ="UP", command = augmenter_vitesse, image = IMAGES[ len(IMAGES) -1 ], bg="White", activebackground="#E8E8E8")
	bouton_reset.grid(row=7)
	label_restart = Label(fenetre, text="Modifier vitesse")
	label_restart.grid(row=8)

	vitesse_down = Image.open("./images/vitesse_down.png")
	IMAGES.append( ImageTk.PhotoImage(vitesse_down) )
	bouton_down = Button(fenetre, text ="DOWN", command = diminuer_vitesse, image = IMAGES[ len(IMAGES) -1 ], bg="White", activebackground="#E8E8E8")
	bouton_down.grid(row=9)


def placer_panel_bas(fenetre):
	"""
		Place le panel bas affichant les informations courantes ainsi que moyens de modifier les valeurs suivantes:
			- Le nombre de slot utilisé.
			- Le nombre de Noeud présent.
			- Le lambda actuellement utilisé.
			- le lambda burst actuellement utilisé.
			- Et la limite minimal des noeuds pour evoyer un message.

		Le panel contient aussi un bouton de validation des données.
		Si aucunes données n'est saisi pour un champs, la valeur de la configuration précèdente est consérvée.
	"""

	nombre_slot = len( controleur.slots_modele )
	nombre_noeud = len( controleur.noeuds_modele )

	#Les labels présentant les nombres de slots, de noeuds, le lambda actuel ainsi que le TIC en milliseconde
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

	#Les labels des entry pour un nouveau nombre de slot/noeud
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

	#Les entry
	entry_slot = Entry(fenetre, width=LONGUEUR_ENTRY)
	entry_noeud = Entry(fenetre, width=LONGUEUR_ENTRY)
	entry_lambda = Entry(fenetre, width=LONGUEUR_ENTRY)
	entry_lambda_burst = Entry(fenetre, width=LONGUEUR_ENTRY)
	entry_limite_message = Entry(fenetre, width=LONGUEUR_ENTRY)

	#Ajout d'un event
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

	#le bouton
	bouton_reset = Button(fenetre, text ="Valider", command = modifier_configuration, bg="YellowGreen", fg="White", activebackground="#7ba428", activeforeground="White", width=LONGUEUR_BOUTON)
	bouton_reset.grid(row=NOMBRE_LIGNE_CANVAS+7, column=4, sticky='E')


def update_label_TIC(fenetre, ligne, colonne):
	"""
		Met a jour le label du panel bas affichant le TIC en millisecondes.
	"""

	global LABEL_TIC

	if LABEL_TIC != None:
		LABEL_TIC.destroy()

	if TIC <= 600:
		message = "TIC : "+str(TIC)+" millisecondes, on est au max !"
	else:
		message = "TIC : "+str(TIC)+" millisecondes"
	LABEL_TIC = Label(fenetre, text = message)
	LABEL_TIC.grid(row=NOMBRE_LIGNE_CANVAS+6, column=1, sticky='W')


def deplacer_vers(canvas, objet, arrivee_x, arrivee_y):
	"""
		Déplace dans le canvas un objet vers un point d'arrivé définit par arrivee_x et arrivee_y.
	"""

	#Convertie les coordonnees en int afin de récupérer la partie entiere des nombres, ainsi les coordonnees coïncideront toujours
	objet_x = int(canvas.coords(objet)[0])
	objet_y = int(canvas.coords(objet)[1])

	#Calcule la taille de la forme de l'objet passé

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


def sortir_message_graphique(canvas, message):
	"""
		Fait sortir graphiquement un mssage du canvas.
	"""

	#L'appelle à la méthode sleep permet de laisser le temps à Tkinter de mettre à jour le canvas
	time.sleep( float(TIC) / float(1000) )

	x = int(canvas.coords(message)[0])
	y = int(canvas.coords(message)[1])

	#Mise en place des directions pour les abscisses et les ordonnées
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

		#Si un bord du canvas est atteint on supprime le message du canvas
		if x == 0 or x == COTE_CANVAS or y == 0 or y == COTE_CANVAS:
			canvas.delete(message)
			break


# # # # # # # # # # # # # # # #		M O D E L E		# # # # # # # # # # # # # # # #

class Noeud:
	"""
		Représente un noeud dans le système, un noeuds peux stocker des messages.
	"""

	def __init__(self, indice_slot_lecture, indice_slot_ecriture, couleur, nb_antenne, debut_periode):
		"""
			Constructeur d'un noeud.
			Il prend en argument l'indice de son slot de lecture, l'indice de son slot d'ecriture, sa couleur (graphique), son nombre d'antenne, ainsi que le décalage en nombre de TIC pour la récéption de message des antennes.
		"""

		self.nb_message = 0
		self.indice_slot_lecture = indice_slot_lecture
		self.indice_slot_ecriture = indice_slot_ecriture
		self.couleur = couleur
		self.nb_antenne = nb_antenne	#Indique le nombre d'antenne auquel est lié le noeuds
		self.debut_periode = debut_periode		#Le décalage selon lequel le noeud recoit des messages des antennes


	def equals(self, autre_noeud):
		"""
			renvoie l'équalité entres deux noeuds.
		"""

		return self.couleur == autre_noeud.couleur


	def update_file_noeud_graphique(self):
		"""
			Met a jour le texte affichant le nombre de message en attente dans le noeud.
		"""

		global controleur

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


	def __str__(self):
		"""
			Renvoie le noeud sous forme de chaine de caractères.
		"""

		return str(self.couleur)

class Slot:

	"""
		Repprésente un slot dans l'anneau, il a un id qui lui est propres ainsi qu'un paquet de message et un indice vers le noeud qui lui accède.
	"""
	def __init__(self, id, indice_noeud_lecture, indice_noeud_ecriture, val_cos, val_sin):
		self.id = id
		self.paquet_message = None	#Indique si le slot possede un paquet de message
		self.indice_noeud_lecture = indice_noeud_lecture		#Si le slot ne peut accèder a aucun noeud, ce champs vaut None
		self.indice_noeud_ecriture = indice_noeud_ecriture
		self.val_cos = val_cos
		self.val_sin = val_sin

	"""
		Renvoie le slot sous forme de chaine de caractères.
	"""
	def __str__(self):
		if self.paquet_message == None:
			return "Je peux accèder au noeud : "+str(self.indice_noeud_accessible)+" Je ne possede pas de message"
		else:
			return "Je peux accèder au noeud : "+str(self.indice_noeud_accessible)+" Je possede un message"


class PaquetMessage:
	"""
		Représente un paquet de message : contient à la fois les coordonnées graphiques du messages, l'indice du noeud auquel il appartient,
		l'id du paquet le représentant graphiquement ainsi que la taille du paquet.
	"""
	def __init__(self, id_message, indice_noeud_emetteur):
		"""
			Le constructeur d'un paquet de message.
			Il prend en paramètre l'id du message graphique et l'indice du noeud emetteur.
		"""
		self.id_message_graphique = id_message
		self.indice_noeud_emetteur = indice_noeud_emetteur
		self.x = None
		self.y = None
		self.taille = None	#La taille du paquet


	def update_position(self, nouveau_x, nouveau_y):
		"""
			Met a jour la position graphique du message.
		"""

		self.x = nouveau_x
		self.y = nouveau_y


	def __str__(self):
		"""
			Renvoie le paquet sous forme de chaine de caractères.
		"""

		global controleur
		return "Message envoyé par le noeud  : "+str(controleur.noeuds_modele[self.indice_noeud_emetteur].couleur)


	def equals(self, autre_message):
		"""
			Retourne l'equalité entre deux messages.
		"""

		return self.id_message_graphique == autre_message.id_message_graphique


###########################################################
############ Partie tirage/hyper exponentielle ############
###########################################################

def effectuer_tirage(probabilite):
	"""
		Effectue un tirage et renvoie True ou False si la variable tirée est contenu dans la probabilité passée en paramètre.
	"""

	tirage = random.uniform(0, 1)
	return tirage <= probabilite


def hyper_expo():
	"""
		Réalise le tirage selon l'hyper exponentielle.
	"""

	if effectuer_tirage(PROBABILITE_BURST) == True:		#Le tirage est tombé sur la faible proba
		return LAMBDA_BURST
	else:
		u = random.uniform(0, 1)
		return loi_de_poisson_naif(u)


def loi_de_poisson_naif(u):
	"""
		Calcule le nombre de message Best Effort transmis par un noeud.
	"""

	p = exp (- LAMBDA)
	x = 0
	f = p
	while (u > f):
		x += 1
		p = p*LAMBDA/x
		f += p
	return x


# # # # # # # # # # # # # # # #		C O N T R O L E U R		# # # # # # # # # # # # # # # #

class Controleur:
	"""
		Classe représentant le système que l'on souhaite modéliser dans sa globalité
		Elle fera l'intermédiaire entre le modèle et la vue.
	"""


	def __init__(self, fenetre, canvas, slots_vue, slots_modele, noeuds_vue, noeuds_modele):
		"""
			Le constructeur.
		"""
		self.fenetre = fenetre
		self.canvas = canvas
		self.slots_vue = slots_vue		#La représentation des slots dans le canvas (un tableau de rectangle)
		self.slots_modele = slots_modele		#Un tableau représentant les slots, chaque case dispose de deux etats si elle dispose ou non d'un message
		self.noeuds_vue = noeuds_vue		#La représentation des noeuds dans le canvas
		self.noeuds_modele = noeuds_modele	#Un tableau de Noeud
		self.continuer = False		#Booléen indiquant s'il faut effectuer d'autres tics ou non
		self.entrys = {}	#Un dictionnaire des entry de l'interface
		self.nb_tic = 0


###########################################################
################ Les listeners des boutons ################
###########################################################

def callback_validation_configuration(event):
	"""
		Gére les inputs au clavier d'un utilisteur lorsqu'il saisie une nouvelle configuration pour l'anneau
	"""

	if event.char == '\r':		#Le bouton entrée
		modifier_configuration()


def reset():
	"""
		Callback au bouton demandant un reset de l'application
		Ici on supprime le canvas et on en crée un nouveau. Les paramètres sont ceux utilisé pour la précédente configuration.
	"""

	global controleur
	global tache

	controleur.continuer = False
	controleur.nb_tic = 0

	#supprime le prochain tic s'il y a afin de ne pas faire planté les threads et l'interface
	if tache != None:
		controleur.fenetre.after_cancel(tache)

	#La méthode after permet ici de faire s'executer les threads en cours
	controleur.fenetre.after(TIC, initialisation, (fenetre) )

def commencer_rotation():
	"""
		Commence la rotaion. Méthode appeler lors d'un clique sur le bouton de commencement.
	"""

	global controleur
	global tache

	if not controleur.continuer:
		controleur.continuer = True


def arreter_rotation():
	"""
		Arrête la rotaion. Méthode appeler lors d'un clique sur le bouton de fin.
	"""

	global controleur
	global tache
	#supprime le prochain tic s'il y a afin de ne pas faire planté les threads et l'interface
	controleur.continuer = False


def augmenter_vitesse():
	"""
		Augmente la vitesse de rotation.
	"""

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


def diminuer_vitesse():
	"""
		Diminue la vitesse de rotation.
	"""

	global TIC

	TIC += 100
	if controleur.continuer == True:
		arreter_rotation()
		calculer_vitesse()
		commencer_rotation()
	else:
		calculer_vitesse()

	update_label_TIC(controleur.fenetre, NOMBRE_LIGNE_CANVAS+4, 1)


def modifier_configuration():
	"""
		Modifie la configuration de l'anneau en fonction des données saisies dans le panel bas.
	"""

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

	#Recupération de la valeur du noeud
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

	#Recupération de la valeur du slot
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

	#Recupération de la valeur du lambda
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

	#Recupération de la valeur du lambda burst
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

"""
	Stop l'appli en faisant attention aux thread restants.
"""
def arreter_appli():
	arreter_rotation()
	fenetre.destroy()


def placer_message(indice_noeud):
	"""
		Action de faire entrer un message d'un noeud jusqu'à son slot.
	"""

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
		#Récupération des valeurs
		canvas = controleur.canvas
		noeud_graphique = controleur.noeuds_vue[ indice_noeud ]
		slot_graphique = controleur.slots_vue[indice_slot]
		couleur_message = controleur.noeuds_modele[ indice_noeud ].couleur

		#Création du message
		id_message_graphique = placer_message_graphique(canvas, noeud_graphique, slot_graphique, couleur_message)
		controleur.slots_modele[indice_slot].paquet_message = PaquetMessage( id_message_graphique, indice_noeud)

		#Mise à jour de la distance
		message_x = canvas.coords(id_message_graphique)[0]
		message_y = canvas.coords(id_message_graphique)[1]
		controleur.slots_modele[indice_slot].paquet_message.update_position(message_x, message_y)


	else:	#Une erreur est survenue, on affiche un message
		print message


def rotation_message():
	"""
		Exécute une rotation des messages dans l'anneau.
	"""
	global controleur
	decaler_messages()
	sortir_message()
	entrer_message()


def entrer_message():
	"""
		Fait entrer dans l'anneau des messages.
		Ici les arrivées de messages sont gérées par l'hyper exponentielle et des files d'attentes.
	"""

	global controleur

	for i in range (NOMBRE_SLOT):		#Parcours des slots de l'anneau
		slot = controleur.slots_modele[i]
		if slot.indice_noeud_ecriture != None:	#Le slot est un slot d'ecriture
			noeud = controleur.noeuds_modele[ slot.indice_noeud_ecriture ]

			#Le slot affiche si c'est sa période de réception de message provenant des antennes
			if controleur.nb_tic % PERIODE_MESSAGE_ANTENNE == noeud.debut_periode:		#C'est la periode du noeud, il reçoit un message de ses antennes
				print "C'est le moment ! Periode du noeud : ", noeud.debut_periode, ". Je recois un message provenant de mes ", noeud.nb_antenne, " antennes."

			nb_message = hyper_expo()	#Le nombre de message Best Effort reçu est géré par l'hyper exponentielle

			noeud.nb_message += nb_message
			if slot.paquet_message == None and noeud.nb_message >= LIMITE_NOMBRE_MESSAGE_MIN:		#Le slot peut recevoir un message et le noeud peut enenvoyer un
				if noeud.nb_message >= LIMITE_NOMBRE_MESSAGE_MAX:
					noeud.nb_message -= LIMITE_NOMBRE_MESSAGE_MAX
				else:		#Le nombre de message est compris entre le minimum est le maximum, on vide donc le noeud
					noeud.nb_message = 0
				placer_message( slot.indice_noeud_ecriture )
			noeud.update_file_noeud_graphique()


def sortir_message():
	"""
		Fait sortir du système un mesage.
	"""

	global controleur
	#Fais sortir les messages qui repassent devant leur Noeud emetteur
	for slot in controleur.slots_modele:
		paquet_message = slot.paquet_message

		if paquet_message and slot.indice_noeud_lecture != None and paquet_message.indice_noeud_emetteur == slot.indice_noeud_lecture:
			t = Thread(target=sortir_message_graphique, args=(controleur.canvas, slot.paquet_message.id_message_graphique) )
			t.start()
			slot.paquet_message = None


def decaler_messages():
	"""
		Methode appelant une methode récursive qui décale d'un slot les message du système.
	"""

	global controleur

	tempon = controleur.slots_modele[1].paquet_message

	decaler_messages2(0, 0, tempon, True)


def decaler_messages2(premier_indice, indice_slot, paquet_message, premier_appel):
	"""
		Méthode récursive qui décale les messages de l'anneau.
	"""

	global controleur

	milieu_x = COTE_CANVAS/2
	milieu_y = COTE_CANVAS/2

	destination_x = milieu_x + cos(2*indice_slot*pi/NOMBRE_SLOT) * DISTANCE_SLOT
	destination_y = milieu_y - sin(2*indice_slot*pi/NOMBRE_SLOT) * DISTANCE_SLOT

	msg = controleur.slots_modele[indice_slot].paquet_message
	if msg != None:
		#On déplace le message
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


def calculer_vitesse():
	"""
		calculer le temps de latence entre chaque mouvement de pixel lors d'un déplacement de message
		Le calcul prend en compte la distance à parcourir entre chaque déplacement.
	"""

	#Coefficent multiplant le nombre maximum de pixel afin de s'assurer que les threads ont
	#suffisament de temps pour finir de bouger les messages
	matela_securite = 100

	milieu_x = COTE_CANVAS/2
	milieu_y = COTE_CANVAS/2

	#Ici on choisi deux slots voisins et on calcul la distance entre ces deux slots
	x1 = milieu_x + cos(0/NOMBRE_SLOT) * DISTANCE_SLOT
	y1 = milieu_y - sin(0/NOMBRE_SLOT) * DISTANCE_SLOT

	x2 = milieu_x + cos(2*pi/NOMBRE_SLOT) * DISTANCE_SLOT
	y2 = milieu_y - sin(2*pi/NOMBRE_SLOT) * DISTANCE_SLOT

	distance_max = max( abs(x1 - x2), abs(y1 - y2) ) #* matela_securite

	global VITESSE_LATENCE_MESSAGE

	#Le résultat est en milliseconde, il faut donc le diviser par 1000 pour l'obtenir en seconde
	pixel_par_seconde = (TIC/distance_max) / (1000 * matela_securite)

	arrondi = format(pixel_par_seconde, '.5f')

	VITESSE_LATENCE_MESSAGE = float(arrondi)

# # # # # # # # # #		M E T H O D E S		M A I N		# # # # # # # # # # # #

def initialisation(fenetre):
	"""
		Met en place le canvas.
	"""

	global controleur
	global IMAGE_JASON

	#On détruit tout les widgets de la fenêtre afin que celle-ci soit toute belle
	for widget in fenetre.winfo_children():
	    widget.destroy()

	#Mise en place du canvas et des données du controleur
	canvas = creer_canvas(fenetre)
	IMAGE_JASON = PhotoImage(file="./images/jason_statham.png")

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


def effectuer_tic():
	"""
		Attend un TIC et effectue une rotation des messages.
	"""

	global controleur
	global tache

	if controleur.continuer == True:
		controleur.nb_tic += 1
		print "Nombre de TIC : ", controleur.nb_tic
		rotation_message()
	tache = controleur.fenetre.after(TIC, effectuer_tic )

def afficher_message_anneau():
	"""
		Affiche l'état des slots de l'anneau.
	"""

	global controleur
	for i in range (NOMBRE_SLOT):
		if controleur.slots_modele[i].paquet_message == None:
			print "Le slot ", controleur.slots_vue[i], " ne contient pas de message"
		else:
			print "Le slot ", controleur.slots_vue[i], " contient un message mis par le noeud ", controleur.noeuds_modele[ controleur.slots_modele[i].paquet_message.indice_noeud_emetteur ]


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
