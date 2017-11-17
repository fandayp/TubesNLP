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

#1, 2, 3, 4, 5, 7, 8, 9, 
fileAcara = ['daftar acara korea/acara11.txt']

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

consumer_key = 'hqtPip2z6tpfEHhSnY6H8QxHm'
consumer_secret = 'HC8FLdoVj6C5ulG82EgcnYHP8BkjEXtbElb9OU5owErE4oRQGV'
access_token = '565380886-A6v6oAnStukXWz4kpmKQ364kOSW7vzAlvzgHgH3o'
access_token_secret = 'bQAwxzdhQUTxJIvkoExuWHkMshuuJ6bOlxRkvuJmpuBit'

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

  print(acara)

  #made a cursor
  search_terms = (acara)
  # you can change it make get tweets

  #Lets save the selected part of the tweets inot json
  for tweet in tweepy.Cursor(api.search, q=search_terms, lang = 'en', tweet_mode='extended', since='2017-11-01').items(100):
    createdAt = str(tweet.created_at)
    authorCreatedAt = str(tweet.author.created_at)
    username = str(tweet.user.name)
    location = str(tweet.user.location)
    if (str(tweet.user.location) == "" or locationChecker(str(tweet.user.location), provinces)):
      location = randomProvinces()
    text = ""
    if 'retweeted_status' in dir(tweet):
      text = tweet.retweeted_status.full_text
    else:
      text = tweet.full_text

    tweetJson.append(
      {'tweetText':text,
      'location': location,
      'tweetCreatedAt':createdAt,
      'username': username,
      'authorName': tweet.author.name,
      })

  #dump the data into json format
  # print(tweetJson, type(tweetJson))
print(len(tweetJson))

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
    # print(type(tweetJson), type(feeds))
    # print(tweetJson, '\n')
    # print(feeds, '\n')
    concatedData = tweetJson + feeds
    # print(concatedData)

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