from requests import get
from bs4 import BeautifulSoup
import sqlite3
import threading
import requests


def send_msg(text, user):
  token = '7182530482:AAFqK8HPClorn0WiDo7xWaLHoA5L8u5MxsE'

  # '1901737419:AAHaDsUkEQTZEPOC0RUKYqIhHmQrPJJFAic'

  # chat_id = user

  # 1130376365 / moj
  # 1911688399 / pracowniczy
  # 1602171553 / Marcin
  # 1901400593 / Kasia
  # 5781252545


  # 6377487020

  chat_id2 = '6377487020'
  url_req = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={user}&text={text}'
  results = requests.get(url_req)

  url_req2 = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id2}&text={text}'
  results2 = requests.get(url_req2)
  print(results.json())


def olx_search(word, min_price=0, max_price=99999999, category='', city='', distance=0, search_amount=0, user=''):
  try:
    min_price = int(min_price)
  except:
    min_price = 0

  try:
    max_price = int(max_price)
  except:
    max_price = 99999999

  connectDB = sqlite3.connect(f'{word}.db')
  cDB = connectDB.cursor()
  cDB.execute(f"""CREATE TABLE IF NOT EXISTS tasks (
          name text,
          price INTEGER,
          link text
      )""")


  if not category and not city:
    URL = f'https://www.olx.pl/oferty/q-{word}/&page=1?search%5Bfilter_float_price%3Afrom%5D={min_price}&search%5Bfilter_float_price%3Ato%5D={max_price}'

  if category and not city:
    URL = f'https://www.olx.pl/{category}/q-{word}/&page=1?search%5Bfilter_float_price%3Afrom%5D={min_price}&search%5Bfilter_float_price%3Ato%5D={max_price}'

  if category and city:
    URL = f'https://www.olx.pl/{category}/{city}/q-{word}/&page=1?search%5Bfilter_float_price%3Afrom%5D={min_price}&search%5Bfilter_float_price%3Ato%5D={max_price}&search%5Bdist%5D={distance}'

  if not category and city:
    URL = f'https://www.olx.pl/{city}/q-{word}/&page=1?search%5Bfilter_float_price%3Afrom%5D={min_price}&search%5Bfilter_float_price%3Ato%5D={max_price}&search%5Bdist%5D={distance}'
  page = get(URL).content
  bs = BeautifulSoup(page, 'html.parser')


  pages_amount = 1

  # Sprawdza czy już skanowało 10 razy

  if search_amount < 4:

    for page_number in range(1, pages_amount + 1):
      print('numer strony: ', page_number)

      if not category and not city:
        URL = f'https://www.olx.pl/oferty/q-{word}/&page={page_number}?search%5Bfilter_float_price%3Afrom%5D={min_price}&search%5Bfilter_float_price%3Ato%5D={max_price}'

      if category and not city:
        URL = f'https://www.olx.pl/{category}/q-{word}/&page={page_number}?search%5Bfilter_float_price%3Afrom%5D={min_price}&search%5Bfilter_float_price%3Ato%5D={max_price}'

      if category and city:
        URL = f'https://www.olx.pl/{category}/{city}/q-{word}/&page={page_number}?search%5Bfilter_float_price%3Afrom%5D={min_price}&search%5Bfilter_float_price%3Ato%5D={max_price}&search%5Bdist%5D={distance}'

      if not category and city:
        URL = f'https://www.olx.pl/{city}/q-{word}/&page={page_number}?search%5Bfilter_float_price%3Afrom%5D={min_price}&search%5Bfilter_float_price%3Ato%5D={max_price}&search%5Bdist%5D={distance}'

      print(URL)
      page = get(URL).content
      bs = BeautifulSoup(page, 'html.parser')
      try:
        empty_list = bs.find(class_='emptynew').get_text()
        # .find('span')
        print('Brak wyszukań')
        connectDB.close()
        return
      except:
        pass
      offer_list = bs.find(class_='css-j0t2x2').find_all(class_='css-1sw7q4x')

      for offer in offer_list:
        offer_name = offer.find(class_='css-u2ayx9').find('h4').get_text().replace("'", "").replace('"', '')
        try:
          offer_link = offer.find(href=True)['href']
          # offer.find('a', class_="detailsLink")
          print(offer_link)
          offer_link = 'olx.pl' + offer_link
        except:
          offer_link = ''
          print('link problem')
        try:
          offer_price = offer.find('p').get_text()
          print(offer_price)
        except:
          offer_price = 0
        try:
          offer_price = offer_price.replace('zł', '').replace(' ', '').replace(',', '.')
          offer_price = int(offer_price)
        except:
          pass
        cDB.execute(f"SELECT * FROM tasks WHERE name='{offer_name}' AND price='{offer_price}'")
        offerts_list = cDB.fetchall()

        if len(offerts_list) == 0:
          cDB.execute("INSERT INTO tasks VALUES (?,?,?)", (offer_name, offer_price, offer_link))
          connectDB.commit()
          print('Nowa oferta:', offer_price, 'zł', offer_name, offer_link)

        elif len(offerts_list) > 0:
          print('Oferta juz istniała: ', offer_price, 'zł', offer_name)
          pass

  # Jeśli było skanowane więcej ni 10 razy
  elif search_amount >= 4:
    for page_number in range(1, 2):
      print('numer strony: ', page_number)

      if not category and not city:
        URL = f'https://www.olx.pl/oferty/q-{word}/&page={page_number}?search%5Bfilter_float_price%3Afrom%5D={min_price}&search%5Bfilter_float_price%3Ato%5D={max_price}'

      if category and not city:
        URL = f'https://www.olx.pl/{category}/q-{word}/&page={page_number}?search%5Bfilter_float_price%3Afrom%5D={min_price}&search%5Bfilter_float_price%3Ato%5D={max_price}'

      if category and city:
        URL = f'https://www.olx.pl/{category}/{city}/q-{word}/&page={page_number}?search%5Bfilter_float_price%3Afrom%5D={min_price}&search%5Bfilter_float_price%3Ato%5D={max_price}&search%5Bdist%5D={distance}'

      if not category and city:
        URL = f'https://www.olx.pl/{city}/q-{word}/&page={page_number}?search%5Bfilter_float_price%3Afrom%5D={min_price}&search%5Bfilter_float_price%3Ato%5D={max_price}&search%5Bdist%5D={distance}'

      print(URL)
      page = get(URL).content
      bs = BeautifulSoup(page, 'html.parser')
      try:
        empty_list = bs.find(class_='emptynew').get_text()
        print('Brak wyszukań')
        connectDB.close()
        return
      except:
        pass

      offer_list = bs.find(class_='css-j0t2x2').find_all(class_='css-1sw7q4x')

      for offer in offer_list:
        offer_name = offer.find(class_='css-u2ayx9').find('h4').get_text().replace("'", "").replace('"', '')
        print(offer_name)
        try:
          offer_price = offer.find('p').get_text()
          print(offer_price)
        except:
          offer_price = 0
        try:
          offer_link = offer.find(href=True)['href']
          print(offer_link)
          offer_link = 'olx.pl' + offer_link
        except:
          offer_link = ''
        try:
          offer_price = offer_price.replace('zł', '').replace(' ', '').replace(',', '.')
          offer_price = int(offer_price)
        except:
          pass
        cDB.execute(f"SELECT * FROM tasks WHERE name='{offer_name}' AND price='{offer_price}'")
        offerts_list = cDB.fetchall()

        if len(offerts_list) == 0:
          cDB.execute("INSERT INTO tasks VALUES (?,?,?)", (offer_name, offer_price, offer_link))
          connectDB.commit()
          print('Nowa oferta:', offer_price, 'zł', offer_name, offer_link)
          send_msg(f'Nowa oferta: {offer_name}, CENA: {offer_price} pln, LINK: {offer_link}', user)

        elif len(offerts_list) > 0:
          print('Oferta juz istniała: ', offer_price, 'zł', offer_name)
          pass

  connectDB.close()


