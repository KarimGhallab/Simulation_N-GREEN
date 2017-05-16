#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <unistd.h>
#include <dirent.h>

#include "../Headers/simulation.h"
#include "../Headers/hyper_expo.h"

void initialiser_slots( Slot *slots[] )
{
	int cpt = 0;
	for (cpt=0; cpt<NOMBRE_SLOT; cpt++)
	{
		slots[cpt] = (Slot *) malloc( sizeof(Slot) );
		slots[cpt]->id = cpt; slots[cpt]->indice_noeud_lecture = -1; slots[cpt]->indice_noeud_ecriture = -1; slots[cpt]->contient_message = 0;
	}
}

void afficher_slots( Slot *slots[] )
{
	int i;
	printf("Les slots de l'anneau\n");
	for (i = 0; i < NOMBRE_SLOT; i++)
	{
		int indice_noeud_emetteur;
		if (slots[i]->contient_message == 0)
			indice_noeud_emetteur = -1;
		else
			indice_noeud_emetteur = slots[i]->paquet_message->indice_noeud_emetteur;
		printf("Indice du tableau : %d     Id du slot : %d    Il contient un paquet : %d    Noeud emetteur du paquet : %d    Indice en lecture : %d    Indice en écriture : %d\n", i, slots[i]->id, slots[i]->contient_message == 1, indice_noeud_emetteur, slots[i]->indice_noeud_lecture, slots[i]->indice_noeud_ecriture);
	}
}

