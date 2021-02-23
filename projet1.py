import requests
import csv342 as csv
from bs4 import BeautifulSoup

liste_url_categorie = []
liste_url_livres = []

# Récupération des liens des catégorie dans un fichier txt

url = 'http://books.toscrape.com/index.html'

response = requests.get(url)

if response.ok:
    soup = BeautifulSoup(response.text, features="html.parser")
    href = soup.findAll("ul", {"class": "nav nav-list"})

    for li in href:
        liste_a = li.findAll('a')
        for a in liste_a:
            lien = a['href']
            liste_url_categorie.append("http://books.toscrape.com/" + lien)
    del liste_url_categorie[0]

    with open('urls_categorie.txt', 'w') as file:                                                                                   # Ouverture d'un fichier txt
        for lien in liste_url_categorie:
            file.write(lien + '\n')

# Accéder à l'url d'une catégorie

with open('urls_categorie.txt', 'r') as file:                                                                                        # Lecture du fichier txt
    for row in file:                                                                                                                 # Pour chaque row dans le fichier
        url = row.strip()

# Récupération des liens de la première page d'une catégorie

        response = requests.get(url)                                                                                                # Requête vers le nouvel url
        if response.ok:
            soup = BeautifulSoup(response.text, features="html.parser")
            href = soup.findAll("div", {
                "class": "image_container"})                                                                                        # Chercher toute les div class: image_container dans la page HTML
            for div in href:                                                                                                        # Chercher les elements div dans la page
                a = div.find('a')                                                                                                   # Pour chaque élément div on va chercher le a
                lien = a['href']                                                                                                    # Pour chaque a on va chercher le href
                liste_url_livres.append("http://books.toscrape.com/catalogue/" + lien[9:])                                                        # Ajout du lien reconstitué à la liste


# Récupération des liens des autres pages

            if soup.find("li", {"class": "next"}):                                                                                      # Si on trouve dans l'objet soup, la balise (li) avec la class "next"
                nxt = soup.findAll("li", {"class": "next"})                                                                             # nxt devient la balise (li) avec la class "next"
                for li in nxt:                                                                                                          # Chercher les elements li dans la page
                    b = li.find('a')                                                                                                    # Pour chaque élément li on va chercher le a
                    lien2 = b['href']

                    url = url[0:-10] + lien2

                    for i in range(2, 8):                                                                                               # Pour I allant de 2 a 8 (car 8 pages maximum)
                        nv_url = url[0:-6] + str(i) + '.html'                                                                           # Nouvel URL = ancien en remplacant le numéro de page par i


                        response = requests.get(nv_url)                                                                                     # Requête vers l'URL

                        if response.ok:                                                                                                     # Même bloc de code que précédement
                            soup = BeautifulSoup(response.text, features="html.parser")                                                                    # Creation de l'objet soup avec le code HTML dedans
                            href = soup.findAll("div", {"class": "image_container"})                                                                                # Chercher toute les div class: image_container dans la page HTML
                            for div in href:                                                                                                # Chercher les elements div dans la page
                                a = div.find('a')                                                                                           # Pour chaque élément div on va chercher le a
                                lien = a['href']                                                                                            # Pour chaque a on va chercher le href
                                liste_url_livres.append("http://books.toscrape.com/catalogue/" + lien[9:])

# Ecriture dans le fichiers txt de la liste contenant les liens

with open('urls_livres.txt', 'w') as file2:                                                                         # Ouverture d'un fichier txt
    for lien in liste_url_livres:
        file2.write(lien + '\n')                                                                             # Ecrite dans le fichier texte les liens


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
