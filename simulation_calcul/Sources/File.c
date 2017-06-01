#include <stdio.h>
#include <stdlib.h>
#include "../Headers/File.h"

File* creer_file()
{
	File *file = (File *) malloc(sizeof(File));
	file->taille = TAILLE_INITIALE;
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
}

void supprimer_message(File *file, int nb_message, int *messages)
{
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
				if (file->messages[ file->indice_debut ].valeur < 0)
					printf("valeur : %d\n", file->messages[ file->indice_debut ].valeur);
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
				if (file->messages[ file->indice_debut ].valeur < 0)
					printf("valeur : %d\n", file->messages[ file->indice_debut ].valeur);
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
	for(i=file->indice_debut; i<file->indice_fin; i++)
	{
		printf("Nombre de message[%d], Valeur des messages [%d]\n", file->messages[i].nombre_valeur, file->messages[i].valeur);
	}
	printf("\n");
}
