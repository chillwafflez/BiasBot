import requests
from bs4 import BeautifulSoup
import csv
import random
from dotenv import load_dotenv
import pandas as pd


yuh = "data\male_idols3.csv"

df = pd.read_csv(yuh)
counter = 0
for i in df.index:
    print(i)
    print(df.loc[i, 'Name'])
    # df.loc[i, 'test'] = 'PENIS'
    df.loc[i][3] = 'PENIS'
    print(df.loc[i])
    if counter == 10:
        break
    counter += 1

df.to_csv('bruhhhh.csv', index=False)

# with open (yuh, 'r', encoding="utf-8") as csvfile:
#     writer = csv.writer(csvfile, delimiter=',')
#     next(writer)     # skip first row which are just column headers
#     counter = 0
#     for row in reader: # loop over the rows
#         print(row)
#         # idol = row[0]

#         if counter == 10:
#             break
#         counter += 1