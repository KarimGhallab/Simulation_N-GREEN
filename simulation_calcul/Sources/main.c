#include "../Headers/simulation.h"
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

int main ( int argc, char *argv[] )
{
	/* Gestion de la génération ou de la non-génération du PDF */
	int generer_pdf = ( (argc == 2) && ( ( strcmp(argv[1], "-pdf") == 0 ) || ( strcmp(argv[1], "-PDF") == 0 ) ) );
	if ( (generer_pdf == 1) && (NOMBRE_TIC >= 500000) )
	{
		generer_pdf = 0;
		printf("Le nombre de Tic est trop élevé pour faire la génération des fichiers PDF. L'ordinateur ne le supportera pas !\n");
	}
	/* Affichage des paramètres de la simulation */
	printf("Nombre de TIC de la simulation : %d\n", NOMBRE_TIC);
	printf("Nombre de slot de l'anneau : %d\n", NOMBRE_SLOT);
	printf("Nombre de noeud de l'anneau : %d\n\n", NOMBRE_NOEUD);

	/* Mise en place de la structure des fichiers necessaire à la sauvegarde des données */
	supprimer_ancien_csv();

	FILE *f = NULL;
	if (generer_pdf == 1)
		f = setup_fichier_attente_message(NOMBRE_TIC);

	time_t debut, fin, total;
	time(&debut);

	int nombre_tic_restant = NOMBRE_TIC;

	/* Initialisation des slots et noeuds de l'anneau. */
	Slot *slots[ NOMBRE_SLOT ];
	Noeud *noeuds[ NOMBRE_NOEUD ];
	initialiser_slots(slots);
	initialiser_noeuds(noeuds, slots);
	TableauDynamique *td = initialiser_tableau_dynamique();

	/*printf("Etat initial des slots\n");
	afficher_slots(slots);


	printf("Etat initial des noeuds\n");
	afficher_noeuds(noeuds);*/

	/*int saut_interval = 40;
	int interval = nombre_tic_restant / saut_interval;
	int cmp = 1;
	int pourcentage;*/
	while (nombre_tic_restant > 0)
	{
	/* Gestion de la barre de chargement */
		/*if (nombre_tic_restant % interval == 0)
		{
			char chargement[ saut_interval +3 ];
			initialiser_barre_chargement(chargement, saut_interval +2, cmp);
			pourcentage = (cmp / (float) saut_interval) *100;
			printf("\r%s %d%%", chargement, pourcentage);
			fflush(stdout);
			cmp++;
		}*/
		entrer_messages( slots, noeuds, NOMBRE_TIC - nombre_tic_restant, td );
		decaler_messages(slots);
		sortir_messages(slots);

		/*afficher_noeuds(noeuds);
		printf("\n\n");

		afficher_slots(slots);
		printf("\n\n");

		printf("\n############################\n");*/

		nombre_tic_restant--;
	}
	printf("\n\n");
	time(&fin);
	total = ( fin - debut );
	printf("Temps total pris pour la rotation totale de l'anneau :  %ld secondes\n", total);
	afficher_tableau_dynamique(td);
	ecrire_quantile_message(td);
	if (f != NULL)
		fclose(f);

	if (generer_pdf == 1)	//On génére les fichiers CSV restants, on génére les PDFs via les scripts R et on ouvre ces PDFs avec evince
	{
		ecrire_etat_noeud(noeuds, NOMBRE_TIC - nombre_tic_restant);

		printf("Libération de la mémoire...\n");
		liberer_memoire(slots, noeuds, td);

		printf("Génération des fichiers PDF...\n");
		fermer_fichier_std();
		generer_PDF();
		afficher_PDF();
	}
	else
	{
		printf("Libération de la mémoire...\n");
		liberer_memoire(slots, noeuds, td);
		printf("Mémoire libérée !\n");
	}
	return (0);
}
