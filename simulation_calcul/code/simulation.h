/*!
 * \file simulation.h
 * \brief Header du fichier principal exécutant la simulation.
 */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "./ListeChainee.h"
#include "./hyper_expo.h"

/*! \def NOMBRE_TIC
 * \brief Représente le nombre de TIC sur lequel portera la simulation.
 */
 #define NOMBRE_TIC 10

 /*! \def NOMBRE_SLOT
  * \brief Indique le nombre de slot de l'anneau.
  */
 #define NOMBRE_SLOT 10

 /*! \def NOMBRE_NOEUD
  * \brief Indique le nombre de noeud de l'anneau.
  */
 #define NOMBRE_NOEUD 5

 /*! \def PERIODE_MESSAGE_ANTENNE
  * \brief Indique la période selon laquelle les antennes enverront des messages aux noeuds.
  */
 #define PERIODE_MESSAGE_ANTENNE 100

 /*! \def LIMITE_NOMBRE_MESSAGE_MIN
  * \brief La limite minimale avant un envoi de message depuis un noeud.
  */
 #define LIMITE_NOMBRE_MESSAGE_MIN 60

 /*! \def LIMITE_NOMBRE_MESSAGE_MAX
  * \brief La limite maximale avant un envoi de message depuis un noeud.
  */
 #define LIMITE_NOMBRE_MESSAGE_MAX 80

//////////////////////////////////////////////////
///////////////// Les structures /////////////////
//////////////////////////////////////////////////

/*! \struct Messages.
 * \brief Structure représentant un groupe de message arrivant dans le noeud.
 * Un groupe de message à une taille ainsi qu'un TIC d'arrivé dans le noeud.
 */
struct Messages
{
	int TIC_arrive;
	int taille;
};
typedef struct Messages Messages;

/*! \struct PaquetMessage
 * \brief Structure représentant un paquet de message curculant dans les slots.
 * Cette structure contient un indice du noeud emetteur du paquet, un nombre de message, et un tableau des différents messages.
 */
struct PaquetMessage
{
	int indice_noeud_emetteur;
	int nombre_messages;
	Messages messages[80];		//Un slot ne peut contenir plus de 80 messages
};
typedef struct PaquetMessage PaquetMessage;

/*! \struct Noeud
 * \brief Structure représentant un Noeud de l'anneau.
 * Elle contient un nombre de message, les indices des slots avec lesquels le noeud peut intéragir, ainsi que le nombre d'antenne liée au noeud et le décalage avec laquelle le noeud doit recevoir un message de ses antennes.
 */

struct Noeud
{
	int id;
	int nb_message;
	int indice_slot_lecture;
	int indice_slot_ecriture;
	int nb_antenne;		//Indique le nombre d'antenne auquel est lié le noeuds
	int debut_periode;		//Le décalage selon lequel le noeud recoit des messages des antennes
	ListeChainee *messages;		//File FIFO contenant les TIC d'arrivé des messages
	int attente_max;		//Le temps d'attente maximal dans le noeud
	int nb_message_total;	//Le nombre de message ayant transité dans le noeud
	int attente_totale;		//Le temps d'attente total des messages
};

typedef struct Noeud Noeud;

/*! \struct Slot
 * \brief Structure représentant un slot dans l'anneau.
 * Un Slot est caractérisé par un id (unique), un booléen insiquant si le slot contient un message ou non, ainsi que les indices du noeud lié au slot s'il y en a un.
 */

struct Slot
{
	int id;
	int paquet_message;		//Indique si le slot possede un paquet de message ()
	int indice_noeud_lecture;		//Si le slot ne peut accèder a aucun noeud, ce champs vaut -1
	int indice_noeud_ecriture;		//Si le slot ne peut accèder a aucun noeud, ce champs vaut -1
};
typedef struct Slot Slot;



//////////////////////////////////////////////////
///////////////// Les fonctions /////////////////
//////////////////////////////////////////////////

/*! \fn void afficher_slots( Slot slots[] )
* \brief Initialise les slots de l'anneau.
* \param slots[] Le tableau des slots à initialiser.
*/
void afficher_slots( Slot slots[] );

/*! \fn void initialiser_slots( Slot slots[] )
* \brief Affiche les slots de l'anneau.
* \param slots[] Les slots à afficher.
*/
void initialiser_slots( Slot slots[] );

/*! \fn void afficher_noeuds( Noeud noeuds[] )
* \brief Initialise les noeuds de l'anneau et modifie en conséquence les indices en écriture/lecture des slots.
* \param noeuds[] Le tableau des noeuds à initialiser.
* \param noeuds[] Le tableau des slots à modifier.
*/
void afficher_noeuds( Noeud noeuds[] );

/*! \fn void initialiser_noeuds( Noeud noeuds[], Slot slots[] )
* \brief Affiche les noeuds de l'anneau.
* \param noeuds[] Les noeuds à afficher.
*/
void initialiser_noeuds( Noeud noeuds[], Slot slots[] );

/*! \fn void entrer_messages( Slot slots[], Noeud noeuds[], int tic );
* \brief Fait entrer des messages dans les noeud selon l'hyper exponentielle et les place dans les slots si cela doit se faire.
* \param noeuds[] Les noeuds qui recevront les messages.
* \param slots[] Les slots qui recevront les messages des noeuds.
* \param tic le tic actuel de l'anneau.
*/
void entrer_messages( Slot slots[], Noeud noeuds[], int tic );


void initialiser_slots( Slot slots[] )
{
	int cpt = 0;
	for (cpt=0; cpt<NOMBRE_SLOT; cpt++)
	{
		Slot tmp = {cpt, 0, -1, -1};
		slots[cpt] = tmp;
	}
}

