#include "TableauDynamiqueDouble.h"

/*! \file hyper_expo.h
    \brief Header du fichier permettant d'exécuter des tirages et de réaliser l'hyper exponentielle.
 */


 /*! \def PROBABILITE_BURST
     \brief Représente la probabilité de réaliser un burst dans l'hyper exponentielle.
  */
#define PROBABILITE_BURST 0.05


/*! \def LAMBDA_GRAND
    \brief Représente lle nombre de message qui arrive dans un noeud lors d'un burst.
 */
#define LAMBDA_GRAND 27


/*! \def LAMBDA_PETIT
    \brief Représente le facteur lambda de la loi de poisson.
 */
#define LAMBDA_PETIT 7


/*! \def TAILLE_TABLEAU
    \brief Représente la taille du tableau nécéssaire au calcul de la loi de poisson optimisée.
 */
#define TAILLE_TABLEAU 10


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
	\param lambda : Le paramètre lambda à utiliser.
    \return Le résultat de la loi de poisson.
 */
int loi_de_poisson_naif(float u, float lambda);


/*! \fn int loi_de_poisson_opti(float u, TableauDynamiqueDouble *tableau_poisson);
    \brief Calcule optimisé du résultat d'une loi de poisson.
    \param u : Variable aléatoire.
	\param lambda : Le paramètre lambda à utiliser.
    \param *tableau_poisson : Le tableau contenant les valeurs de la loi de poisson.
    \return Le résultat de la loi de poisson.
 */
int loi_de_poisson_opti(float u, float lambda, TableauDynamiqueDouble *tableau_poisson);


/*! \fn TableauDynamiqueDouble *initialiser_tableau_poisson
    \brief Initialise le tableau avec les résultats de le loi de poisson.
	Cette fonction est utilisé dans le cadre de l'algorithme optimisé.
	\param lambda : Le paramètre lambda petit de la loi de poisson
   	\return : le tableau initialisé.
 */
TableauDynamiqueDouble *initialiser_tableau_poisson(float lambda);


/*! \fn int hyper_expo(TableauDynamiqueDouble *tableau_poisson)
    \brief Hyper exponentielle.
	\param *tableau_poisson Le tableau contenant les données pré-calculées pour la loi de poisson.
    \return Le nombre de message reçu via la loi hyper exponentielle.
 */
int hyper_expo(TableauDynamiqueDouble *tableau_poisson);
