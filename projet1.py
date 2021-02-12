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

    price_exclu_tax = soup.findAll("td")[2]

    price_incl_tax = soup.findAll("td")[3]

    number_available = soup.findAll("td")[5]

    number_reviews = soup.findAll("td")[6]

    description = soup.findAll("p")[3]















