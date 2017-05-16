#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "../Headers/hyper_expo.h"

int effectuer_tirage(float probabilite)
{
	float tirage = generer_aleatoire(0, 1.00f);
	return tirage <= probabilite;
}

float generer_aleatoire(float borne_min, float borne_max)
{
	/*static int DECALAGE = 0;
	srand(clock() + DECALAGE);		//Met en place le générateur en fonction du temps et d'un décalage.
	DECALAGE++;*/
	float tirage = ((float)rand() / RAND_MAX * (borne_max - borne_min) ) + borne_min;
	return tirage;
}

int loi_de_poisson_naif(float u)
{
	double p = exp (- LAMBDA);
	int x = 0;
	double f = p;
	while (u > f)
	{
		x += 1;
		p = p*LAMBDA/x;
		f += p;
	}
	return x;
}

int loi_de_poisson_opti(float u, double tableau_poisson[] )
{
	//Initialisation des variables
	initialiser_tableau( tableau_poisson );

	int maxi = TAILLE_TABLEAU;
	double maxF = tableau_poisson[ TAILLE_TABLEAU -1];
	double maxP = maxF;

	int x;
	if (u <= maxF)		//On peut trouver la valeur à l'aide du tableau
	{
		x = 0;
		while (u > tableau_poisson[x])
		{
			x++;
		}
	}
	else
	{
		x = maxi;
		int f = maxF;
		int p = maxP;

		while (u > f)
		{
			x++;
			p = p*LAMBDA/x;
			f = f + p;
		}
	}
	return x;
}

void initialiser_tableau(double tableau_poisson[] )
{
	tableau_poisson[0] = exp(-LAMBDA);
	double p = tableau_poisson[0];

	int i;
	for (i=0; i<TAILLE_TABLEAU; i++)
	{
		p = p*LAMBDA/i;
		tableau_poisson[i] = tableau_poisson[i-1]+p;
	}
}

int hyper_expo()
{
	if (effectuer_tirage(PROBABILITE_BURST) == 1)		//Le tirage est tombé sur la faible proba
		return NOMBRE_MESSAGE_BURST;
	else
	{
		float u = generer_aleatoire(0, 1.0f);
		//double tableau_poisson[TAILLE_TABLEAU];
		int nb_message = loi_de_poisson_naif(u);
		//int nb_message = loi_de_poisson_opti(u, tableau_poisson);
		return nb_message;
	}
}
