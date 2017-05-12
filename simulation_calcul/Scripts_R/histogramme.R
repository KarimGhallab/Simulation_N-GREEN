library(ggplot2)
library(scales)

chemin_fichier = "../CSV/attentes_messages.csv"

#Active la création de fichier PDF lorsqu'un plot est executé
pdf("../PDF/repartition_attente_message.pdf")

donnees = read.csv(chemin_fichier)

donnees


titre = "Répartition des temps d'attentes des messages"

ggplot(data=donnees, aes(donnees$TIC_attente)) +
geom_histogram(aes(fill=..count..)) +
scale_y_continuous(labels = comma) +
scale_x_continuous(labels = comma) +
labs(fill = "Nombre d'occurence", labels = comma) +
xlab("Nombre de TIC") +
ylab("Nombre de message") +
ggtitle(titre)


dev.off()
q(save="no")
