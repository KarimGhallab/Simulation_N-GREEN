#coding: utf8

from Tkinter import *
from math import cos, sin, pi, exp
from threading import Thread
from PIL import Image, ImageTk
import tkMessageBox
import time
import random

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

TIC = 600	#Temps d'attente entre chaque mouvement de l'anneau, envoi de message etc

global tache
tache = None

global LABEL_TIC
LABEL_TIC = None

global TEXTS_NOEUDS
TEXTS_NOEUDS = None

#Les variables pour l'hyper exponentielle
PROBABILITE_BURST = 0.01
global LAMBDA 
LAMBDA = 1

global LAMBDA_BURST
LAMBDA_BURST = 140

LIMITE_NOMBRE_MESSAGE = 80

# # # # # # # # # # # # # # # #		V U E	# # # # # # # # # # # # # # # #
"""
	Créer une fenetre Tkinter avec son titre.
"""
def creer_fenetre():
	# On crée une fenêtre, racine de notre interface
	fenetre = Tk()
	fenetre.title("Jason Statham : <3")
	
	return fenetre

"""
	Créer un canvas avec une croix au centre et le place dans la fenetre.
"""
def creer_canvas(fenetre):
	canvas = Canvas(fenetre, width=COTE_CANVAS, height=COTE_CANVAS, background='#909090')
	ligne1 = canvas.create_line(COTE_CANVAS/2, 0, COTE_CANVAS/2, COTE_CANVAS, fill="White")
	ligne2 = canvas.create_line(0, COTE_CANVAS/2, COTE_CANVAS, COTE_CANVAS/2, fill="White")
	
	canvas.grid(row=0, column=1, rowspan=NOMBRE_LIGNE_CANVAS, columnspan=4)
	
	return canvas


"""
	Place sur la toile les slots et renvoie un tableau contenant :
	En indice 0 les slots du modele
	En indice 1 les slots de la vue.
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
		slots_modele[i-1] = Slot(i, None, None)
		texte = canvas.create_text(nouveau_x, nouveau_y)
	return slots_modele, slots_vue


"""
	Place sur la toile les noeuds et renvoie un tableau contenant :
	En indice 0 les noeuds du modele
	En indice 1 les noeuds de la vue.
