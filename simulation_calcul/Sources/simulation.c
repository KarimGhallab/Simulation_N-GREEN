#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <unistd.h>
#include <dirent.h>

#include "../Headers/simulation.h"
#include "../Headers/hyper_expo.h"

Anneau* initialiser_anneau( int nombre_slot, int nombre_noeud, int generer_pdf )
{
	static int numero = 0;
	numero++;
	Anneau *anneau = (Anneau*) malloc( sizeof(Anneau) );

	anneau->nombre_slot = nombre_slot; anneau->nombre_noeud = nombre_noeud;
	anneau->numero_anneau = numero; anneau->nb_message = 0; anneau->decallage = 0;
	anneau->couple_lecture = (int **) malloc(nombre_noeud * sizeof(int *) );
	anneau->couple_ecriture = (int **) malloc(nombre_noeud * sizeof(int *) );

	if (generer_pdf == 1)
		anneau->messages = initialiser_tableau_dynamique();
	else
		anneau->messages = NULL;


	initialiser_slots(anneau, nombre_slot);
	initialiser_noeuds(anneau, nombre_noeud);

	return anneau;
}

void afficher_etat_anneau(Anneau *anneau)
{
	Slot *slots = anneau->slots; Noeud *noeuds = anneau->noeuds;
	int nombre_slot = anneau->nombre_slot; int nombre_noeud = anneau->nombre_noeud;
	int nombre_message = anneau->nb_message; int nombre_slot_plein = 0;


	int i;
	/* Le nombre de slot contenant un message */
	for(i=0; i<nombre_slot;i++)
	{
		if (slots[i].contient_message == 1)
			nombre_slot_plein++;
	}
	printf("Anneau numéro %d\n", anneau->numero_anneau);
	printf("%d/%d slots sont plein\n", nombre_slot_plein, nombre_slot);
	printf("Le nombre de message ayant circulé dans l'anneau est de : %d\n", nombre_message);
	for(i=0; i<nombre_noeud;i++)
		printf("Le Noeud numéro %d contient %lf message(s)\n", i, noeuds[i].file_messages->nb_message_file);

	/*printf("Affichage des couples\n");
	printf("Couple lecture\n");
	for(i=0; i<nombre_noeud;i++)
		printf("Le Noeud [%d] Slot [%d] \n", anneau->couple_lecture[i][0], anneau->couple_lecture[i][1]);

	printf("Couple ecriture\n");
	for(i=0; i<nombre_noeud;i++)
		printf("Le Noeud [%d] Slot [%d] \n", anneau->couple_ecriture[i][0], anneau->couple_ecriture[i][1]);*/
}

void initialiser_slots( Anneau *anneau, int nombre_slot )
{
	anneau->slots = (Slot*) malloc( nombre_slot * sizeof(Slot) );

	int cpt = 0;
	for (cpt=0; cpt<nombre_slot; cpt++)
	{
		anneau->slots[cpt].id = cpt; anneau->slots[cpt].indice_noeud_lecture = -1;
		anneau->slots[cpt].indice_noeud_ecriture = -1; anneau->slots[cpt].contient_message = 0;
	}
}

void afficher_slots( Anneau *anneau )
{
	Slot *slots = anneau->slots;
	int nombre_slot = anneau->nombre_slot;

	int i;
	printf("Les slots de l'anneau\n");
	for (i = 0; i < nombre_slot; i++)
	{
		int indice_noeud_emetteur;
		if (slots[i].contient_message == 0)
			indice_noeud_emetteur = -1;
		else
			indice_noeud_emetteur = slots[i].noeud_emetteur_paquet;
		printf("Indice du tableau : %d     Id du slot : %d    Il contient un paquet : %d    Noeud emetteur du paquet : %d    Indice en lecture : %d    Indice en écriture : %d\n", i, slots[i].id, slots[i].contient_message == 1, indice_noeud_emetteur, slots[i].indice_noeud_lecture, slots[i].indice_noeud_ecriture);
	}
}

