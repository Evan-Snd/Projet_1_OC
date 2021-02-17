import requests
from bs4 import BeautifulSoup

Liste = []


url = 'http://books.toscrape.com/catalogue/category/books/poetry_23/index.html'

response = requests.get(url)

if response.ok:
    soup = BeautifulSoup(response.text, features="html.parser")
    href = soup.findAll("div", {"class": "image_container"})
    for div in href:
        a = div.find('a')
        lien = a['href']
        Liste.append("http://books.toscrape.com/catalogue" + lien[8:])

    print(Liste)