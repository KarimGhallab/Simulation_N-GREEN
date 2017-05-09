#include "../Headers/simulation.h"
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main ()
{
	time_t debut, fin, total;
	time(&debut);

	int nombre_tic_restant = NOMBRE_TIC;
	printf("Nombre de slot de l'anneau : %d\n", NOMBRE_SLOT);
	printf("Nombre de noeud de l'anneau : %d\n\n", NOMBRE_NOEUD);

	/* Initialisation des slots et noeuds de l'anneau. */
	Slot *slots[ NOMBRE_SLOT ];
	Noeud *noeuds[ NOMBRE_NOEUD ];
	initialiser_slots(slots);
	initialiser_noeuds(noeuds, slots);

	/*printf("Etat initial des slots\n");
	afficher_slots(slots);

	printf("Etat initial des noeuds\n");
	afficher_noeuds(noeuds);*/

	while (nombre_tic_restant > 0)
	{
		entrer_messages( slots, noeuds, NOMBRE_TIC - nombre_tic_restant );
		decaler_messages(slots);
		sortir_messages(slots);

		/*afficher_noeuds(noeuds);
		printf("\n\n");

		afficher_slots(slots);
		printf("\n\n");

		printf("\n############################\n");*/


		nombre_tic_restant--;
	}
	time(&fin);
	total = ( fin - debut );
	printf("Temps total pris :  %ld secondes\n", total);

	liberer_memoire(slots, noeuds);

	return (0);
}
