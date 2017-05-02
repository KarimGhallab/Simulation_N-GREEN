#include<stdio.h>

#define NOMBRE_TIC 10		//Le nombre de TIC à effectuer

/* Décalaration des structures */

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
	int indice_noeud_lecture;		//Si le slot ne peut accèder a aucun noeud, ce champs vaut Null
	int indice_noeud_ecriture;		//Si le slot ne peut accèder a aucun noeud, ce champs vaut Null
};
typedef struct Slot Slot;

/*	 M A I N 	 */

/**
 * Méthode main.
 * Elle effectue un nombre prédéfini de TIC dans l'anneau et effectue des calculs sur le déroulement des actions dans l'anneau.
*/
int main ()
{
	int nombre_tic_restant = NOMBRE_TIC;
	while (nombre_tic_restant > 0)
	{
		printf("%d\n", nombre_tic_restant);
		nombre_tic_restant--;
	}
	return 0;
}
