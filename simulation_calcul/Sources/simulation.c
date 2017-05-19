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
	Anneau *anneau = (Anneau*) malloc( sizeof(Anneau) );

	anneau->nombre_slot = nombre_slot; anneau->nombre_noeud = nombre_noeud;
	anneau->nb_message = 0;

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
	Slot **slots = anneau->slots; Noeud **noeuds = anneau->noeuds;
	int nombre_slot = anneau->nombre_slot; int nombre_noeud = anneau->nombre_noeud;
	int nombre_message = anneau->nb_message; int nombre_slot_plein = 0;


	int i;
	/* Le nombre de slot contenant un message */
	for(i=0; i<nombre_slot;i++)
	{
		if (slots[i]->contient_message == 1)
			nombre_slot_plein++;
	}
	printf("%d/%d slots sont plein", nombre_slot_plein, nombre_slot);
	printf("Le nombre de message ayant circulé dans l'anneau est de : %d\n", nombre_message);
	for(i=0; i<nombre_noeud;i++)
	{
		printf("Le Noeud numéro %d contient %lf message(s)\n", i, noeuds[i]->file_messages->taille_utilisee);
	}
}

void initialiser_slots( Anneau *anneau, int nombre_slot )
{
	anneau->slots = (Slot**) malloc( nombre_slot * sizeof(Slot) );

	int cpt = 0;
	for (cpt=0; cpt<nombre_slot; cpt++)
	{
		anneau->slots[cpt] = (Slot *) malloc( sizeof(Slot) );
		anneau->slots[cpt]->id = cpt; anneau->slots[cpt]->indice_noeud_lecture = -1;
		anneau->slots[cpt]->indice_noeud_ecriture = -1; anneau->slots[cpt]->contient_message = 0;
	}
}

void afficher_slots( Anneau *anneau )
{
	Slot **slots = anneau->slots;
	int nombre_slot = anneau->nombre_slot;

	int i;
	printf("Les slots de l'anneau\n");
	for (i = 0; i < nombre_slot; i++)
	{
		int indice_noeud_emetteur;
		if (slots[i]->contient_message == 0)
			indice_noeud_emetteur = -1;
		else
			indice_noeud_emetteur = slots[i]->paquet_message->indice_noeud_emetteur;
		printf("Indice du tableau : %d     Id du slot : %d    Il contient un paquet : %d    Noeud emetteur du paquet : %d    Indice en lecture : %d    Indice en écriture : %d\n", i, slots[i]->id, slots[i]->contient_message == 1, indice_noeud_emetteur, slots[i]->indice_noeud_lecture, slots[i]->indice_noeud_ecriture);
	}
}

void initialiser_noeuds( Anneau *anneau, int nombre_noeud )
{
	anneau->noeuds = (Noeud**) malloc( nombre_noeud * sizeof(Noeud) );
	Noeud **noeuds = anneau->noeuds; Slot **slots = anneau->slots;
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
		noeuds[j] = (Noeud *) malloc( sizeof(Noeud) );

		noeuds[j]->id = j; noeuds[j]->nb_message = 0; noeuds[j]->indice_slot_lecture = indice_slot_lecture;
		noeuds[j]->indice_slot_ecriture = indice_slot_ecriture; noeuds[j]->nb_antenne = nombre_antenne;
		noeuds[j]->debut_periode = debut_periode;
		noeuds[j]->attente_max = 0; noeuds[j]->nb_message_total = 0; noeuds[j]->attente_totale = 0;

		noeuds[j]->file_messages = creer_file();

		/* Met à jour les indices des slots */
		slots[ indice_slot_lecture ]->indice_noeud_lecture = j;
		slots[ indice_slot_ecriture ]->indice_noeud_ecriture = j;
	}
}

void afficher_noeuds( Anneau *anneau )
{
	printf("Les noeuds de l'anneau\n");
	int nombre_noeud = anneau->nombre_noeud;
	Noeud **noeuds = anneau->noeuds;

	int i;
	for (i = 0; i < nombre_noeud; i++)
	{
		//Version complete
		//printf("Indice du tableau : %d     Id du noeud : %d    Nombre de message : %d    Indice en lecture : %d    Indice en écriture : %d    Nombre d'antenne : %d    Décalage : %d    Attente max : %d    nb message total : %d    attente total : %d\n\n", i, noeuds[i].id, noeuds[i].nb_message, noeuds[i].indice_slot_lecture, noeuds[i].indice_slot_ecriture, noeuds[i].nb_antenne, noeuds[i].debut_periode, noeuds[i].attente_max, noeuds[i].nb_message_total, noeuds[i].attente_totale);
		//version courte
		printf("Indice du tableau : %d     Id du noeud : %d    Nombre de message : %d    Indice en lecture : %d    Indice en écriture : %d    Attente max : %d    nb message total : %lf    attente total : %lf\n\n", i, noeuds[i]->id, noeuds[i]->nb_message, noeuds[i]->indice_slot_lecture, noeuds[i]->indice_slot_ecriture, noeuds[i]->attente_max, noeuds[i]->nb_message_total, noeuds[i]->attente_totale);
	}
}

