#coding: utf8

from Tkinter import *
from math import cos, sin, pi
from threading import Thread
from PIL import Image, ImageTk
import tkMessageBox
import time
import random

# # # # # # # # # # # # # # # #		C O N S T A N T E	 # # # # # # # # # # # # # # # #

IMAGES = []

COULEURS_MESSAGE = ["yellowgreen", "orange", "turquoise", "royalblue", "purple", "teal", "tan", "snow", "mediumseagreen", "black", "Chartreuse", "CornflowerBlue", "DarkGray", "DarkOliveGreen", "DarkMagenta", "Lavender", "SandyBrown", "LightCoral"]

COTE_CANVAS = 700	#Définit la hauteur/largeur de la toile sur laquelle seront déssinés les slots et les noeuds

global NOMBRE_SLOT
NOMBRE_SLOT = 25		#Le nombre de slot du système
COTE_SLOT = 15		#La hauteur/largeur d'un slot
DISTANCE_SLOT = COTE_CANVAS/3	#La distance d'un slot par rapport à l'axe central du canvas

global NOMBRE_NOEUD
NOMBRE_NOEUD = 8	#Le nombre de noeud du système
COTE_NOEUD = COTE_SLOT + 5		#La hauteur/largeur d'un noeud
DISTANCE_NOEUD = DISTANCE_SLOT + 50		#La distance d'un noeud par rapport à l'axe central du canvas
COULEUR_NOEUD = "CadetBlue3"	#La couleur graphique d'un noeud

global VITESSE_LATENCE_MESSAGE
VITESSE_LATENCE_MESSAGE = 0.002		#Le temps d'attente en seconde entre chaque déplacement de message dans la canvas
COTE_MESSAGE = 4

LONGUEUR_BOUTON = COTE_CANVAS/60
LONGUEUR_ENTRY = COTE_CANVAS/100

NOMBRE_LIGNE_CANVAS = 100

CLE_ENTRY_SLOT = 1
CLE_ENTRY_NOEUD = 2
CLE_ENTRY_PROBA = 3

TIC = 500	#Temps d'attente entre chaque mouvement de l'anneau, envoi de message etc

global PROBABILITE
PROBABILITE = 0.33

global tache
tache = None

# # # # # # # # # # # # # # # #		V U E	# # # # # # # # # # # # # # # #

def creer_fenetre():
	# On crée une fenêtre, racine de notre interface
	fenetre = Tk()
	fenetre.grid_columnconfigure(0, weight=1)
	fenetre.title("Jason Statham : <3")
	
	return fenetre


def creer_canvas(fenetre):
	canvas = Canvas(fenetre, width=COTE_CANVAS, height=COTE_CANVAS, background='AntiqueWhite3')
	ligne1 = canvas.create_line(COTE_CANVAS/2, 0, COTE_CANVAS/2, COTE_CANVAS)
	ligne2 = canvas.create_line(0, COTE_CANVAS/2, COTE_CANVAS, COTE_CANVAS/2)
	
	canvas.grid(row=0, column=1, rowspan=NOMBRE_LIGNE_CANVAS, columnspan=4)
	
	return canvas

"""
	Place sur la toile les slots et renvoie un tableau contenant :
	En indice 0 les slots du modele
	En indice 1 les slots de la vue
"""
def placer_slots(fenetre, canvas):
	slots_vue = [None] * NOMBRE_SLOT	#Tableau qui contiendra les rectangles représentant les slots du modèle
	slots_modele = [ None ] * NOMBRE_SLOT
	
	#Le point du milieu
	milieu_x = COTE_CANVAS/2
	milieu_y = COTE_CANVAS/2
	
	for i in range(1, NOMBRE_SLOT+1):
		nouveau_x = milieu_x + cos(2*i*pi/NOMBRE_SLOT) * DISTANCE_SLOT
		nouveau_y = milieu_y - sin(2*i*pi/NOMBRE_SLOT) * DISTANCE_SLOT
		
		slots_vue[i-1] = canvas.create_rectangle(nouveau_x - COTE_SLOT, nouveau_y - COTE_SLOT, nouveau_x + COTE_SLOT, nouveau_y + COTE_SLOT)
		slots_modele[i-1] = Slot(i, None)
		texte = canvas.create_text(nouveau_x, nouveau_y, text="S "+str(slots_vue[i-1]) )
	return slots_modele, slots_vue