void initialiser_noeuds( Anneau *anneau, int nombre_noeud )
{
	anneau->noeuds = (Noeud*) malloc( nombre_noeud * sizeof(Noeud) );
	Noeud *noeuds = anneau->noeuds; Slot *slots = anneau->slots;
	int nombre_slot = anneau->nombre_slot;

	time_t t;
	srand((unsigned) time(&t));		//Initialise le générateur de nombre aléatoire

	int pas = nombre_slot / nombre_noeud;
	int nombre_antenne;
	int j;
	for (j=0; j<nombre_noeud; j++)
	{
		/* Génére le nombre d'antenne pour le noeud courant */
		if ( (j == 0) || (j == nombre_noeud -1) )
				nombre_antenne = 0;
		else
				nombre_antenne = ( rand() % 4 ) +1;	//Génére un entier entre 1 et 5
		int debut_periode = rand() % 99;

		int indice_slot_lecture = (( (j*pas) + ((j+1)*pas) ) / 2) - 1;
		int indice_slot_ecriture = indice_slot_lecture - 1;
		if (indice_slot_ecriture < 0)
				indice_slot_ecriture = nombre_slot -1;

		/* Création du noeud */
		noeuds[j].id = j; noeuds[j].nb_message = 0; noeuds[j].indice_slot_lecture = indice_slot_lecture;
		noeuds[j].indice_slot_ecriture = indice_slot_ecriture; noeuds[j].nb_antenne = nombre_antenne;
		noeuds[j].debut_periode = debut_periode;
		noeuds[j].attente_max = 0; noeuds[j].nb_message_total = 0; noeuds[j].attente_totale = 0;
		noeuds[j].tableau_tics_envois = initialiser_tableau_dynamique();

		noeuds[j].file_messages = creer_file();

		/* Met à jour les indices des slots */
		slots[ indice_slot_lecture ].indice_noeud_lecture = j;
		slots[ indice_slot_ecriture ].indice_noeud_ecriture = j;
	}

	int i;
	int **couple_lecture = anneau->couple_lecture;
	int **couple_ecriture = anneau->couple_ecriture;
	for (i=0; i<nombre_noeud; i++)
	{
		couple_lecture[i] = (int *) malloc(2 * sizeof(int) );
		couple_lecture[i][0] = noeuds[i].id;
		couple_lecture[i][1] = slots [noeuds[i].indice_slot_lecture].id;

		couple_ecriture[i] = (int *) malloc(2 * sizeof(int) );
		couple_ecriture[i][0] = noeuds[i].id;
		couple_ecriture[i][1] = slots [noeuds[i].indice_slot_ecriture].id;
	}
}

void afficher_noeuds( Anneau *anneau )
{
	printf("Les noeuds de l'anneau\n");
	int nombre_noeud = anneau->nombre_noeud;
	Noeud *noeuds = anneau->noeuds;

	int i;
	for (i = 0; i < nombre_noeud; i++)
	{
		//Version complete
		//printf("Indice du tableau : %d     Id du noeud : %d    Nombre de message : %d    Indice en lecture : %d    Indice en écriture : %d    Nombre d'antenne : %d    Décalage : %d    Attente max : %d    nb message total : %d    attente total : %d\n\n", i, noeuds[i].id, noeuds[i].nb_message, noeuds[i].indice_slot_lecture, noeuds[i].indice_slot_ecriture, noeuds[i].nb_antenne, noeuds[i].debut_periode, noeuds[i].attente_max, noeuds[i].nb_message_total, noeuds[i].attente_totale);
		//version courte
		printf("Indice du tableau : %d     Id du noeud : %d    Nombre de message : %d    Indice en lecture : %d    Indice en écriture : %d    Attente max : %d    nb message total : %lf    attente total : %lf\n\n", i, noeuds[i].id, noeuds[i].nb_message, noeuds[i].indice_slot_lecture, noeuds[i].indice_slot_ecriture, noeuds[i].attente_max, noeuds[i].nb_message_total, noeuds[i].attente_totale);
	}
}

