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
	anneau->numero_anneau = numero; anneau->nb_message = 0;

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
	{
		printf("Le Noeud numéro %d contient %lf message(s)\n", i, noeuds[i].file_messages->taille_utilisee);
	}
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
			indice_noeud_emetteur = slots[i].paquet_message->indice_noeud_emetteur;
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

		noeuds[j].file_messages = creer_file();

		/* Met à jour les indices des slots */
		slots[ indice_slot_lecture ].indice_noeud_lecture = j;
		slots[ indice_slot_ecriture ].indice_noeud_ecriture = j;
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

void effectuer_simulation(Anneau *anneau, int generer_pdf)
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

	//time_t debut, fin, total;
	clock_t debut = clock();

	while (nombre_tic_restant > 0)
	{
		/* Gestion de la barre de chargement */
		if (nombre_tic_restant % interval == 0)
		{
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
	}	//fin de la rotation
	printf("\n");
	afficher_etat_anneau(anneau);

	printf("\n\n\n");
	//time(&fin);
	//total = ( fin - debut );
	clock_t fin = clock();
	double total = (double)(fin - debut) / CLOCKS_PER_SEC;		//CLOCKS_PER_SEC est une constante déclarée dans time.h
	printf("Temps pris pour la rotation totale de l'anneau : %.3f secondes.\n", total);

	/* Gestion de la création ou non-création des CSVs et PDFs */
	if (generer_pdf == 1)	//On génére les fichiers CSVs on génére les PDFs via les scripts R et on ouvre ces PDFs avec evince
	{
		printf("Ecriture des fichiers CSV...\n");
		ecrire_fichier_csv(anneau);
	}
}

void entrer_messages( Anneau *anneau, int tic )
{
	Noeud *noeuds = anneau->noeuds; Slot *slots = anneau->slots;
	TableauDynamique *td = anneau->messages;
	int nombre_slot = anneau->nombre_slot;

	Noeud *noeud;	//Le noeud courant
	int nb_message;		//Le nombre de message envoyé par le noeud courant
	int messages[80];	//Un tableau des messages qu'envoi le noeud courant
	int i;
	for (i=0; i< nombre_slot; i++)
	{
		if (slots[i].indice_noeud_ecriture != -1)	//Le slot est un slot d'ecriture
		{
			noeud = &noeuds[ slots[i].indice_noeud_ecriture ];

			//Le slot affiche si c'est sa période de réception de message provenant des antennes
			/*if (tic % PERIODE_MESSAGE_ANTENNE == noeuds[ slots[i].indice_noeud_ecriture ].debut_periode)	//C'est la periode du noeud, il reçoit un message de ses antennes
				printf ("C'est le moment ! Periode du noeud : %d. Je recois un message provenant de mes %d antennes.\n", noeud.debut_periode, noeud.nb_antenne);*/

			nb_message = hyper_expo();
			//int nb_message = 20;
			//printf("Le noeud %d recois %d messages\n", noeud->id, nb_message);

			//On ajoute au noeud le tic d'arrivé des messages
			int j;
			for (j=0; j<nb_message; j++)
				ajouter_message( noeud->file_messages, tic );

			noeud->nb_message += nb_message;
			noeud->nb_message_total += nb_message;

			if ( ( slots[i].contient_message == 0) && (noeud->nb_message >= LIMITE_NOMBRE_MESSAGE_MIN) )
			{
				int k;
				if (noeud->nb_message >= LIMITE_NOMBRE_MESSAGE_MAX)
				{
					/* On enleve les messages du noeud */
					for (k=0; k<LIMITE_NOMBRE_MESSAGE_MAX; k++)
						messages[k] = supprimer_message( noeuds[ slots[i].indice_noeud_ecriture ].file_messages );
					anneau->nb_message += LIMITE_NOMBRE_MESSAGE_MAX;
					placer_message( noeud, noeud->id, &slots[ noeud->indice_slot_ecriture ], LIMITE_NOMBRE_MESSAGE_MAX, messages, tic, td);
					noeuds[ slots[i].indice_noeud_ecriture ].nb_message -= LIMITE_NOMBRE_MESSAGE_MAX;
				}
				else	//Le nombre de message est compris entre le minimum est le maximum, on vide donc le noeud.
				{
					//On enleve les messages du noeud
					int nb_messages_noeud = noeud->nb_message;
					for (k=0; k<nb_messages_noeud; k++)
						messages[k] = supprimer_message( noeud->file_messages );
					anneau->nb_message += nb_messages_noeud;
					placer_message( noeud, noeud->id, &slots[ noeud->indice_slot_ecriture ], nb_messages_noeud, messages, tic, td );
					noeuds[ slots[i].indice_noeud_ecriture ].nb_message = 0;
				}
			}
		}
	}
}