"""
	Place sur la toile les noeuds et renvoie un tableau contenant :
	En indice 0 les noeuds du modele
	En indice 1 les noeuds de la vue
"""
def placer_noeuds(fenetre, canvas, slots_modele, slots_vue):
	noeuds_vue = [None] * NOMBRE_NOEUD
	noeuds_modele = [None] * NOMBRE_NOEUD
	
	milieu_x = COTE_CANVAS/2
	milieu_y = COTE_CANVAS/2
	
	pas = NOMBRE_SLOT // NOMBRE_NOEUD
	
	for j in range(NOMBRE_NOEUD):
		indice_slot_accessible = j*pas - 1
		noeuds_modele[j] = Noeud(indice_slot_accessible, COULEURS_MESSAGE[j], PROBABILITE)
		
		slots_modele[ indice_slot_accessible ].indice_noeud_accessible = j
		
		x = milieu_x + cos(2*j*pas*pi/NOMBRE_SLOT) * DISTANCE_NOEUD
		y = milieu_y - sin(2*j*pas*pi/NOMBRE_SLOT) * DISTANCE_NOEUD
		noeuds_vue[j] = canvas.create_rectangle( x - COTE_NOEUD, y - COTE_NOEUD, x + COTE_NOEUD, y + COTE_NOEUD, fill=COULEURS_MESSAGE[j] )
		
		#le texte du rectangle
		texte = canvas.create_text(x, y, text="N "+str(noeuds_vue[j]))
	return noeuds_modele, noeuds_vue, slots_modele
			
"""
	Place un message à un point de départ et le fait se déplacer jusqu'a un point d'arrivé
"""
def placer_message_graphique(canvas, depart, arrive, couleur_message):
	coordonnees = canvas.coords(depart)
	
	depart_x = (coordonnees[0] + coordonnees[2])/2
	depart_y = (coordonnees[1] + coordonnees[3])/2
	
	coordonnees = canvas.coords(arrive)
	
	arrivee_x = (coordonnees[0] + coordonnees[2])/2
	arrivee_y = (coordonnees[1] + coordonnees[3])/2
	
	#Le point est placé
	message = canvas.create_rectangle(depart_x-COTE_MESSAGE, depart_y-COTE_MESSAGE, depart_x+COTE_MESSAGE, depart_y+COTE_MESSAGE, fill=couleur_message)
	
	#On fait se déplacer le message
	t = Thread(target=deplacer_vers, args=(canvas, message, arrivee_x, arrivee_y))
	t.start()
	
	return message


"""
	place le panel gauche de la fenetre contenant les boutons:
		- Start
		- Stop
		- Restart
"""
def placer_panel_gauche(fenetre):
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
	bouton_reset.grid(row=6)
	label_restart = Label(fenetre, text="Modifier vitesse")
	label_restart.grid(row=7)
	
	vitesse_down = Image.open("./images/vitesse_down.png")
	IMAGES.append( ImageTk.PhotoImage(vitesse_down) )
	bouton_down = Button(fenetre, text ="DOWN", command = diminuer_vitesse, image = IMAGES[ len(IMAGES) -1 ], bg="White", activebackground="#E8E8E8")
	bouton_down.grid(row=8)
	
	

	
