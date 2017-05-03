#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

/*!
 * \file hyper_expo.h
 * \brief Fichier permettant d'exécuter des tirages et de réaliser l'hyper exponentielle.
 */


 /*! \def PROBABILITE_BURST
  * \brief Représente la probabilité de réaliser un burst dans l'hyper exponentielle.
  */
#define PROBABILITE_BURST 0.01


/*! \def NOMBRE_MESSAGE_BURST
 * \brief Représente lle nombre de message qui arrive dans un noeud lors d'un burst.
 */
#define NOMBRE_MESSAGE_BURST 140


/*! \def LAMBDA
 * \brief Représente le facteur lambda de la loi de poisson.
 */
#define LAMBDA 10


/*! \def TAILLE_TABLEAU
 * \brief Représente la taille du tableau nécéssaire au calcul de la loi de poisson optimisée.
 */
#define TAILLE_TABLEAU 10

extern int DECALAGE = 0;


/*! \fn int effectuer_tirage(float probabilite)
   \brief Effectue un tirage et indique si la probabilité a été tiré.
   \param probabilite : La probabilité du tirage.
   \return 1 si la probabilité a été tiré, 0 sinon.
*/
int effectuer_tirage(float probabilite);


/*! \fn float generer_aleatoire(float borne_min, float borne_max)
   \brief Génére un nombre aléatoir situé entre la borne min et la borne max
   \param borne_min : La borne minimale du nombre à générer.
   \param borne_max : La borne maximale du nombre à générer.
   \return Le nombre généré.
*/
float generer_aleatoire(float borne_min, float borne_max);


/*! \fn int loi_de_poisson_naif(float u)
   \brief Calcule naif du résultat d'une loi de poisson.
   \param u : Variable aléatoire.
   \return Le résultat de la loi de poisson.
*/
int loi_de_poisson_naif(float u);


/*! \fn int loi_de_poisson_opti(float u)
   \brief Calcule optimisé du résultat d'une loi de poisson.
   \param u : Variable aléatoire.
   \param tableau_poisson : Le tableau contenant les valeurs de la loi de poisson.
   \return Le résultat de la loi de poisson.
*/
int loi_de_poisson_opti(float u, double tableau_poisson[]);


/*! \fn void initialiser_tableau(double tableau_poisson[] );
   \brief Initialise le tableau avec les résultats de le loi de poisson.
	Cette fonction est utilisé dans le cadre de l'algorithme optimisé.
   \param tableau_poisson[] : le tableau à initialiser.
*/
void initialiser_tableau(double tableau_poisson[] );


/*! \fn int hyper_expo()
   \brief Hyper exponentielle.
   \return Le nombre de message reçu via la loi hyper exponentielle.
*/
int hyper_expo();

int effectuer_tirage(float probabilite)
{
	float tirage = generer_aleatoire(0, 1.0f);
	return tirage <= probabilite;
}

float generer_aleatoire(float borne_min, float borne_max)
{
	srand(clock() + DECALAGE);		//Met en place le générateur en fonction du temps et d'un décalage.
	DECALAGE++;
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
	{
		printf ("Burst !\nOn envoie %d messages.", NOMBRE_MESSAGE_BURST);
		return NOMBRE_MESSAGE_BURST;
	}
	else
	{
		float u = generer_aleatoire(0, 1.0f);
		//double tableau_poisson[TAILLE_TABLEAU];
		int nb_message = loi_de_poisson_naif(u);
		//int nb_message = loi_de_poisson_opti(u, tableau_poisson);
		return nb_message;
	}
}
