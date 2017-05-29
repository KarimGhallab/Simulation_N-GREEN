#include "../Headers/simulation.h"
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <unistd.h>

int main ( int argc, char *argv[] )
{
	/* Mise en place de la structure des fichiers necessaire à la sauvegarde des données */
	supprimer_ancien_csv();

	/* Gestion de la génération ou de la non-génération du PDF */
	int generer_pdf = ( (argc == 2) && ( ( strcmp(argv[1], "-pdf") == 0 ) || ( strcmp(argv[1], "-PDF") == 0 ) ) );

	/* Initialisation des anneaux */
	int nombre_slot = 25; int nombre_noeud = 5;
	int nombre_anneau = 1; int i;
	Anneau *anneaux[nombre_anneau];
	for (i=0; i<nombre_anneau; i++)
		anneaux[i] = initialiser_anneau(nombre_slot, nombre_noeud, generer_pdf);

	for (i=0; i<nombre_anneau; i++)
	{
		printf("Simulation n° %d\n", i+1);
		effectuer_simulation(anneaux[i], generer_pdf);
		printf("Libération de la mémoire...\n");
		liberer_memoire_anneau(anneaux[i]);
	}
	if (generer_pdf == 1)
	{
		printf("Génération des fichiers PDF...\n");
		int copie_stdout = dup(1);
		fermer_fichier_std();
		int res = generer_PDF();
		res = afficher_PDF();
		if (res != 1)
		{
			dup2(copie_stdout, 1);
			printf("Erreur lors de la génération ou l'affichage du PDF...\n");
			close(1);
		}
	}
	else
		fermer_fichier_std();
	return (0);
}
