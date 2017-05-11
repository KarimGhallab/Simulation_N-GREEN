/*!
 * \file File.h
 * \brief Header du fichier contenant la structure représentant une file.
 */

#define TAILLE_MAX 5000000

struct File
{
	int messages[ TAILLE_MAX ];
	int indice_fin;
	int indice_debut;
};

typedef struct File File;

File* creer_file();

void ajouter_message(File *file, int message);

int supprimer_message(File *file);

void liberer_file(File *file);
