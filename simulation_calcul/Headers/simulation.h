#include "./File.h"
#include "./TableauDynamique.h"
#include <stdio.h>

/*! \file simulation.h
    \brief Header du fichier principal contenant les fonctions et structures necessaires au main.
 */

/*! \def NOMBRE_TIC
    \brief Représente le nombre de TIC sur lequel portera la simulation.
 */
#define NOMBRE_TIC 200000

/*! \def PERIODE_MESSAGE_ANTENNE
    \brief Indique la période selon laquelle les antennes enverront des messages aux noeuds.
 */
#define PERIODE_MESSAGE_ANTENNE 100

/*! \def LIMITE_NOMBRE_MESSAGE_MIN
    \brief La limite minimale avant un envoi de message depuis un noeud.
 */
#define LIMITE_NOMBRE_MESSAGE_MIN 60

/*! \def LIMITE_NOMBRE_MESSAGE_MAX
    \brief La limite maximale avant un envoi de message depuis un noeud.
 */
#define LIMITE_NOMBRE_MESSAGE_MAX 80

//////////////////////////////////////////////////
///////////////// Les structures /////////////////
//////////////////////////////////////////////////

/*! \struct PaquetMessage
    \brief Structure représentant un paquet de message curculant dans les slots.
    Cette structure contient l'indice du noeud emetteur du paquet, le nombre de message, et un tableau des différents messages.
 */
struct PaquetMessage
{
	int indice_noeud_emetteur;
	int nombre_messages;
	int messages[80];		//Un slot ne peut contenir plus de 80 messages (Un message contient uniquement son tic d'arrivé).
};
typedef struct PaquetMessage PaquetMessage;

/*! \struct Noeud
    \brief Structure représentant un Noeud de l'anneau.
    Elle contient un nombre de message, les indices des slots avec lesquels le noeud peut intéragir, ainsi que le nombre d'antenne liée au noeud et le décalage avec laquelle le noeud doit recevoir un message de ses antennes.
 */
struct Noeud
{
	int id;
	int nb_message;
	int indice_slot_lecture;
	int indice_slot_ecriture;
	int nb_antenne;		//Indique le nombre d'antenne auquel est lié le noeuds
	int debut_periode;		//Le décalage selon lequel le noeud recoit des messages des antennes
	File *file_messages;		//File FIFO contenant les TIC d'arrivé des messages
	int attente_max;		//Le temps d'attente maximal dans le noeud
	double nb_message_total;	//Le nombre de message ayant transité dans le noeud
	double attente_totale;		//Le temps d'attente total des messages
};

typedef struct Noeud Noeud;

/*! \struct Slot
    \brief Structure représentant un slot dans l'anneau.
    Un Slot est caractérisé par un id (unique), un booléen insiquant si le slot contient un message ou non, ainsi que les indices du noeud lié au slot s'il y en a un.
 */
struct Slot
{
	int id;
	int contient_message;		//Indique si le slot contient un message.
	PaquetMessage *paquet_message;		//Le pquet de message du slot.
	int indice_noeud_lecture;		//Si le slot ne peut accèder a aucun noeud, ce champs vaut -1.
	int indice_noeud_ecriture;		//Si le slot ne peut accèder a aucun noeud, ce champs vaut -1.
};
typedef struct Slot Slot;

/*! \struct Anneau
    \brief Structure représentant un anneau de la simulation
    Il contient des noeuds, des slots, un tableau dynamique de message ainsi qu'un nombre de messages ayant circulé dans l'anneau.
 */
struct Anneau
{
	int numero_anneau;
	Noeud **noeuds;
	Slot **slots;
	TableauDynamique *messages;
	double nb_message;
	int nombre_slot;
	int nombre_noeud;
};
typedef struct Anneau Anneau;

//////////////////////////////////////////////////
///////////////// Les fonctions /////////////////
//////////////////////////////////////////////////

/*! \fn void initialiser_anneau( int nombre_slot, int nombre_noeud, int generer_pdf )
    \brief Initialise un anneau.
    \param nombre_slot Le nombre de slot de la simulation.
    \param nombre_noeud Le nombre de noeud de la simulation.
    \param generer_pdf Booléen indiquant la génération ou non-génération de PDF en fin de simulation.
    \return Un pointeur sur l'anneau créé.
 */
Anneau* initialiser_anneau( int nombre_slot, int nombre_noeud, int generer_pdf );

/*! \fn void afficher_etat_anneau(Anneau *anneau)
    \brief Affiche l'état actuel de l'anneau.
    \param *anneau L'anneau à afficher.
 */
void afficher_etat_anneau(Anneau *anneau);

/*! \fn void afficher_slots( Anneau *anneau )
    \brief Affiche les slots de l'anneau.
    \param *anneau L'anneau pour lequel on souhaite afficher les slots.
 */
void afficher_slots( Anneau *anneau );

/*! \fn void initialiser_slots( Anneau *anneau, int nombre_slot );
    \brief Initialise les slots de l'anneau.
    \param *anneau L'anneau qui contiendra les slots.
    \param nombre_slot Le nombre de slot à initialiser.
 */
void initialiser_slots( Anneau *anneau, int nombre_slot );

/*! \fn void afficher_noeuds( Anneau *anneau )
	\brief Affiche les noeuds de l'anneau.
	\param *anneau L'anneau pour lequel on souhaite afficher les noeuds.
 */
void afficher_noeuds( Anneau *anneau );

/*! \fn void initialiser_noeuds( Anneau *anneau, int nombre_noeud )
    \brief Initialise les noeuds de l'anneau.
    \param *anneau L'anneau qui contiendra les noeuds
    \param nombre_noeud Le nombre de noeud à initialiser.
 */