"""
def placer_noeuds(fenetre, canvas, slots_modele, slots_vue):
	global TEXTS_NOEUDS
	
	noeuds_vue = [None] * NOMBRE_NOEUD
	noeuds_modele = [None] * NOMBRE_NOEUD
	TEXTS_NOEUDS = [None] * NOMBRE_NOEUD
	
	milieu_x = COTE_CANVAS/2
	milieu_y = COTE_CANVAS/2
	
	pas = NOMBRE_SLOT // NOMBRE_NOEUD
	
	for j in range(NOMBRE_NOEUD):
		indice_slot_accessible = (( (j*pas) + ((j+1)*pas) ) / 2) - 1
		
		periode = int(random.uniform(10, 40))	#La période se situe entre 10 et 40 TIC
		
		if j == 0 or j == NOMBRE_NOEUD-1:	#L'anneau doit contenir deux noeuds n'étant liés avec aucunes antennes
			nb_antenne = 0
		else:
			nb_antenne = int(random.uniform(1, 5))	#Au maximum 5 antennes
			
		noeuds_modele[j] = Noeud(indice_slot_accessible, indice_slot_accessible-1, COULEURS_MESSAGE[j], nb_antenne, periode)
		
		slots_modele[ indice_slot_accessible ].indice_noeud_lecture = j
		slots_modele[ indice_slot_accessible-1 ].indice_noeud_ecriture = j
		
		#Modification des couleur des slots
		couleur = noeuds_modele[j].couleur
		canvas.itemconfig(slots_vue[indice_slot_accessible], outline=couleur)
		canvas.itemconfig(slots_vue[indice_slot_accessible-1], outline=couleur)
		
		
		#Récupération des slots dont dépendent la position du noeud
		x_slot = canvas.coords( slots_vue[ indice_slot_accessible ] )[0] + COTE_SLOT
		x_slot_suivant = canvas.coords( slots_vue[ indice_slot_accessible -1] )[0] + COTE_SLOT
		
		y_slot = canvas.coords( slots_vue[ indice_slot_accessible ] )[1] + COTE_SLOT
		y_slot_suivant = canvas.coords( slots_vue[ indice_slot_accessible -1] )[1] + COTE_SLOT
		
		#Calcule de la position du noeud
		x = ( x_slot + x_slot_suivant ) / 2
		y = ( y_slot + y_slot_suivant) / 2
		if x < COTE_CANVAS/2:
			x -= 40
		elif x > COTE_CANVAS/2:
			x += 40
			
		if y < COTE_CANVAS/2:
			y -= 40
		elif y > COTE_CANVAS/2:
			y += 40
			
		noeuds_vue[j] = canvas.create_rectangle( x - COTE_NOEUD, y - COTE_NOEUD, x + COTE_NOEUD, y + COTE_NOEUD, fill=COULEURS_MESSAGE[j] )
		
		#le texte du rectangle
		TEXTS_NOEUDS[j] = canvas.create_text(x, y, text="0")
	return noeuds_modele, noeuds_vue, slots_modele


"""
	Place un message à un point de départ et le fait se déplacer jusqu'a un point d'arrivé.
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
		- Augmenter vitesse
		- Diminuer vitesse.
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
	bouton_reset.grid(row=7)
	label_restart = Label(fenetre, text="Modifier vitesse")
	label_restart.grid(row=8)
	
	vitesse_down = Image.open("./images/vitesse_down.png")
	IMAGES.append( ImageTk.PhotoImage(vitesse_down) )
	bouton_down = Button(fenetre, text ="DOWN", command = diminuer_vitesse, image = IMAGES[ len(IMAGES) -1 ], bg="White", activebackground="#E8E8E8")
	bouton_down.grid(row=9)

	
