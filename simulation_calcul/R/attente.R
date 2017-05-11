library(ggplot2)
options(device=pdf)

#Active la création de fichier PDF lorsqu'un plot est executé

#Stocke une liste avec tout les fichers CSV du dossier
fichiers = list.files(pattern="*.csv")
pdf("attente.pdf")

#Pour chaque fichier CSV, on cree un graphique
for (fichier in fichiers)
{
	donnees = print(read.csv(fichier))
	print(donnees)

	#Créé des 'Grouped Bar Plot'
	p <- ggplot(donnees, main ="Test 1", aes(factor(numero_noeud), TIC, fill = type_attente) ) +
	geom_bar(stat="identity", position = "dodge")

	#Sauvegarde le plot dans le fichier PDF
	print(p)
}

dev.off()
q(save="no")
