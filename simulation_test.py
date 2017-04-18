#coding: utf8

from Tkinter import *
from math import cos, sin, pi
from threading import Thread
import time

# # # # # # # # # # # # # # # #		C O N S T A N T E	 # # # # # # # # # # # # # # # #
COULEURS_MESSAGE = ["yellowgreen", "orange", "turquoise", "royalblue", "purple", "teal", "tan", "snow", "mediumseagreen", "black"]

COTE_CANVAS = 600	#Définit la hauteur/largeur de la toile sur laquelle seront déssinés les slots et les noeuds

NOMBRE_SLOT = 25	#Le nombre de slot du système
COTE_SLOT = 15		#La hauteur/largeur d'un slot
DISTANCE_SLOT = COTE_CANVAS/3	#La distance d'un slot par rapport à l'axe central du canvas

NOMBRE_NOEUD = 8	#Le nombre de noeud du système
COTE_NOEUD = COTE_SLOT + 5		#La hauteur/largeur d'un noeud
DISTANCE_NOEUD = DISTANCE_SLOT + 50		#La distance d'un noeud par rapport à l'axe central du canvas
COULEUR_NOEUD = "CadetBlue3"	#La couleur graphique d'un noeud

COTE_MESSAGE = 2
VITESSE_LATENCE_MESSAGE = 0.002		#Le temps d'attente entre chaque rafréchisement du canvas lors d'un déplacement

TIC = 2000	#Temps d'attente entre chaque mouvement de l'anneau, envoi de message etc



# # # # # # # # # # # # # # # #		V U E	# # # # # # # # # # # # # # # #
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
	#canvas.bind("<Button-1>", callback)
	
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
		texte = canvas.create_text(nouveau_x, nouveau_y, text="S "+str(slots_vue[i-1]))
	canvas.pack()
	return slots_modele, slots_vue


"""
	Place sur la toile les noeuds et renvoie un tableau contenant :
	En indice 0 les noeuds du modele
	En indice 1 les noeuds de la vue
"""
def placer_noeuds(fenetre, canvas, slots_modele):
	noeuds_vue = [None] * NOMBRE_NOEUD
	noeuds_modele = [None] * NOMBRE_NOEUD
	
	milieu_x = COTE_CANVAS/2
	milieu_y = COTE_CANVAS/2
	
	pas = NOMBRE_SLOT // NOMBRE_NOEUD
	
	for j in range(NOMBRE_NOEUD):
		indice_slot_accessible = j*pas - 1
		noeuds_modele[j] = Noeud(indice_slot_accessible, COULEURS_MESSAGE[j])
		
		slots_modele[ indice_slot_accessible ].indice_noeud_accessible = j
		
		x = milieu_x + cos(2*j*pas*pi/NOMBRE_SLOT) * DISTANCE_NOEUD
		y = milieu_y - sin(2*j*pas*pi/NOMBRE_SLOT) * DISTANCE_NOEUD
		noeuds_vue[j] = canvas.create_rectangle( x - COTE_NOEUD, y - COTE_NOEUD, x + COTE_NOEUD, y + COTE_NOEUD, fill=COULEURS_MESSAGE[j] )
		
		#le texte du rectangle
		texte = canvas.create_text(x, y, text="N "+str(noeuds_vue[j]))
	canvas.pack()
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
	Déplace dans le canvas un objet vers un point d'arrivé définit par arrivee_x et arrivee_y
"""
def deplacer_vers(canvas, objet, arrivee_x, arrivee_y):
	#Convertie les coordonnees en int afin de récupérer la partie entiere des nombres, ainsi les coordonnees coïncideront toujours
	objet_x = int(canvas.coords(objet)[0])
	objet_y = int(canvas.coords(objet)[1])
	
	canvas.coords(objet, objet_x-COTE_MESSAGE, objet_y-COTE_MESSAGE, objet_x+COTE_MESSAGE, objet_y+COTE_MESSAGE)
	
	arrivee_x = int(arrivee_x)
	arrivee_y = int(arrivee_y)
	
	while objet_x != arrivee_x or objet_y != arrivee_y:
		if objet_x < arrivee_x:
			canvas.move(objet, 1, 0)
		elif objet_x > arrivee_x:
			canvas.move(objet, -1, 0)
		if objet_y < arrivee_y:
			canvas.move(objet, 0, 1)
		elif objet_y > arrivee_y:
			canvas.move(objet, 0, -1)
		canvas.update()
			
		objet_x = canvas.coords(objet)[0]
		objet_y = canvas.coords(objet)[1]
		canvas.pack()
		time.sleep(VITESSE_LATENCE_MESSAGE)

def rotation_message(controleur):
	pass

# # # # # # # # # # # # # # # #		M O D E L E		# # # # # # # # # # # # # # # #

"""
	Représente un noeud dans le système, un noeuds peux stocker des messages
