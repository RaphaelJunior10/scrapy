# scrapy
Scrapy est un script python permettant de telecharger la première image d'une liste de produitès sur Google en utilisant le web scrapping.

Il n'y a aucun module à installer, le script débute en téléchargeant les modules nécessaires si ces derniers ne sont pas installés.
Il faudra créer un réprtoire nommé path à la racine du projet, c'est bien ce répertoire qui contiendra les images téléchargées.
Le script récupère les données à télécharger dans une base de données, il faudrait remplir l'objet tab de facon à ce qu'il contienne les données nécessaires sous la forme suivante:
nom_enregistré:nom_image_à_télécharger
