"""Import Libraries"""
import pandas as pd
pd.__version__
from pathlib import Path

df_crawler = pd.read_csv(Path().joinpath('01_input', 'crawler.csv'), sep = ",")

"""Set Options"""
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

"""Import Data"""

"""Dateien in Pandas-Dataframes einlesen"""
# df_bfs3 = pd.read_excel('../data/df_bfs3.xlsx', sheet_name='PLZ4', encoding = 'ISO-8859–1')
#df_crawler = pd.read_csv('../data/crawler.csv', sep = ",")
"""
Data Preparation - Crawler Daten (Alle Immobilien)
"""

""" Typen Vergabe herauslesen und nach Gewerbe- und Wohnobjekt sortieren """

df_crawler.groupby('type').count() #Kontrollschritt

liste_typen = ['Attikawohnung',
               'Bauernhaus',
               'Dachwohnung',
               'Doppeleinfamilienhaus',
               'Einfamilienhaus',
               'Einliegerwohnung',
               'Einzelzimmer',
               'Loft',
               'Maisonette / Duplex',
               'Mansarde',
               'Möbliertes Wohnobjekt',
               'Möbliertes Wohnobjekt',
               'Reihenfamilienhaus',
               'Rustico',
               'Studio',
               'Terrassenhaus',
               'Terrassenwohnung',
               'VillaWohnung',
               'Wohnung']

df_crawler.loc[df_crawler['type'].isin(liste_typen), 'OBJEKT_TYP'] = 'Wohnung'
df_crawler.loc[-df_crawler['type'].isin(liste_typen), 'OBJEKT_TYP'] = 'Diverse'

df_wohnung = df_crawler.query('OBJEKT_TYP == "Wohnung"')
df_wohnung.groupby('type').count() #Kontrollschritt

df_crawler = df_wohnung

"""Unerwünschte Zeichen und Wörter entfernen"""
df_crawler = df_crawler.replace("\n","", regex = True)
df_crawler['adress'] = df_crawler['adress'].replace("Adresse","", regex = True)
df_crawler['room'] = df_crawler['room'].replace("Zimmer","", regex = True)
df_crawler['room'] = df_crawler['room'].replace(" ","", regex = True)
df_crawler['price'] = df_crawler['price'].replace("'","", regex = True)

"""Neue Spalten mit Zielwerten erstellen"""
df_crawler["Strasse"] = df_crawler["adress"].str.extract("(^.*?(?=[0-9]))")
df_crawler["Hausnummer"] = df_crawler["adress"].str.extract("(\d+(?=\d{4}))")
df_crawler["PLZ Ort"] = df_crawler["adress"].str.extract(".*(\d{4}?.*).*$")
df_crawler["Fläche"] = df_crawler["surface"].str.extract("([0-9]{2,3})")
df_crawler["Preis"] = df_crawler["price"].str.extract("(\\d+)")

"""PLZ und Ort aus Spalte 'PLZ Ort' extrahieren"""
df_crawler['PLZ Ort'] = df_crawler['PLZ Ort'].astype('str')
df_crawler['PLZ'] = df_crawler["PLZ Ort"].str.split(n=1, expand=True)[0]
df_crawler['Ort'] = df_crawler["PLZ Ort"].str.split(n=1, expand=True)[1]


"""Crawler: Spalten umbenennen"""
df_crawler = df_crawler.rename(columns={'room':'Zimmer'})
df_crawler = df_crawler.rename(columns={'Unnamed: 0':'ID'})

"""Crawler: nicht mehr benötigte Spalten entfernen"""
df_crawler = df_crawler.drop(columns='surface')
df_crawler = df_crawler.drop(columns='price')
df_crawler = df_crawler.drop(columns='adress')
df_crawler = df_crawler.drop(columns='PLZ Ort')

"""Spalten umsortieren"""
df_crawler = df_crawler[['ID', 'date', 'Strasse', 'Hausnummer', 'PLZ', 'Ort', 'type', 'Zimmer', 'Fläche', 'Preis']]

"""Exportieren Crawler bereinigt"""
df_crawler.to_csv(Path().joinpath('02_output', 'df_crawler.csv'), sep = ';', encoding = 'utf-8')


# UNUSED CODE - DONE IN TABLEAU PREP
# """
# Data Preparation - Bundesamt für Statistik (Data Source 3 PLZ)
# """
#
# """Spalten umbenennen"""
# df_bfs3 = df_bfs3.rename(columns={"PLZ4":"PLZ"})
# df_bfs3 = df_bfs3.rename(columns={"KTKZ":"Kanton"})
#
# """Nicht benötigte Spalten entfernen"""
# df_bfs3 = df_bfs3.drop(columns=['GDENAMK', 'GDENR', '%_IN_GDE'])
#
# """Duplikate entfernen"""
# df_bfs3.drop_duplicates(subset="PLZ", keep="first", inplace=True)
#
# """Dictionary erstellen mit Abkürzungen und vollständigem Namen des Kantons"""
# dict_kuerzel = {"ZH":"Zürich",  "BE":"Bern",   "LU":"Luzern", "UR":"Uri",    "SZ":"Schwyz", "OW":"Obwalden",   "NW":"Nidwalden",  "GL":"Glarus", "ZG":"Zug",    "FR":"Freiburg",   "SO":"Solothurn",  "BS":"Basel-Stadt",    "BL":"Basel-Landschaft",   "SH":"Schaffhausen",   "AR":"Appenzell Ausserrhoden", "AI":"Appenzell Innerrhoden",  "SG":"St. Gallen", "GR":"Graubünden", "AG":"Aargau", "TG":"Thurgau",    "TI":"Tessin", "VD":"Waadt",  "VS":"Wallis", "NE":"Neuenburg",  "GE":"Genf",   "JU":"Jura"}
#
# """Type PLZ"""
# type(df_bfs3["PLZ"][1])
#
# """PLZ Spalte in 'str' umwandeln"""
# df_bfs3['PLZ'] = df_bfs3['PLZ'].astype('str')
# type(df_bfs3["PLZ"][1])
# df_bfs3.replace({"Kanton":dict_kuerzel},inplace=True)
#
# """
# Merging Dataframes - Crawler und Data Source 3
# """
#
# df_merged = pd.merge(df_crawler, df_bfs3, on = 'PLZ', how = 'left')
#
# """Spalten umsortieren"""
# df_merged = df_merged[['ID', 'date', 'Strasse', 'Hausnummer', 'PLZ', 'Ort', 'Kanton', 'type', 'Zimmer', 'Fläche', 'Preis']]
#
# """Daten Merged exportieren (für Tableau Prep)"""
# df_merged.head()
#
# """Zusammengeführte Daten vom Crawler und vom Bundesamt für Statistik exportieren als CSV-File in Output-Folder"""
# df_merged.to_csv('../output/df_crawler_merged.csv')
