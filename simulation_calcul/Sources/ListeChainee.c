#include <stdio.h>
#include <stdlib.h>
#include "../Headers/ListeChainee.h"

ListeChainee *creer_Liste_chainee()
{
    ListeChainee *liste = (ListeChainee *) malloc( sizeof(liste) );
    //Maillon *premier = (Maillon *) malloc( sizeof(*premier) );


    liste->premier = NULL;

    return liste;
}


/*! \fn void inserer_fin( ListeChainee *liste, int tic_arrive )
   \brief Insère en fin de liste un nouveau maillon.
   \param liste : La liste chainée sur laquelle on souhaite ajouter l'élément.
   \param tic_arrive : La valeur de l'élément.
*/
void inserer_fin(ListeChainee *liste, int tic_arrive)
{
    /* Création du nouvel élément */
    Maillon *nouveau = (Maillon *) malloc( sizeof(*nouveau) );

	nouveau->tic_arrive = tic_arrive;
	nouveau->suivant = NULL;

    /* Insertion de l'élément à la fin de la liste */
	Maillon *courant = liste->premier;

	//Exception si la liste est vide
	if (courant == NULL)
		liste->premier = nouveau;
	else
	{
		while (courant->suivant != NULL)
		{
			courant = courant->suivant;
		}
		/* Sortie de la boucle, courant est le dernier élément */
		courant->suivant = nouveau;
	}
}


/*! \fn int supprimer_premier( ListeChainee *liste )
   \brief Supprime le premier élément de la liste et renvoie sa valeur.
   \param liste : La liste chainée pour laquelle nous souhaitons supprimer le premier maillon.
*/
int supprimer_premier(ListeChainee *liste)
{
	/* La liste contient un premier élément */
	if (liste->premier != NULL)
    {
        Maillon *aSupprimer = liste->premier;
		int tic = aSupprimer->tic_arrive;
        liste->premier = aSupprimer->suivant;
        free(aSupprimer);
		return tic;
    }
	else
	{
		printf("liste vide\n");
		return -1;
	}
}


/*! \fn int liste_est_vide(ListeChainee *liste)
   \brief Indique si une liste est vide ou non.
   \param liste : la liste chainée.
   \return 1 Si la liste est vide, 0 si elle contient au moins un élément.
*/
int liste_est_vide(ListeChainee *liste)
{
	Maillon *premier = liste->premier;
	if (premier == NULL)
		return 1;
	else
		return 0;
}


/*! \fn void afficher_liste( ListeChainee *liste )
   \brief Affiche une liste chainée.
   \param liste : La liste chainée que nous souhaitons afficher.
*/
void afficher_liste(ListeChainee *liste)
{
	if (liste_est_vide(liste) == 0)
	{
		Maillon *courant = liste->premier;
		int compteur = 0;
		while (courant->suivant != NULL)
		{
			printf("Indice de la chaine : %d; Valeur du maillon : %d\n", compteur, courant->tic_arrive);
			courant = courant->suivant;
			compteur++;
		}
		printf("Indice de la chaine : %d; Valeur du maillon : %d\n", compteur, courant->tic_arrive);
	}
	else
	{
		printf("la liste est vide\n");
	}
}
