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

int loi_de_poisson_naif(float u)
{
	double p = exp (- LAMBDA);
	int x = 0;
	double f = p;
	do
	{
		x += 1;
		p = p*LAMBDA/x;
		f += p;
	} while (u > f);
	return x;
}

int loi_de_poisson_opti(float u, TableauDynamiqueFloat *tableau_poisson )
{
	int maxi = tableau_poisson->taille_utilisee;
	double *tableau = tableau_poisson->tableau;
	double maxF = tableau[ maxi -1];
	double maxP = maxF;

	int x;
	if (u <= maxF)		//On peut trouver la valeur à l'aide du tableau
	{
		x = 0;
		double somme = 0;
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
			p = p*LAMBDA/x;
			f = f + p;
		}
		//printf("\nNb message %d \n", x);
	}
	return x;
}

TableauDynamiqueFloat *initialiser_tableau_poisson()
{
	printf("Initialisation du tableau\n");
	TableauDynamiqueFloat *tableau_poisson = initialiser_tableau_dynamique_float();
	ajouter_valeur_tableau_dynamique_float(tableau_poisson, exp(-LAMBDA) );

	double p = tableau_poisson->tableau[0];
	double seuil = 0.9999999;
	double somme = 0;

	int compteur = 1;
	while (somme < seuil)
	{
		p = p*LAMBDA/compteur;
		double nouvelle_valeur = tableau_poisson->tableau[ compteur-1 ]+p;
		ajouter_valeur_tableau_dynamique_float(tableau_poisson, nouvelle_valeur);
		//printf("Indice : %d  Valeur : %lf\n", tableau_poisson->taille_utilisee-1, nouvelle_valeur);
		somme = tableau_poisson->tableau[ compteur ];
		compteur++;
	}

	return tableau_poisson;
}

int hyper_expo(TableauDynamiqueFloat *tableau_poisson)
{
	if (effectuer_tirage(PROBABILITE_BURST) == 1)		//Le tirage est tombé sur la faible proba
		return NOMBRE_MESSAGE_BURST;
	else
	{
		float u = generer_aleatoire(0, 1.0f);
		int nb_message = loi_de_poisson_opti(u, tableau_poisson);
		return nb_message;
	}
}