void effectuer_simulation(Anneau *anneau, int generer_pdf, int afficher_chargement)
{
	/* Affichage des paramètres de la simulation */
	printf("\n");
	printf("Nombre de TIC de la simulation : %d.\n", NOMBRE_TIC);
	printf("Nombre de slot de l'anneau : %d.\n", anneau->nombre_slot);
	printf("Nombre de noeud de l'anneau : %d.\n", anneau->nombre_noeud);
	if (generer_pdf == 1)
		printf("Generation des PDFs : Oui.\n\n");
	else
		printf("Generation des PDFs : Non.\n\n");

	int nombre_tic_restant = NOMBRE_TIC;
	int saut_interval = 40; int cmp = 1;
	int interval = nombre_tic_restant / saut_interval;
	int pourcentage;
	char chargement[ saut_interval +3 ];

	while (nombre_tic_restant > 0)
	{
		//printf("Tic numéro %d\n", (NOMBRE_TIC - nombre_tic_restant) + 1);
		/* Gestion de la barre de chargement */
		if ((afficher_chargement == 1) && (nombre_tic_restant % interval == 0) )
		{
			initialiser_barre_chargement(chargement, saut_interval +2, cmp);
			pourcentage = (cmp / (float) saut_interval) *100;
			printf("\r%s %d%%", chargement, pourcentage);
			fflush(stdout);
			cmp++;
		}
		entrer_messages( anneau, NOMBRE_TIC - nombre_tic_restant );
		sortir_messages( anneau );
		decaler_messages( anneau );

		/*afficher_noeuds(noeuds);
		printf("\n\n");

		afficher_slots(slots);
		printf("\n\n");*/

		nombre_tic_restant--;
	}	//fin de la rotation
	printf("\n");

	ecrire_tics_sorties(anneau);

	afficher_etat_anneau(anneau);

	printf("\n\n\n");

	/* Gestion de la création ou non-création des CSVs et PDFs */
	if (generer_pdf == 1)	//On génére les fichiers CSVs on génére les PDFs via les scripts R et on ouvre ces PDFs avec evince
	{
		printf("Ecriture des fichiers CSV...\n");
		ecrire_fichier_csv(anneau);
	}
}

void entrer_messages( Anneau *anneau, int tic )
{
	TableauDynamique *td = anneau->messages;
	int ** couple_ecriture = anneau->couple_ecriture;
	int nombre_slot = anneau->nombre_slot;
	int nombre_noeud = anneau->nombre_noeud;

	Noeud *noeud;	//Le noeud courant
	Slot *slot;
	int nb_message;		//Le nombre de message envoyé par le noeud courant

	int i;

	for (i=0; i< nombre_noeud; i++)
	{
		noeud = &(anneau->noeuds[ couple_ecriture[i][0] ]);
		int position_slot = (couple_ecriture[i][1] + anneau->decallage) % nombre_slot;
		slot = &(anneau->slots[position_slot]);

		//Le noeud affiche si c'est sa période de réception de message provenant des antennes
		/*if (tic % PERIODE_MESSAGE_ANTENNE == noeud->debut_periode)
			printf ("C'est le moment ! Periode du noeud : %d. Je recois un message provenant de mes %d antennes.\n", noeud->debut_periode, noeud->nb_antenne);*/

		nb_message = hyper_expo();
		//printf("Le noeud %d recois %d messages\n", noeud->id, nb_message);

		//On ajoute au noeud le tic d'arrivé des messages
		ajouter_message( noeud->file_messages, nb_message, tic );

		noeud->nb_message += nb_message;
		noeud->nb_message_total += nb_message;

		if ( ( slot->contient_message == 0) && (noeud->nb_message >= LIMITE_NOMBRE_MESSAGE_MIN) )
		{
			if (noeud->nb_message >= LIMITE_NOMBRE_MESSAGE_MAX)
			{
				/* On enleve les messages du noeud */
				int messages[LIMITE_NOMBRE_MESSAGE_MAX];
				supprimer_message( noeud->file_messages, LIMITE_NOMBRE_MESSAGE_MAX, messages );
				anneau->nb_message += LIMITE_NOMBRE_MESSAGE_MAX;
				placer_message( noeud, noeud->id, slot, LIMITE_NOMBRE_MESSAGE_MAX, messages, tic, td);
				noeud->nb_message -= LIMITE_NOMBRE_MESSAGE_MAX;
			}
			else	//Le nombre de message est compris entre le minimum est le maximum, on vide donc le noeud.
			{
				//On enleve les messages du noeud
				int nb_messages_noeud = noeud->nb_message;
				int messages[nb_messages_noeud];
				supprimer_message( noeud->file_messages, nb_messages_noeud, messages );
				anneau->nb_message += nb_messages_noeud;
				placer_message( noeud, noeud->id, slot, nb_messages_noeud, messages, tic, td );
				noeud->nb_message = 0;
			}
		}
	}
}

