/*! \file CoupleNombreValeur.h
    \brief Header du fichier décrivant une structure à deux entrées spécifiant le nombre d'occurence d'une valeur.
 */

 /*! \struct CoupleNombreValeur
     \brief Structure à deux entrées spécifiant le nombre d'occurence d'une valeur et la valeur.
  */
 struct CoupleNombreValeur
 {
 	int nombre_valeur;
 	int valeur;
 };
 typedef struct CoupleNombreValeur CoupleNombreValeur;

 /*! \fn CoupleNombreValeur* initialiser_couple_nombre_valeur( int nombre_valeur, int valeur)
     \brief Initialise un anneau.
     \param nombre_valeur Le nombre de valeur du couple.
     \param valeur La valeur du couple.
     \return Un pointeur sur le couple créé.
  */
 CoupleNombreValeur initialiser_couple_nombre_valeur( int nombre_valeur, int valeur);
