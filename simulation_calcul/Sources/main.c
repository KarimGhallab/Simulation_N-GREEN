#include "../Headers/simulation.h"
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <time.h>
#include <string.h>
#include <unistd.h>
#include <omp.h>

int main ( int argc, char *argv[] )
{
	/* Mise en place de la structure des fichiers necessaire à la sauvegarde des données */
	//supprimer_ancien_csv();

	/* Gestion de la génération ou de la non-génération du PDF */
	int generer_pdf = ( (argc == 2) && ( ( strcmp(argv[1], "-pdf") == 0 ) || ( strcmp(argv[1], "-PDF") == 0 ) ) );

	/* Initialisation des anneaux */
	int nombre_slot = 25; int nombre_noeud = 5;
	int nombre_anneau = 1; int i;
	Anneau *anneaux[nombre_anneau];

	for (i=0; i<nombre_anneau; i++)
		anneaux[i] = initialiser_anneau(nombre_slot, nombre_noeud, generer_pdf, POLITIQUE_ENVOI_NON_PRIORITAIRE);
		//anneaux[i] = initialiser_anneau(nombre_slot, nombre_noeud, generer_pdf, POLITIQUE_ENVOI_PRIORITAIRE);

	struct timeval tb, te;
	gettimeofday(&tb, NULL); // get current time
    double beg_milliseconds = tb.tv_sec*1000LL + tb.tv_usec/1000; // calcule les miliseconde

	#pragma omp parallel for
	for (i=0; i<nombre_anneau; i++)
	{
		printf("Simulation n° %d\n", i+1);
		if (i == 0)
			effectuer_simulation(anneaux[i], generer_pdf, 1);
		else
			effectuer_simulation(anneaux[i], generer_pdf, 0);
		printf("Libération de la mémoire pour l'anneau %d...\n", i+1);
		liberer_memoire_anneau(anneaux[i]);
	}

	gettimeofday(&te, NULL); // get current time
	double end_milliseconds = te.tv_sec*1000LL + te.tv_usec/1000;
	double total = (end_milliseconds - beg_milliseconds) / 1000 ;

	printf("Temps pris pour la rotation totale de l'anneau ou des anneaux : %.3f secondes.\n", total);

	if (generer_pdf == 1)
	{
		printf("Génération des fichiers PDF...\n");
		fermer_fichier_std();
		int res = generer_PDF();
		res = afficher_PDF();
		if (res != 1)
			printf("Erreur lors de la génération ou l'affichage du PDF...\n");
	}
	else
		fermer_fichier_std();
	return (0);
}