void placer_message( Noeud *noeud, int indice_noeud_emetteur, Slot *slot, int nombre_message, int messages[], int tic, TableauDynamique *td )
{
	//printf("Le noeud %d envoie un message\n", noeud->id);
	//printf("\nAjout de la valeur %d au noeud numéro %d\n", tic, noeud->id);
	ajouter_valeur(noeud->tableau_tics_envois, tic);
	slot->noeud_emetteur_paquet = indice_noeud_emetteur;

	/* Affecte le tableau de message */
	/* Met à jour les temps d'attentes du noeud qui envoie le message */
	int i; int temps_attente_message;

	for (i=0; i<nombre_message; i++)
	{
		temps_attente_message = tic - messages[i];
		if (td != NULL)
			ajouter_valeur(td, temps_attente_message);

		if (temps_attente_message > noeud->attente_max)
			noeud->attente_max = temps_attente_message;

		noeud->attente_totale += temps_attente_message;
	}
	slot->contient_message = 1;
}

void decaler_messages( Anneau *anneau )
{
	int nombre_slot = anneau->nombre_slot;
	anneau->decallage++;
	anneau->decallage = anneau->decallage % nombre_slot;
}

void sortir_messages( Anneau *anneau )
{
	Slot *slot;
	Noeud *noeud;
	int nombre_slot = anneau->nombre_slot;
	int nombre_noeud = anneau->nombre_noeud;
	int **couple_lecture = anneau->couple_lecture;
	int i;
	for (i=0; i< nombre_noeud; i++)
	{
		noeud = &(anneau->noeuds[ couple_lecture[i][0] ]);
		int position_slot = (couple_lecture[i][1] + anneau->decallage) % nombre_slot;

		slot = &(anneau->slots[position_slot]);

		if ( (slot->contient_message == 1) && (noeud->id == slot->noeud_emetteur_paquet) )
			slot->contient_message = 0;
	}
}

void liberer_memoire_anneau( Anneau *anneau )
{
	Noeud *noeuds = anneau->noeuds;
	TableauDynamique *td = anneau->messages;
	int nombre_noeud = anneau->nombre_noeud;
	/* Libère la mémoire prise par les slots */
	free(anneau->slots);

	/* Libère la mémoire prise par les noeuds et leurs File */
	int i;
	for (i=0; i<nombre_noeud; i++)
	{
		liberer_file( noeuds[i].file_messages );
		free(anneau->couple_lecture[i]);
		free(anneau->couple_ecriture[i]);
	}
	free(anneau->couple_ecriture);
	free(anneau->couple_lecture);
	free(noeuds);

	/* Libération de l'espace mémoire pris par le tableau dynamique */
	if (td != NULL)
	{
		free(td->tableau);
		free(td);
	}

	free(anneau);
}

