#include "../Headers/TableauDynamiqueDouble.h"
#include <stdio.h>
#include <stdlib.h>

TableauDynamiqueDouble* initialiser_tableau_dynamique_double()
{
	TableauDynamiqueDouble *td = (TableauDynamiqueDouble *) malloc( sizeof(TableauDynamiqueDouble) );
	td->taille_tableau = TAILLE_INITIALE_TABLEAU_DOUBLE;
	td->tableau = (double *) calloc(TAILLE_INITIALE_TABLEAU_DOUBLE, sizeof(double) );
	td->taille_utilisee = 0;
	return td;
}

void ajouter_valeur_tableau_dynamique_double( TableauDynamiqueDouble *td, double valeur )
{
	td->tableau[td->taille_utilisee] = valeur;
	td->taille_utilisee++;

	if (td->taille_utilisee == td->taille_tableau)		//Il faut réallouer l'espace du tableau
	{
		td->tableau = (double * ) realloc(td->tableau, (2 * td->taille_tableau) * sizeof(double) );
		td->taille_tableau = td->taille_tableau * 2;
	}
}

void afficher_tableau_dynamique_double( TableauDynamiqueDouble *td )
{
	int taille_utilisee = td->taille_utilisee;
	int taille_tableau = td->taille_tableau;
	int i;
	printf("Taille totale du tableau : %d\n", taille_tableau);
	printf("Taille utilisée du tableau : %d\n", taille_utilisee);
	for (i=0; i<taille_tableau; i++)
		printf("[%lf] ", td->tableau[i]);
	printf("\n\n");
}
