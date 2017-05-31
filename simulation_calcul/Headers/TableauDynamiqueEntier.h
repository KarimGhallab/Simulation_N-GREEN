/*! \file TableauDynamiqueEntier.h
    \brief Header du fichier de la structure de tableau dynamique.
 */

 /*! \def TAILLE_INITIALE_TABLEAU
     \brief La taille initiale du tableau de la structure TableauDynamiqueEntier.
  */
 #define TAILLE_INITIALE_TABLEAU 10000

/*! \struct TableauDynamiqueEntier
    \brief Structure représentant tableau d'entier avec une taille dynamique.
    Un tableau dynamique contient un tableau d'entier, une taille de tableau (dynamique), ainsi qu'une taille de tableau utilisée.
 */
struct TableauDynamiqueEntier
{
	int taille_tableau;
	int taille_utilisee;
	int *tableau;
};
typedef struct TableauDynamiqueEntier TableauDynamiqueEntier;


/*! \fn TableauDynamiqueEntier* initialiser_tableau_dynamique_entier()
    \brief Initialise un tableau dynamique d'entier.
    \return TableauDynamiqueEntier* Un pointeur vers le tableau dynamique d'entier.
 */
TableauDynamiqueEntier* initialiser_tableau_dynamique_entier();

/*! \fn void ajouter_valeur_tableau_dynamique_entier( TableauDynamiqueEntier *td, int valeur )
    \brief Ajoute une valeur au tableau dynamique d'entier.
     La taille du tableau peut etre réallouer si necessaire.
    \param *td Le tableau auquel on souhaite ajouter la valeur.
    \param valeur La valeur à ajouter.
 */
void ajouter_valeur_tableau_dynamique_entier( TableauDynamiqueEntier *td, int valeur );

/*! \fn void afficher_tableau_dynamique_entier( TableauDynamiqueEntier *td )
    \brief Affiche un tableau dynamique d'entier.
    \param *td Un pointeur sur le tableau dynamique d'entier à afficher.
 */
void afficher_tableau_dynamique_entier( TableauDynamiqueEntier *td );
