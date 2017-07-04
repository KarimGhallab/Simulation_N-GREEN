#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

#define LAMBDA_PETIT 7
#define LAMBDA_GRAND 27
#define PROBABILITE_BURST 0.05

int loi_de_poisson_naif(float u, float lamb)
{
	double p = exp (- lamb);
	int x = 0;
	double f = p;
	do
	{
		x += 1;
		p = p*lamb/x;
		f += p;
	} while (u > f);
	return x;
}

float generer_aleatoire(float borne_min, float borne_max)
{
	float tirage = ((float)rand() / RAND_MAX * (borne_max - borne_min) ) + borne_min;
	return tirage;
}

int effectuer_tirage(float probabilite)
{
	float tirage = generer_aleatoire(0, 1.00f);
	return tirage <= probabilite;
}

int hyper_expo()
{
	float u = generer_aleatoire(0, 1.0f);
	if (effectuer_tirage(PROBABILITE_BURST) == 1)	//Lambda grand
		return (loi_de_poisson_naif(u, LAMBDA_GRAND));
	else											//lambda petit
		return (loi_de_poisson_naif(u, LAMBDA_PETIT));
}

int main()
{
	srand(time(NULL));
	double variance = 0.0;
	double moyenne = 0.0;

	int nb_simuls = 20000000;
	int result;
	float tirage;
	for(int i=0;i<nb_simuls;i++)
	{
		tirage = (float)rand() / RAND_MAX ;
		//result = loi_de_poisson_naif(tirage, LAMBDA_PETIT);
		result = hyper_expo();
		variance += (result*result);
		moyenne += result;
	}

	moyenne /= nb_simuls;

	variance /= nb_simuls;
	variance -= (moyenne*moyenne);

	printf("Variance = %f, Moyenne = %f\n",variance,moyenne);
	return 0;
}
