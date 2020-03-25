"""Import Library"""
import pandas as pd
import xlrd

"""Import Data"""

"""Dateien in Pandas-Dataframes einlesen"""
df_bfs2 = pd.read_excel('../data/df_bfs2.xlsx', sheet_name='2017' ,skiprows=4, encoding = 'ISO-8859–1')

"""
Data Preparation - Bundesamt für Statistik (Data Source 2 Mietdaten)
"""

"""Nicht benötigte Spalten entfernen"""
df_bfs2 = df_bfs2.iloc[1:27,[0,3,5,7,9,11,13]]
df_bfs2.head()

"""Spalten umbenennen"""
column_names = list(df_bfs2.columns)
column_names_replacements = ["Ort","1","2","3","4","5","6"]
rename_dict = dict(zip(column_names,column_names_replacements))
df_bfs2 = df_bfs2.rename(columns=rename_dict)

"""Hinzufügen der fehlenden Spalte mit halben Zimmerangaben (Berechnung der Mittelwerte)"""
for i in range(1,6):
  a = str(i +0.5)
  df_bfs2[str(a)] = (df_bfs2.iloc[:,i]+df_bfs2.iloc[:,i+1])/2

df_bfs2 = pd.melt(df_bfs2, id_vars=["Ort"],)
df_bfs2 = df_bfs2.rename(columns={"variable":"Zimmer","value":"Durchschnittspreis/m2"})

"""Daten exportieren (für Tableau Prep)"""
df_bfs2.to_csv('../output/df_bfs_mietpreise_m2.csv')

