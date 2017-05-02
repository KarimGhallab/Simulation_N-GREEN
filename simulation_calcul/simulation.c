#include<stdio.h>
#include <stdlib.h>
#include <time.h>

#define NOMBRE_TIC 10		//Le nombre de TIC à effectuer.
#define NOMBRE_SLOT 10		//Le nombre de slot dans l'anneau.
#define NOMBRE_NOEUD 5	//Le nombre de noeud dans l'anneau.

/* Déclaration des structures */

/**
 * Structure représentant un groupe de message arrivant dans le noeud.
 * Un groupe de message à une taille ainsi qu'un TIC d'arrivé dans le noeud.
*/
struct Messages
{
	int TIC_arrive;
	int taille;
};
typedef struct Messages Messages;

/**
 * Structure représentant un paquet de message curculant dans les slots.
 * Cette structure contient un indice du noeud emetteur du paquet, un nombre de message, et un tableau des différents messages.
*/
struct PaquetMessage
{
	int indice_noeud_emetteur;
	int nombre_messages;
	Messages messages[80];		//Un slot ne peut contenir plus de 80 messages
};
typedef struct PaquetMessage PaquetMessage;

/**
 * Structure représentant un Noeud de l'anneau.
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
};
typedef struct Noeud Noeud;

/**
 * Structure représentant un slot dans l'anneau.
 * Un Slot est caractérisé par un id (unique), un booléen insiquant si le slot contient un message ou non, ainsi que les indices du noeud lié au slot s'il y en a un.
*/

struct Slot
{
	int id;
	int paquet_message;		//Indique si le slot possede un paquet de message
	int indice_noeud_lecture;		//Si le slot ne peut accèder a aucun noeud, ce champs vaut -1
	int indice_noeud_ecriture;		//Si le slot ne peut accèder a aucun noeud, ce champs vaut -1
};
typedef struct Slot Slot;

/* Déclaration des fonctions */
void afficher_slots( Slot slots[] );
void initialiser_slots( Slot slots[] );

void afficher_noeuds( Noeud noeuds[] );
void initialiser_noeuds( Noeud noeuds[], Slot slots[] );

/*	 M A I N 	 */

/**
 * Méthode main.
 * Elle effectue un nombre prédéfini de TIC dans l'anneau et effectue des calculs sur le déroulement des actions dans l'anneau.
*/
int main ()
{
	int nombre_tic_restant = NOMBRE_TIC;
	printf("Nombre de slot de l'anneau : %d\n", NOMBRE_SLOT);
	printf("Nombre de noeud de l'anneau : %d\n\n", NOMBRE_NOEUD);
	//Initialisation des slots et noeuds de l'anneau.
	Slot slots[ NOMBRE_SLOT ];
	Noeud noeuds[ NOMBRE_NOEUD ];
	initialiser_slots(slots);
	initialiser_noeuds(noeuds, slots);

	afficher_slots(slots);
	printf("\n###################################################\n\n");
	afficher_noeuds(noeuds);


	/*while (nombre_tic_restant > 0)
	{
		printf("%d\n", nombre_tic_restant);
		nombre_tic_restant--;
	}*/
	return 0;
}

/**
 * Initialise les slots de l'anneau.
*/
void initialiser_slots( Slot slots[] )
{
	int cpt = 0;
	for (cpt=0; cpt<NOMBRE_SLOT; cpt++)
	{
		Slot tmp = {cpt, 0, -1, -1};
		slots[cpt] = tmp;
	}
}

/**
 * Affiche les slots de l'anneau.
*/
void afficher_slots( Slot slots[] )
{
	int i;
	printf("Les slots de l'anneau\n");
	for (i = 0; i < NOMBRE_SLOT; i++)
	{
		printf("Indice du tableau : %d     Id du noeud : %d    Il contient un paquet : %d    Indice en lecture : %d    Indice en écriture : %d\n", i, slots[i].id, slots[i].paquet_message == 1, slots[i].indice_noeud_lecture, slots[i].indice_noeud_ecriture);
	}
}

/**
 * Initialise les noeuds de l'anneau et met à jour les slots.
*/
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

		Noeud tmp = {j, 0, indice_slot_lecture, indice_slot_ecriture, nombre_antenne, debut_periode};
		noeuds[j] = tmp;

		/* Met à jour les indices des slots */
		slots[ indice_slot_lecture ].indice_noeud_lecture = j;
		slots[ indice_slot_ecriture ].indice_noeud_ecriture = j;
	}
}

/**
 * Affiche les noeuds de l'anneau.
*/
void afficher_noeuds( Noeud noeuds[] )
{
	printf("Les neouds de l'anneau\n");
	int i;
	for (i = 0; i < NOMBRE_NOEUD; i++)
	{
		printf("Indice du tableau : %d     Id du noeud : %d    Nombre de message : %d    Indice en lecture : %d    Indice en écriture : %d    Nombre d'antenne : %d    Décalage : %d\n", i, noeuds[i].id, noeuds[i].nb_message, noeuds[i].indice_slot_lecture, noeuds[i].indice_slot_ecriture, noeuds[i].nb_antenne, noeuds[i].debut_periode);
	}
}