"""
	Place le panel bas affichant les informations courantes ainsi que moyens de modifier les valeurs suivantes:
		- Le nombre de slot utilisé.
		- Le nombre de Noeud présent.
		- Le lambda actuellement utilisé.
	Le panel contient aussi un bouton de validation des données.
	Si aucunes données n'est saisi pour un champs, la valeur de la configuration précèdente est consérvée.
"""	
def placer_panel_bas(fenetre):
	nombre_slot = len( controleur.slots_modele )
	nombre_noeud = len( controleur.noeuds_modele )
	
	#Les labels présentant les nombres de slots, de noeuds, le lambda actuel ainsi que le TIC en milliseconde
	label_slot_actuel = Label(fenetre, text = "Nombre de slot : "+str(nombre_slot) )
	label_noeud_actuel = Label(fenetre, text = "Nombre de noeud : "+str(nombre_noeud) )
	label_lambda_actuel = Label(fenetre, text = "Lambda actuel : "+str(LAMBDA) )
	label_lambda_burst_actuel = Label(fenetre, text = "Lambda Burst : "+str(LAMBDA_BURST) )
	
	label_slot_actuel.grid(row=NOMBRE_LIGNE_CANVAS+1, column=1, sticky='W')
	label_noeud_actuel.grid(row=NOMBRE_LIGNE_CANVAS+2, column=1, sticky='W')
	label_lambda_actuel.grid(row=NOMBRE_LIGNE_CANVAS+3, column=1, sticky='W')
	label_lambda_burst_actuel.grid(row=NOMBRE_LIGNE_CANVAS+4, column=1, sticky='W')
	update_label_TIC(fenetre, NOMBRE_LIGNE_CANVAS+5, 1)
	
	#Les labels des entry pour un nouveau nombre de slot/noeud
	label_nouveau_slot = Label(fenetre, text = "Nouveau nombre de slot : ")
	label_nouveau_noeud = Label(fenetre, text = "Nouveau nombre de noeud : ")
	label_nouveau_lambda = Label(fenetre, text = "Nouvelle valeur du lambda : ")
	label_nouveau_lambda_burst = Label(fenetre, text = "Nouvelle valeur du lambda Burst : ")
	
	label_nouveau_slot.grid(row=NOMBRE_LIGNE_CANVAS+1, column=2, sticky='W')
	label_nouveau_noeud.grid(row=NOMBRE_LIGNE_CANVAS+2, column=2, sticky='W')
	label_nouveau_lambda.grid(row=NOMBRE_LIGNE_CANVAS+3, column=2, sticky='W')
	label_nouveau_lambda_burst.grid(row=NOMBRE_LIGNE_CANVAS+4, column=2, sticky='W')
	
	#Les entry
	entry_slot = Entry(fenetre, width=LONGUEUR_ENTRY)
	entry_noeud = Entry(fenetre, width=LONGUEUR_ENTRY)
	entry_lambda = Entry(fenetre, width=LONGUEUR_ENTRY)
	entry_lambda_burst = Entry(fenetre, width=LONGUEUR_ENTRY)
	
	#Ajout d'un event
	entry_slot.bind("<Key>", callback_validation_configuration)
	entry_noeud.bind("<Key>", callback_validation_configuration)
	entry_lambda.bind("<Key>", callback_validation_configuration)
	entry_lambda_burst.bind("<Key>", callback_validation_configuration)
	
	controleur.entrys[CLE_ENTRY_SLOT] = entry_slot
	controleur.entrys[CLE_ENTRY_NOEUD] = entry_noeud
	controleur.entrys[CLE_ENTRY_LAMBDA] = entry_lambda
	controleur.entrys[CLE_ENTRY_LAMBDA_BURST] = entry_lambda_burst
	
	entry_slot.grid(row=NOMBRE_LIGNE_CANVAS+1, column=3, sticky='W')
	entry_noeud.grid(row=NOMBRE_LIGNE_CANVAS+2, column=3, sticky='W')
	entry_lambda.grid(row=NOMBRE_LIGNE_CANVAS+3, column=3, sticky='W')
	entry_lambda_burst.grid(row=NOMBRE_LIGNE_CANVAS+4, column=3, sticky='W')
	
	#le bouton
	bouton_reset = Button(fenetre, text ="Valider", command = modifier_configuration, bg="YellowGreen", fg="White", activebackground="#7ba428", activeforeground="White", width=LONGUEUR_BOUTON)
	bouton_reset.grid(row=NOMBRE_LIGNE_CANVAS+6, column=4, sticky='E')


"""
	Met a jour le label du panel bas affichant le TCI en millisecondes.
"""
def update_label_TIC(fenetre, ligne, colonne):
	global LABEL_TIC
	
	if LABEL_TIC != None:
		LABEL_TIC.destroy()
	
	if TIC <= 600:
		message = "TIC : "+str(TIC)+" millisecondes, on est au max !"
	else:
		message = "TIC : "+str(TIC)+" millisecondes"
	LABEL_TIC = Label(fenetre, text = message)
	LABEL_TIC.grid(row=NOMBRE_LIGNE_CANVAS+5, column=1, sticky='W')


""" 
	Déplace dans le canvas un objet vers un point d'arrivé définit par arrivee_x et arrivee_y.
"""
def deplacer_vers(canvas, objet, arrivee_x, arrivee_y):
	#Convertie les coordonnees en int afin de récupérer la partie entiere des nombres, ainsi les coordonnees coïncideront toujours
	objet_x = int(canvas.coords(objet)[0])
	objet_y = int(canvas.coords(objet)[1])
	
	#Calcule la taille de la forme de l'objet passé
	x1 = canvas.coords(objet)[0]
	x2 = canvas.coords(objet)[2]
	
	canvas.coords(objet, objet_x - COTE_MESSAGE, objet_y - COTE_MESSAGE, objet_x + COTE_MESSAGE, objet_y + COTE_MESSAGE)
	
	arrivee_x = int(arrivee_x) - COTE_MESSAGE
	arrivee_y = int(arrivee_y) - COTE_MESSAGE
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


