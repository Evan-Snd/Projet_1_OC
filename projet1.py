import requests
import csv342 as csv
from bs4 import BeautifulSoup


Liste =['UPC', 'Titre', 'PrixTaxeInclu', 'PrixTaxeExclu', 'NbrDispon', 'NbrReviews', 'Description', 'Categorie', 'ImageURL']

url = "http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html"
response = requests.get(url)

if response.ok:
    soup = BeautifulSoup(response.text, features="html.parser")

    code = soup.find("td")

    title = soup.find("h1")















