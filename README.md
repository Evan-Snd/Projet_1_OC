# Web Scraping
***
This project is a web scraping project. The purpose is to collect data from a web site and to write them in a csv file. The data are : 
product page url
universal product code (upc)
title
price including tax
price excluding tax
number available
product description
category
review rating
image url
This project also recovers the image of the product by downloading it.

# Intro

Create a folder and put all the file (projet1.py, README, requirement.txt) in this folder. 

# Install package

pip install -requirements.txt

# Change the path of the folder in the code

Before launch the code, you need to change the path of the folder where you want to save the data ( Line 118, variable cheminDossier )

# Create environment (GitBash)

cd path_folder ( Go to the desired folder )
virtualenv nomEnv

# Activate environment (GitBash)

for windows : ". nomEnv/Scripts/Activate" or ". nomEnv/Scripts/activate"

# Launch project

"python projet1.py" (GitBash)