void initialiser_noeuds( Noeud *noeuds[], Slot *slots[] )
{
	time_t t;
	srand((unsigned) time(&t));		//Initialise le générateur de nombre aléatoire

	int pas = NOMBRE_SLOT / NOMBRE_NOEUD;
	int nombre_antenne;
	int j;
	for (j=0; j<NOMBRE_NOEUD; j++)
	{
		/* Génére le nombre d'antenne pour le noeud courant */
		if ( (j == 0) || (j == NOMBRE_NOEUD -1) )
				nombre_antenne = 0;
		else
				nombre_antenne = ( rand() % 4 ) +1;	//Génére un entier entre 1 et 5
		int debut_periode = rand() % 99;

		int indice_slot_lecture = (( (j*pas) + ((j+1)*pas) ) / 2) - 1;
		int indice_slot_ecriture = indice_slot_lecture - 1;
		if (indice_slot_ecriture < 0)
				indice_slot_ecriture = NOMBRE_SLOT -1;

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

void afficher_noeuds( Noeud *noeuds[] )
{
	printf("Les noeuds de l'anneau\n");
	int i;
	for (i = 0; i < NOMBRE_NOEUD; i++)
	{
		//Version complete
		//printf("Indice du tableau : %d     Id du noeud : %d    Nombre de message : %d    Indice en lecture : %d    Indice en écriture : %d    Nombre d'antenne : %d    Décalage : %d    Attente max : %d    nb message total : %d    attente total : %d\n\n", i, noeuds[i].id, noeuds[i].nb_message, noeuds[i].indice_slot_lecture, noeuds[i].indice_slot_ecriture, noeuds[i].nb_antenne, noeuds[i].debut_periode, noeuds[i].attente_max, noeuds[i].nb_message_total, noeuds[i].attente_totale);
		//version courte
		printf("Indice du tableau : %d     Id du noeud : %d    Nombre de message : %d    Indice en lecture : %d    Indice en écriture : %d    Attente max : %d    nb message total : %lf    attente total : %lf\n\n", i, noeuds[i]->id, noeuds[i]->nb_message, noeuds[i]->indice_slot_lecture, noeuds[i]->indice_slot_ecriture, noeuds[i]->attente_max, noeuds[i]->nb_message_total, noeuds[i]->attente_totale);
	}
}

TableauDynamique* initialiser_tableau_dynamique()
{
	TableauDynamique *td = (TableauDynamique *) malloc( sizeof(TableauDynamique) );
	td->taille_tableau = TAILLE_INITIALE_TABLEAU;
	td->tableau = (int *) calloc(TAILLE_INITIALE_TABLEAU, sizeof(int) );
	td->taille_utilisee = 0;
	return td;
}

void afficher_tableau_dynamique( TableauDynamique *td )
{
	int taille_utilisee = td->taille_utilisee;
	int taille_tableau = td->taille_tableau;
	int i;
	printf("Taille totale du tableau : %d\n", taille_tableau);
	printf("Taille utilisée du tableau : %d\n", taille_utilisee);
	for (i=0; i<taille_tableau; i++)
		printf("[%d] ", td->tableau[i]);
	printf("\n\n");
}

void ajouter_valeur( TableauDynamique *td, int valeur )
{
	if (td->taille_utilisee+1 > td->taille_tableau)		//Il faut réallouer l'espace du tableau
	{
		printf("Limite atteinte, On double la taille du tableau\n");
		td->tableau = (int * ) realloc(td->tableau, (2 * td->taille_tableau) * sizeof(int) );
		td->taille_tableau = td->taille_tableau * 2;
	}
	td->tableau[td->taille_utilisee] = valeur;
	td->taille_utilisee++;
}

void entrer_messages( Slot *slots[], Noeud *noeuds[], int tic, FILE *f )
{
	Noeud *noeud;	//Le noeud courant
	int nb_message;		//Le nombre de message envoyé par le noeud courant
	int messages[80];	//Un tableau des messages qu'envoi le noeud courant
	int i;
	for (i=0; i< NOMBRE_SLOT; i++)
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

					placer_message( noeud, noeud->id, slots[ noeud->indice_slot_ecriture ], LIMITE_NOMBRE_MESSAGE_MAX, messages, tic, f );
					noeuds[ slots[i]->indice_noeud_ecriture ]->nb_message -= LIMITE_NOMBRE_MESSAGE_MAX;
				}
				else	//Le nombre de message est compris entre le minimum est le maximum, on vide donc le noeud.
				{
					//On enleve les messages du noeud
					int nb_messages_noeud = noeud->nb_message;
					for (k=0; k<nb_messages_noeud; k++)
						messages[k] = supprimer_message( noeud->file_messages );

					placer_message( noeud, noeud->id, slots[ noeud->indice_slot_ecriture ], noeud->nb_message, messages, tic, f );
					noeuds[ slots[i]->indice_noeud_ecriture ]->nb_message = 0;
				}
			}
		}
	}
}

void placer_message( Noeud *noeud, int indice_noeud_emetteur, Slot *slot, int nombre_message, int messages[], int tic, FILE *f )
{
	//printf("Le noeud %d envoie un message\n", noeud->id);
	PaquetMessage *paquet = (PaquetMessage *) malloc( sizeof(PaquetMessage) );
	paquet->indice_noeud_emetteur = indice_noeud_emetteur;
	paquet->nombre_messages = nombre_message;

	/* Affecte le tableau de message */
	/* Met à jour les temps d'attentes du noeud qui envoi le message */
	int i; int temps_attente[ nombre_message ]; int temps_attente_message;

	for (i=0; i<nombre_message; i++)
	{
		paquet->messages[i] = messages[i];

		temps_attente_message = tic - paquet->messages[i];
		temps_attente[i] = temps_attente_message;

		if (temps_attente_message > noeud->attente_max)
			noeud->attente_max = temps_attente_message;

		noeud->attente_totale += temps_attente_message;
	}
	slot->paquet_message = paquet;
	slot->contient_message = 1;

	/* Ecrit dans un fichier les temps d'attente des messages */
	ecrire_attente_message(f, temps_attente, nombre_message, indice_noeud_emetteur);
}

