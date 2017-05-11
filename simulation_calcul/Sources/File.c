#include <stdio.h>
#include <stdlib.h>
#include "../Headers/File.h"

File* creer_file()
{
	File *file = (File *) malloc(sizeof(File));
	file->indice_fin = 0;
	file->indice_debut = 0;

	return file;
}

void ajouter_message(File *file, int message)
{
    file->messages[ file->indice_fin ] = message;
    file->indice_fin++;
}

int supprimer_message(File *file)
{
    int message = file->messages[ file->indice_debut ];
	file->indice_debut++;
    return message;
}