void initialiser_noeuds( Anneau *anneau, int nombre_noeud );

/*! \fn void entrer_messages( Anneau *anneau, int tic )
    \brief Fait entrer des messages dans les noeuds de l'anneau selon l'hyper exponentielle et les place dans ses slots si cela doit se faire.
    \param *anneau L'anneau dans lequel on fait entrer les messages.
    \param tic Le tic d'entrée des messages.
 */
void entrer_messages( Anneau *anneau, int tic );

/*! \fn void void placer_message( Noeud *noeud, int indice_noeud_emetteur, Slot *slot, int nombre_message, int messages[], int tic, TableauDynamique *td )
    \brief Transmet un paquet de message d'un noeud vers son slot d'écriture.
    \param *noeud Un pointeur vers le noeud qui transmet le paquet.
    \param indice_noeud_emetteur L'indice du noeud qui envoie le message.
    \param *slot Un pointeur sur le slot qui recevra le paquet de message.
    \param nombre_message Le nombre de message qui doit etre transmis.
    \param messages[] Les messages du paquet. (contiennent le tic d'arrivé dans le noeud).
    \param tic Le tic actuel de l'anneau.
    \param *td Le tableau des tic de message de toute la simulation.
 */
void placer_message( Noeud *noeud, int indice_noeud_emetteur, Slot *slot, int nombre_message, int messages[], int tic, TableauDynamique *td );

/*! \fn void decaler_messages( Anneau *anneau )
    \brief Décale les paquets de mesage des slots de l'anneau (décalage dans le sens des aiguilles d'une montre).
    \param *anneau L'anneau sur lequel on souhaite décaler les messages.
 */
void decaler_messages( Anneau *anneau );

/*! \fn void sortir_messages( Anneau *anneau )
    \brief Fait sortir des slots de l'anneau les paquets de message lorsqu'ils sont en face de leur noeud emetteur.
    \param *anneau L'anneau sur lequel on souhaite sortir les messages.
*/
void sortir_messages( Anneau *anneau );

/*! \fn void liberer_memoire_anneau( Anneau *anneau )
    \brief Libère la mémoire prise par un anneau.
    \param *anneau L'anneau à libérer.
*/
void liberer_memoire_anneau( Anneau *anneau );

/*! \fn void fermer_fichier_std()
    \brief Ferme les fichiers stdin, stdout et stderr.
    \return -1 S'il y aune erreur ors de l'appel à la fonction system(), 0 sinon
*/
void fermer_fichier_std();

/*! \fn void void initialiser_barre_chargement(char *chargement, int taille_tableau, int nombre_chargement);
    \brief Initialise la chaine de caractère necessaire à l'affichage de la progression de la simulation.
    \param *chargement La chaine de caractères à initialiser.
	\param taille_tableau La taille de la chaine de caractères.
    \param nombre_chargement Le nombre de caractère à mettre dans la chaine.
 */
void initialiser_barre_chargement(char *chargement, int taille_tableau, int nombre_chargement);

/*! \fn int cmpfunc (const void * a, const void * b)
    \brief Méthode de comparaison pour la fonction qsort().
    \param *a Le premier paramètre à comparer.
    \param *b Le second paramètre à comparer.
 */
int cmpfunc (const void * a, const void * b);

/*! \fn void ecrire_fichier_csv(Anneau *anneau);
    \brief Ecrit les fichiers CSVs avc les données obtenus par la simulation d'un anneau.
    \param *anneau L'anneau pour lequel on souhaite sauvegarder les données.
 */
void ecrire_fichier_csv(Anneau *anneau);

/*! \fn void ecrire_nb_message_attente_csv(double **quantiles, int taille_tableau, int *bornes, int numero_anneau)
	\brief Ecrit un fichier .csv qui contiendra les nombres de messages ayant attendu un temps d'attente contenu dans un interval.
    \param **quantiles[] Les quantiles à écrire dans le fichier.
    \param taille_tableau La taille du tableau des quantiles.
    \param *bornes Un tableau des bornes coresspondant aux quantiles.
	\param numero_anneau Le numéro de l'anneau utilisé pour le nom de fichier.
 */
void ecrire_nb_message_attente_csv(double **quantiles, int taille_tableau, int *bornes, int numero_anneau);

/*! \fn void ecrire_temps_attente_csv( Anneau *anneau, double *quantiles, int *bornes, int taille_tableau )
    \brief Ecrit les differents temps d'attentes de la simulation selon des quantiles.
    \param *anneau L'anneau pour lequel on souhaite écrire les temps d'attentes.
	\param *quantiles Le tableau des données à sauvegarder.
	\param *bornes Un tableau des bornes coresspondant aux quantiles.
	\param numero_anneau Le numéro de l'anneau utilisé pour le nom de fichier.
*/
void ecrire_temps_attente_csv( Anneau *anneau, double *quantiles, int *bornes, int taille_tableau );

/*! \fn int generer_PDF()
    \brief Lance les scripts R afin de générer les PDF à partir des fichiers CSV
    \return -1 S'il y aune erreur ors de l'appel à la fonction system(), 0 sinon
    \pre la simulation à généré des fichiers CSV.
*/
int generer_PDF();

/*! \fn int afficher_PDF()
    \brief Lance le programme evince avec les fichiers PDF générés durant la simulation
    \pre la simulation à généré des fichiers CSV.
*/
int afficher_PDF();

/*! \fn void supprimer_ancien_csv()
    \brief Supprime les fichiers present dans le répertoire des fichiers csv du projet.
*/
void supprimer_ancien_csv();