def searching_function_loop():
  threading.Timer(120.0, searching_function_loop).start()
  connectDB = sqlite3.connect('search_phrases.db')
  cDB = connectDB.cursor()
  cDB.execute("SELECT rowid, * FROM pharses")
  searches_list = cDB.fetchall()

  for search in searches_list:
    olx_search(search[1], min_price=search[2], max_price=search[3], category=search[4], city=search[5],
               distance=search[6], search_amount=search[7], user=search[8])

    new_number = search[7] + 1
    cDB.execute(f"""
    UPDATE pharses
    SET search_amount = '{new_number}'
    WHERE rowid = {search[0]};
    """)
    connectDB.commit()
    print('ilość wyszukań: ', search[7] + 1)
  connectDB.close()


# searching_function_loop()


'''
def search_phrases_db():

  connectDB = sqlite3.connect(f'search_phrases.db')
  cDB = connectDB.cursor()

  cDB.execute(f"""CREATE TABLE IF NOT EXISTS pharses(
          phrase text,
          min_price INTEGER,
          max_price INTEGER,
          category text,
          city text,
          max_distance INTEGER,
          search_amount INTEGER,
          user text
      )""")

  connectDB.close()

search_phrases_db()
'''

'''
def users_db():

  connectDB = sqlite3.connect(f'users.db')
  cDB = connectDB.cursor()

  cDB.execute(f"""CREATE TABLE IF NOT EXISTS users(
          user_name text,
          user_id INTEGER
      )""")

  connectDB.close()

users_db()
'''
