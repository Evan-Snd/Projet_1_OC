import requests
import csv342 as csv
from bs4 import BeautifulSoup


liste = []


url = 'http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html'

response = requests.get(url)

if response.ok:
    soup = BeautifulSoup(response.text, features="html.parser")
    href = soup.findAll("div", {"class": "image_container"})
    for div in href:
        a = div.find('a')
        lien = a['href']
        liste.append("http://books.toscrape.com/catalogue" + lien[8:])

if soup.findAll("li", {"class": "next"}):
    nxt = soup.findAll("li", {"class": "next"})
    for li in nxt:
        b = li.find('a')
        lien2 = b['href']

    url = url[0:-10] + lien2


    for i in range(2, 8):
        nv_url = url[0:-6] + str(i) + '.html'

        response2 = requests.get(nv_url)

        if response2.ok:
            soup = BeautifulSoup(response2.text, features="html.parser")
            href = soup.findAll("div", {"class": "image_container"})
            for div in href:
                a = div.find('a')
                lien = a['href']
                liste.append("http://books.toscrape.com/catalogue" + lien[8:])

with open('urls.txt', 'w') as file:
    for link in liste:
        file.write(link + '\n')


Liste = ['UPC', 'Titre', 'PrixTaxeInclu', 'PrixTaxeExclu', 'NbrDispon', 'NbrReviews', 'Categorie',
         'ImageURL', 'URL', 'Description']

with open('test.csv', 'w', newline='', encoding='utf-8') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(Liste)

with open('urls.txt', 'r') as file:
    for row in file:
        url = row.strip()

        response = requests.get(url)
        if response.ok:
            soup = BeautifulSoup(response.text, features="html.parser")

            code = soup.find("td")

            title = soup.find("h1")

            price_exclu_tax = soup.findAll("td")[2]

            price_incl_tax = soup.findAll("td")[3]

            number_available = soup.findAll("td")[5]

            number_reviews = soup.findAll("td")[6]

            category = soup.findAll("li")[2]

            image_url = soup.find("img")["src"]

            description = soup.findAll("p")[3]

            with open('test.csv', 'a', newline='', encoding='utf-8') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow([code.text, title.text, price_exclu_tax.text[1:], price_incl_tax.text[1:], number_available.text, number_reviews.text, category.text[1:-1], "http://books.toscrape.com" + image_url[5:], url, description.text])
