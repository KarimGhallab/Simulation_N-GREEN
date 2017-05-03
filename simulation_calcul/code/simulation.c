#include "./simulation.h"
#include "./ListeChainee.h"
#include "./hyper_expo.h"
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

	while (nombre_tic_restant > 0)
	{
		printf("%d\n", effectuer_tirage(0.5) );
		nombre_tic_restant--;
	}
	return 0;
}
