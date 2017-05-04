#include "./simulation.h"
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

	printf("Etat initial\n");
	afficher_slots(slots);

	printf("Premier décalage\n");
	decaler_slots(slots);
	afficher_slots(slots);

	printf("Second décalage\n");
	decaler_slots(slots);
	afficher_slots(slots);

	printf("Troisième décalage\n");
	decaler_slots(slots);
	afficher_slots(slots);

	printf("Quatrième décalage\n");
	decaler_slots(slots);
	afficher_slots(slots);

	while (nombre_tic_restant > 0)
	{
		/*entrer_messages( slots, noeuds, NOMBRE_TIC - nombre_tic_restant );
		afficher_slots(slots);
		printf("\n\n");
		afficher_noeuds(noeuds);
		printf("\n\n");
		printf("\n############################\n");*/
		nombre_tic_restant--;
	}
	return 0;
}
