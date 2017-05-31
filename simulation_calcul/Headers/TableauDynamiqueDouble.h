/*! \file TableauDynamiqueDouble.h
    \brief Header du fichier de la strcture de tableau dynamique contenant des doubles.
 */

 /*! \def TAILLE_INITIALE_TABLEAU_DOUBLE
     \brief La taille initiale du tableau de la structure TableauDynamiqueDouble.
  */
 #define TAILLE_INITIALE_TABLEAU_DOUBLE 1000

/*! \struct TableauDynamiqueDouble
    \brief Structure représentant tableau de double avec une taille dynamique.
 */
struct TableauDynamiqueDouble
{
	int taille_tableau;
	int taille_utilisee;
	double *tableau;
};
typedef struct TableauDynamiqueDouble TableauDynamiqueDouble;

/*! \fn TableauDynamiqueDouble* initialiser_tableau_dynamique_double()
    \brief Initialise un tableau dynamique de double.
    \return TableauDynamiqueDouble* Un pointeur vers le tableau dynamique.
 */
TableauDynamiqueDouble* initialiser_tableau_dynamique_double();

/*! \fn void ajouter_valeur_tableau_dynamique_double( TableauDynamiqueDouble *td, double valeur )
    \brief Ajoute une valeur au tableau dynamique de double.
     La taille du tableau peut etre réallouer si necessaire.
    \param *td Le tableau auquel on souhaite ajouter la valeur.
    \param valeur La valeur à ajouter.
 */
void ajouter_valeur_tableau_dynamique_double( TableauDynamiqueDouble *td, double valeur );

/*! \fn void afficher_tableau_dynamique_double( TableauDynamiqueDouble *td )
    \brief Affiche un tableau dynamique de flottant.
    \param *td Un pointeur sur le tableau dynamique de flottant à afficher.
 */
void afficher_tableau_dynamique_double( TableauDynamiqueDouble *td );
