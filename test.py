from requests import get
from bs4 import BeautifulSoup
import sqlite3
import threading
import requests


URL = 'https://www.donedeal.ie/cars'
page = get(URL).content 
bs = BeautifulSoup(page, 'html.parser')
test = bs.find_all(class_ = 'card__price')

for x in test:
    print(x)
