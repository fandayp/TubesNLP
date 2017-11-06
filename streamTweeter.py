import tweepy
import pymongo
from bson import json_util
import json

consumer_key = 'gET7oqtyEhh8CR7ERpBUxuHFc'
consumer_secret = '0PC0DJAdFi4cuOhlBQUzCGOZGVPGK1KxnCU8KIvc9SlAD144Aj'
access_token = '732587676-GhORtrYwFjWkpqVboAiukwok1uhLVLvB08CnZxlG'
access_token_secret = 'IXNw1vYaJ24vSOhBTWrbG5acJ5GX9VJTY6V3Igk49roUS'

# Authenticate twitter Api
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
#made a cursor
search_terms = ('Indonesia OR Korupsi')
c = tweepy.Cursor(api.search, q=search_terms, since='2017-11-01', until='2017-11-07',)
c.pages(15) # you can change it make get tweets

#Lets save the selected part of the tweets inot json
tweetJson = []
for tweet in c.items():
    if tweet.lang == 'en':
        createdAt = str(tweet.created_at)
        authorCreatedAt = str(tweet.author.created_at)
        location = str(tweet.user.location)
        username = str(tweet.user.name)
        tweetJson.append(
          {'tweetText':tweet.text,
          'location': location,
          'tweetCreatedAt':createdAt,
          'username': username,
          'authorName': tweet.author.name,
          })
#dump the data into json format
data = json.dumps(tweetJson)
print(data)
fileName = 'tweetCSV.csv'
try:
	saveFile = open(fileName, 'a')
	saveFile.write(data)
	saveFile.write('\n')
	saveFile.close()
except BaseException as e:
	print('failed ondata,', str(e))
	time.sleep(5)