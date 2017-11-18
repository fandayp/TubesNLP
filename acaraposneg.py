from textblob import TextBlob
import json

with open('dataTest.txt') as json_data:
	d = json.load(json_data)

newTweet = []

for item in d:
	if (item['tweetText'] != ""):
		blob = TextBlob(item['tweetText'])
		if (blob.correct().sentiment.polarity > 0):
			sentiment = 'positif'
		else:
			sentiment = 'negatif'
		newTweet.append(
            {'tweetText':item['tweetText'],
            'location': item['location'],
            'tweetCreatedAt':item['tweetCreatedAt'],
            'username': item['username'],
            'authorName': item['authorName'],
            'sentiment': sentiment
            })

for item in newTweet:
	print(item,"\n")