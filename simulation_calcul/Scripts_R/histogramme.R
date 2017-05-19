library(ggplot2)
library(scales)

chemin_fichier = "../CSV/attentes_messages.csv"

#Active la création de fichier PDF lorsqu'un plot est executé
pdf("../PDF/repartition_attente_message.pdf")

donnees = read.csv(chemin_fichier)

############# Trie des abscisses #############
donnees$interval <- as.character(donnees$interval)
donnees$interval <- factor(donnees$interval, levels=unique(donnees$interval))

nombre_tic_str = colnames(donnees)[3]	#Le nombre de tic de la simulation

############# On enleve le 'X' devant le nombre de TIC #############
taille_texte = nchar(nombre_tic_str)
nombre_tic = substring(nombre_tic_str, 2, taille_texte)
nombre_tic = comma( as.numeric(nombre_tic) )

texte_info = paste("Fait à partir d'une simulation de", nombre_tic)
texte_info = paste(texte_info, "tics")

titre = "Répartition des temps d'attentes des messages"

ggplot(data=donnees, aes(x = donnees$interval, y = donnees$count)) +
geom_histogram(stat = "identity",col="red", fill="green", alpha = .2 ) +
geom_text(aes(label=comma(donnees$count), y = donnees$count), size = 3, hjust=0.5, vjust=-0.5, color="black") +
theme(axis.text=element_text(size=7), axis.title=element_text(size=12,face="bold"), plot.caption=element_text(size=8, face="italic")) +
scale_y_continuous(labels = comma, name = "Nombre de message") +
scale_x_discrete(name = "Nombre de TIC") +
labs(caption = texte_info) +
ggtitle(titre)


dev.off()
q(save="no")
