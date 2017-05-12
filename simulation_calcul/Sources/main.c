#include "../Headers/simulation.h"
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

int main ( int argc, char *argv[] )
{
	int generer_pdf = ( (argc == 2) && ( ( strcmp(argv[1], "pdf") == 0 ) || ( strcmp(argv[1], "PDF") == 0 ) ) );
	if ( (generer_pdf == 1) && (NOMBRE_TIC >= 500000) )
	{
		generer_pdf = 0;
		printf("Le nombre de Tic est trop élevé pour faire la génération des fichiers PDF. L'ordinateur ne le supportera pas !\n");
	}

	/* Mise en place de la structure des fichiers necessaire à la sauvegarde des données */
	supprimer_ancien_csv();

	FILE *f = NULL;
	if (generer_pdf == 1)
		f = setup_fichier_attente_message();

	time_t debut, fin, total;
	time(&debut);

	int nombre_tic_restant = NOMBRE_TIC;
	printf("Nombre de slot de l'anneau : %d\n", NOMBRE_SLOT);
	printf("Nombre de noeud de l'anneau : %d\n\n", NOMBRE_NOEUD);

	/* Initialisation des slots et noeuds de l'anneau. */
	Slot *slots[ NOMBRE_SLOT ];
	Noeud *noeuds[ NOMBRE_NOEUD ];
	initialiser_slots(slots);
	initialiser_noeuds(noeuds, slots);

	/*printf("Etat initial des slots\n");
	afficher_slots(slots);


	printf("Etat initial des noeuds\n");
	afficher_noeuds(noeuds);*/

	while (nombre_tic_restant > 0)
	{
		entrer_messages( slots, noeuds, NOMBRE_TIC - nombre_tic_restant, f );
		decaler_messages(slots);
		sortir_messages(slots);

		/*afficher_noeuds(noeuds);
		printf("\n\n");

		afficher_slots(slots);
		printf("\n\n");

		printf("\n############################\n");*/

		nombre_tic_restant--;
	}
	time(&fin);
	total = ( fin - debut );
	printf("Temps total pris pour la rotation totale de l'anneau :  %ld secondes\n", total);

	if (f != NULL)
		fclose(f);

	/* On génére les fichiers CSV restant, on génére les PDF via les cript R et on ouvre ces PDF avec evince */
	if (generer_pdf == 1)
	{
		ecrire_etat_noeud(noeuds, NOMBRE_TIC - nombre_tic_restant);

		printf("Libération de la mémoire\n");
		liberer_memoire(slots, noeuds);

		printf("Génération des fichiers PDF...\n");
		generer_PDF();
		printf("Ouverture des fichiers PDF...\n");
		afficher_PDF();
	}
	else
	{
		printf("Libération de la mémoire");
		liberer_memoire(slots, noeuds);
	}

	return (0);
}
