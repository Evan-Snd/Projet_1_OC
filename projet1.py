import requests
import csv342 as csv
from bs4 import BeautifulSoup
import urllib.request
import os

liste_url_categorie = []
liste_url_livres = []

# Récupération des liens des catégorie dans un fichier txt

def recuperation_liens_categories():

    url = 'http://books.toscrape.com/index.html'

    response = requests.get(url)

    if response.ok:
        global soup
        soup = BeautifulSoup(response.text, features="html.parser")
        classe = soup.findAll("ul", {"class": "nav nav-list"})

        for li in classe:
            liste_a = li.findAll('a')
            for a in liste_a:
                lien = a['href']
                liste_url_categorie.append("http://books.toscrape.com/" + lien)
        del liste_url_categorie[0]

# Ecrire dans un fichier texte

def ecrire_dans_un_fichier_texte(nomFichier, liste_url):

    with open(nomFichier, 'w') as file:                                                                                                                 # Ouverture d'un fichier txt
        for lien in liste_url:
            file.write(lien + '\n')

# Accéder à l'url d'une catégorie

def acceder_url(nomFichier, nom):

    with open(nomFichier, 'r') as nom:                                                                                                                  # Lecture du fichier txt
        for row in nom:                                                                                                                                 # Pour chaque row dans le fichier
            global url2
            url2 = row.strip()

            recuperation_lien_page(url2)
            obtention_des_liens_autre_pages(url2)

# Récupération des liens de la première page d'une catégorie

def recuperation_lien_page(url):

    response = requests.get(url)                                                                                                                # Requête vers le nouvel url

    if response.ok:
        global soup
        soup = BeautifulSoup(response.text, features="html.parser")
        classe = soup.findAll("div", {"class": "image_container"})                                                                              # Chercher toute les div class: image_container dans la page HTML
        for div in classe:                                                                                                                      # Chercher les elements div dans la page
            liste_a = div.find('a')                                                                                                             # Pour chaque élément div on va chercher le a
            lien = liste_a['href']                                                                                                              # Pour chaque a on va chercher le href
            liste_url_livres.append("http://books.toscrape.com/catalogue/" + lien[9:])                                                          # Ajout du lien reconstitué à la liste

# Récupération des liens des autres pages

def obtention_des_liens_autre_pages(url):

    if soup.find("li", {"class": "next"}):                                                                                                  # Si on trouve dans l'objet soup, la balise (li) avec la class "next"
        nxt = soup.findAll("li", {"class": "next"})                                                                                         # nxt devient la balise (li) avec la class "next"
        for li in nxt:                                                                                                                      # Chercher les elements li dans la page
            b = li.find('a')                                                                                                                # Pour chaque élément li on va chercher le a
            lien2 = b['href']

            url = url[0:-10] + lien2

            for i in range(2, 9):                                                                                                           # Pour I allant de 2 a 8 (car 8 pages maximum)
                global nv_url
                nv_url = url[0:-6] + str(i) + '.html'                                                                                       # Nouvel URL = ancien en remplacant le numéro de page par i
                recuperation_lien_page(nv_url)
    del liste_url_livres[1000:]


# Création et écriture dans le fichier csv des informations souhaités pour chaque URL enregistré dans le fichier txt

def creation_ecriture_fichier_csv_donnees_souhaitees_et_telechargement_image():

    with open('urls_livres.txt', 'r') as file2:                                                                                                         # Lecture du fichier txt
        for row in file2:                                                                                                                               # Pour chaque row dans le fichier
            url = row.strip()                                                                                                                           # URL prends la valeur de row

            response = requests.get(url)                                                                                                                # Requête vers le nouvel url
            if response.ok:
                soup = BeautifulSoup(response.text, features="html.parser")                                                                             # Creation de l'objet soup avec le code html dedans

                code = soup.find("td")                                                                                                                  # Chercher le premier td

                title = soup.find("h1")                                                                                                                 # Chercher h

                price_exclu_tax = soup.findAll("td")[2]                                                                                                 # Chercher le deuxième td

                price_incl_tax = soup.findAll("td")[3]                                                                                                  # Chercher le troisième td

                number_available = soup.findAll("td")[5]                                                                                                # Chercher le cinquième td

                number_reviews = soup.findAll("td")[6]                                                                                                  # Chercher le sixième td

                category = soup.findAll("li")[2]                                                                                                        # Chercher le deuxième li

                image_url = soup.find("img")["src"]                                                                                                     # Chercher l'URL de l'image

                description = soup.findAll("p")[3]                                                                                                      # Chercher le troisième p

                file_name = category.text[1:-1] + '.csv'

                urlImage = "http://books.toscrape.com" + image_url[5:]
                cheminDossier = "C:\\Users\\sinda\\OpenClassroom2\\projet1\\" + category.text[1:-1]
                titreImg = title.text + '.jpg'
                descriptionProduit = description.text

                specialChars = ":#/\"*?'-"

                for specialChar in specialChars:
                    titreImg = titreImg.replace(specialChar, '_')
                descriptionProduit = descriptionProduit.replace('Ã©', "é")
                descriptionProduit = descriptionProduit.replace('¢', "")
                descriptionProduit = descriptionProduit.replace('â â', "_")
                descriptionProduit = descriptionProduit.replace('â', "_")

                if os.path.exists(cheminDossier):
                    pass
                else:
                    os.makedirs(cheminDossier)

                with open(cheminDossier + '\\' + file_name, 'a', newline='', encoding='utf-16') as csvfile:                                              # Ecriture dans le fichier csv des données récupérés
                    spamwriter = csv.writer(csvfile, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    spamwriter.writerow([code.text, title.text, price_exclu_tax.text[1:], price_incl_tax.text[1:], number_available.text, number_reviews.text, category.text[1:-1], "http://books.toscrape.com" + image_url[5:], url, descriptionProduit])

                urllib.request.urlretrieve(urlImage, cheminDossier + '\\' + titreImg)

recuperation_liens_categories()
ecrire_dans_un_fichier_texte('urls_categorie.txt', liste_url_categorie)
acceder_url('urls_categorie.txt', 'file')
recuperation_lien_page(url2)
obtention_des_liens_autre_pages(url2)
ecrire_dans_un_fichier_texte('urls_livres.txt', liste_url_livres)
creation_ecriture_fichier_csv_donnees_souhaitees_et_telechargement_image()