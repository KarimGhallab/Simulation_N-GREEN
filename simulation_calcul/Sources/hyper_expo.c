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
	float tirage = ((float)rand() / RAND_MAX * (borne_max - borne_min) ) + borne_min;
	return tirage;
}

int loi_de_poisson_naif(float u, float lambda)
{
	double p = exp (- lambda);
	int x = 0;
	double f = p;
	do
	{
		x += 1;
		p = p*lambda/x;
		f += p;
	} while (u > f);
	return x;
}

int loi_de_poisson_opti(float u, float lambda, TableauDynamiqueDouble *tableau_poisson)
{
	int maxi = tableau_poisson->taille_utilisee;
	double *tableau = tableau_poisson->tableau;
	double maxF = tableau[ maxi -1];
	double maxP = maxF;

	int x;
	if (u <= maxF)		//On peut trouver la valeur à l'aide du tableau
	{
		x = 0;
		do
		{
			x++;
		} while (u > tableau[x-1]);
	}
	else
	{
		x = maxi;
		double f = maxF;
		double p = maxP;

		while (u > f)
		{
			x++;
			p = p*lambda/x;
			f = f + p;
		}
	}
	return x;
}

TableauDynamiqueDouble *initialiser_tableau_poisson(float lambda)
{
	TableauDynamiqueDouble *tableau_poisson = initialiser_tableau_dynamique_double();
	ajouter_valeur_tableau_dynamique_double(tableau_poisson, exp(-lambda) );

	double p = tableau_poisson->tableau[0];
	double seuil = 0.9999999;
	double somme = 0;

	int compteur = 1;
	while (somme < seuil)
	{
		p = p*lambda/compteur;
		double nouvelle_valeur = tableau_poisson->tableau[ compteur-1 ]+p;
		ajouter_valeur_tableau_dynamique_double(tableau_poisson, nouvelle_valeur);
		somme = tableau_poisson->tableau[ compteur ];
		compteur++;
	}

	return tableau_poisson;
}

int hyper_expo(TableauDynamiqueDouble *tableau_poisson)
{
	float u = generer_aleatoire(0, 1.0f);
	if (effectuer_tirage(PROBABILITE_BURST) == 1)	//Lambda grand
	{
		int message =  loi_de_poisson_naif(u, LAMBDA_GRAND);
		printf("Burst : %d\n", message);
		return message;
	}
	else											//lambda petit
	{
		int message =  (loi_de_poisson_opti(u, LAMBDA_PETIT, tableau_poisson));
		printf("Normal : %d\n", message);
		return message;
	}
}
