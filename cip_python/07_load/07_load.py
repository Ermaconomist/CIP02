### load modules
import pandas as pd
import sqlalchemy
from pathlib import Path

df_final = pd.read_csv('C:\\Users\\usera\\Desktop\\cip_python\\04_output Tableau Prep\\Final_Dataset.csv')
# write to mssql-server // code um db-exist-check erweitern
engine = sqlalchemy.create_engine('mssql://ids-db/CIP_FS2020?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server')

df_final.to_sql("Final_Dataset", con = engine, if_exists = "replace")
