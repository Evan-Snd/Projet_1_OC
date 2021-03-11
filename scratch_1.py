import requests
import csv342 as csv
from bs4 import BeautifulSoup
import urllib.request
from PIL import Image

liste_url_categorie = []
liste_url_livres = []
Liste = ['UPC', 'Titre', 'PrixTaxeInclu', 'PrixTaxeExclu', 'NbrDispon', 'NbrReviews', 'Categorie', 'ImageURL', 'URL',
         'Description']  # Création d'un liste


# Récupération des liens des catégorie dans un fichier txt

def recuperation_liens_categories():
    url = 'http://books.toscrape.com/index.html'

    response = requests.get(url)

    if response.ok:
        soup = BeautifulSoup(response.text, features="html.parser")
        classe = soup.findAll("ul", {"class": "nav nav-list"})

        for li in classe:
            liste_a = li.findAll('a')
            for a in liste_a:
                lien = a['href']
                liste_url_categorie.append("http://books.toscrape.com/" + lien)
        del liste_url_categorie[0]


# Accéder à l'url d'une catégorie

def acceder_url(nomFichier, nom):
    with open(nomFichier, 'r') as nom:  # Lecture du fichier txt
        for row in nom:  # Pour chaque row dans le fichier
            url = row.strip()
            return url

            # Récupération des liens de la première page d'une catégorie

            def recuperation_lien_page():

                response = requests.get(url)  # Requête vers le nouvel url
                if response.ok:
                    soup = BeautifulSoup(response.text, features="html.parser")
                    classe = soup.findAll("div", {
                        "class": "image_container"})  # Chercher toute les div class: image_container dans la page HTML
                    for div in classe:  # Chercher les elements div dans la page
                        liste_a = div.find('a')  # Pour chaque élément div on va chercher le a
                        lien = liste_a['href']  # Pour chaque a on va chercher le href
                        liste_url_livres.append(
                            "http://books.toscrape.com/catalogue/" + lien[9:])  # Ajout du lien reconstitué à la liste


recuperation_liens_categories()
acceder_url('urls_categorie.txt', 'file')
recuperation_liens_categories()