"""
class Noeud:
	def __init__(self, indice_slot_accessible, couleur):
		self.nb_message = 0
		self.indice_slot_accessible = indice_slot_accessible
		self.couleur = couleur

class Slot:
	def __init__(self, id, indice_noeud_accessible):
		self.id = id
		self.message = None
		self.indice_noeud_accessible = indice_noeud_accessible

	def set_message(self, message):
		self.message = message
	
	def __str__(self):
		if self.message == None:
			return "Je peux accèder au noeud : "+str(self.indice_noeud_accessible)+" Je ne possede pas de message"
		else:
			return "Je peux accèder au noeud : "+str(self.indice_noeud_accessible)+" Je possede un message"

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
		
		noeud_vue = controleur.noeuds_vue[ indice_noeud ]
		slot_vue = controleur.slots_vue[indice_slot]
	
	else:	#Une erreur est survenue, on affiche un message
		print message

"""
	Exécute une rotation des messages dans l'anneau 

"""
def rotation_message():
	global controleur
	
	decaler_messages()
		
	for slot in controleur.slots_modele:
		message = slot.message
		if message and message.indice_noeud_emetteur == slot.indice_noeud_accessible:
			sortir_message(message)

	for indice in range( len(controleur.slots_modele) ):
		controleur.slots_modele[indice].message
		message = controleur.slots_modele[indice].message
		if message != None:
			message.a_bouge = False

"""
	Fait sortir du système un mesage
"""
def sortir_message(message):
	global controleur
	for slot in controleur.slots_modele:
		if slot.message and slot.message.equals(message):
			slot.message = None
	""" Ajouter fonction de suppresion graphique """
		
"""
	Methode appelenar une methode recursif qui décale d'un slot les message du système
"""
def decaler_messages():
	global controleur

	tempon = controleur.slots_modele[1].message
	
	decaler_messages2(0, 0, tempon, True)
	
"""
	Méthode récursif qui décale les messages du système
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
		
###############################################################################
# # # # # # # # # # # # # # # #		M A I N 	# # # # # # # # # # # # # # # #
###############################################################################
"""
	Effectue à un intervalle régulier le tic (Temps définis par la variable TIC)
"""
def initialisation():
	global controleur
	for i in range(NOMBRE_NOEUD):
		placer_message(i)
		
	for indice in range( len(controleur.slots_modele) ):
		controleur.slots_modele[indice].message
		message = controleur.slots_modele[indice].message
	controleur.fenetre.after(TIC, effectuer_tic )

"""
	Attend un TIC et effectue une rotation des messages
"""
def effectuer_tic():
	global controleur
	rotation_message()
	controleur.fenetre.after(TIC, effectuer_tic )

global controleur
fenetre = creer_fenetre()
canvas = creer_canvas(fenetre)

slots = placer_slots(fenetre, canvas)
slots_modele = slots[0]
slots_vue = slots[1]

noeuds = placer_noeuds(fenetre, canvas, slots_modele)

noeuds_modele = noeuds[0]
noeuds_vue = noeuds[1]
slots_modele = noeuds[2]

controleur = Controleur(fenetre, canvas, slots_vue, slots_modele, noeuds_vue, noeuds_modele)

""" Affichage des noeuds et de leurs slots respectifs """

# On démarre la boucle Tkinter qui s'interompt quand on ferme la fenêtre
fenetre.after(1000, initialisation)
fenetre.mainloop()