"""
	Place le panel bas affichant les informations courantes ainsi que moyens de modifier les valeurs suivantes:
		- Le nombre de slot utilisé
		- Le nombre de Noeud présent
		- La probabilité unitaire des noeuds
	Le panel contient aussi un bouton de validation des données
	Si aucunes données n'est saisi pour un champs, la valeur de la configuration précèdente est consérvée'
"""	
def placer_panel_bas(fenetre):
	nombre_slot = len( controleur.slots_modele )
	nombre_noeud = len( controleur.noeuds_modele )
	proba = controleur.noeuds_modele[0].probabilite
	
	#Les labels présentant les nombres de slots, de noeuds ainsi que la proba actuel
	label_slot_actuel = Label(fenetre, text = "Nombre de slot : "+str(nombre_slot) )
	label_noeud_actuel = Label(fenetre, text = "Nombre de noeud : "+str(nombre_noeud) )
	label_proba_actuelle = Label(fenetre, text = "Probabilité actuel : "+str(proba) )
	
	label_slot_actuel.grid(row=NOMBRE_LIGNE_CANVAS+1, column=1, sticky='W')
	label_noeud_actuel.grid(row=NOMBRE_LIGNE_CANVAS+2, column=1, sticky='W')
	label_proba_actuelle.grid(row=NOMBRE_LIGNE_CANVAS+3, column=1, sticky='W')
	
	#Les labels des entry pour un nouveau nombre de slot/noeud
	label_nouveau_slot = Label(fenetre, text = "Nouveau nombre de slot : ")
	label_nouveau_noeud = Label(fenetre, text = "Nouveau nombre de noeud : ")
	label_nouvelle_proba = Label(fenetre, text = "Nouvelle valeur de la probabilité : ")
	
	label_nouveau_slot.grid(row=NOMBRE_LIGNE_CANVAS+1, column=2, sticky='W')
	label_nouveau_noeud.grid(row=NOMBRE_LIGNE_CANVAS+2, column=2, sticky='W')
	label_nouvelle_proba.grid(row=NOMBRE_LIGNE_CANVAS+3, column=2, sticky='W')
	
	#Les entry
	entry_slot = Entry(fenetre, width=LONGUEUR_ENTRY)
	entry_noeud = Entry(fenetre, width=LONGUEUR_ENTRY)
	entry_proba = Entry(fenetre, width=LONGUEUR_ENTRY)
	
	controleur.entrys[CLE_ENTRY_SLOT] = entry_slot
	controleur.entrys[CLE_ENTRY_NOEUD] = entry_noeud
	controleur.entrys[CLE_ENTRY_PROBA] = entry_proba
	
	entry_slot.grid(row=NOMBRE_LIGNE_CANVAS+1, column=3, sticky='W')
	entry_noeud.grid(row=NOMBRE_LIGNE_CANVAS+2, column=3, sticky='W')
	entry_proba.grid(row=NOMBRE_LIGNE_CANVAS+3, column=3, sticky='W')
	
	#le bouton
	bouton_reset = Button(fenetre, text ="Valider", command = modifier_configuration, bg="YellowGreen", fg="White", activebackground="#7ba428", activeforeground="White", width=LONGUEUR_BOUTON)
	bouton_reset.grid(row=NOMBRE_LIGNE_CANVAS+4, column=4, sticky='E')

""" 
	Déplace dans le canvas un objet vers un point d'arrivé définit par arrivee_x et arrivee_y
"""
def deplacer_vers(canvas, objet, arrivee_x, arrivee_y):
	#Convertie les coordonnees en int afin de récupérer la partie entiere des nombres, ainsi les coordonnees coïncideront toujours
	objet_x = int(canvas.coords(objet)[0])
	objet_y = int(canvas.coords(objet)[1])
	
	canvas.coords(objet, objet_x-COTE_MESSAGE, objet_y-COTE_MESSAGE, objet_x+COTE_MESSAGE, objet_y+COTE_MESSAGE)
	
	arrivee_x = int(arrivee_x)
	arrivee_y = int(arrivee_y)
	cmpt = 0
	while objet_x != arrivee_x or objet_y != arrivee_y:
		if objet_x < arrivee_x:
			canvas.move(objet, 1, 0)
		elif objet_x > arrivee_x:
			canvas.move(objet, -1, 0)
		if objet_y < arrivee_y:
			canvas.move(objet, 0, 1)
		elif objet_y > arrivee_y:
			canvas.move(objet, 0, -1)
		cmpt += 1
		objet_x = canvas.coords(objet)[0]
		objet_y = canvas.coords(objet)[1]
		time.sleep(VITESSE_LATENCE_MESSAGE)
	#print "Nombre de déplacement : "+str(cmpt)

"""
	Fonction faisant sortir de l'interface un message
"""
def sortir_message_graphique(canvas, message):
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

