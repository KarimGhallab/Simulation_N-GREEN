/*!
 * \file File.h
 * \brief Header du fichier contenant la structure représentant une file.
 */

 /*! \def TAILLE_MAX
  * \brief La taille maximale d'un tableau de message pour une File.
  */
#define TAILLE_INITIALE 500000

/*! \struct File
 * \brief Structure représentant une File de message.
 */
struct File
{
	int *messages;
	int indice_fin;
	int indice_debut;
	double taille;
	double taille_utilisee;
};
typedef struct File File;

/*! \fn File* creer_file()
 * \brief Ajoute un message en fin de file.
 * \return *File La file créée.
 */
File* creer_file();

/*! \fn void ajouter_message(File *file, int message)
 * \brief Ajoute un message en fin de file.
 * \param *file la file à laquelle on souhaite ajouter un message.
 * \param message Le message à ajouter.
 */
void ajouter_message(File *file, int message);

/*! \fn int supprimer_message(File *file)
 * \brief Retire un message en debut de file.
 * \param *file la file à laquelle on souhaite retirer un message.
 * \return Le message retiré de la file.
 */
int supprimer_message(File *file);

/*! \fn void liberer_file(File *file)
 * \brief Libère l'espace mémoire pris par la file
 * \param *file la file pour laquelle on souhaite libèrer l'espace mémoire.
 */
void liberer_file(File *file);

/*! \fn void afficher_messages_file(File *file)
 * \brief Affiche la liste des messages d'une file.
 * \param *file la file pour laquelle on souhaite afficher les messages.
 */
void afficher_messages_file(File *file);
