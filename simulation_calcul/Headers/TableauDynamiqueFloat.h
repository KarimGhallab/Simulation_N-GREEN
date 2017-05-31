/*! \file TableauDynamiqueFloat.h
    \brief Header du fichier de la strcture de tableau dynamique contenant des flottants.
 */

 /*! \def TAILLE_INITIALE_TABLEAU
     \brief La taille initiale du tableau de la structure TableauDynamiqueFloat.
  */
 #define TAILLE_INITIALE_TABLEAU 100

/*! \struct TableauDynamiqueFloat
    \brief Structure représentant tableau de flottant avec une taille dynamique.
 */
struct TableauDynamiqueFloat
{
	int taille_tableau;
	int taille_utilisee;
	double *tableau;
};
typedef struct TableauDynamiqueFloat TableauDynamiqueFloat;

/*! \fn TableauDynamiqueFloat* initialiser_tableau_dynamique_float()
    \brief Initialise un tableau dynamique de flottant.
    \return TableauDynamiqueFloat* Un pointeur vers le tableau dynamique.
 */
TableauDynamiqueFloat* initialiser_tableau_dynamique_float();

/*! \fn void ajouter_valeur_tableau_dynamique_float( TableauDynamiqueFloat *td, float valeur )
    \brief Ajoute une valeur au tableau dynamique de flottant.
     La taille du tableau peut etre réallouer si necessaire.
    \param *td Le tableau auquel on souhaite ajouter la valeur.
    \param valeur La valeur à ajouter.
 */
void ajouter_valeur_tableau_dynamique_float( TableauDynamiqueFloat *td, double valeur );

/*! \fn void afficher_tableau_dynamique_float( TableauDynamiqueFloat *td )
    \brief Affiche un tableau dynamique de flottant.
    \param *td Un pointeur sur le tableau dynamique de flottant à afficher.
 */
void afficher_tableau_dynamique_float( TableauDynamiqueFloat *td );