void fermer_fichier_std()
{
	close(0);
	close(1);
	close(2);
}

void initialiser_barre_chargement(char *chargement, int taille_tableau, int nombre_chargement)
{
	chargement[0] = '[';
	chargement[taille_tableau-1] = ']';
	chargement[taille_tableau] = '\0';

	int i;
	for(i=1; i<=nombre_chargement;i++)
		chargement[i] = '=';
	if (i < taille_tableau -1)
	{
		for(i=nombre_chargement; i<taille_tableau-1;i++)
		{
			if (i != taille_tableau -1)
				chargement[i] = ' ';
		}
	}
}

void ecrire_tics_sorties(Anneau *anneau)
{
	int nombre_noeud = anneau->nombre_noeud; int nombre_slot = anneau->nombre_slot;
	Noeud *noeuds = anneau->noeuds;
	int numero_anneau = anneau->numero_anneau;
	int i;

	char *debut_nom_fichier = "../../fichiers_simulations/simulation";
	char buffer[3];
	char chemin_fichier[65];

	strcpy(chemin_fichier, debut_nom_fichier);
	sprintf(buffer, "%d", numero_anneau);
	strcat(chemin_fichier, buffer);
	strcat(chemin_fichier, ".csv");

	/* Ouverture du fichier */
	FILE *f = fopen(chemin_fichier, "w");
	if (f != NULL)
	{
		/* Ecriture des nombre de noeuds et des slots */
		fprintf(f, "%d\n%d\n", nombre_noeud, nombre_slot);

		int j;
		for(i=0; i<nombre_noeud; i++)
		{
			fprintf(f, "%d,", i);
			TableauDynamique *td = noeuds[i].tableau_tics_envois;
			int taille_utilisee = td->taille_utilisee;
			for (j=0; j<taille_utilisee; j++)
			{
				//printf("Ecriture de la valeur : %d\n", );
				if (j == taille_utilisee -1)
					fprintf(f, "%d", td->tableau[j]);
				else
					fprintf(f, "%d,", td->tableau[j]);
			}
			fprintf(f, "\n");
		}
		fclose(f);
	}
	else
		printf("Erreur ouverture du fichiers pour stocker les tics de sorties des noeuds\n");
}

int cmpfunc (const void * a, const void * b)
{
   return ( *(int*)a - *(int*)b );
}

