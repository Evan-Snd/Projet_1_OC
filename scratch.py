import requests
import csv342 as csv
from bs4 import BeautifulSoup
import urllib.request

liste_url_categorie = []
liste_url_livres = []


# Création et écriture dans le fichier csv des informations souhaités pour chaque URL enregistré dans le fichier txt

Liste = ['UPC', 'Titre', 'PrixTaxeInclu', 'PrixTaxeExclu', 'NbrDispon', 'NbrReviews', 'Categorie',
         'ImageURL', 'URL', 'Description']                                                                  # Création d'un liste

with open('test.csv', 'w', newline='', encoding='utf-8') as csvfile:                                        # Creation du fichier csv
    spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)               # !!!!!!!!!
    spamwriter.writerow(Liste)                                                                              # Ecriture de la Liste dans le fichier CSV

with open('urls_livres.txt', 'r') as file2:                                                                         # Lecture du fichier txt
    for row in file2:                                                                                        # Pour chaque row dans le fichier
        url = row.strip()                                                                                   # URL prends la valeur de row

        response = requests.get(url)                                                                        # Requête vers le nouvel url
        if response.ok:
            soup = BeautifulSoup(response.text, features="html.parser")                                     # Creation de l'objet soup avec le code html dedans

            code = soup.find("td")                                                                          # Chercher le premier td

            title = soup.find("h1")                                                                         # Chercher h

            price_exclu_tax = soup.findAll("td")[2]                                                         # Chercher le deuxième td

            price_incl_tax = soup.findAll("td")[3]                                                          # Chercher le troisième td

            number_available = soup.findAll("td")[5]                                                        # Chercher le cinquième td

            number_reviews = soup.findAll("td")[6]                                                          # Chercher le sixième td

            category = soup.findAll("li")[2]                                                                # Chercher le deuxième li

            image_url = soup.find("img")["src"]                                                             # Chercher l'URL de l'image

            description = soup.findAll("p")[3]                                                              # Chercher le troisième p

            file_name = category.text[1:-1] + '.csv'

            with open(file_name, 'a', newline='', encoding='utf-8') as csvfile:                            # Ecriture dans le fichier csv des données récupérés
                spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow([code.text, title.text, price_exclu_tax.text[1:], price_incl_tax.text[1:], number_available.text, number_reviews.text, category.text[1:-1], "http://books.toscrape.com" + image_url[5:], url, description.text])

            urlImage = "http://books.toscrape.com" + image_url[5:]
            print(urlImage)
            titreImage = 'Images-' + title.text[:10] + '.jpg'

            urllib.request.urlretrieve(urlImage, titreImage)