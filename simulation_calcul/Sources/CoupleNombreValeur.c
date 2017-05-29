#include <stdlib.h>
#include "../Headers/CoupleNombreValeur.h"

CoupleNombreValeur* initialiser_couple_nombre_valeur( int nombre_valeur, int valeur)
{
	CoupleNombreValeur *cnv = (CoupleNombreValeur *) malloc( sizeof(CoupleNombreValeur) );
	cnv->nombre_valeur = nombre_valeur; cnv->valeur = valeur;

	return cnv;
}