"""
	Fonction faisant sortir de l'interface un message.
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
	Représente un noeud dans le système, un noeuds peux stocker des messages.
"""
class Noeud:
	def __init__(self, indice_slot_lecture, indice_slot_ecriture, couleur, nb_antenne, periode):
		self.nb_message = 0
		self.indice_slot_lecture = indice_slot_lecture
		self.indice_slot_ecriture = indice_slot_ecriture
		self.couleur = couleur
		self.nb_antenne = nb_antenne	#Indique le nombre d'antenne auquel est lié le noeuds
		self.periode = periode		#La période selon laquelle le noeud recoit des messages des antennes


	"""
		renvoie l'équalité entres deux noeuds.
	"""
	def equals(self, autre_noeud):
		return self.couleur == autre_noeud.couleur

	
	"""
		Met a jour le text affichant le nombre de message en attente dans le noeud.
	"""
	def update_file_noeud_graphique(self):
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
		return str(self.couleur)
		
"""
	Repprésente un slot dans l'anneau, il a un id qui lui est propres ainsi qu'un paquet de message et un indice vers le noeud qui lui accède.
"""
class Slot:
	def __init__(self, id, indice_noeud_lecture, indice_noeud_ecriture):
		self.id = id
		self.paquet_message = None	#Indique si le slot possede un paquet de message
		self.indice_noeud_lecture = indice_noeud_lecture		#Si le slot ne peut accèder a aucun noeud, ce champs vaut None
		self.indice_noeud_ecriture = indice_noeud_ecriture

	"""
		Renvoie le slot sous forme de chaine de caractères.
	"""	
	def __str__(self):
		if self.paquet_message == None:
			return "Je peux accèder au noeud : "+str(self.indice_noeud_accessible)+" Je ne possede pas de message"
		else:
			return "Je peux accèder au noeud : "+str(self.indice_noeud_accessible)+" Je possede un message"


"""
	Représente un paquet de message : contient à la fois les coordonnées graphiques du messages, l'indice du noeud auquel il appartient, 
	l'id du paquet le représentant graphiquement ainsi que la taille du paquet.
"""
class PaquetMessage:
	def __init__(self, id_message, indice_noeud_emetteur):
		self.id_message_graphique = id_message
		self.indice_noeud_emetteur = indice_noeud_emetteur
		self.x = None
		self.y = None
		self.taille = None	#La taille du paquet
	
	
	"""
		Met a jour la position graphique du message.
	"""
	def update_position(self, nouveau_x, nouveau_y):
		self.x = nouveau_x
		self.y = nouveau_y
	
	
	"""
		Renvoie le paquet sous forme de chaine de caractères.
	"""
	def __str__(self):
		global controleur
		return "Message envoyé par le noeud  : "+str(controleur.noeuds_modele[self.indice_noeud_emetteur].couleur)
	
	
	"""
		Retourne l'equalité entre deux messages.
	"""	
	def equals(self, autre_message):
		return self.id_message_graphique == autre_message.id_message_graphique


###########################################################
############ Partie tirage/hyper exponentielle ############
###########################################################
		
"""
	Effectue un tirage et renvoie True ou False si la variable tirée est contenu dans la probabilité passée en paramètre.
"""			
def effectuer_tirage(probabilite):
	tirage = random.uniform(0, 1)
	return tirage <= probabilite


"""
	Réalise le tirage selon l'hyper exponentielle.
"""
def hyper_expo():
	if effectuer_tirage(PROBABILITE_BURST) == True:		#Le tirage est tombé sur la faible proba
		return LAMBDA_BURST
	else:
		u = random.uniform(0, 1)
		return loi_de_poisson_naif(u)


"""
	Calcule le nombre de message Best Effort transmis par un noeud.
"""
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

"""
	Classe représentant le système que l'on souhaite modéliser dans sa globalité 
	Elle fera l'intermédiaire entre le modèle et la vue.
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
		self.nb_tic = 0


###########################################################
################ Les listeners des boutons ################
###########################################################
"""

