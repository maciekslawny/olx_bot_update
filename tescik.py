from requests import get
from bs4 import BeautifulSoup
import sqlite3
import threading


URL = f'https://www.olx.pl/oferty/q-ps4/&page=1?search%5Bfilter_float_price%3Afrom%5D=0&search%5Bfilter_float_price%3Ato%5D=99999999'
page = get(URL).content
bs = BeautifulSoup(page, 'html.parser')
# print(bs)
offer_list = bs.find(class_='css-oukcj3').find_all(class_='css-1sw7q4x')
# print(offer_list)
for offer in offer_list:
    # print(offer)

    offer_name = offer.find(class_='css-u2ayx9').find('h6').get_text().replace("'", "").replace('"', '')
    print(offer_name)

# < div
#
#
# class ="css-1sw7q4x" data-cy="l-card" >
# < a class ="css-rc5s2u" href="/d/oferta/konsola-ps4-bez-gier-CID99-IDTOznb.html" >
# < div class ="css-qfzx1y" >
# < div class ="css-1venxj6" type="list" >
# < div class ="css-1ut25fa" type="list" >
# < div class ="css-pn1izb" type="list" >
# < div class ="css-gl6djm" >
# < img class ="css-8wsg1m" src="/app/static/media/no_thumbnail.15f456ec5.svg" / >
# < /div >
# < /div >
# < div class ="css-13aawz3" >
# < div class ="css-1av34ht" >
# < div class ="css-3xiokn" >
# < /div >
# < /div >
# < /div >
# < /div >
# < div class ="css-1apmciz" type="list" >
# < div class ="css-u2ayx9" >
# < h6 class ="css-16v5mdi er34gjf0" > konsola ps4 bez gier < /h6 > < p class ="css-10b0gli er34gjf0" data-testid="ad-price" > 500 zł < /p > < /div > < span > < span class ="css-3lkihg" title="Używane" > < span > Używane < /span > < /span > < /span > < div class ="css-odp1qd" > < p class ="css-veheph er34gjf0" data-testid="location-date" > Bobowa < !-- --> - < !-- -->26 marca 2023 < /p > < div class ="css-1kfqt7f" color="text-global-secondary" > < /div > < /div > < span class ="css-1x8zoa0" data-testid="adAddToFavorites" > < div class ="css-1fxp90q" > < svg class ="css-znbvx0" height="1em" viewbox="0 0 24 24" width="1em" xmlns="http://www.w3.org/2000/svg" > < path d="M20.219 10.367 12 20.419 3.806 10.4A3.96 3.96 0 0 1 3 8c0-2.206 1.795-4 4-4a4.004 4.004 0 0 1 3.868 3h2.264A4.003 4.003 0 0 1 17 4c2.206 0 4 1.794 4 4 0 .868-.279 1.698-.781 2.367M17 2a5.999 5.999 0 0 0-5 2.686A5.999 5.999 0 0 0 7 2C3.692 2 1 4.691 1 8a5.97 5.97 0 0 0 1.232 3.633L10.71 22h2.582l8.501-10.399A5.943 5.943 0 0 0 23 8c0-3.309-2.692-6-6-6" fill="currentColor" fill-rule="evenodd" > < /path > < /svg > < div class ="css-5xgpg7" data-testid="favorite-icon" > Obserwuj < /div > < /div > < /span > < /div > < /div > < /div > < /a > < /div >
#
# < div
#
#
# class ="css-1sw7q4x" data-cy="l-card" > < a class ="css-rc5s2u" href="/d/oferta/pad-dualschock-4-v2-playstation-4-ps4-czarny-CID99-IDTxcWM.html" > < div class ="css-qfzx1y" > < div class ="css-1venxj6" type="list" > < div class ="css-1ut25fa" type="list" > < div class ="css-pn1izb" type="list" > < div class ="css-gl6djm" > < img class ="css-8wsg1m" src="/app/static/media/no_thumbnail.15f456ec5.svg" / > < /div > < /div > < div class ="css-13aawz3" > < div class ="css-1av34ht" > < div class ="css-3xiokn" > < div class ="css-1xwefxo" > < div class ="css-1cigxpj" > < svg class ="css-d7r8uj" height="1em" viewbox="0 0 24 24" width="1em" xmlns="http://www.w3.org/2000/svg" > < path d="M21 15.999h-.343A3.501 3.501 0 0 0 17.5 14a3.501 3.501 0 0 0-3.156 1.997l-4.687.002A3.5 3.5 0 0 0 6.5 14a3.5 3.5 0 0 0-3.158 2L3 16.002V5h11v6l1 1h6v3.999zM17.5 19c-.827 0-1.5-.673-1.5-1.5s.673-1.5 1.5-1.5 1.5.673 1.5 1.5-.673 1.5-1.5 1.5zm-11 0c-.827 0-1.5-.673-1.5-1.5S5.673 16 6.5 16s1.5.673 1.5 1.5S7.327 19 6.5 19zm12-12 2.25 3H16V7h2.5zm1-2H16V4l-1-1H2L1 4v13.002l1.001 1 1.039-.001A3.503 3.503 0 0 0 6.5 21a3.502 3.502 0 0 0 3.46-3l4.08-.003A3.503 3.503 0 0 0 17.5 21a3.502 3.502 0 0 0 3.46-3.001H22l1-1V9.665L19.5 5z" fill="currentColor" fill-rule="evenodd" > < /path > < /svg > < /div > < /div > < /div > < /div > < /div > < /div > < div class ="css-1apmciz" type="list" > < div class ="css-u2ayx9" > < h6 class ="css-16v5mdi er34gjf0" > Pad Dualschock 4 V2 PlayStation 4 ps4 czarny < /h6 > < p class ="css-10b0gli er34gjf0" data-testid="ad-price" > < span class ="css-1c0ed4l" > < svg class ="css-1ojrdd5" height="1em" viewbox="0 0 24 24" width="1em" xmlns="http://www.w3.org/2000/svg" > < path d="M21 15.999h-.343A3.501 3.501 0 0 0 17.5 14a3.501 3.501 0 0 0-3.156 1.997l-4.687.002A3.5 3.5 0 0 0 6.5 14a3.5 3.5 0 0 0-3.158 2L3 16.002V5h11v6l1 1h6v3.999zM17.5 19c-.827 0-1.5-.673-1.5-1.5s.673-1.5 1.5-1.5 1.5.673 1.5 1.5-.673 1.5-1.5 1.5zm-11 0c-.827 0-1.5-.673-1.5-1.5S5.673 16 6.5 16s1.5.673 1.5 1.5S7.327 19 6.5 19zm12-12 2.25 3H16V7h2.5zm1-2H16V4l-1-1H2L1 4v13.002l1.001 1 1.039-.001A3.503 3.503 0 0 0 6.5 21a3.502 3.502 0 0 0 3.46-3l4.08-.003A3.503 3.503 0 0 0 17.5 21a3.502 3.502 0 0 0 3.46-3.001H22l1-1V9.665L19.5 5z" fill="currentColor" fill-rule="evenodd" > < /path > < /svg > < /span > 145 zł < span class ="css-1vxklie" > do negocjacji < /span > < /p > < /div > < span > < span class ="css-3lkihg" title="Używane" > < span > Używane < /span > < /span > < /span > < div class ="css-odp1qd" > < p class ="css-veheph er34gjf0" data-testid="location-date" > Sosnowiec < !-- --> - < !-- -->Odświeżono dnia 30 marca 2023 < /p > < div class ="css-1kfqt7f" color="text-global-secondary" > < /div > < /div > < span class ="css-1x8zoa0" data-testid="adAddToFavorites" > < div class ="css-1fxp90q" > < svg class ="css-znbvx0" height="1em" viewbox="0 0 24 24" width="1em" xmlns="http://www.w3.org/2000/svg" > < path d="M20.219 10.367 12 20.419 3.806 10.4A3.96 3.96 0 0 1 3 8c0-2.206 1.795-4 4-4a4.004 4.004 0 0 1 3.868 3h2.264A4.003 4.003 0 0 1 17 4c2.206 0 4 1.794 4 4 0 .868-.279 1.698-.781 2.367M17 2a5.999 5.999 0 0 0-5 2.686A5.999 5.999 0 0 0 7 2C3.692 2 1 4.691 1 8a5.97 5.97 0 0 0 1.232 3.633L10.71 22h2.582l8.501-10.399A5.943 5.943 0 0 0 23 8c0-3.309-2.692-6-6-6" fill="currentColor" fill-rule="evenodd" > < /path > < /svg > < div class ="css-5xgpg7" data-testid="favorite-icon" > Obserwuj < /div > < /div > < /span > < /div > < /div > < /div > < /a > < /div >
