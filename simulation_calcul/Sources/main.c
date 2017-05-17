#include "../Headers/simulation.h"
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

int main ( int argc, char *argv[] )
{
	/* Gestion de la génération ou de la non-génération du PDF */
	int generer_pdf = ( (argc == 2) && ( ( strcmp(argv[1], "-pdf") == 0 ) || ( strcmp(argv[1], "-PDF") == 0 ) ) );

	/* Affichage des paramètres de la simulation */
	printf("\n");
	printf("Nombre de TIC de la simulation : %d.\n", NOMBRE_TIC);
	printf("Nombre de slot de l'anneau : %d.\n", NOMBRE_SLOT);
	printf("Nombre de noeud de l'anneau : %d.\n", NOMBRE_NOEUD);
	TableauDynamique *td = NULL;
	if (generer_pdf == 1)
	{
		printf("Generation des PDFs : Oui.\n\n");
		td = initialiser_tableau_dynamique();
	}
	else
		printf("Generation des PDFs : Non.\n\n");

	/* Mise en place de la structure des fichiers necessaire à la sauvegarde des données */
	supprimer_ancien_csv();

	time_t debut, fin, total;
	time(&debut);

	int nombre_tic_restant = NOMBRE_TIC;

	/* Initialisation des slots et noeuds de l'anneau. */
	Slot *slots[ NOMBRE_SLOT ];
	Noeud *noeuds[ NOMBRE_NOEUD ];
	initialiser_slots(slots);
	initialiser_noeuds(noeuds, slots);

	/*printf("Etat initial des slots\n");
	afficher_slots(slots);


	printf("Etat initial des noeuds\n");
	afficher_noeuds(noeuds);*/

	int saut_interval = 40;
	int interval = nombre_tic_restant / saut_interval;
	int cmp = 1;
	int pourcentage;
	while (nombre_tic_restant > 0)
	{
		/* Gestion de la barre de chargement */
		if (nombre_tic_restant % interval == 0)
		{
			//printf("Entré dans la zone de chargement\n");
			char chargement[ saut_interval +3 ];
			initialiser_barre_chargement(chargement, saut_interval +2, cmp);
			pourcentage = (cmp / (float) saut_interval) *100;
			printf("\r%s %d%%", chargement, pourcentage);
			fflush(stdout);
			cmp++;
			//printf("\n");
			//printf("Sortie de la zone de chargement\n");
		}
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
	printf("Temps total pris pour la rotation totale de l'anneau : %ld secondes.\n", total);

	if (generer_pdf == 1)	//On génére les fichiers CSV restants, on génére les PDFs via les scripts R et on ouvre ces PDFs avec evince
	{
		printf("Ecriture des fichiers CSV...\n");
		ecrire_etat_noeud(noeuds, NOMBRE_TIC - nombre_tic_restant);
		ecrire_repartition_attentes(td);

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
		fermer_fichier_std();
		printf("Mémoire libérée !\n");
	}
	return (0);
}
