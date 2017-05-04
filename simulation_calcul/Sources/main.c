#include "../Headers/simulation.h"
#include <stdio.h>
#include <stdlib.h>

int main ()
{
	int nombre_tic_restant = NOMBRE_TIC;
	printf("Nombre de slot de l'anneau : %d\n", NOMBRE_SLOT);
	printf("Nombre de noeud de l'anneau : %d\n\n", NOMBRE_NOEUD);

	/* Initialisation des slots et noeuds de l'anneau. */
	Slot slots[ NOMBRE_SLOT ];
	Noeud noeuds[ NOMBRE_NOEUD ];
	initialiser_slots(slots);
	initialiser_noeuds(noeuds, slots);

	printf("Etat initial des slots\n");
	afficher_slots(slots);

	printf("Etat initial des noeuds\n");
	afficher_noeuds(noeuds);

	while (nombre_tic_restant > 0)
	{
		entrer_messages( slots, noeuds, NOMBRE_TIC - nombre_tic_restant );
		decaler_messages(slots);
		afficher_slots(slots);
		printf("\n\n");
		afficher_noeuds(noeuds);
		printf("\n\n");
		printf("\n############################\n");
		nombre_tic_restant--;
	}
	/*int j; int nb_message = 100000;
	ListeChainee *liste = creer_Liste_chainee();
	for (j=0; j<nb_message; j++)
		inserer_fin(liste, j);*/
	return 0;
}