"""
def callback_validation_configuration(event):
	if event.char == '\r':		#Le bouton entrée
		modifier_configuration()


"""
	Callback au bouton demandant un reset de l'application
	Ici on supprime le canvas et on en crée un nouveau. Les paramètres sont ceux utilisé pour la précédente configuration.
"""
def reset():
	global controleur
	global tache
	
	controleur.continuer = False
	controleur.nb_tic = 0
	
	#supprime le prochain tic s'il y a afin de ne pas faire planté les threads et l'interface
	if tache != None:
		controleur.fenetre.after_cancel(tache)
		
	#La méthode after permet ici de faire s'executer les threads en cours
	controleur.fenetre.after(TIC, initialisation, (fenetre) )

"""
	Commence la rotaion. Méthode appeler lors d'un clique sur le bouton de commencement.
"""
def commencer_rotation():
	global controleur
	global tache

	if not controleur.continuer:
		controleur.continuer = True


"""
	Arrête la rotaion. Méthode appeler lors d'un clique sur le bouton de fin.
"""
def arreter_rotation():
	global controleur
	global tache
	#supprime le prochain tic s'il y a afin de ne pas faire planté les threads et l'interface
	controleur.continuer = False


"""
	Augmente la vitesse de rotation.
"""
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


"""
	Diminue la vitesse de rotation.
"""
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


"""
	Modifie la configuration de l'anneau en fonction des données saisies dans le panel bas.
"""
def modifier_configuration():
	global controleur
	global NOMBRE_NOEUD
	global NOMBRE_SLOT
	global LAMBDA
	global LAMBDA_BURST
	
	tmp_noeud = NOMBRE_NOEUD
	tmp_slot = NOMBRE_SLOT
	tmp_lambda = LAMBDA
	nb_champ_vide = 0
	
	erreur = False
	
	valeur_noeud = controleur.entrys[ CLE_ENTRY_NOEUD ].get()
	valeur_slot = controleur.entrys[ CLE_ENTRY_SLOT ].get()
	valeur_lambda = controleur.entrys[ CLE_ENTRY_LAMBDA ].get()
	valeur_lambda_burst = controleur.entrys[ CLE_ENTRY_LAMBDA_BURST ].get()
	
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
		
	if erreur or nb_champ_vide == len(controleur.entrys):
		NOMBRE_NOEUD = tmp_noeud
		NOMBRE_SLOT = tmp_slot
		LAMBDA = tmp_lambda
	else:	#Il n'y a aucune erreur, on redéfinit la nouvelle configuration
		print "Avant reset val lambda burst: ", LAMBDA_BURST
		reset()
		tkMessageBox.showinfo("Chargement", "Votre nouvelle configuration est en cours de chargement !;)")

"""
	Stop l'appli en faisant attention aux thread restants.
"""
def arreter_appli():
	arreter_rotation()
	fenetre.destroy()


"""
	Action de faire entrer un message d'un noeud jusqu'à son slot.
"""
def placer_message(indice_noeud):
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


"""
	Exécute une rotation des messages dans l'anneau.
"""
def rotation_message():
	global controleur
	decaler_messages()
	sortir_message()
	entrer_message()


"""
	Fait entrer dans l'anneau des messages.
	Ici les arrivées de messages sont gérées par l'hyper exponentielle et des files d'attentes.
"""
def entrer_message():
	global controleur
	
	for i in range (NOMBRE_SLOT):		#Parcours des slots de l'anneau
		slot = controleur.slots_modele[i]
		if slot.indice_noeud_ecriture != None:	#Le slot est un slot d'ecriture
			noeud = controleur.noeuds_modele[ slot.indice_noeud_ecriture ]
			
			#Le slot affiche si c'est sa période de réception de message provenant des antennes
			if controleur.nb_tic % noeud.periode == 0:
				print "C'est le moment ! Periode du noeud : ", noeud.periode, ". Je recois un message provenant de mes ", noeud.nb_antenne, " antennes."
			
			nb_message = hyper_expo()	#Le nombre de message Best Effort reçu est géré par l'hyper exponentielle
	
			noeud.nb_message += nb_message
			if slot.paquet_message == None and noeud.nb_message >= LIMITE_NOMBRE_MESSAGE:		#Le slot peut recevoir un message
				noeud.nb_message -= LIMITE_NOMBRE_MESSAGE
				placer_message( slot.indice_noeud_ecriture )
			noeud.update_file_noeud_graphique()


"""
	Fait sortir du système un mesage.
