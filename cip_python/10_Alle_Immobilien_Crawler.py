"""Import Libraries"""
import itertools
import requests
from bs4 import BeautifulSoup as soup
import re
import pandas as pd
import sqlalchemy



# um anzahl seiten zu extrahieren --------------------------------------------------------------------------------------

# Der gesamte Crawler benötigt ca. 3-4h
# url = "https://www.alle-immobilien.ch/de/mieten/"

# Beispiel-Crawler um nur die Daten von Cham mit der PLZ 6330 zu crawlen
url = "https://www.alle-immobilien.ch/de/mieten/in-6330/"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
}

html_page = requests.get(url, headers = headers).text

data = soup(html_page, "html.parser")

var_num2loop = re.findall('\d+',
                          data.find('span', class_ = 'search-results__subheadline').text)

var_loops = round((int(var_num2loop[0]) / 20) + 0.5) # auf nächste ganze Zahl runden

# loops ----------------------------------------------------------------------------------------------------------------
list_urls = ["{}{}{}".format(url, "?pageNum=", i) for i in range(1, var_loops + 1)]

data_pages = [] # intitialize List
for item in list_urls:
  page = requests.get(item, headers = headers)
  data_pages.append(soup(page.text, 'html.parser'))



list_date        = [item.find_all('span', class_ = 'tags__timestamp') for item in data_pages]
list_date_flat   = list(itertools.chain(*list_date))
list_date_text   = [item.text for item in list_date_flat]


list_type        = [item.find_all('span', class_ = 'tags__apartment') for item in data_pages]
list_type_flat   = list(itertools.chain(*list_type))
list_type_text   = [item.text for item in list_type_flat]


list_adress      = [item.find_all('div', class_ = 'tag__address') for item in data_pages]
list_adress_flat = list(itertools.chain(*list_adress))
list_adress_text = [item.text for item in list_adress_flat]


list_price       = [item.find_all('div', class_ = 'tag__price') for item in data_pages]
list_price_flat  = list(itertools.chain(*list_price))
list_price_text  = [item.text for item in list_price_flat]


list_surface       = [item.find_all('div', id = lambda value: value and value.startswith("search-result-list-ad-link-surface")) for item in data_pages]
list_surface_flat  = list(itertools.chain(*list_surface))
list_surface_text  = [item.text for item in list_surface_flat]


list_room       = [item.find_all('div', id = lambda value: value and value.startswith("search-result-list-ad-link-room")) for item in data_pages]
list_room_flat  = list(itertools.chain(*list_room))
list_room_text  = [item.text for item in list_room_flat]


# dataframe erstellen
df_alle_immo = pd.DataFrame(
    {
        'date'    : list_date_text,
        'type'    : list_type_text,
        'adress'  : list_adress_text,
        'price'   : list_price_text,
        'surface' : list_surface_text,
        'room'    : list_room_text,
    })

print(df_alle_immo)

# output als csv
df_alle_immo.to_csv('./01_input/crawler_6330.csv', encoding = 'utf-8')


