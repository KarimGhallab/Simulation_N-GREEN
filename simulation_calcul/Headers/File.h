#include "CoupleNombreValeur.h"

/*! \file File.h
    \brief Header du fichier contenant la structure représentant une file.
 */

 /*! \def TAILLE_INITIALE
     \brief La taille initiale d'un tableau de message pour une File.
  */
#define TAILLE_INITIALE 500000

/*! \struct File
    \brief Structure représentant une File de message.
 */
struct File
{
	CoupleNombreValeur *messages;
	int indice_fin;
	int indice_debut;
	double taille;
	double nb_message_file;
};
typedef struct File File;

/*! \fn File* creer_file()
    \brief Ajoute un message en fin de file.
    \return *File La file créée.
 */
File* creer_file();

/*! \fn void ajouter_message(File *file, int nb_message, int message)
    \brief Ajoute un message en fin de file.
    \param *file la file à laquelle on souhaite ajouter un message.
	\param nb_message Le nombre de message à ajouter.
	\param message Le message à ajouter pour chaque nombre de message.
 */
void ajouter_message(File *file, int nb_message, int message);

/*! \fn void supprimer_message(File *file, int nb_message, int *messages)
    \brief Retire plusieurs messages en debut de file et les ajoute au tableau de message.
    \param *file la file à laquelle on souhaite retirer les messages.
	\param nb_message Le nombre de message que l'on souhaite retirer.
	\param *messages Le tableau de message à initialiser.
 */
void supprimer_message(File *file, int nb_message, int *messages);

/*! \fn void liberer_file(File *file)
    \brief Libère l'espace mémoire pris par la file
    \param *file la file pour laquelle on souhaite libèrer l'espace mémoire.
 */
void liberer_file(File *file);

/*! \fn void afficher_messages_file(File *file)
    \brief Affiche la liste des messages d'une file.
    \param *file la file pour laquelle on souhaite afficher les messages.
 */
void afficher_messages_file(File *file);