"""
	Représente un noeud dans le système, un noeuds peux stocker des messages
"""
class Noeud:
	def __init__(self, indice_slot_accessible, couleur, probabilite):
		self.nb_message = 0
		self.indice_slot_accessible = indice_slot_accessible
		self.couleur = couleur
		self.probabilite = probabilite
		self.vient_de_sortir_message = False

class Slot:
	def __init__(self, id, indice_noeud_accessible):
		self.id = id
		self.message = None
		self.indice_noeud_accessible = indice_noeud_accessible		#Si le slot ne peut accèder a aucun noeud, ce champs vaut None

	def set_message(self, message):
		self.message = message
	
	def __str__(self):
		if self.message == None:
			return "Je peux accèder au noeud : "+str(self.indice_noeud_accessible)+" Je ne possede pas de message"
		else:
			return "Je peux accèder au noeud : "+str(self.indice_noeud_accessible)+" Je possede un message"


"""
	Représente un message : contient à la fois les coordonées graphiques du messages, l'indice du slot auquel il appartient ainsi 		que l'emetteur du message
"""

class Message:
	def __init__(self, id_message, indice_noeud_emetteur):
		self.id_message_graphique = id_message
		self.indice_noeud_emetteur = indice_noeud_emetteur
		self.x = None
		self.y = None
		self.a_bouge = False	#Indique si le message à bougé graphiquement
	
	def update_position(self, nouveau_x, nouveau_y):
		self.x = nouveau_x
		self.y = nouveau_y
	
	def __str__(self):
		global controleur
		return "Message envoyé par le noeud  : "+str(controleur.noeuds_modele[self.indice_noeud_emetteur].couleur)
		
	def equals(self, autre_message):
		return self.id_message_graphique == autre_message.id_message_graphique

		
"""
	Effectue un tirage et renvoie True ou False si la variable tirée est contenu dans la probabilité passée en paramètre
"""			
def effectuer_tirage(probabilite):
	tirage = random.uniform(0, 1)
	return tirage <= probabilite
	

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
		self.continuer = False		#Booléen indiquant s'il faut effectuer d'autres tics ou non
		self.entrys = {}	#Un dictionnaire des entry de l'interface


###########################################################
################ Les listeners des boutons ################
###########################################################
"""
	Callback au bouton demandant un reset de l'application
	Ici on supprime le canvas et on en crée un nouveau. Les paramètres sont ceux utilisé pour la précédente configuration
"""
def reset():
	global controleur
	global tache
	
	controleur.continuer = False
	
	#supprime le prochain tic s'il y a afin de ne pas faire planté les threads et l'interface
	if tache != None:
		controleur.fenetre.after_cancel(tache)
		
	#La méthode after permet ici de faire s'executer les threads en cours
	controleur.fenetre.after(TIC, initialisation, (fenetre) )
	
def commencer_rotation():
	global controleur
	global tache

	if not controleur.continuer:
		controleur.continuer = True
		tache = controleur.fenetre.after(0, effectuer_tic)


def arreter_rotation():
	global controleur
	global tache
	#supprime le prochain tic s'il y a afin de ne pas faire planté les threads et l'interface
	if tache != None:
		controleur.fenetre.after_cancel(tache)
	controleur.continuer = False

"""
	Augmente la vitesse de rotation
"""
def augmenter_vitesse():
	global TIC
	global tache
	print tache

	arreter_rotation()
	if TIC - 100 >= 500:
		TIC -= 100
		calculer_vitesse()
	
		print "TIC : "+str(TIC)
	
		print "Latence ! "+str(VITESSE_LATENCE_MESSAGE)
		#effectuer_tic()

"""
	Diminue la vitesse de rotation
"""
def diminuer_vitesse():
	global TIC
	
	print "Diminution de la vitesse..."
	arreter_rotation()
	TIC += 100
	calculer_vitesse()

	print "TIC : "+str(TIC)

	print "Latence ! "+str(VITESSE_LATENCE_MESSAGE)


