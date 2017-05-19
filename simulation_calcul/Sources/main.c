#include "../Headers/simulation.h"
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

int main ( int argc, char *argv[] )
{
	/* Gestion de la génération ou de la non-génération du PDF */
	int generer_pdf = ( (argc == 2) && ( ( strcmp(argv[1], "-pdf") == 0 ) || ( strcmp(argv[1], "-PDF") == 0 ) ) );

	int nombre_slot = 25; int nombre_noeud = 5;
	/* Initialisation de l'anneau */
	Anneau *anneau = initialiser_anneau(nombre_slot, nombre_noeud, generer_pdf);

	/* Affichage des paramètres de la simulation */
	printf("\n");
	printf("Nombre de TIC de la simulation : %d.\n", NOMBRE_TIC);
	printf("Nombre de slot de l'anneau : %d.\n", nombre_slot);
	printf("Nombre de noeud de l'anneau : %d.\n", nombre_noeud);
	if (generer_pdf == 1)
		printf("Generation des PDFs : Oui.\n\n");
	else
		printf("Generation des PDFs : Non.\n\n");

	/* Mise en place de la structure des fichiers necessaire à la sauvegarde des données */
	supprimer_ancien_csv();

	time_t debut, fin, total;
	time(&debut);

	int nombre_tic_restant = NOMBRE_TIC;

	/*printf("Etat initial des slots\n");
	afficher_slots(anneau->slots);


	printf("Etat initial des noeuds\n");
	afficher_noeuds(anneau->noeuds);*/

	int saut_interval = 40;
	int interval = nombre_tic_restant / saut_interval;
	int cmp = 1;
	int pourcentage;

	printf("\n");
	while (nombre_tic_restant > 0)
	{
		/* Gestion de la barre de chargement */
		if (nombre_tic_restant % interval == 0)
		{
			char chargement[ saut_interval +3 ];
			initialiser_barre_chargement(chargement, saut_interval +2, cmp);
			pourcentage = (cmp / (float) saut_interval) *100;
			printf("\r%s %d%%", chargement, pourcentage);
			fflush(stdout);
			cmp++;
		}
		entrer_messages( anneau, NOMBRE_TIC - nombre_tic_restant );
		decaler_messages( anneau );
		sortir_messages( anneau );

		/*afficher_noeuds(noeuds);
		printf("\n\n");

		afficher_slots(slots);
		printf("\n\n");*/

		nombre_tic_restant--;
	}
	printf("\n\n\n");
	time(&fin);
	total = ( fin - debut );
	printf("Temps total pris pour la rotation totale de l'anneau : %ld secondes.\n", total);

	afficher_etat_anneau(anneau);

	/* Gestion de la création ou non-création des CSVs et PDFs */
	if (generer_pdf == 1)	//On génére les fichiers CSVs on génére les PDFs via les scripts R et on ouvre ces PDFs avec evince
	{
		printf("Ecriture des fichiers CSV...\n");
		ecrire_etat_noeud(anneau, NOMBRE_TIC - nombre_tic_restant);
		ecrire_repartition_attentes(anneau);

		printf("Libération de la mémoire...\n");
		liberer_memoire_anneau(anneau);

		printf("Génération des fichiers PDF...\n");
		fermer_fichier_std();
		generer_PDF();
		afficher_PDF();
	}
	else
	{
		printf("Libération de la mémoire...\n");
		liberer_memoire_anneau(anneau);
		fermer_fichier_std();
	}
	return (0);
}
