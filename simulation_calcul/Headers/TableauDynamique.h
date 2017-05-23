/*! \file TableauDynamique.h
    \brief Header du fichier de la strcture de tableau dynamique.
 */

 /*! \def TAILLE_INITIALE_TABLEAU
     \brief La taille initiale du tableau de la structure TableauDynamique.
  */
 #define TAILLE_INITIALE_TABLEAU 100000

/*! \struct TableauDynamique
    \brief Structure représentant tableau de taille dynamique.
    Un tableau dynamique contient un tableau d'entier, une taille de tableau (dynamique), ainsi qu'une taille de tableau utilisée.
 */
struct TableauDynamique
{
	int taille_tableau;
	int taille_utilisee;
	int *tableau;
};
typedef struct TableauDynamique TableauDynamique;


/*! \fn TableauDynamique* initialiser_tableau_dynamique()
    \brief Initialise un tableau dynamique.
    \return TableauDynamique* Un pointeur vers le tableau dynamique.
 */
TableauDynamique* initialiser_tableau_dynamique();

/*! \fn void ajouter_valeur( TableauDynamique *td, int valeur )
    \brief Ajoute une valeur au tableau dynamique.
     La taille du tableau peut etre réallouer si necessaire.
    \param *td Le tableau auquel on souhaite ajouter la valeur.
    \param valeur La valeur à ajouter.
 */
void ajouter_valeur( TableauDynamique *td, int valeur );

/*! \fn void afficher_tableau_dynamique( TableauDynamique *td )
    \brief Affiche un tableau dynamique.
    \param *td Un pointeur sur le tableau dynamique à afficher.
 */
void afficher_tableau_dynamique( TableauDynamique *td );
