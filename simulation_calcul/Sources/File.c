#include <stdio.h>
#include <stdlib.h>
#include "../Headers/File.h"

File* creer_file()
{
	File *file = (File *) malloc(sizeof(File));
	file->taille = TAILLE_INITIALE;
	file->nb_message_file = 0;
	file->indice_fin = 0;
	file->indice_debut = 0;

	file->messages = (CoupleNombreValeur *) malloc(file->taille * sizeof(CoupleNombreValeur) );

	return file;
}

void ajouter_message(File *file, int nb_message, int message)
{
	if (file->indice_fin >= file->taille)
	{
		File *ancien_pointeur = file;
		file->messages = (CoupleNombreValeur *) realloc(file->messages, (2 * file->taille) * sizeof(CoupleNombreValeur) );
		file->taille = 2 * file->taille;
		if (ancien_pointeur != file)
			free(ancien_pointeur);
	}

	CoupleNombreValeur cnv = initialiser_couple_nombre_valeur(nb_message, message);
	file->messages[file->indice_fin] = cnv;
    file->indice_fin++;
	file->nb_message_file += nb_message;
}

void supprimer_message(File *file, int nb_message, int *messages)
{
	file->nb_message_file -= nb_message;
	if (file->indice_debut >= file->taille)
	{
		File *ancien_pointeur = file;
		file->messages = (CoupleNombreValeur *) realloc(file->messages, (2 * file->taille) * sizeof(CoupleNombreValeur) );
		file->taille = 2 * file->taille;
		if (ancien_pointeur != file)
			free(ancien_pointeur);
	}
	int nb_message_restant = nb_message;
	int indice_messages = 0;
	int i;

	while (nb_message_restant != 0)
	{
		if ( file->messages[ file->indice_debut ].nombre_valeur < nb_message_restant )		//Le nombre de message est insuffisant pour complêter le nb de message demandé
		{
			nb_message_restant -= file->messages[ file->indice_debut ].nombre_valeur;
			for(i=0; i<file->messages[ file->indice_debut ].nombre_valeur; i++)
			{
				messages[indice_messages] = file->messages[ file->indice_debut ].valeur;
				indice_messages++;
			}
			file->indice_debut++;
		}
		else
		{
			file->messages[ file->indice_debut ].nombre_valeur -= nb_message_restant;
			for(i=0; i<nb_message_restant; i++)
			{
				messages[indice_messages] = file->messages[ file->indice_debut ].valeur;
				indice_messages++;
			}
			nb_message_restant = 0;
		}
	}
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
	{
		/*if (file->messages[i] != NULL)
			printf("Nombre de message[%d], Valeur des messages [%d]\n", file->messages[i][0], file->messages[i][1]);*/
	}
	printf("\n");
}
