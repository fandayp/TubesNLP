from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time

cust_key = 'gET7oqtyEhh8CR7ERpBUxuHFc'
cust_secret = '0PC0DJAdFi4cuOhlBQUzCGOZGVPGK1KxnCU8KIvc9SlAD144Aj'
acc_token = '732587676-GhORtrYwFjWkpqVboAiukwok1uhLVLvB08CnZxlG'
acc_secret = 'IXNw1vYaJ24vSOhBTWrbG5acJ5GX9VJTY6V3Igk49roUS'

trackList = ["mahasiswa"]

class listener(StreamListener):
	def on_data(self, data):
		fileName = 'tweetCSV.csv'
		try:
			# print("Saving to ", fileName)

			# only get the tweet
			tweetText = data.split(',"text":"')[1].split('","source')[0]
			print(tweetText)

			saveFile = open(fileName, 'a')
			saveFile.write(data)
			saveFile.write('\n')
			saveFile.close()
			return True
		except BaseException as e:
			print('failed ondata,', str(e))
			time.sleep(5)

	def on_error(self, status):
		print(status)

auth = OAuthHandler(cust_key, cust_secret)
auth.set_access_token(acc_token, acc_secret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=trackList)