def modifier_configuration():
	global controleur
	global NOMBRE_NOEUD
	global NOMBRE_SLOT
	global PROBABILITE
	
	tmp_noeud = NOMBRE_NOEUD
	tmp_slot = NOMBRE_SLOT
	tmp_proba = PROBABILITE
	
	erreur = False
	
	valeur_noeud = controleur.entrys[ CLE_ENTRY_NOEUD ].get()
	valeur_slot = controleur.entrys[ CLE_ENTRY_SLOT ].get()
	valeur_proba = controleur.entrys[ CLE_ENTRY_PROBA ].get()
	
	if valeur_noeud != "":
		valeur_noeud = int(valeur_noeud)
		if valeur_noeud > len(COULEURS_MESSAGE):
			message = "Désolé mais nous ne pouvons produire plus de "+str( len(COULEURS_MESSAGE) )+" noeuds.\nAfin de pouvoir produire plus de noeud, demander à l'esclave d'ajouter des couleurs dans le tableau de couleur"
			tkMessageBox.showerror("Erreur nombre de noeud !", message)
			erreur = True
		elif valeur_noeud <= 0:
			message = "Le nombre de noeud doit etre supérieur à 0"
			tkMessageBox.showerror("Erreur nombre de noeud !", message)
			erreur = True
		else:
			NOMBRE_NOEUD = valeur_noeud
			
	if valeur_slot != "":
		valeur_slot = int(valeur_slot)
		if valeur_slot <= 0:
			message = "Le nombre de slot doit etre supérieur à 0"
			tkMessageBox.showerror("Erreur nombre de noeud !", message)
			erreur = True
		else:
			NOMBRE_SLOT = valeur_slot
	
	if valeur_noeud > valeur_slot:
		message = "Le nombre de noeud ne peut être supérieur au nombre de slot"
		tkMessageBox.showerror("Erreur nombre de noeud et nombre de slot!", message)
		erreur = True

	if valeur_proba != "":
		valeur_proba = float(valeur_proba)
		if valeur_proba > 1 or valeur_proba < 0:
			message = "Une probabilité doit être forcément comprise dans l'intervalle ] 0;1 ["
			tkMessageBox.showerror("Erreur probabilité !", message)
			erreur = True
		else:
			PROBABILITE = valeur_proba
	
	if erreur:
		NOMBRE_NOEUD = tmp_noeud
		NOMBRE_SLOT = tmp_slot
		PROBABILITE = tmp_proba
	else:
		reset()

	
"""
	Action de faire entrer un message d'un noeud jusqu'à son slot
"""
def placer_message(indice_noeud):
	global controleur
	noeud_modele = controleur.noeuds_modele[ indice_noeud ]
	indice_slot = controleur.noeuds_modele[ indice_noeud ].indice_slot_accessible
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
		controleur.slots_modele[indice_slot].set_message(Message( id_message_graphique, indice_noeud) )
		
		#Mise à jour de la distance
		message_x = canvas.coords(id_message_graphique)[0]
		message_y = canvas.coords(id_message_graphique)[1]
		controleur.slots_modele[indice_slot].message.update_position(message_x, message_y)
		
	
	else:	#Une erreur est survenue, on affiche un message
		print message


"""
	Exécute une rotation des messages dans l'anneau 

"""
def rotation_message():
	global controleur
	decaler_messages()
	sortir_message()
	entrer_message()


def entrer_message():
	global controleur
	#Fait entrer les messages selon un tirage
	for slot in controleur.slots_modele:
		if slot.indice_noeud_accessible != None and slot.message == None:	#Le slot peut recevoir un message
			noeud = controleur.noeuds_modele[ slot.indice_noeud_accessible ]
			if not noeud.vient_de_sortir_message:
			
				faire_tirage = effectuer_tirage(noeud.probabilite)
			
				if faire_tirage:
					placer_message( slot.indice_noeud_accessible )


"""
	Fait sortir du système un mesage
"""
def sortir_message():
	global controleur
	#Fais sortir les messages qui repassent devant leur Noeud emetteur
	for slot in controleur.slots_modele:
		message = slot.message
		
		if message and message.indice_noeud_emetteur == slot.indice_noeud_accessible:
			t = Thread(target=sortir_message_graphique, args=(controleur.canvas, slot.message.id_message_graphique) )
			t.start()
			slot.message = None
					
			controleur.noeuds_modele[ message.indice_noeud_emetteur ].vient_de_sortir_message = True
		elif slot.indice_noeud_accessible != None:
			controleur.noeuds_modele[ slot.indice_noeud_accessible ].vient_de_sortir_message = False
	
		
