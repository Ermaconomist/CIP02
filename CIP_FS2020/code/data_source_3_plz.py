"""Import Libraries"""
import pandas as pd
import xlrd

"""Import Data"""

"""Dateien in Pandas-Dataframes einlesen"""
df_bfs3 = pd.read_excel('../data/df_bfs3.xlsx', sheet_name='PLZ4', encoding = 'ISO-8859–1')

""" 
Data Preparation - Bundesamt für Statistik (Data Source 3 PLZ) 
"""

"""Spalten umbenennen"""
df_bfs3 = df_bfs3.rename(columns={"PLZ4":"PLZ"})
df_bfs3 = df_bfs3.rename(columns={"KTKZ":"Kanton"})

"""Nicht benötigte Spalten entfernen"""
df_bfs3 = df_bfs3.drop(columns=['GDENAMK', 'GDENR', '%_IN_GDE'])

"""Duplikate entfernen"""
df_bfs3.drop_duplicates(subset="PLZ", keep="first", inplace=True)

"""Dictionary erstellen mit Abkürzungen und vollständigem Namen des Kantons"""
dict_kuerzel = {"ZH":"Zürich",  "BE":"Bern",   "LU":"Luzern", "UR":"Uri",    "SZ":"Schwyz", "OW":"Obwalden",   "NW":"Nidwalden",  "GL":"Glarus", "ZG":"Zug",    "FR":"Freiburg",   "SO":"Solothurn",  "BS":"Basel-Stadt",    "BL":"Basel-Landschaft",   "SH":"Schaffhausen",   "AR":"Appenzell Ausserrhoden", "AI":"Appenzell Innerrhoden",  "SG":"St. Gallen", "GR":"Graubünden", "AG":"Aargau", "TG":"Thurgau",    "TI":"Tessin", "VD":"Waadt",  "VS":"Wallis", "NE":"Neuenburg",  "GE":"Genf",   "JU":"Jura"}

"""Type PLZ"""
type(df_bfs3["PLZ"][1])

"""PLZ Spalte in 'str' umwandeln"""
df_bfs3['PLZ'] = df_bfs3['PLZ'].astype('str')
type(df_bfs3["PLZ"][1])
df_bfs3.replace({"Kanton":dict_kuerzel},inplace=True)

"""Exportieren Crawler bereinigt"""
df_bfs3.to_csv('../output/df_PLZ.csv')
