#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <unistd.h>
#include <dirent.h>

#include "../Headers/simulation.h"


Anneau* initialiser_anneau( int nombre_slot, int nombre_noeud, int generer_pdf, int politique_envoi )
{
	static int numero = 0;
	numero++;
	Anneau *anneau = (Anneau*) malloc( sizeof(Anneau) );

	anneau->nombre_slot = nombre_slot; anneau->nombre_noeud = nombre_noeud;
	anneau->numero_anneau = numero; anneau->nb_messages_initaux = 0; anneau->nb_messages_prioritaires = 0;
	anneau->decallage = 0; anneau->politique_envoi = politique_envoi;
	anneau->couple_lecture = (int **) malloc(nombre_noeud * sizeof(int *) );
	anneau->couple_ecriture = (int **) malloc(nombre_noeud * sizeof(int *) );
	anneau->tableau_poisson = initialiser_tableau_poisson();

	if (generer_pdf == 1)
	{
		anneau->messages_initaux = initialiser_tableau_dynamique_entier();
		if (politique_envoi == POLITIQUE_ENVOI_PRIORITAIRE)
			anneau->messages_prioritaires = initialiser_tableau_dynamique_entier();
		else
			anneau->messages_prioritaires = NULL;
	}
	else
	{
		anneau->messages_initaux = NULL;
		anneau->messages_prioritaires = NULL;
	}


	initialiser_slots(anneau, nombre_slot);
	initialiser_noeuds(anneau, nombre_noeud);

	return anneau;
}

