import tweepy
import pymongo
import json
import pandas as pd
import os
import time
from random import randint
from bson import json_util

df=pd.read_csv('provinces.csv', sep=',',header=None)
provinces = df[1]

fileAcara = ['listAcara.txt', 'listAcara2.txt']

fileName = 'tweetCSV.csv'

def randomProvinces():
  rand = randint(0,33)
  return df[1][rand]

def locationChecker(item, provinces):
  ret = True
  location = item
  if location in provinces:
    ret = False

  return ret

consumer_key = 'gET7oqtyEhh8CR7ERpBUxuHFc'
consumer_secret = '0PC0DJAdFi4cuOhlBQUzCGOZGVPGK1KxnCU8KIvc9SlAD144Aj'
access_token = '732587676-GhORtrYwFjWkpqVboAiukwok1uhLVLvB08CnZxlG'
access_token_secret = 'IXNw1vYaJ24vSOhBTWrbG5acJ5GX9VJTY6V3Igk49roUS'

# Authenticate twitter Api
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

tweetJson = []

for i in fileAcara:
  print(i, '\n')
  daftarAcara = [line.rstrip('\n') for line in open(i)]
  acara = ""
  for item in daftarAcara:
    if (acara == ""):
      acara += item
    else:
      acara = acara + ' OR ' + item

  #made a cursor
  search_terms = ('Indonesia')
  c = tweepy.Cursor(api.search, q=search_terms, since='2017-11-01')
  c.pages(150) # you can change it make get tweets

  #Lets save the selected part of the tweets inot json
  for tweet in c.items():
      if tweet.lang == 'en':
          createdAt = str(tweet.created_at)
          authorCreatedAt = str(tweet.author.created_at)
          location = str(tweet.user.location)
          if (str(tweet.user.location) == "" or locationChecker(str(tweet.user.location), provinces)):
            location = randomProvinces()
          username = str(tweet.user.name)
          tweetJson.append(
            {'tweetText':tweet.text,
            'location': location,
            'tweetCreatedAt':createdAt,
            'username': username,
            'authorName': tweet.author.name,
            })

  #dump the data into json format
  # print(tweetJson, type(tweetJson))

if (os.stat(fileName).st_size == 0):
  print("True")
  data = json.dumps(tweetJson)
  try:
    saveFile = open(fileName, 'a')
    saveFile.write(data)
    saveFile.write('\n')
    saveFile.close()
  except BaseException as e:
    print('failed ondata,', str(e))
    time.sleep(5)  
else:
  print("False")
  with open(fileName, mode='r', encoding='utf-8') as feedsjson:
    feeds = json.load(feedsjson)
    print(type(tweetJson), type(feeds))
    print(tweetJson, '\n')
    print(feeds, '\n')
    concatedData = tweetJson + feeds
    print(concatedData)

  open(fileName, 'w').close()
  data = json.dumps(concatedData)
  try:
    saveFile = open(fileName, 'a')
    saveFile.write(data)
    saveFile.write('\n')
    saveFile.close()
  except BaseException as e:
    print('failed ondata,', str(e))
    time.sleep(5)