void ecrire_fichier_csv(Anneau *anneau)
{
	int nombre_quantile = 5;
	//Ecriture de la répartition des temps d'attente (Min, Max, moyenne)
	int i; int j = 0; int nombre_colonne = 4;
	double max; double min; double somme_valeur = 0;
	TableauDynamique *td = anneau->messages;
	int taille_utilisee = td->taille_utilisee;

	/* Trie du tableau */
	int *tableau = td->tableau;
	qsort(tableau, taille_utilisee, sizeof(int), cmpfunc);

	int val_max = tableau[taille_utilisee-1];
	int bornes_superieures[nombre_quantile];

	int interval = taille_utilisee / nombre_quantile+1;
	for(i=1; i<=nombre_quantile; i++)
		bornes_superieures[i-1] = i * interval;
	if (bornes_superieures[nombre_quantile-1] < taille_utilisee)
		bornes_superieures[nombre_quantile-1] = taille_utilisee;
	int borne_superieure = bornes_superieures[0];

	//Allocation du tableau
	double **quantiles = (double **) calloc(nombre_quantile+1, sizeof(double));	//tableau de la forme: nombre_message, min, max, moyenne
	for(i=0; i<nombre_quantile+1; i++)
		quantiles[i] = (double *) calloc(nombre_colonne, sizeof(double));	//La premiere ligne du tableau

	min = tableau[0];
	for (i=0; i<taille_utilisee; i++)
	{
		if ( (i % interval == 0) && (i != 0))
		{
			//Assignation des valeurs pour la borne précedente
			max = tableau[i-1];
			quantiles[j][2] = max; quantiles[j][3] = somme_valeur/quantiles[j][0];
			somme_valeur = 0;
			min = tableau[i];
			j++;
			if (j < nombre_quantile+1)
				quantiles[j][1] = min;
		}
		somme_valeur += tableau[i];
		if (j < nombre_quantile+1)
			quantiles[j][0]++;
	}
	quantiles[nombre_quantile-1][2] = val_max;
	quantiles[nombre_quantile-1][3] = somme_valeur/quantiles[j][0];

	ecrire_nb_message_attente_csv(anneau, quantiles, nombre_quantile, bornes_superieures);
	/* Libération de la mémoire du quantile */
	for(i=0; i<nombre_quantile+1; i++)
		free(quantiles[i]);
	free(quantiles);

	//Ecriture du nombre de message ayant attendu selon un interval de TIC
	double *quantiles_nb_message = (double *) calloc(nombre_quantile, sizeof(double));	//tableau de la forme: nombre_message, min, max, moyenne

	j = 0;
	interval = val_max / nombre_quantile;;
	if (interval < 1)
		interval = 1;
	for(i=1; i<=nombre_quantile; i++)
		bornes_superieures[i-1] = i * interval;

	if (bornes_superieures[nombre_quantile-1] < val_max)
		bornes_superieures[nombre_quantile-1] = val_max;

	borne_superieure = bornes_superieures[0];

	min = tableau[0];
	for (i=0; i<taille_utilisee; i++)
	{
		if ( (tableau[i] >= borne_superieure) && (j < nombre_quantile-1) )
		{
			j++;
			borne_superieure = bornes_superieures[j];
		}
		quantiles_nb_message[j]++;
	}
	ecrire_temps_attente_csv(anneau, quantiles_nb_message, bornes_superieures, nombre_quantile);
	free(quantiles_nb_message);
}

void ecrire_nb_message_attente_csv(Anneau *anneau, double **quantiles, int taille_tableau, int *bornes)
{
	int numero_anneau = anneau->numero_anneau;
	int nombre_noeud = anneau->nombre_noeud;
	int nombre_slot = anneau->nombre_slot;

	char *debut_nom_fichier = "../CSV/repartition_attentes";
	char buffer[3];
	char chemin_fichier[65];

	strcpy(chemin_fichier, debut_nom_fichier);
	sprintf(buffer, "%d", numero_anneau);
	strcat(chemin_fichier, buffer);
	strcat(chemin_fichier, ".csv");

	/* Ouverture du fichier */
	FILE *f = fopen(chemin_fichier, "w");

	fprintf(f, "interval,type_valeur,valeur,TIC,nb_slot,nb_noeud\n");
	int i;
	int borne_inferieure = 0;
	for (i=0; i<taille_tableau; i++)
	{
		int borne_superieure = bornes[i];
		if (quantiles[i][0] == 0)
			break;
		fprintf(f, "%d:%d,Min,%lf,%d,%d,%d\n", borne_inferieure, borne_superieure, quantiles[i][1], NOMBRE_TIC, nombre_slot, nombre_noeud);
		fprintf(f, "%d:%d,Moyenne,%lf,%d,%d,%d\n", borne_inferieure, borne_superieure, quantiles[i][3], NOMBRE_TIC, nombre_slot, nombre_noeud);
		fprintf(f, "%d:%d,Max,%lf,%d,%d,%d\n", borne_inferieure, borne_superieure, quantiles[i][2], NOMBRE_TIC, nombre_slot, nombre_noeud);
		borne_inferieure = borne_superieure+1;
	}
	fclose(f);
}

