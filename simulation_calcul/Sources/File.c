#include <stdio.h>
#include <stdlib.h>
#include "../Headers/File.h"

File* creer_file()
{
	File *file = (File *) malloc(sizeof(File));
	file->messages = (int*) calloc(TAILLE_INITIALE, sizeof(int) );
	file->taille = TAILLE_INITIALE;
	file->taille_utilisee = 0;
	file->indice_fin = 0;
	file->indice_debut = 0;

	return file;
}

void ajouter_message(File *file, int message)
{
	if (file->indice_fin >= file->taille)
	{
		file->messages = (int*) realloc(file->messages, (2 * file->taille) * sizeof(int) );
		file->taille = 2 * file->taille;
	}
	file->messages[ file->indice_fin ] = message;
    file->indice_fin++;
	file->taille_utilisee++;
}

int supprimer_message(File *file)
{
	if (file->indice_debut >= file->taille)
	{
		file->messages = (int*) realloc(file->messages, (2 * file->taille) * sizeof(int) );
		file->taille = 2 * file->taille;
	}
	int message = file->messages[ file->indice_debut ];
	file->indice_debut++;
	file->taille_utilisee--;
    return message;
}

void liberer_file(File *file)
{
	free(file->messages);
	free(file);
}

void afficher_messages_file(File *file)
{
	int i;
	for(i=0; i<file->taille; i++)
		printf("[%d]", file->messages[i]);
	printf("\n");
}