void afficher_etat_anneau(Anneau *anneau)
{
	Slot *slots = anneau->slots; Noeud *noeuds = anneau->noeuds;
	int nombre_slot = anneau->nombre_slot; int nombre_noeud = anneau->nombre_noeud;
	int nombre_message = anneau->nb_messages_initaux + anneau->nb_messages_prioritaires;
	int nombre_slot_plein = 0;


	int i;
	/* Le nombre de slot contenant un message */
	for(i=0; i<nombre_slot;i++)
	{
		if (slots[i].contient_message == 1)
			nombre_slot_plein++;
	}
	printf("Anneau numéro %d\n", anneau->numero_anneau);
	if (anneau->politique_envoi == POLITIQUE_ENVOI_PRIORITAIRE)
		printf("Politique d'envoi : prorité au C-RAN\n");
	else
		printf("Politique d'envoi : sans priorité\n");

	if (nombre_slot_plein > 1)
		printf("%d/%d slots sont pleins\n", nombre_slot_plein, nombre_slot);
	else
		printf("%d/%d slot est plein\n", nombre_slot_plein, nombre_slot);
	printf("Le nombre de message ayant circulé dans l'anneau est de : %d\n", nombre_message);
	if (anneau->politique_envoi == POLITIQUE_ENVOI_NON_PRIORITAIRE)
	{
		for(i=0; i<nombre_noeud;i++)
			printf("Le Noeud numéro %d contient %lf message(s)\n", i, noeuds[i].nb_message);
	}
	else
	{
		for(i=0; i<nombre_noeud;i++)
			printf("Le Noeud numéro %d contient %lf message(s) Best effort et %lf message(s) prioritaire(s)\n", i, noeuds[i].nb_message_best_effort, noeuds[i].nb_message_prioritaires);
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
		noeuds[j].nb_message_best_effort = 0; noeuds[j].nb_message_best_effort_total = 0;
		noeuds[j].nb_message_prioritaires = 0; noeuds[j].nb_message_prioritaires_total = 0;
		noeuds[j].tableau_tics_envois = initialiser_tableau_dynamique_entier();

		noeuds[j].file_messages_initiale = creer_file();

		/* Gestion des cas en fonction de la politique d'envoi */
		if (anneau->politique_envoi == POLITIQUE_ENVOI_PRIORITAIRE)
			noeuds[j].file_messages_prioritaires = creer_file();
		else
			noeuds[j].file_messages_prioritaires = NULL;

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
		printf("Indice du tableau : %d     Id du noeud : %d    Nombre de message : %lf    Indice en lecture : %d    Indice en écriture : %d    Attente max : %d    nb message total : %lf    attente total : %lf\n\n", i, noeuds[i].id, noeuds[i].nb_message, noeuds[i].indice_slot_lecture, noeuds[i].indice_slot_ecriture, noeuds[i].attente_max, noeuds[i].nb_message_total, noeuds[i].attente_totale);
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

void afficher_tableau(int *tab, int taille)
{
	int i;
	for(i=0; i<taille; i++)
	{
		if (tab[i]<0)
			printf("%d   ", tab[i]);
	}
	printf("\n");
}

void entrer_messages( Anneau *anneau, int tic )
{
	TableauDynamiqueEntier *td_initial = anneau->messages_initaux;
	TableauDynamiqueEntier *td_prioritaire = anneau->messages_prioritaires;
	int ** couple_ecriture = anneau->couple_ecriture;
	int nombre_slot = anneau->nombre_slot;
	int nombre_noeud = anneau->nombre_noeud;
	int position_slot;
	int politique_anneau = anneau->politique_envoi;

	Noeud *noeud;	//Le noeud courant
	Slot *slot;
	int nb_message_noeud, nb_message_best_effort, nb_message_prioritaires;		//Le nombre de message du noeud courant et les nombres de message reçus par la noeud courant.
	int nb_message_par_antenne = 10;
	int messages_initaux[LIMITE_NOMBRE_MESSAGE_MAX];
	int messages_prioritaires[LIMITE_NOMBRE_MESSAGE_MAX];

	int i;
	for (i=0; i< nombre_noeud; i++)
	{
		noeud = &(anneau->noeuds[ couple_ecriture[i][0] ]);
		position_slot = (couple_ecriture[i][1] + anneau->decallage) % nombre_slot;
		slot = &(anneau->slots[position_slot]);

		/* Ajout des messages provenant des antennes */
		if (tic % PERIODE_MESSAGE_ANTENNE == noeud->debut_periode)
		{
			nb_message_prioritaires = nb_message_par_antenne * noeud->nb_antenne;
			if (politique_anneau == POLITIQUE_ENVOI_PRIORITAIRE)
			{
				ajouter_message( noeud->file_messages_prioritaires, nb_message_prioritaires, tic );
				noeud->nb_message_prioritaires += nb_message_prioritaires;
				noeud->nb_message_prioritaires_total += nb_message_prioritaires;
			}
			else
			{
				ajouter_message( noeud->file_messages_initiale, nb_message_prioritaires, tic );
				noeud->nb_message += nb_message_prioritaires;
				noeud->nb_message_total += nb_message_prioritaires;
			}
		}

		/* Ajout des messages best effort */
		nb_message_best_effort = hyper_expo(anneau->tableau_poisson);
		ajouter_message( noeud->file_messages_initiale, nb_message_best_effort, tic );

		if (politique_anneau == POLITIQUE_ENVOI_PRIORITAIRE)
		{
			noeud->nb_message_best_effort += nb_message_best_effort;
			noeud->nb_message_best_effort_total += nb_message_best_effort;
			nb_message_noeud = noeud->nb_message_best_effort + noeud->nb_message_prioritaires;
		}
		else
		{
			noeud->nb_message += nb_message_best_effort;
			noeud->nb_message_total += nb_message_best_effort;

			nb_message_noeud = noeud->nb_message;
		}

		if ( ( slot->contient_message == 0) && (nb_message_noeud >= LIMITE_NOMBRE_MESSAGE_MIN) )
		{
			if (nb_message_noeud >= LIMITE_NOMBRE_MESSAGE_MAX)	//On envoie le plus de message possible
			{
				//int messages[LIMITE_NOMBRE_MESSAGE_MAX];
				if (politique_anneau == POLITIQUE_ENVOI_PRIORITAIRE)
				{
					if (noeud->nb_message_prioritaires >= LIMITE_NOMBRE_MESSAGE_MAX)	//On envoie que des messages prioritaire
					{
						anneau->nb_messages_prioritaires += LIMITE_NOMBRE_MESSAGE_MAX;
						supprimer_message( noeud->file_messages_prioritaires, LIMITE_NOMBRE_MESSAGE_MAX, messages_prioritaires );
						placer_message( noeud, noeud->id, slot, 0, LIMITE_NOMBRE_MESSAGE_MAX, messages_initaux, messages_prioritaires, tic, td_initial, td_prioritaire);
					}
					else	//Il faut envoyer tout les prioritaire + le reste en best effort
					{
						nb_message_prioritaires = noeud->nb_message_prioritaires;
						nb_message_best_effort = LIMITE_NOMBRE_MESSAGE_MAX - nb_message_prioritaires;

						supprimer_message( noeud->file_messages_prioritaires, nb_message_prioritaires, messages_prioritaires);
						supprimer_message( noeud->file_messages_initiale, nb_message_best_effort, messages_initaux );

						noeud->nb_message_prioritaires -= nb_message_prioritaires;
						noeud->nb_message_best_effort -= nb_message_best_effort;

						anneau->nb_messages_prioritaires += nb_message_prioritaires;
						anneau->nb_messages_initaux += nb_message_best_effort;

						placer_message( noeud, noeud->id, slot, nb_message_best_effort, nb_message_prioritaires, messages_initaux, messages_prioritaires, tic, td_initial, td_prioritaire);
					}
				}
				else
				{
					anneau->nb_messages_initaux += LIMITE_NOMBRE_MESSAGE_MAX;
					supprimer_message( noeud->file_messages_initiale, LIMITE_NOMBRE_MESSAGE_MAX, messages_initaux);
					noeud->nb_message -= LIMITE_NOMBRE_MESSAGE_MAX;

					placer_message( noeud, noeud->id, slot, LIMITE_NOMBRE_MESSAGE_MAX, 0, messages_initaux, NULL, tic, td_initial, td_prioritaire);
				}
			}
			else	//Le nombre de message est compris entre le minimum est le maximum, on vide donc le noeud.
			{
				if (politique_anneau == POLITIQUE_ENVOI_PRIORITAIRE)
				{
					nb_message_prioritaires = noeud->nb_message_prioritaires;
					nb_message_best_effort = noeud->nb_message_best_effort;

					supprimer_message( noeud->file_messages_prioritaires, nb_message_prioritaires, messages_prioritaires);
					supprimer_message( noeud->file_messages_initiale, nb_message_best_effort, messages_initaux );

					noeud->nb_message_best_effort = 0;
					noeud->nb_message_prioritaires = 0;

					//afficher_tableau(messages_prioritaires, nombre_messages_prioritaires);
					placer_message( noeud, noeud->id, slot, nb_message_best_effort, nb_message_prioritaires, messages_initaux, messages_prioritaires, tic, td_initial, td_prioritaire );
					anneau->nb_messages_initaux += nb_message_best_effort;
					anneau->nb_messages_prioritaires += nb_message_prioritaires;
				}
				else
				{
					supprimer_message( noeud->file_messages_initiale, nb_message_noeud, messages_initaux );
					placer_message( noeud, noeud->id, slot, nb_message_noeud, 0, messages_initaux, NULL, tic, td_initial, td_prioritaire );
					noeud->nb_message = 0;
					anneau->nb_messages_initaux += nb_message_noeud;
				}
			}
		}
	}
}

void placer_message( Noeud *noeud, int indice_noeud_emetteur, Slot *slot, int nombre_messages_initaux, int nombre_messages_prioritaires, int *messages_initaux, int *messages_prioritaires, int tic, TableauDynamiqueEntier *td_initial, TableauDynamiqueEntier *td_prioritaire )
{
	//printf("Le noeud %d envoie un message\n", noeud->id);
	//printf("\nAjout de la valeur %d au noeud numéro %d\n", tic, noeud->id);
	ajouter_valeur_tableau_dynamique_entier(noeud->tableau_tics_envois, tic);
	slot->noeud_emetteur_paquet = indice_noeud_emetteur;

	/* Met à jour les temps d'attentes du noeud qui envoie le message */
	int i; int temps_attente_message;

	/* Parcours du tableau de messages initiaux */
	for (i=0; i<nombre_messages_initaux; i++)
	{
		temps_attente_message = tic - messages_initaux[i];
		if (td_initial != NULL)
			ajouter_valeur_tableau_dynamique_entier(td_initial, temps_attente_message);

		if (temps_attente_message > noeud->attente_max)
			noeud->attente_max = temps_attente_message;

		noeud->attente_totale += temps_attente_message;
	}

	if (messages_prioritaires != NULL)	//Politique d'envoi de message prioritaire
	{
		afficher_tableau(messages_prioritaires, nombre_messages_prioritaires);
		/* Parcours du tableau de messages prioritaires */
		for (i=0; i<nombre_messages_prioritaires; i++)
		{
			temps_attente_message = tic - messages_prioritaires[i];
			//printf("valeur %d\n", messages_prioritaires[i]);
			if (td_prioritaire != NULL)
				ajouter_valeur_tableau_dynamique_entier(td_prioritaire, temps_attente_message);

			if (temps_attente_message > noeud->attente_max)
				noeud->attente_max = temps_attente_message;

			noeud->attente_totale += temps_attente_message;
		}
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
	TableauDynamiqueEntier *td_initial = anneau->messages_initaux;
	TableauDynamiqueEntier *td_prioritaire = anneau->messages_prioritaires;

	free(anneau->tableau_poisson->tableau);
	free(anneau->tableau_poisson);
	int nombre_noeud = anneau->nombre_noeud;
	/* Libère la mémoire prise par les slots */
	free(anneau->slots);

	/* Libère la mémoire prise par les noeuds et leurs File */
	int i;
	for (i=0; i<nombre_noeud; i++)
	{
		liberer_file( noeuds[i].file_messages_initiale );
		if (noeuds[i].file_messages_prioritaires != NULL)
			liberer_file(noeuds[i].file_messages_prioritaires);
		free(noeuds[i].tableau_tics_envois->tableau);
		free(noeuds[i].tableau_tics_envois);
		free(anneau->couple_lecture[i]);
		free(anneau->couple_ecriture[i]);
	}
	free(anneau->couple_ecriture);
	free(anneau->couple_lecture);
	free(noeuds);

	/* Libération de l'espace mémoire pris par le tableau dynamique */
	if (td_initial != NULL)
	{
		free(td_initial->tableau);
		free(td_initial);
	}
	if (td_prioritaire != NULL)
	{
		free(td_prioritaire->tableau);
		free(td_prioritaire);
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
			TableauDynamiqueEntier *td = noeuds[i].tableau_tics_envois;
			int taille_utilisee = td->taille_utilisee;
			for (j=0; j<taille_utilisee; j++)
			{
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


	/* Trie des tableaux */
	TableauDynamiqueEntier *td_initial = anneau->messages_initaux;
	int taille_utilisee_td_initial = td_initial->taille_utilisee;
	int *tableau_initial = td_initial->tableau;
	qsort(tableau_initial, taille_utilisee_td_initial, sizeof(int), cmpfunc);

	TableauDynamiqueEntier *td_prioritaire = anneau->messages_prioritaires;
	int taille_utilisee_td_prioritaire; int *tableau_prioritaire;
	if (td_prioritaire != NULL)
	{
		taille_utilisee_td_prioritaire = td_prioritaire->taille_utilisee;
		tableau_prioritaire = td_prioritaire->tableau;
		qsort(tableau_prioritaire, taille_utilisee_td_prioritaire, sizeof(int), cmpfunc);
	}


	int val_max = tableau_initial[ taille_utilisee_td_initial-1 ];
	int bornes_superieures[nombre_quantile];

	int interval = taille_utilisee_td_initial / nombre_quantile+1;
	for(i=1; i<=nombre_quantile; i++)
		bornes_superieures[i-1] = i * interval;
	if (bornes_superieures[nombre_quantile-1] < taille_utilisee_td_initial)
		bornes_superieures[nombre_quantile-1] = taille_utilisee_td_initial;
	int borne_superieure = bornes_superieures[0];

	//Allocation du tableau
	double **quantiles_initial = (double **) calloc(nombre_quantile+1, sizeof(double));	//tableau de la forme: nombre_message, min, max, moyenne
	double **quantiles_prioritaire = (double **) calloc(nombre_quantile+1, sizeof(double));	//tableau de la forme: nombre_message, min, max, moyenne
	for(i=0; i<nombre_quantile+1; i++)
	{
		quantiles_initial[i] = (double *) calloc(nombre_colonne, sizeof(double));	//La premiere ligne du tableau
		quantiles_prioritaire[i] = (double *) calloc(nombre_colonne, sizeof(double));	//La premiere ligne du tableau
	}

	min = tableau_initial[0];
	for (i=0; i<taille_utilisee_td_initial; i++)
	{
		if ( (i % interval == 0) && (i != 0))
		{
			//Assignation des valeurs pour la borne précedente
			max = tableau_initial[i-1];
			quantiles_initial[j][2] = max; quantiles_initial[j][3] = somme_valeur/quantiles_initial[j][0];
			somme_valeur = 0;
			min = tableau_initial[i];
			j++;
			if (j < nombre_quantile+1)
				quantiles_initial[j][1] = min;
		}
		somme_valeur += tableau_initial[i];
		if (j < nombre_quantile+1)
			quantiles_initial[j][0]++;
	}
	quantiles_initial[nombre_quantile-1][2] = val_max;
	quantiles_initial[nombre_quantile-1][3] = somme_valeur/quantiles_initial[j][0];

	ecrire_nb_message_attente_csv(anneau, quantiles_initial, nombre_quantile, bornes_superieures);
	/* Libération de la mémoire du quantile */
	for(i=0; i<nombre_quantile+1; i++)
		free(quantiles_initial[i]);
	free(quantiles_initial);

	//Ecriture du nombre de message ayant attendu selon un interval de TIC
	double *quantiles_nb_messages_initiaux = (double *) calloc(nombre_quantile, sizeof(double));	//tableau de la forme: nombre_message, min, max, moyenne
	double *quantiles_nb_messages_prioritaire = (double *) calloc(nombre_quantile, sizeof(double));	//tableau de la forme: nombre_message, min, max, moyenne

	j = 0;
	interval = val_max / nombre_quantile;;
	if (interval < 1)
		interval = 1;
	for(i=1; i<=nombre_quantile; i++)
		bornes_superieures[i-1] = i * interval;

	if (bornes_superieures[nombre_quantile-1] < val_max)
		bornes_superieures[nombre_quantile-1] = val_max;

	borne_superieure = bornes_superieures[0];

	min = tableau_initial[0];
	for (i=0; i<taille_utilisee_td_initial; i++)
	{
		if ( (tableau_initial[i] >= borne_superieure) && (j < nombre_quantile-1) )
		{
			j++;
			borne_superieure = bornes_superieures[j];
		}
		quantiles_nb_messages_initiaux[j]++;
	}

	if (td_prioritaire != NULL)
	{
		printf("Génération des quantiles de messages prioritaires\n");
		j = 0;
		for (i=0; i<taille_utilisee_td_prioritaire; i++)
		{
			//printf("Tableau : %d\n", tableau_initial[taille_utilisee_td_initial-1]);
			if ( (tableau_prioritaire[i] >= borne_superieure) && (j < nombre_quantile-1) )
			{
				//printf("Quantiles[j] : %lf\n", quantiles_nb_messages_prioritaire[j]);
				j++;
				borne_superieure = bornes_superieures[j];
			}
			quantiles_nb_messages_prioritaire[j]++;
		}
		printf("Quantiles[j] : %lf\n", quantiles_nb_messages_prioritaire[j]);
		ecrire_temps_attente_csv(anneau, quantiles_nb_messages_initiaux, quantiles_nb_messages_prioritaire, bornes_superieures, nombre_quantile);
	}
	else
		ecrire_temps_attente_csv(anneau, quantiles_nb_messages_initiaux, NULL, bornes_superieures, nombre_quantile);
	free(quantiles_nb_messages_initiaux);
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

void ecrire_temps_attente_csv( Anneau *anneau, double *quantiles_initial, double *quantiles_prioritaire, int *bornes, int taille_tableau )
{
	int nombre_noeud = anneau->nombre_noeud;
	int nombre_slot = anneau->nombre_slot;
	double nb_messages_initiaux_total = anneau->nb_messages_initaux;
	double nb_messages_prioritaire_total = anneau->nb_messages_prioritaires;

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

	fprintf(f, "interval,type,taux,TIC,nb_slot,nb_noeud\n");
	int i;
	double pourcentage_initial, pourcentage_prioritaire;
	int borne_inferieure = 0;
	for (i=0; i<taille_tableau; i++)
	{
		int borne_superieure = bornes[i];
		if ( (quantiles_initial[i] == 0) && ( (quantiles_prioritaire != NULL) || (quantiles_prioritaire[i] == 0) ) )
			break;
		if (quantiles_prioritaire != NULL)
		{
			pourcentage_initial = (quantiles_initial[i] / nb_messages_initiaux_total);
			pourcentage_prioritaire = (quantiles_prioritaire[i] / nb_messages_prioritaire_total);
			fprintf(f, "%d:%d,Best effort,%lf,%d,%d,%d\n", borne_inferieure, borne_superieure, pourcentage_initial, NOMBRE_TIC, nombre_slot, nombre_noeud);
			fprintf(f, "%d:%d,Prioritaire,%lf,%d,%d,%d\n", borne_inferieure, borne_superieure, pourcentage_prioritaire, NOMBRE_TIC, nombre_slot, nombre_noeud);
		}
		else
		{
			pourcentage_initial = (quantiles_initial[i] / nb_messages_initiaux_total);
			fprintf(f, "%d:%d,Tous type,%lf,%d,%d,%d\n", borne_inferieure, borne_superieure, pourcentage_initial, NOMBRE_TIC, nombre_slot, nombre_noeud);
		}
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