void afficher_slots( Slot slots[] )
{
	int i;
	printf("Les slots de l'anneau\n");
	for (i = 0; i < NOMBRE_SLOT; i++)
	{
		printf("Indice du tableau : %d     Id du noeud : %d    Il contient un paquet : %d    Indice en lecture : %d    Indice en écriture : %d\n", i, slots[i].id, slots[i].paquet_message == 1, slots[i].indice_noeud_lecture, slots[i].indice_noeud_ecriture);
	}
}

void initialiser_noeuds( Noeud noeuds[], Slot slots[] )
{
	time_t t;
	srand((unsigned) time(&t));		//Initialise le générateur de nombre aléatoire

	int pas = NOMBRE_SLOT / NOMBRE_NOEUD;
	int nombre_antenne;
	int j;
	for (j=0; j<NOMBRE_NOEUD; j++)
	{
		/* Génére le nombre d'antenne pour le noeud courant */
		if ( (j == 0) || (j == NOMBRE_NOEUD -1) )
				nombre_antenne = 0;
		else
				nombre_antenne = ( rand() % 4 ) +1;	//Génére un entier entre 1 et 5
		int debut_periode = rand() % 99;

		int indice_slot_lecture = (( (j*pas) + ((j+1)*pas) ) / 2) - 1;
		int indice_slot_ecriture = indice_slot_lecture - 1;
		if (indice_slot_ecriture < 0)
				indice_slot_ecriture = NOMBRE_SLOT -1;

		Noeud tmp = {j, 0, indice_slot_lecture, indice_slot_ecriture, nombre_antenne, debut_periode, NULL, 0, 0, 0};
		tmp.messages = creer_Liste_chainee();
		noeuds[j] = tmp;

		/* Met à jour les indices des slots */
		slots[ indice_slot_lecture ].indice_noeud_lecture = j;
		slots[ indice_slot_ecriture ].indice_noeud_ecriture = j;
	}
}

void afficher_noeuds( Noeud noeuds[] )
{
	printf("Les neouds de l'anneau\n");
	int i;
	for (i = 0; i < NOMBRE_NOEUD; i++)
	{
		printf("Indice du tableau : %d     Id du noeud : %d    Nombre de message : %d    Indice en lecture : %d    Indice en écriture : %d    Nombre d'antenne : %d    Décalage : %d\n", i, noeuds[i].id, noeuds[i].nb_message, noeuds[i].indice_slot_lecture, noeuds[i].indice_slot_ecriture, noeuds[i].nb_antenne, noeuds[i].debut_periode);
	}
}

void entrer_messages( Slot slots[], Noeud noeuds[], int tic )
{
	int i;
	for (i=0; i< NOMBRE_SLOT; i++)
	{
		Slot slot = slots[i];
		if (slot.indice_noeud_ecriture != -1)	//Le slot est un slot d'ecriture
		{
			Noeud noeud = noeuds[ slots[i].indice_noeud_ecriture ];

			//Le slot affiche si c'est sa période de réception de message provenant des antennes
			if (tic % PERIODE_MESSAGE_ANTENNE == noeuds[ slots[i].indice_noeud_ecriture ].debut_periode)	//C'est la periode du noeud, il reçoit un message de ses antennes
				printf ("C'est le moment ! Periode du noeud : %d. Je recois un message provenant de mes %d antennes.", noeud.debut_periode, noeud.nb_antenne);

			int nb_message = hyper_expo();
			printf("Le noeud %d reçois %d messages\n", noeuds[ slots[i].indice_noeud_ecriture ].id, nb_message);

			//On ajoute au noeud le tic d'arrivé des messages
			int j;
			for (j=0; j<nb_message; j++)
				inserer_fin(noeuds[ slots[i].indice_noeud_ecriture ].messages, tic);

			noeuds[ slots[i].indice_noeud_ecriture ].nb_message += nb_message;

			if ( (slots[i].paquet_message == 0) && (noeuds[ slots[i].indice_noeud_ecriture ].nb_message >= LIMITE_NOMBRE_MESSAGE_MIN) )
			{
				printf("Envoie de message possible\n");
				int k;
				if (noeuds[ slots[i].indice_noeud_ecriture ].nb_message >= LIMITE_NOMBRE_MESSAGE_MAX)
				{
					/* On enleve les messages du noeud */
					int messages [ LIMITE_NOMBRE_MESSAGE_MAX ];
					for (k=0; k<LIMITE_NOMBRE_MESSAGE_MAX; k++)
						messages[k] = supprimer_premier(noeuds[ slots[i].indice_noeud_ecriture ].messages);

					noeuds[ slots[i].indice_noeud_ecriture ].nb_message -= LIMITE_NOMBRE_MESSAGE_MAX;
				}
				else	//Le nombre de message est compris entre le minimum est le maximum, on vide donc le noeud.
				{
					//On enleve les messages du noeud
					int messages [ noeuds[ slots[i].indice_noeud_ecriture ].nb_message ];
					for (k=0; k<noeuds[ slots[i].indice_noeud_ecriture ].nb_message; k++)
						messages[k] = supprimer_premier(noeuds[ slots[i].indice_noeud_ecriture ].messages);

					noeuds[ slots[i].indice_noeud_ecriture ].nb_message = 0;
				//placer_message( noeud, messages );
				}
				printf("A la fin du tic, le noeud %d contient %d messages\n", noeuds[ slots[i].indice_noeud_ecriture ].id, noeuds[ slots[i].indice_noeud_ecriture ].nb_message);
			}
		}
	}
}
