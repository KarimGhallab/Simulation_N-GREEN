/*!
 * \file ListeChainee.h
 * \brief Header du fichier contenant la structure représentant une liste chainée ainsi que les fonctions pour l'utilisé comme une FIFO.
 */


/*! \struct Maillon.
 * \brief Structure représentant Maillon de la liste chainée.
 * Elle contient un tic d'arrivé et un pointeur sur le maillon suivant.
 */
typedef struct Maillon Maillon;
struct Maillon
{
	int tic_arrive;
	Maillon *suivant;
};

/*! \struct ListeChainee.
 * \brief Structure représentant une liste chainée.
 * Elle contient un pointeur sur le premier maillon de la liste.
 */
struct ListeChainee
{
	Maillon *premier;
};

typedef struct ListeChainee ListeChainee;

/*! \fn ListeChainee *creer_Liste_chainee()
   \brief Constructeur d'une liste chainée.
   \return un pointeur sur le premier élement de la liste.
*/
ListeChainee *creer_Liste_chainee();

/*! \fn void inserer_fin( ListeChainee *liste, int tic_arrive )
   \brief Insère en fin de liste un nouveau maillon.
   \param liste : La liste chainée sur laquelle on souhaite ajouter l'élément.
   \param tic_arrive : La valeur de l'élément.
*/
void inserer_fin( ListeChainee *liste, int tic_arrive );


/*! \fn int supprimer_premier( ListeChainee *liste )
   \brief Supprime le premier élément de la liste et renvoie sa valeur.
   \param liste : La liste chainée pour laquelle nous souhaitons supprimer le premier maillon.
*/
int supprimer_premier(ListeChainee *liste);

/*! \fn int liste_est_vide(ListeChainee *liste)
   \brief Indique si une liste est vide ou non.
   \param liste : la liste chainée.
   \return 1 Si la liste est vide, 0 si elle contient au moins un élément.
*/
int liste_est_vide(ListeChainee *liste);

/*! \fn void afficher_liste( ListeChainee *liste )
   \brief Affiche une liste chainée.
   \param liste : La liste chainée que nous souhaitons afficher.
*/
void afficher_liste(ListeChainee *liste);
