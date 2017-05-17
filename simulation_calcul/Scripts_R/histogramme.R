library(ggplot2)
library(scales)

chemin_fichier = "../CSV/attentes_messages.csv"

#Active la création de fichier PDF lorsqu'un plot est executé
pdf("../PDF/repartition_attente_message.pdf")

donnees = read.csv(chemin_fichier)

nombre_tic_str = colnames(donnees)[3]	#Le nombre de tic de la simulation
taille_texte = nchar(nombre_tic_str) 	#La taille du texte du nombre de tic
nombre_tic = substring(nombre_tic_str, 2, taille_texte)		#Enleve le 'X' devant l'entête

texte_info = paste("Fait à partir d'une simulation de", nombre_tic)
texte_info = paste(texte_info, "tics")
texte_info

titre = "Répartition des temps d'attentes des messages"

ggplot(data=donnees, aes(x = donnees$interval, y = donnees$count)) +
geom_histogram(stat = "identity") +
scale_y_continuous(labels = comma) +#scale_x_continuous(labels = comma) +
labs(fill = "Nombre d'occurence", labels = comma) +
xlab("Nombre de TIC") +
ylab("Nombre de message") +
labs(caption = texte_info) +
ggtitle(titre)


dev.off()
q(save="no")
