#include <stdlib.h>
#include "../Headers/CoupleNombreValeur.h"

CoupleNombreValeur initialiser_couple_nombre_valeur( int nombre_valeur, int valeur)
{
	CoupleNombreValeur cnv = {nombre_valeur, valeur};
	return cnv;
}