void placer_message( Noeud *noeud, int indice_noeud_emetteur, Slot *slot, int nombre_message, int messages[], int tic, TableauDynamique *td )
{
	//printf("Le noeud %d envoie un message\n", noeud->id);
	PaquetMessage *paquet = (PaquetMessage *) malloc( sizeof(PaquetMessage) );
	paquet->indice_noeud_emetteur = indice_noeud_emetteur;
	paquet->nombre_messages = nombre_message;

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
	slot->paquet_message = paquet;
	slot->contient_message = 1;
}

void decaler_messages( Anneau *anneau )
{
	int nombre_slot = anneau->nombre_slot;
	Slot *slots = anneau->slots;
	PaquetMessage *tmp_message = slots[ nombre_slot-1 ].paquet_message;
	int tmp_contient = slots[ nombre_slot-1 ].contient_message;

	int i;
	/* Boucle sur le tableau de la fin jusqu'à la première case */
	for (i=nombre_slot-1; i>=0; i--)
	{
		if (i -1 < 0)	//Il faut échanger le premier est le dernier élement
		{
			slots[ nombre_slot-1 ].paquet_message = tmp_message;
			slots[ nombre_slot-1 ].contient_message = tmp_contient;
		}
		else
		{
			PaquetMessage *tmp_message_bis = slots[i-1].paquet_message;
			slots[i-1].paquet_message = tmp_message;
			tmp_message = tmp_message_bis;

			int tmp_contient_bis = slots[i-1].contient_message;
			slots[i-1].contient_message = tmp_contient;
			tmp_contient = tmp_contient_bis;
		}
	}
}

void sortir_messages( Anneau *anneau )
{
	Slot *slots = anneau->slots;
	int nombre_slot = anneau->nombre_slot;
	int i;
	for (i=0; i<nombre_slot; i++)
	{
		if ( (slots[i].contient_message == 1) && (slots[i].indice_noeud_lecture == slots[i].paquet_message->indice_noeud_emetteur) )
		{
			//printf("Le slot %d sort un message\n", slots[i]->id);
			free( slots[i].paquet_message ) ;
			slots[i].contient_message = 0;
		}
	}
}

void liberer_memoire_anneau( Anneau *anneau )
{
	Slot *slots = anneau->slots; Noeud *noeuds = anneau->noeuds;
	TableauDynamique *td = anneau->messages;
	int nombre_noeud = anneau->nombre_noeud; int nombre_slot = anneau->nombre_slot;
	int i;
	/* Libère la mémoire prise par les slots et leur paquet de message */
	for (i=0; i<nombre_slot; i++)
	{
		if (slots[i].contient_message == 1)
		{
			free( slots[i].paquet_message );
		}
		//free( slots[i] );
	}
	free(slots);

	/* Libère la mémoire prise par les noeuds et leurs File */
	for (i=0; i<nombre_noeud; i++)
	{
		liberer_file( noeuds[i].file_messages );
	}
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

	//printf("Taille du tableau : %d, Nombre de chargement : %d\n", taille_tableau, nombre_chargement);
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
		//printf("%lf ", quantiles_nb_message[j]);
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
				//strcat(commande, " > /tmp/out.txt");

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
