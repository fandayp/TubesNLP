import json
import pandas as pd
from random import randint

df=pd.read_csv('provinces.csv', sep=',',header=None)
provinces = df[1]

def randomProvinces():
	rand = randint(0,33)
	return df[1][rand]

def locationChecker(item, provinces):
	ret = True
	location = item['location']
	if location in provinces:
		ret = False

	return ret

#read JSON file
with open('tweetCSV.csv') as json_data:
    d = json.load(json_data)

for item in d:
	if (item['location'] == "" or locationChecker(item, provinces)):
		item['location'] = randomProvinces()

for item in d:
	print(item)