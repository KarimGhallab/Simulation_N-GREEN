#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

#include "../Headers/simulation.h"

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

		noeuds[j]->messages = creer_Liste_chainee();

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

void entrer_messages( Slot *slots[], Noeud *noeuds[], int tic )
{
	int i;
	for (i=0; i< NOMBRE_SLOT; i++)
	{
		if (slots[i]->indice_noeud_ecriture != -1)	//Le slot est un slot d'ecriture
		{
			Noeud *noeud = noeuds[ slots[i]->indice_noeud_ecriture ];

			//Le slot affiche si c'est sa période de réception de message provenant des antennes
			/*if (tic % PERIODE_MESSAGE_ANTENNE == noeuds[ slots[i].indice_noeud_ecriture ].debut_periode)	//C'est la periode du noeud, il reçoit un message de ses antennes
				printf ("C'est le moment ! Periode du noeud : %d. Je recois un message provenant de mes %d antennes.\n", noeud.debut_periode, noeud.nb_antenne);*/

			int nb_message = hyper_expo();
			//int nb_message = 20;
			//printf("Le noeud %d recois %d messages\n", noeud->id, nb_message);

			//On ajoute au noeud le tic d'arrivé des messages
			int j;
			for (j=0; j<nb_message; j++)
				inserer_fin(noeuds[ slots[i]->indice_noeud_ecriture ]->messages, tic);

			noeuds[ slots[i]->indice_noeud_ecriture ]->nb_message += nb_message;
			noeuds[ slots[i]->indice_noeud_ecriture ]->nb_message_total += nb_message;

			if ( ( slots[i]->contient_message == 0) && (noeuds[ slots[i]->indice_noeud_ecriture ]->nb_message >= LIMITE_NOMBRE_MESSAGE_MIN) )
			{
				int k;
				if (noeuds[ slots[i]->indice_noeud_ecriture ]->nb_message >= LIMITE_NOMBRE_MESSAGE_MAX)
				{
					/* On enleve les messages du noeud */
					int messages [ LIMITE_NOMBRE_MESSAGE_MAX ];
					for (k=0; k<LIMITE_NOMBRE_MESSAGE_MAX; k++)
						messages[k] = supprimer_premier(noeuds[ slots[i]->indice_noeud_ecriture ]->messages);

					placer_message( noeuds[ slots[i]->indice_noeud_ecriture ], noeuds[ slots[i]->indice_noeud_ecriture ]->id, slots[ noeud->indice_slot_ecriture ], LIMITE_NOMBRE_MESSAGE_MAX, messages, tic );
					noeuds[ slots[i]->indice_noeud_ecriture ]->nb_message -= LIMITE_NOMBRE_MESSAGE_MAX;
				}
				else	//Le nombre de message est compris entre le minimum est le maximum, on vide donc le noeud.
				{
					//On enleve les messages du noeud
					int messages [ noeuds[ slots[i]->indice_noeud_ecriture ]->nb_message ];
					for (k=0; k<noeuds[ slots[i]->indice_noeud_ecriture ]->nb_message; k++)
						messages[k] = supprimer_premier(noeuds[ slots[i]->indice_noeud_ecriture ]->messages);

					placer_message( noeuds[ slots[i]->indice_noeud_ecriture ], noeuds[ slots[i]->indice_noeud_ecriture ]->id, slots[ noeud->indice_slot_ecriture ], noeuds[ slots[i]->indice_noeud_ecriture ]->nb_message, messages, tic );
					noeuds[ slots[i]->indice_noeud_ecriture ]->nb_message = 0;
				}
			}
		}
	}
}

void placer_message( Noeud *noeud, int indice_noeud_emetteur, Slot *slot, int nombre_message, int messages[], int tic )
{
	//printf("Le noeud %d envoie un message\n", noeud->id);
	PaquetMessage *paquet = (PaquetMessage *) malloc( sizeof(PaquetMessage) );
	paquet->indice_noeud_emetteur = indice_noeud_emetteur;
	paquet->nombre_messages = nombre_message;

	/* Affecte le tableau de message */
	/* Met à jour les temps d'attentes du noeud qui envoi le message */
	int i;
	for (i=0; i<nombre_message; i++)
	{
		paquet->messages[i] = messages[i];

		int temps_attente_message = tic - paquet->messages[i];
		if (temps_attente_message > noeud->attente_max)
			noeud->attente_max = temps_attente_message;

		noeud->attente_totale += temps_attente_message;
	}
	slot->paquet_message = paquet;
	slot->contient_message = 1;
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

void liberer_memoire( Slot *slots[], Noeud *noeuds[] )
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
		vider_liste( noeuds[i]->messages );
		free( noeuds[i] );
	}

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

void ecrire_etat_noeud( Noeud *noeuds[] )
{
	static int numero_fichier = 1;

	/* Récupère les données à ecrire */
	double attente_max[ NOMBRE_NOEUD ];
	double attente_moyenne[ NOMBRE_NOEUD ];

	get_temps_attente_max(noeuds, attente_max);
	get_temps_attente_moyen(noeuds, attente_moyenne);

	/* Création du nom du fichier csv */
	char *debut_nom_fichier = "../R/attente";
	char buffer[3];
	char chemin_fichier[20];

	strcpy(chemin_fichier, debut_nom_fichier);

	sprintf(buffer, "%d", numero_fichier);
	strcat(chemin_fichier, buffer);
	strcat(chemin_fichier, ".csv");

	/* Ouverture du fichier */
	FILE *f = fopen(chemin_fichier, "w");

	fprintf(f, "numero_noeud,type_attente,TIC\n");

	int i;

	/* Les deux tableaux font la même taille (celle du nommbre de noeud dans l'anneau) */
	for (i=0; i<NOMBRE_NOEUD; i++)
	{
		fprintf(f, "%d,max,%lf\n", i, attente_max[i]);
		fprintf(f, "%d,moyenne,%lf\n", i, attente_moyenne[i]);
	}
	fclose(f);

	numero_fichier++;
}

void afficher_graphique_attente()
{
	/* Lance le prgramme R qui crée un PDF avec le graphique avant de l'ouvrir avec evince */
	system("R -f ../R/attente.R");
	system("evince ../R/Rplots.pdf &");

}
