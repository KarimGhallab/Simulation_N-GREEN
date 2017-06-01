library(ggplot2)
library(scales)

# On part du principe que les fichiers CSVs sont toujours générés par deux.
nombre_fichiers = length(list.files(path ="../CSV/", pattern="*.csv"))

#Active la création de fichier PDF lorsqu'un plot est executé
pdf("../PDF/distribution_attentes.pdf")

for (numero_fichier in 1:(nombre_fichiers/2) )
{
	chemin_fichier = paste("../CSV/attente_anneau", as.character(numero_fichier), sep="")
	chemin_fichier = paste(chemin_fichier, ".csv", sep="")

	#On cmmence avec la lecture du fichiers indiquant les nombres de messages
	donnees = read.csv(chemin_fichier)

	############# Trie des abscisses #############
	donnees$intervalle <- as.character(donnees$intervalle)
	donnees$intervalle <- factor(donnees$intervalle, levels=unique(donnees$intervalle))

	nombre_tic = comma(donnees$TIC[1])	#Le nombre de tic de la simulation
	nombre_slot = as.character(donnees$nb_slot[1])
	nombre_noeud = as.character(donnees$nb_noeud[1])

	############# On écrit un petit message récapitulatif de la simulation #############
	texte_info = paste("Fait à partir d'une simulation de", nombre_tic)
	texte_info = paste(texte_info, "tics")
	texte_info = paste(texte_info, "avec")
	texte_info = paste(texte_info, nombre_slot)
	texte_info = paste(texte_info, "slots")
	texte_info = paste(texte_info, "et")
	texte_info = paste(texte_info, nombre_noeud)
	texte_info = paste(texte_info, "noeuds")

	titre = "Répartition des temps d'attentes des messages"

	############# Obtention des pourcentages #############
	pourcentages = NULL
	for (valeur in donnees$taux)
	{
		pourcentage = valeur * 100
		pourcentage = format(pourcentage, digits=3)
		abscisse = paste(pourcentage, "%", sep="")
		pourcentages <- c(pourcentages, abscisse)
	}
	#print(pourcentages)
	############# Génération du graphique indiquant le nombre de message ayant attendu #############
	#p <- ggplot(data=donnees, aes(x = donnees$intervalle, y = donnees$taux)) +
	p <- ggplot(donnees, aes(x=donnees$intervalle, y=donnees$taux, fill=type)) +
	geom_bar(stat="identity", position = "dodge") +
	geom_text(aes(label=pourcentages, y = donnees$taux), size = 3, hjust=0.5, vjust=-0.5, color="black", position = position_dodge(width =0.9)) +
	theme(axis.text=element_text(size=7), axis.title=element_text(size=12,face="bold"), plot.caption=element_text(size=8, face="italic")) +
	scale_y_continuous(labels = percent, name = "Nombre de message") +
	scale_x_discrete(name = "Intervalle") +
	labs(caption = texte_info) +
	ggtitle(titre)

	print(p)

	###############################################################
	#### On passe au graphique indiquant les moyennes, min, max ###
	###############################################################
	chemin_fichier = paste("../CSV/repartition_attentes", as.character(numero_fichier), sep="")
	chemin_fichier = paste(chemin_fichier, ".csv", sep="")

	#On cmmence avec la lecture du fichiers indiquant les nombres de messages
	donnees = read.csv(chemin_fichier)

	titre = "Temps d'attentes des messages"
	############# Trie des abscisses #############
	donnees$intervalle <- as.character(donnees$intervalle)
	donnees$intervalle <- factor(donnees$intervalle, levels=unique(donnees$intervalle))

	nombre_tic = comma(donnees$TIC[1])	#Le nombre de tic de la simulation

	#p <- ggplot2.barplot(data=donnees, xName='intervalle', yName="valeur",groupName='type_valeur', position = position_dodge() )
	p <- ggplot(donnees, aes(x=intervalle, y=valeur, fill=type_valeur)) +
	geom_bar(stat="identity", position = "dodge") +
	scale_size_area("Type d'attente") +
	ylab("Nombre de TIC") +
	xlab("Quantile") +
	geom_text(aes(label=donnees$valeur, y = donnees$valeur), size = 3, angle=90, position = position_dodge(width =0.9), hjust=1.2, vjust=0.7, color="white") +
	theme(legend.background = element_rect(fill="lightblue", size = 0.5, linetype="solid"), axis.text=element_text(size=7), axis.title=element_text(size=12,face="bold"), plot.caption=element_text(size=8, face="italic"), axis.text.x=element_blank(),) +
	scale_fill_discrete(name = "Type d'attente") +
	labs(caption = texte_info) +
	ggtitle(titre)

	print(p)
}

dev.off()
q(save="no")
