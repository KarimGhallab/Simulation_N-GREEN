/*!
 * \file simulation.h
 * \brief Header du fichier principal exécutant la simulation.
 */

/*! \def NOMBRE_TIC
 * \brief Représente le nombre de TIC sur lequel portera la simulation.
 */
 #define NOMBRE_TIC 10		//Le nombre de TIC à effectuer.

 /*! \def NOMBRE_SLOT
  * \brief Indique le nombre de slot de l'anneau.
  */
 #define NOMBRE_SLOT 10		//Le nombre de slot dans l'anneau.

 /*! \def NOMBRE_NOEUD
  * \brief Indique le nombre de noeud de l'anneau.
  */
 #define NOMBRE_NOEUD 5	//Le nombre de noeud dans l'anneau.


//////////////////////////////////////////////////
///////////////// Les structures /////////////////
//////////////////////////////////////////////////

/*! \struct Messages.
 * \brief Structure représentant un groupe de message arrivant dans le noeud.
 * Un groupe de message à une taille ainsi qu'un TIC d'arrivé dans le noeud.
 */
struct Messages
{
	int TIC_arrive;
	int taille;
};
typedef struct Messages Messages;

/*! \struct PaquetMessage
 * \brief Structure représentant un paquet de message curculant dans les slots.
 * Cette structure contient un indice du noeud emetteur du paquet, un nombre de message, et un tableau des différents messages.
 */
struct PaquetMessage
{
	int indice_noeud_emetteur;
	int nombre_messages;
	Messages messages[80];		//Un slot ne peut contenir plus de 80 messages
};
typedef struct PaquetMessage PaquetMessage;

/*! \struct Noeud
 * \brief Structure représentant un Noeud de l'anneau.
 * Elle contient un nombre de message, les indices des slots avec lesquels le noeud peut intéragir, ainsi que le nombre d'antenne liée au noeud et le décalage avec laquelle le noeud doit recevoir un message de ses antennes.
 */

struct Noeud
{
	int id;
	int nb_message;
	int indice_slot_lecture;
	int indice_slot_ecriture;
	int nb_antenne;		//Indique le nombre d'antenne auquel est lié le noeuds
	int debut_periode;		//Le décalage selon lequel le noeud recoit des messages des antennes
};
typedef struct Noeud Noeud;

/*! \struct Slot
 * \brief Structure représentant un slot dans l'anneau.
 * Un Slot est caractérisé par un id (unique), un booléen insiquant si le slot contient un message ou non, ainsi que les indices du noeud lié au slot s'il y en a un.
 */

struct Slot
{
	int id;
	int paquet_message;		//Indique si le slot possede un paquet de message
	int indice_noeud_lecture;		//Si le slot ne peut accèder a aucun noeud, ce champs vaut -1
	int indice_noeud_ecriture;		//Si le slot ne peut accèder a aucun noeud, ce champs vaut -1
};
typedef struct Slot Slot;

//////////////////////////////////////////////////
///////////////// Les fonctions /////////////////
//////////////////////////////////////////////////

/*! \fn void afficher_slots( Slot slots[] )
* \brief Initialise les slots de l'anneau.
* \param slots[] Le tableau des slots à initialiser.
*/
void afficher_slots( Slot slots[] );

/*! \fn void initialiser_slots( Slot slots[] )
* \brief Affiche les slots de l'anneau.
* \param slots[] Les slots à afficher.
*/
void initialiser_slots( Slot slots[] );

/*! \fn void afficher_noeuds( Noeud noeuds[] )
* \brief Initialise les noeuds de l'anneau et modifie en conséquence les indices en écriture/lecture des slots.
* \param noeuds[] Le tableau des noeuds à initialiser.
* \param noeuds[] Le tableau des slots à modifier.
*/
void afficher_noeuds( Noeud noeuds[] );

/*! \fn void initialiser_noeuds( Noeud noeuds[], Slot slots[] )
* \brief Affiche les noeuds de l'anneau.
* \param noeuds[] Les noeuds à afficher.
*/
void initialiser_noeuds( Noeud noeuds[], Slot slots[] );
