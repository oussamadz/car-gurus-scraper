#!/usr/bin/python3
import requests as rq
import pandas as pd 
import json 

#https://www.cargurus.ca/Cars/detailListingJson.action?inventoryListing=323959470
offset = 0


def save_data(line):
    with open("result.csv", 'a') as f:
        f.write(line + "\n")

def clean(text):
    return text.replace('\n','').replace('\t','').replace(',','')

while offset <= 7280:
    url = f"https://www.cargurus.ca/Cars/searchResults.action?zip=T5L&inventorySearchWidgetType=BODYSTYLE&searchId=ca60ef5e-d977-4adb-894a-db1425b4f7dc&nonShippableBaseline=0&shopByTypes=NEAR_BY&sortDir=ASC&sourceContext=carGurusHomePageBody&distance=500&sortType=DEAL_SCORE&entitySelectingHelper.selectedEntity=bg5&offset={offset}&maxResults=15&filtersModified=true"
    try:
        pg = rq.get(url)
        data = json.loads(pg.text)
    except:
        try:
            pg = rq.get(url)
            data = json.loads(pg.text)
        except:
            print("Error loading search")
            break
    for d in data:
        print(f"offset: {offset}: {d['carYear']} {d['makeName']} {d['modelName']} {d['id']}")
        year = d['carYear']
        make = clean(d['makeName'])
        model = clean(d['modelName'])
        try:
            trim = clean(d['trimName'])
        except:
            trim = "N/A"
        try:
            mileage = "{:.2f}".format(float(d['mileage'])/1.609)
        except:
            mileage = "N/A"
        try:
            price = clean(str(d['price']))
        except:
            price = "N/A"
        pgvin = rq.get(f"https://www.cargurus.ca/Cars/detailListingJson.action?inventoryListing={d['id']}")
        vin = clean(json.loads(pgvin.text)['listing']['vin'])
        save_data(f"{year},{make},{model},{trim},{vin},{mileage},{price}")
    offset+=15