void decaler_messages( Slot *slots[] )
{
	PaquetMessage *tmp_message = slots[ NOMBRE_SLOT-1 ]->paquet_message;
	int tmp_contient = slots[ NOMBRE_SLOT-1 ]->contient_message;

	int i;
	/* Boucle sur le tableau de la fin jusqu'à la première case */
	for (i=NOMBRE_SLOT-1; i>=0; i--)
	{
		if (i -1 < 0)	//Il faut échanger le premier est le dernier élement
		{
			slots[ NOMBRE_SLOT-1 ]->paquet_message = tmp_message;
			slots[ NOMBRE_SLOT-1 ]->contient_message = tmp_contient;
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

void sortir_messages( Slot *slots[] )
{
	int i;
	for (i=0; i<NOMBRE_SLOT; i++)
	{
		if ( (slots[i]->contient_message == 1) && (slots[i]->indice_noeud_lecture == slots[i]->paquet_message->indice_noeud_emetteur) )
			{
				//printf("Le slot %d sort un message\n", slots[i]->id);
				free( slots[i]->paquet_message ) ;
				slots[i]->contient_message = 0;
			}
	}
}

void liberer_memoire( Slot *slots[], Noeud *noeuds[], TableauDynamique *td )
{
	int i;
	/* Libère la mémoire prise par les slots et leur paquet de message */
	for (i=0; i<NOMBRE_SLOT; i++)
	{
		if (slots[i]->contient_message == 1)
		{
			free( slots[i]->paquet_message );
		}
		free( slots[i] );
	}

	/* Libère la mémoire prise par les noeuds et leurs liste chainees */
	for (i=0; i<NOMBRE_NOEUD; i++)
	{
		free( noeuds[i]->file_messages );
		free( noeuds[i] );
	}
	
	/* Libération de l'espace mémoire pris par le tableau dynamique */
	free(td->tableau);
	free(td);
}

void fermer_fichier_std()
{
	close(0);
	close(1);
	close(2);
}


void get_temps_attente_max( Noeud *noeuds[], double resultats[] )
{
	int i = 0;
	for (i=0; i<NOMBRE_NOEUD; i++)
		resultats[i] = noeuds[i]->attente_max;
}

void get_temps_attente_moyen( Noeud *noeuds[], double resultats[] )
{
	int i = 0;
	for (i=0; i<NOMBRE_NOEUD; i++)
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

void ecrire_etat_noeud( Noeud *noeuds[], int tic)
{
	static int numero_fichier = 1;

	/* Récupère les données à ecrire */
	double attente_max[ NOMBRE_NOEUD ];
	double attente_moyenne[ NOMBRE_NOEUD ];

	get_temps_attente_max(noeuds, attente_max);
	get_temps_attente_moyen(noeuds, attente_moyenne);

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
	for (i=0; i<NOMBRE_NOEUD; i++)
	{
		fprintf(f, "%d,max,%lf,%d\n", i, attente_max[i], tic);
		fprintf(f, "%d,moyenne,%lf,%d\n", i, attente_moyenne[i], tic);
	}
	fclose(f);

	numero_fichier++;
}

void generer_PDF()
{
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
				system(commande);
			}
		}
		closedir(repertoire);
	}
}

void afficher_PDF()
{
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
				system(commande);
			}
		}
		closedir(repertoire);
	}
}

void ecrire_attente_message(FILE *f, int tics[], int taille_tableau, int noeud_emetteur)
{
	if (f != NULL)
	{
		int i;
		for (i=0; i<taille_tableau; i++)
			fprintf(f, "%d,%d\n", noeud_emetteur, tics[i]);
	}
}

FILE* setup_fichier_attente_message(int tic)
{
	char *nom_fichier = "../CSV/attentes_messages.csv";
	FILE *f = fopen(nom_fichier, "w");	//Ouvre un fichier, si le fichier existe déjà, son contenu est ecrasé
	fprintf(f, "Noeud,TIC_attente,%d\n", tic);
	return f;
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