void ecrire_temps_attente_csv( Anneau *anneau, double *quantiles, int *bornes, int taille_tableau )
{
	int nombre_noeud = anneau->nombre_noeud;
	int nombre_slot = anneau->nombre_slot;
	double nb_message_total = anneau->nb_message;

	/* Création du nom du fichier csv */
	char *debut_nom_fichier = "../CSV/attente_anneau";
	char buffer[3];
	char chemin_fichier[41];

	strcpy(chemin_fichier, debut_nom_fichier);
	sprintf(buffer, "%d", anneau->numero_anneau);
	strcat(chemin_fichier, buffer);
	strcat(chemin_fichier, ".csv");

	/* Ouverture du fichier */
	FILE *f = fopen(chemin_fichier, "w");

	fprintf(f, "interval,taux,TIC,nb_slot,nb_noeud\n");
	int i;
	int borne_inferieure = 0;
	for (i=0; i<taille_tableau; i++)
	{
		int borne_superieure = bornes[i];
		if (quantiles[i] == 0)
			break;
		double pourcentage = (quantiles[i] / nb_message_total);
		fprintf(f, "%d:%d,%lf,%d,%d,%d\n", borne_inferieure, borne_superieure, pourcentage, NOMBRE_TIC, nombre_slot, nombre_noeud);
		borne_inferieure = borne_superieure+1;
	}
	fclose(f);
}

int generer_PDF()
{
	int resultat = 1;
	DIR *repertoire;
	struct dirent *dir;

	repertoire = opendir("../Scripts_R/");	//On ouvre le répertoire des scripts R
	if (repertoire)		//Le repertoire s'est ouvert avec succès
	{
		//On execute tous les scripts R
		while ( (dir = readdir(repertoire) ) != NULL)
		{
			if (( strcmp(dir->d_name, ".") != 0 ) && ( strcmp(dir->d_name, "..") != 0 ) )
			{
				char commande[100] = "R -f ";

				char chemin_fichier[30] = "../Scripts_R/";

				strcat(chemin_fichier, dir->d_name);
				strcat(commande, chemin_fichier);

				/* La commande est prête ! On peut l'exécuter ! */
				if (system(commande) == -1)
					resultat = 1;
			}
		}
		closedir(repertoire);
	}
	return resultat;
}

int afficher_PDF()
{
	int resultat = 1;
	DIR *repertoire;
	struct dirent *dir;

	repertoire = opendir("../PDF/");	//On ouvre le répertoire des scripts R
	if (repertoire)		//Le repertoire s'est ouvert avec succès
	{
		//On lance evince avex tous les fichiers PDF
		while ( (dir = readdir(repertoire) ) != NULL)
		{
			if (( strcmp(dir->d_name, ".") != 0 ) && ( strcmp(dir->d_name, "..") != 0 ) )
			{
				char commande[100] = "evince ";

				char chemin_fichier[50] = "../PDF/";

				strcat(chemin_fichier, dir->d_name);
				strcat(commande, chemin_fichier);
				strcat(commande, " &");

				/* La commande est prête ! On peut l'exécuter ! */
				if (system(commande) == -1)
					resultat = 1;
			}
		}
		closedir(repertoire);
	}
	return resultat;
}

void supprimer_ancien_csv()
{
	DIR *repertoire;
	struct dirent *dir;

	/* Le premier repertoire */
	repertoire = opendir("../CSV/");
	if (repertoire)		//Le repertoire s'est ouvert avec succès
	{
		//On supprime tout les fichiers CSVs
		while ( (dir = readdir(repertoire) ) != NULL)
		{
			char chemin_fichier[65] = "../CSV/";
			strcat(chemin_fichier, dir->d_name);
			FILE *f = fopen(chemin_fichier, "r");

			if (f != NULL)
			{
				fclose(f);
				remove(chemin_fichier);
			}
		}
		closedir(repertoire);
	}
}