"""
	Methode appelant une methode récursive qui décale d'un slot les message du système
"""
def decaler_messages():
	global controleur

	tempon = controleur.slots_modele[1].message
	
	decaler_messages2(0, 0, tempon, True)

	
"""
	Méthode récursive qui décale les messages du système
"""
def decaler_messages2(premier_indice, indice_slot, message, premier_appel):
	global controleur
	
	milieu_x = COTE_CANVAS/2
	milieu_y = COTE_CANVAS/2

	destination_x = milieu_x + cos(2*indice_slot*pi/NOMBRE_SLOT) * DISTANCE_SLOT
	destination_y = milieu_y - sin(2*indice_slot*pi/NOMBRE_SLOT) * DISTANCE_SLOT
	
	msg = controleur.slots_modele[indice_slot].message
	if msg != None:
		t = Thread(target=deplacer_vers, args=( controleur.canvas, msg.id_message_graphique, destination_x, destination_y ))
		t.start()
	
	if indice_slot-1 < 0:
		nouvelle_indice = len(controleur.slots_modele) -1
	else:
		nouvelle_indice = indice_slot-1
		
	if indice_slot != premier_indice or premier_appel:
		tempon = controleur.slots_modele[indice_slot].message
		
		decaler_messages2(premier_indice, nouvelle_indice, tempon, False)
		controleur.slots_modele[indice_slot].message = message
	else:
		controleur.slots_modele[indice_slot].message = message


"""
	calculer le temps de latence entre chaque mouvement de pixel lors d'un déplacement de message
	Le calcul prend en compte la distance à parcourir entre chaque déplacement
"""
def calculer_vitesse():
	#Coefficent multiplant le nombre maximum de pixel afin de s'assurer que les threads ont
	#suffisament de temps pour finir de bouger les messages
	matela_securite = 1.5
	
	milieu_x = COTE_CANVAS/2
	milieu_y = COTE_CANVAS/2
	
	#Ici on choisi deux slots voisins et on calcul la distance entre ces deux slots
	x1 = milieu_x + cos(0/NOMBRE_SLOT) * DISTANCE_NOEUD
	y1 = milieu_y - sin(0/NOMBRE_SLOT) * DISTANCE_NOEUD
	
	x2 = milieu_x + cos(2*pi/NOMBRE_SLOT) * DISTANCE_NOEUD
	y2 = milieu_y - sin(2*pi/NOMBRE_SLOT) * DISTANCE_NOEUD
	
	distance_max = max( abs(x1 - x2), abs(y1 - y2) ) * matela_securite
	
	global VITESSE_LATENCE_MESSAGE
	
	#Le résultat est en miliseconde, il faut donc le diviser par 1000 pour l'obtenir en seconde
	pixel_par_seconde = (TIC/distance_max) / 1000
	
	arrondi = format(pixel_par_seconde, '.3f')
	
	VITESSE_LATENCE_MESSAGE = float(arrondi)
	
# # # # # # # # # #		M E T H O D E S		M A I N		# # # # # # # # # # # # 

"""
	Met en place le canvas
"""
def initialisation(fenetre):
	global controleur
	
	#premier appel à la méthode
	if controleur:
		controleur.canvas.destroy()		#On détruit le canvas précèdent
	
	#Mise en place du canvas et des données du controleur
	canvas = creer_canvas(fenetre)

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


"""
	Attend un TIC et effectue une rotation des messages
"""
def effectuer_tic():
	global controleur
	global tache
	rotation_message()
	
	if controleur.continuer:
		tache = controleur.fenetre.after(TIC, effectuer_tic )


###############################################################################
# # # # # # # # # # # # # # # #		M A I N 	# # # # # # # # # # # # # # # #
###############################################################################

global controleur
controleur = None

fenetre = creer_fenetre()

initialisation(fenetre)
fenetre.mainloop()