void entrer_messages( Anneau *anneau, int tic )
{
	Noeud **noeuds = anneau->noeuds; Slot **slots = anneau->slots;
	TableauDynamique *td = anneau->messages;
	int nombre_slot = anneau->nombre_slot;

	Noeud *noeud;	//Le noeud courant
	int nb_message;		//Le nombre de message envoyé par le noeud courant
	int messages[80];	//Un tableau des messages qu'envoi le noeud courant
	int i;
	for (i=0; i< nombre_slot; i++)
	{
		if (slots[i]->indice_noeud_ecriture != -1)	//Le slot est un slot d'ecriture
		{
			noeud = noeuds[ slots[i]->indice_noeud_ecriture ];

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

			if ( ( slots[i]->contient_message == 0) && (noeud->nb_message >= LIMITE_NOMBRE_MESSAGE_MIN) )
			{
				int k;
				if (noeud->nb_message >= LIMITE_NOMBRE_MESSAGE_MAX)
				{
					/* On enleve les messages du noeud */
					for (k=0; k<LIMITE_NOMBRE_MESSAGE_MAX; k++)
						messages[k] = supprimer_message( noeuds[ slots[i]->indice_noeud_ecriture ]->file_messages );
					anneau->nb_message += LIMITE_NOMBRE_MESSAGE_MAX;
					placer_message( noeud, noeud->id, slots[ noeud->indice_slot_ecriture ], LIMITE_NOMBRE_MESSAGE_MAX, messages, tic, td);
					noeuds[ slots[i]->indice_noeud_ecriture ]->nb_message -= LIMITE_NOMBRE_MESSAGE_MAX;
				}
				else	//Le nombre de message est compris entre le minimum est le maximum, on vide donc le noeud.
				{
					//On enleve les messages du noeud
					int nb_messages_noeud = noeud->nb_message;
					for (k=0; k<nb_messages_noeud; k++)
						messages[k] = supprimer_message( noeud->file_messages );
					anneau->nb_message += nb_messages_noeud;
					placer_message( noeud, noeud->id, slots[ noeud->indice_slot_ecriture ], nb_messages_noeud, messages, tic, td );
					noeuds[ slots[i]->indice_noeud_ecriture ]->nb_message = 0;
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
	/* Met à jour les temps d'attentes du noeud qui envoi le message */
	int i; int temps_attente_message;

	for (i=0; i<nombre_message; i++)
	{
		paquet->messages[i] = messages[i];

		temps_attente_message = tic - paquet->messages[i];
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
	Slot **slots = anneau->slots;
	PaquetMessage *tmp_message = slots[ nombre_slot-1 ]->paquet_message;
	int tmp_contient = slots[ nombre_slot-1 ]->contient_message;

	int i;
	/* Boucle sur le tableau de la fin jusqu'à la première case */
	for (i=nombre_slot-1; i>=0; i--)
	{
		if (i -1 < 0)	//Il faut échanger le premier est le dernier élement
		{
			slots[ nombre_slot-1 ]->paquet_message = tmp_message;
			slots[ nombre_slot-1 ]->contient_message = tmp_contient;
		}
		else
		{
			PaquetMessage *tmp_message_bis = slots[i-1]->paquet_message;
			slots[i-1]->paquet_message = tmp_message;
			tmp_message = tmp_message_bis;

			int tmp_contient_bis = slots[i-1]->contient_message;
			slots[i-1]->contient_message = tmp_contient;
			tmp_contient = tmp_contient_bis;
		}
	}
}

void sortir_messages( Anneau *anneau )
{
	Slot **slots = anneau->slots;
	int nombre_slot = anneau->nombre_slot;
	int i;
	for (i=0; i<nombre_slot; i++)
	{
		if ( (slots[i]->contient_message == 1) && (slots[i]->indice_noeud_lecture == slots[i]->paquet_message->indice_noeud_emetteur) )
			{
				//printf("Le slot %d sort un message\n", slots[i]->id);
				free( slots[i]->paquet_message ) ;
				slots[i]->contient_message = 0;
			}
	}
}

void liberer_memoire_anneau( Anneau *anneau )
{
	Slot **slots = anneau->slots; Noeud **noeuds = anneau->noeuds;
	TableauDynamique *td = anneau->messages;
	int nombre_noeud = anneau->nombre_noeud; int nombre_slot = anneau->nombre_slot;
	int i;
	/* Libère la mémoire prise par les slots et leur paquet de message */
	for (i=0; i<nombre_slot; i++)
	{
		if (slots[i]->contient_message == 1)
		{
			free( slots[i]->paquet_message );
		}
		free( slots[i] );
	}
	free(slots);

	/* Libère la mémoire prise par les noeuds et leurs liste chainees */
	for (i=0; i<nombre_noeud; i++)
	{
		liberer_file( noeuds[i]->file_messages );
		free( noeuds[i] );
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


void get_temps_attente_max( Anneau *anneau, double resultats[] )
{
	Noeud **noeuds = anneau->noeuds;
	int nombre_noeud = anneau->nombre_noeud;
	int i = 0;
	for (i=0; i<nombre_noeud; i++)
		resultats[i] = noeuds[i]->attente_max;
}

void get_temps_attente_moyen( Anneau *anneau, double resultats[] )
{
	Noeud **noeuds = anneau->noeuds;
	int nombre_noeud = anneau->nombre_noeud;
	int i = 0;
	for (i=0; i<nombre_noeud; i++)
		resultats[i] = noeuds[i]->attente_totale/noeuds[i]->nb_message_total;
}

void supprimer_ancien_csv()
{
	DIR *repertoire;
	struct dirent *dir;

	repertoire = opendir("../CSV/");	//On ouvre le répertoire des fichiers csv
	if (repertoire)		//Le repertoire s'est ouvert avec succès
	{
		//On supprime tout les fichiers csv
		while ( (dir = readdir(repertoire) ) != NULL)
		{
			char chemin_fichier[30] = "../CSV/";
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

void ecrire_etat_noeud( Anneau *anneau, int tic )
{
	static int numero_fichier = 1;
	int nombre_noeud = anneau->nombre_noeud;

	/* Récupère les données à ecrire */
	double attente_max[ nombre_noeud ];
	double attente_moyenne[ nombre_noeud ];

	get_temps_attente_max(anneau, attente_max);
	get_temps_attente_moyen(anneau, attente_moyenne);

	/* Création du nom du fichier csv */
	char *debut_nom_fichier = "../CSV/attente";
	char buffer[3];
	char chemin_fichier[20];

	strcpy(chemin_fichier, debut_nom_fichier);
	sprintf(buffer, "%d", numero_fichier);
	strcat(chemin_fichier, buffer);
	strcat(chemin_fichier, ".csv");

	/* Ouverture du fichier */
	FILE *f = fopen(chemin_fichier, "w");
	fprintf(f, "numero_noeud,type_attente,TIC,TIC_actuel\n");

	int i;

	/* Les deux tableaux font la même taille (celle du nommbre de noeud dans l'anneau) */
	for (i=0; i<nombre_noeud; i++)
	{
		fprintf(f, "%d,max,%lf,%d\n", i, attente_max[i], tic);
		fprintf(f, "%d,moyenne,%lf,%d\n", i, attente_moyenne[i], tic);
	}
	fclose(f);

	numero_fichier++;
}

int generer_PDF()
{
	int erreur = 0;
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
				strcat(commande, " > /tmp/out.txt");

				/* La commande est prête ! On peut l'exécuter ! */
				if (system(commande) == -1)
					erreur = 1;
			}
		}
		closedir(repertoire);
	}
	return erreur;
}

int afficher_PDF()
{
	int erreur = 0;
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
					erreur = 1;
			}
		}
		closedir(repertoire);
	}
	return erreur;
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

void ecrire_repartition_attentes(Anneau *anneau)
{
	TableauDynamique *td = anneau->messages;

	/* Trie du tableau */
	int *tableau = td->tableau;
	qsort(tableau, td->taille_utilisee, sizeof(int), cmpfunc);

	int nombre_valeur = 4;

	//int interval = NOMBRE_TIC / nombre_valeur;
	int premiere_limite = 7; int deuxieme_limite = 10; int troisieme_limite = 15; int quatrieme_limite = 20;
	int bornes_superieurs[] = {premiere_limite, deuxieme_limite, troisieme_limite, quatrieme_limite};
	int borne_superieure = bornes_superieurs[0];
	int i;
	int j = 0;
	double *quantiles = (double *) calloc(nombre_valeur, sizeof(double));

	for (i=0; i<td->taille_utilisee; i++)
	{
		if ( (tableau[i] >= borne_superieure) && (j < nombre_valeur-1) )
		{
			j++;
			borne_superieure = bornes_superieurs[j];
		}
		//printf("Valeur entre %d et %d\n", borne_inferieure, borne_superieure);
		quantiles[j]++;
	}
	ecrire_attente_message(quantiles, nombre_valeur, bornes_superieurs);
}

void ecrire_attente_message(double quantiles[], int taille_tableau, int bornes[])
{
	/* Ouverture du fichier */
	char *chemin_fichier = "../CSV/attentes_messages.csv";
	FILE *f = fopen(chemin_fichier, "w");

	fprintf(f, "interval,count,%d\n", NOMBRE_TIC);

	int i;
	int borne_inferieure = 0;
	for (i=0; i<taille_tableau; i++)
	{
		int borne_superieure = bornes[i];
		if (quantiles[i] == 0)
			break;
		fprintf( f, "%d:%d,%lf\n", borne_inferieure, borne_superieure, quantiles[i] );
		borne_inferieure = borne_superieure+1;
	}
	free(quantiles);
	fclose(f);
}
