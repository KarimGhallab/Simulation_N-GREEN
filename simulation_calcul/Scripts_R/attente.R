library(ggplot2)

#Active la création de fichier PDF lorsqu'un plot est executé

#Stocke une liste avec tout les fichers CSV du dossier
fichiers = list.files(path ="../CSV/", pattern="*.csv")
pdf("../PDF/attente.pdf")

#Pour chaque fichier CSV, on cree un graphique
for (fichier in fichiers)
{
	if (fichier != "attentes_messages.csv")
	{
		chemin_fichier = paste("../CSV/", fichier, sep="")
		donnees = read.csv(chemin_fichier)

		#Création du titre du plot
		titre = "Temps d'attente au TIC"
		titre = paste(titre, donnees[1,4])

		#Créé des 'Grouped Bar Plot'
		p <- ggplot(donnees, aes(x=numero_noeud, y=TIC, fill=type_attente)) +
		geom_bar(stat="identity", position = "dodge") +
		scale_size_area("Type d'attente") +
		xlab("Numéro du noeud") +
		ylab("Nombre de TIC") +
		geom_text(aes(label=donnees$TIC, y = donnees$TIC), size = 3, angle=90, position = position_dodge(width =0.9), hjust=1.2, vjust=0.7, color="white") +
		ggtitle(titre) +
		theme(legend.background = element_rect(fill="lightblue", size=0.5, linetype="solid")) +
		scale_fill_discrete(name = "Type d'attente")

		#Sauvegarde le plot dans le fichier PDF
		print(p)
	}
}

dev.off()
q(save="no")