"""
def sortir_message():
	global controleur
	#Fais sortir les messages qui repassent devant leur Noeud emetteur
	for slot in controleur.slots_modele:
		paquet_message = slot.paquet_message
		
		if paquet_message and slot.indice_noeud_lecture != None and paquet_message.indice_noeud_emetteur == slot.indice_noeud_lecture:
			t = Thread(target=sortir_message_graphique, args=(controleur.canvas, slot.paquet_message.id_message_graphique) )
			t.start()
			slot.paquet_message = None


"""
	Methode appelant une methode récursive qui décale d'un slot les message du système.
"""
def decaler_messages():
	global controleur

	tempon = controleur.slots_modele[1].paquet_message
	
	decaler_messages2(0, 0, tempon, True)

	
"""
	Méthode récursive qui décale les messages de l'anneau.
"""
def decaler_messages2(premier_indice, indice_slot, paquet_message, premier_appel):
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
		
		if indice_slot -1 < 0:
			indice_slot_suivant = len (controleur.slots_vue) - 1
		else:
			indice_slot_suivant = indice_slot - 1
		
		slot_graphique = controleur.slots_vue[ indice_slot ]
		slot_graphique_suivant = controleur.slots_vue[ indice_slot_suivant ]
		
	
	if indice_slot-1 < 0:
		nouvelle_indice = len(controleur.slots_modele) -1
	else:
		nouvelle_indice = indice_slot-1
		
	if indice_slot != premier_indice or premier_appel:
		tempon = controleur.slots_modele[indice_slot].paquet_message
		
		decaler_messages2(premier_indice, nouvelle_indice, tempon, False)
		controleur.slots_modele[indice_slot].paquet_message = paquet_message
	else:
		controleur.slots_modele[indice_slot].paquet_message = paquet_message


"""
	calculer le temps de latence entre chaque mouvement de pixel lors d'un déplacement de message
	Le calcul prend en compte la distance à parcourir entre chaque déplacement.
"""
def calculer_vitesse():
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

"""
	Met en place le canvas.
"""
def initialisation(fenetre):
	global controleur
	
	#On détruit tout les widgets de la fenêtre afin que celle-ci soit toute belle
	for widget in fenetre.winfo_children():
	    widget.destroy()
	
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
	
	effectuer_tic()


"""
	Attend un TIC et effectue une rotation des messages.
"""
def effectuer_tic():
	global controleur
	global tache
	
	if controleur.continuer == True:
		controleur.nb_tic += 1
		print "Nombre de TIC : ", controleur.nb_tic
		rotation_message()
	tache = controleur.fenetre.after(TIC, effectuer_tic )

"""
	Affiche l'état des slots de l'anneau.
"""
def afficher_message_anneau():
	global controleur
	for i in range (NOMBRE_SLOT):
		if controleur.slots_modele[i].paquet_message == None:
			print "Le slot ", controleur.slots_vue[i], " ne contient pas de message"
		else:
			print "Le slot ", controleur.slots_vue[i], " contient un message mis par le noeud ", controleur.noeuds_modele[ controleur.slots_modele[i].paquet_message.indice_noeud_emetteur ]


###############################################################################
# # # # # # # # # # # # # # # #		M A I N 	# # # # # # # # # # # # # # # #
###############################################################################

global controleur
controleur = None

fenetre = creer_fenetre()
fenetre.protocol("WM_DELETE_WINDOW", arreter_appli)	#Réagi à la demande d'un utilisateur de quitter l'application

initialisation(fenetre)
fenetre.mainloop()
